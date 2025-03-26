import * as cdk from "aws-cdk-lib";
import { CfnOutput, Stack, StackProps } from "aws-cdk-lib";
import * as wafv2 from "aws-cdk-lib/aws-wafv2";
import { Construct } from "constructs";

interface FrontendWafStackProps extends StackProps {
  readonly envPrefix: string;
  readonly allowedIpV4AddressRanges: string[];
  readonly allowedIpV6AddressRanges: string[];
}

/**
 * Frontend WAF
 */
export class FrontendWafStack extends Stack {
  /**
   * Web ACL ARN
   */
  public readonly webAclArn: CfnOutput;

  /**
   * Whether IPv6 is used or not
   */
  public readonly ipV6Enabled: boolean;

  constructor(scope: Construct, id: string, props: FrontendWafStackProps) {
    super(scope, id, props);

    const sepHyphen = props.envPrefix ? "-" : "";
    const rules: wafv2.CfnWebACL.RuleProperty[] = [];

    // create Ipset for ACL
    if (props.allowedIpV4AddressRanges.length > 0) {
      const ipV4SetReferenceStatement = new wafv2.CfnIPSet(
        this,
        "FrontendIpV4Set",
        {
          ipAddressVersion: "IPV4",
          scope: "CLOUDFRONT",
          addresses: props.allowedIpV4AddressRanges,
        }
      );
      rules.push({
        priority: 0,
        name: "FrontendWebAclIpV4RuleSet",
        action: { allow: {} },
        visibilityConfig: {
          cloudWatchMetricsEnabled: true,
          metricName: "FrontendWebAcl",
          sampledRequestsEnabled: true,
        },
        statement: {
          ipSetReferenceStatement: { arn: ipV4SetReferenceStatement.attrArn },
        },
      });
    }
    if (props.allowedIpV6AddressRanges.length > 0) {
      const ipV6SetReferenceStatement = new wafv2.CfnIPSet(
        this,
        "FrontendIpV6Set",
        {
          ipAddressVersion: "IPV6",
          scope: "CLOUDFRONT",
          addresses: props.allowedIpV6AddressRanges,
        }
      );
      rules.push({
        priority: 1,
        name: "FrontendWebAclIpV6RuleSet",
        action: { allow: {} },
        visibilityConfig: {
          cloudWatchMetricsEnabled: true,
          metricName: "FrontendWebAcl",
          sampledRequestsEnabled: true,
        },
        statement: {
          ipSetReferenceStatement: { arn: ipV6SetReferenceStatement.attrArn },
        },
      });
      this.ipV6Enabled = true;
    } else {
      this.ipV6Enabled = false;
    }

    if (rules.length > 0) {
      const webAcl = new wafv2.CfnWebACL(this, "WebAcl", {
        defaultAction: { block: {} },
        name: `${props.envPrefix}${sepHyphen}FrontendWebAcl`,
        scope: "CLOUDFRONT",
        visibilityConfig: {
          cloudWatchMetricsEnabled: true,
          metricName: "FrontendWebAcl",
          sampledRequestsEnabled: true,
        },
        rules,
      });

      this.webAclArn = new cdk.CfnOutput(this, "WebAclId", {
        value: webAcl.attrArn,
      });
    } else {
      throw new Error(
        "One or more allowed IP ranges must be specified in IPv4 or IPv6."
      );
    }
  }
}
