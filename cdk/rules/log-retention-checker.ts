import { Construct } from "constructs";
import { IAspect, Annotations } from "aws-cdk-lib";
import * as logs from "aws-cdk-lib/aws-logs";
import { DockerImageFunction } from "aws-cdk-lib/aws-lambda";
import { PythonFunction } from "@aws-cdk/aws-lambda-python-alpha";

export class LogRetentionChecker implements IAspect {
  public visit(node: Construct): void {
    const warningMessage =
      "Log retention period is not set. Logs will be kept indefinitely, leading to increased Cloudwatch Logs costs. Set a retention period to reduce costs.";

    if (node instanceof DockerImageFunction) {
      if (node._logRetention === undefined) {
        // We need to access the private `_logRetention` custom resource, the only public property - `logGroup` - provides an ARN reference to the resource, instead of the resource itself.
        // https://github.com/aws/aws-cdk/blob/deeb2ad0bc38101a9f1fa8162ad5d6008900a98d/packages/%40aws-cdk/custom-resource-handlers/lib/custom-resources-framework/classes.ts#L232
        Annotations.of(node).addWarning(warningMessage);
      }
    } else if (node instanceof PythonFunction) {
      // We need to access the private `_logRetention` custom resource, the only public property - `logGroup` - provides an ARN reference to the resource, instead of the resource itself.
      // https://github.com/aws/aws-cdk/blob/deeb2ad0bc38101a9f1fa8162ad5d6008900a98d/packages/%40aws-cdk/custom-resource-handlers/lib/custom-resources-framework/classes.ts#L232
      if (node._logRetention === undefined) {
        Annotations.of(node).addWarning(warningMessage);
      }
    } else if (node instanceof logs.CfnLogGroup) {
      if (node.retentionInDays === undefined) {
        Annotations.of(node).addWarning(warningMessage);
      }
    }
  }
}
