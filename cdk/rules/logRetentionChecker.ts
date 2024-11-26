import { Construct } from 'constructs';
import { IAspect, Annotations } from 'aws-cdk-lib';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as logs from 'aws-cdk-lib/aws-logs';
import {
  DockerImageFunction,
} from "aws-cdk-lib/aws-lambda";
import { PythonFunction } from "@aws-cdk/aws-lambda-python-alpha";


export class LogRetentionChecker implements IAspect {
  public visit(node: Construct): void {
    if (node instanceof DockerImageFunction) {
      if (node._logRetention === undefined) {
        Annotations.of(node).addWarning('CloudWatch log retention period will be reduced from indefinite to 3 months to optimize costs.');
      }
    } else if (node instanceof PythonFunction) {
      if (node._logRetention === undefined) {
        Annotations.of(node).addWarning('CloudWatch log retention period will be reduced from indefinite to 3 months to optimize costs.');
      }
    } else if (node instanceof logs.CfnLogGroup) {
      if (node.retentionInDays === undefined) {
        Annotations.of(node).addWarning('CloudWatch log retention period will be reduced from indefinite to 3 months to optimize costs.');
      }
    }
  }
}