#!/usr/bin/env node
import "source-map-support/register";
import * as cdk from "aws-cdk-lib";
import { BedrockChatStack } from "../lib/bedrock-chat-stack";
import { BedrockRegionResourcesStack } from "../lib/bedrock-region-resources";
import { FrontendWafStack } from "../lib/frontend-waf-stack";
import { TIdentityProvider } from "../lib/utils/identity-provider";
import { LogRetentionChecker } from "../rules/log-retention-checker";

const app = new cdk.App();

const BEDROCK_REGION = app.node.tryGetContext("bedrockRegion");

// Allowed IP address ranges for this app itself
const ALLOWED_IP_V4_ADDRESS_RANGES: string[] = app.node.tryGetContext(
  "allowedIpV4AddressRanges"
);
const ALLOWED_IP_V6_ADDRESS_RANGES: string[] = app.node.tryGetContext(
  "allowedIpV6AddressRanges"
);

// Allowed IP address ranges for the published API
const PUBLISHED_API_ALLOWED_IP_V4_ADDRESS_RANGES: string[] =
  app.node.tryGetContext("publishedApiAllowedIpV4AddressRanges");
const PUBLISHED_API_ALLOWED_IP_V6_ADDRESS_RANGES: string[] =
  app.node.tryGetContext("publishedApiAllowedIpV6AddressRanges");
const ALLOWED_SIGN_UP_EMAIL_DOMAINS: string[] = app.node.tryGetContext(
  "allowedSignUpEmailDomains"
);
const IDENTITY_PROVIDERS: TIdentityProvider[] =
  app.node.tryGetContext("identityProviders");
const USER_POOL_DOMAIN_PREFIX: string = app.node.tryGetContext(
  "userPoolDomainPrefix"
);
const AUTO_JOIN_USER_GROUPS: string[] =
  app.node.tryGetContext("autoJoinUserGroups");

const ENABLE_MISTRAL: boolean = app.node.tryGetContext("enableMistral");
const SELF_SIGN_UP_ENABLED: boolean =
  app.node.tryGetContext("selfSignUpEnabled");
const USE_STAND_BY_REPLICAS: boolean =
  app.node.tryGetContext("enableRagReplicas");
const ENABLE_BEDROCK_CROSS_REGION_INFERENCE: boolean = app.node.tryGetContext(
  "enableBedrockCrossRegionInference"
);
const ENABLE_LAMBDA_SNAPSTART: boolean = app.node.tryGetContext("enableLambdaSnapStart");

// WAF for frontend
// 2023/9: Currently, the WAF for CloudFront needs to be created in the North America region (us-east-1), so the stacks are separated
// https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-webacl.html
const waf = new FrontendWafStack(app, `FrontendWafStack`, {
  env: {
    // account: process.env.CDK_DEFAULT_ACCOUNT,
    region: "us-east-1",
  },
  allowedIpV4AddressRanges: ALLOWED_IP_V4_ADDRESS_RANGES,
  allowedIpV6AddressRanges: ALLOWED_IP_V6_ADDRESS_RANGES,
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
      region: BEDROCK_REGION,
    },
    crossRegionReferences: true,
  }
);

const ALTERNATE_DOMAIN_NAME: string = app.node.tryGetContext("alternateDomainName");
const HOSTED_ZONE_ID: string = app.node.tryGetContext("hostedZoneId");

const chat = new BedrockChatStack(app, `BedrockChatStack`, {
  env: {
    // account: process.env.CDK_DEFAULT_ACCOUNT,
    region: process.env.CDK_DEFAULT_REGION,
  },
  crossRegionReferences: true,
  bedrockRegion: BEDROCK_REGION,
  webAclId: waf.webAclArn.value,
  enableIpV6: waf.ipV6Enabled,
  identityProviders: IDENTITY_PROVIDERS,
  userPoolDomainPrefix: USER_POOL_DOMAIN_PREFIX,
  publishedApiAllowedIpV4AddressRanges:
    PUBLISHED_API_ALLOWED_IP_V4_ADDRESS_RANGES,
  publishedApiAllowedIpV6AddressRanges:
    PUBLISHED_API_ALLOWED_IP_V6_ADDRESS_RANGES,
  allowedSignUpEmailDomains: ALLOWED_SIGN_UP_EMAIL_DOMAINS,
  autoJoinUserGroups: AUTO_JOIN_USER_GROUPS,
  enableMistral: ENABLE_MISTRAL,
  selfSignUpEnabled: SELF_SIGN_UP_ENABLED,
  documentBucket: bedrockRegionResources.documentBucket,
  useStandbyReplicas: USE_STAND_BY_REPLICAS,
  enableBedrockCrossRegionInference: ENABLE_BEDROCK_CROSS_REGION_INFERENCE,
  enableLambdaSnapStart: ENABLE_LAMBDA_SNAPSTART,
  alternateDomainName: ALTERNATE_DOMAIN_NAME,
  hostedZoneId: HOSTED_ZONE_ID,
});
chat.addDependency(waf);
chat.addDependency(bedrockRegionResources);

cdk.Aspects.of(chat).add(new LogRetentionChecker());
