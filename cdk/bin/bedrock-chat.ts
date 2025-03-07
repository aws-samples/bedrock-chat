#!/usr/bin/env node
import "source-map-support/register";
import * as cdk from "aws-cdk-lib";
import { BedrockChatStack } from "../lib/bedrock-chat-stack";
import { BedrockRegionResourcesStack } from "../lib/bedrock-region-resources";
import { FrontendWafStack } from "../lib/frontend-waf-stack";
import { LogRetentionChecker } from "../rules/log-retention-checker";
import { getBedrockChatParameters } from "../lib/utils/parameter-models";

const app = new cdk.App();

// Get parameters specific to the Bedrock Chat application
const params = getBedrockChatParameters(app);

// WAF for frontend
// 2023/9: Currently, the WAF for CloudFront needs to be created in the North America region (us-east-1), so the stacks are separated
// https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-webacl.html
const waf = new FrontendWafStack(app, `FrontendWafStack`, {
  env: {
    // account: process.env.CDK_DEFAULT_ACCOUNT,
    region: "us-east-1",
  },
  allowedIpV4AddressRanges: params.allowedIpV4AddressRanges,
  allowedIpV6AddressRanges: params.allowedIpV6AddressRanges,
});

// The region of the LLM model called by the converse API and the region of Guardrail must be in the same region.
// CustomBotStack contains Knowledge Bases is deployed in the same region as the LLM model, and source bucket must be in the same region as Knowledge Bases.
// Therefore, define BedrockRegionResourcesStack containing the source bucket in the same region as the LLM model.
// Ref: https://docs.aws.amazon.com/bedrock/latest/userguide/s3-data-source-connector.html
const bedrockRegionResources = new BedrockRegionResourcesStack(
  app,
  `BedrockRegionResourcesStack`,
  {
    env: {
      // account: process.env.CDK_DEFAULT_ACCOUNT,
      region: params.bedrockRegion,
    },
    crossRegionReferences: true,
  }
);

const chat = new BedrockChatStack(app, `BedrockChatStack`, {
  env: {
    // account: process.env.CDK_DEFAULT_ACCOUNT,
    region: process.env.CDK_DEFAULT_REGION,
  },
  crossRegionReferences: true,
  bedrockRegion: params.bedrockRegion,
  webAclId: waf.webAclArn.value,
  enableIpV6: waf.ipV6Enabled,
  identityProviders: params.identityProviders,
  userPoolDomainPrefix: params.userPoolDomainPrefix,
  publishedApiAllowedIpV4AddressRanges:
    params.publishedApiAllowedIpV4AddressRanges,
  publishedApiAllowedIpV6AddressRanges:
    params.publishedApiAllowedIpV6AddressRanges,
  allowedSignUpEmailDomains: params.allowedSignUpEmailDomains,
  autoJoinUserGroups: params.autoJoinUserGroups,
  enableMistral: params.enableMistral,
  selfSignUpEnabled: params.selfSignUpEnabled,
  documentBucket: bedrockRegionResources.documentBucket,
  useStandbyReplicas: params.enableRagReplicas,
  enableBedrockCrossRegionInference: params.enableBedrockCrossRegionInference,
  enableLambdaSnapStart: params.enableLambdaSnapStart,
  alternateDomainName: params.alternateDomainName,
  hostedZoneId: params.hostedZoneId,
});
chat.addDependency(waf);
chat.addDependency(bedrockRegionResources);

cdk.Aspects.of(chat).add(new LogRetentionChecker());
