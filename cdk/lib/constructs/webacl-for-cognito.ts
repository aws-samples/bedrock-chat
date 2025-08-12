import { Construct } from "constructs";
import * as wafv2 from "aws-cdk-lib/aws-wafv2";
import { CfnOutput } from "aws-cdk-lib";

export interface WebAclForCognitoProps {
  envPrefix: string;
  readonly allowedIpV4AddressRanges: string[];
  readonly allowedIpV6AddressRanges: string[];
}

export class WebAclForCognito extends Construct {
  public readonly webAclArn: string;
  constructor(scope: Construct, id: string, props: WebAclForCognitoProps) {
    super(scope, id);

    const sepHyphen = props.envPrefix ? "-" : "";
    const rules: wafv2.CfnWebACL.RuleProperty[] = [];

    if (props.allowedIpV4AddressRanges.length > 0) {
      const ipV4SetReferenceStatement = new wafv2.CfnIPSet(this, "IpV4Set", {
        ipAddressVersion: "IPV4",
        scope: "REGIONAL",
        addresses: props.allowedIpV4AddressRanges,
      });
      rules.push({
        priority: 0,
        name: "CognitoWebAclIpV4RuleSet",
        action: { allow: {} },
        visibilityConfig: {
          cloudWatchMetricsEnabled: true,
          metricName: "CognitoWebAcl",
          sampledRequestsEnabled: true,
        },
        statement: {
          ipSetReferenceStatement: { arn: ipV4SetReferenceStatement.attrArn },
        },
      });
    }

    if (props.allowedIpV6AddressRanges.length > 0) {
      const ipV6SetReferenceStatement = new wafv2.CfnIPSet(this, "IpV6Set", {
        ipAddressVersion: "IPV6",
        scope: "REGIONAL",
        addresses: props.allowedIpV6AddressRanges,
      });
      rules.push({
        priority: 1,
        name: "CognitoWebAclIpV6RuleSet",
        action: { allow: {} },
        visibilityConfig: {
          cloudWatchMetricsEnabled: true,
          metricName: "CognitoWebAcl",
          sampledRequestsEnabled: true,
        },
        statement: {
          ipSetReferenceStatement: { arn: ipV6SetReferenceStatement.attrArn },
        },
      });
    }
    if (rules.length > 0) {
      const webAcl = new wafv2.CfnWebACL(this, "WebAcl", {
        defaultAction: { block: {} },
        name: `${props.envPrefix}${sepHyphen}CognitoWebAcl-${id}`,
        scope: "REGIONAL",
        visibilityConfig: {
          cloudWatchMetricsEnabled: true,
          metricName: "CognitoWebAcl",
          sampledRequestsEnabled: true,
        },
        rules,
      });
      new CfnOutput(this, "WebAclArn", {
        value: webAcl.attrArn,
      });

      this.webAclArn = webAcl.attrArn;
    } else {
      throw new Error(
        "One or more allowed IP ranges for Cognito must be specified in IPv4 or IPv6."
      );
    }
  }
}