#!/usr/bin/env node
import "source-map-support/register";
import * as cdk from "aws-cdk-lib";
import { ApiPublishmentStack } from "../lib/api-publishment-stack";
import * as apigateway from "aws-cdk-lib/aws-apigateway";

const app = new cdk.App();

const BEDROCK_REGION = app.node.tryGetContext("bedrockRegion");

// Usage plan for the published API
const PUBLISHED_API_THROTTLE_RATE_LIMIT: number | undefined =
  app.node.tryGetContext("publishedApiThrottleRateLimit")
    ? Number(app.node.tryGetContext("publishedApiThrottleRateLimit"))
    : undefined;
const PUBLISHED_API_THROTTLE_BURST_LIMIT: number | undefined =
  app.node.tryGetContext("publishedApiThrottleBurstLimit")
    ? Number(app.node.tryGetContext("publishedApiThrottleBurstLimit"))
    : undefined;
const PUBLISHED_API_QUOTA_LIMIT: number | undefined = app.node.tryGetContext(
  "publishedApiQuotaLimit"
)
  ? Number(app.node.tryGetContext("publishedApiQuotaLimit"))
  : undefined;
const PUBLISHED_API_QUOTA_PERIOD: "DAY" | "WEEK" | "MONTH" | undefined =
  app.node.tryGetContext("publishedApiQuotaPeriod")
    ? app.node.tryGetContext("publishedApiQuotaPeriod")
    : undefined;
const PUBLISHED_API_DEPLOYMENT_STAGE = app.node.tryGetContext(
  "publishedApiDeploymentStage"
);
const PUBLISHED_API_ID: string = app.node.tryGetContext("publishedApiId");
const PUBLISHED_API_ALLOWED_ORIGINS_STRING: string = app.node.tryGetContext(
  "publishedApiAllowedOrigins"
);
const PUBLISHED_API_ALLOWED_ORIGINS: string[] = JSON.parse(
  PUBLISHED_API_ALLOWED_ORIGINS_STRING || '["*"]'
);

console.log(
  `PUBLISHED_API_THROTTLE_RATE_LIMIT: ${PUBLISHED_API_THROTTLE_RATE_LIMIT}`
);
console.log(
  `PUBLISHED_API_THROTTLE_BURST_LIMIT: ${PUBLISHED_API_THROTTLE_BURST_LIMIT}`
);
console.log(`PUBLISHED_API_QUOTA_LIMIT: ${PUBLISHED_API_QUOTA_LIMIT}`);
console.log(`PUBLISHED_API_QUOTA_PERIOD: ${PUBLISHED_API_QUOTA_PERIOD}`);
console.log(
  `PUBLISHED_API_DEPLOYMENT_STAGE: ${PUBLISHED_API_DEPLOYMENT_STAGE}`
);
console.log(`PUBLISHED_API_ID: ${PUBLISHED_API_ID}`);
console.log(`PUBLISHED_API_ALLOWED_ORIGINS: ${PUBLISHED_API_ALLOWED_ORIGINS}`);

const webAclArn = cdk.Fn.importValue("PublishedApiWebAclArn");

const conversationTableName = cdk.Fn.importValue(
  "BedrockClaudeChatConversationTableName"
);
const tableAccessRoleArn = cdk.Fn.importValue(
  "BedrockClaudeChatTableAccessRoleArn"
);
const largeMessageBucketName = cdk.Fn.importValue(
  "BedrockClaudeChatLargeMessageBucketName"
);

// NOTE: DO NOT change the stack id naming rule.
const publishedApi = new ApiPublishmentStack(
  app,
  `ApiPublishmentStack${PUBLISHED_API_ID}`,
  {
    env: {
      region: process.env.CDK_DEFAULT_REGION,
    },
    bedrockRegion: BEDROCK_REGION,
    conversationTableName: conversationTableName,
    tableAccessRoleArn: tableAccessRoleArn,
    webAclArn: webAclArn,
    largeMessageBucketName: largeMessageBucketName,
    usagePlan: {
      throttle:
        PUBLISHED_API_THROTTLE_RATE_LIMIT !== undefined &&
        PUBLISHED_API_THROTTLE_BURST_LIMIT !== undefined
          ? {
              rateLimit: PUBLISHED_API_THROTTLE_RATE_LIMIT,
              burstLimit: PUBLISHED_API_THROTTLE_BURST_LIMIT,
            }
          : undefined,
      quota:
        PUBLISHED_API_QUOTA_LIMIT !== undefined &&
        PUBLISHED_API_QUOTA_PERIOD !== undefined
          ? {
              limit: PUBLISHED_API_QUOTA_LIMIT,
              period: apigateway.Period[PUBLISHED_API_QUOTA_PERIOD],
            }
          : undefined,
    },
    deploymentStage: PUBLISHED_API_DEPLOYMENT_STAGE,
    corsOptions: {
      allowOrigins: PUBLISHED_API_ALLOWED_ORIGINS,
      allowMethods: apigateway.Cors.ALL_METHODS,
      allowHeaders: apigateway.Cors.DEFAULT_HEADERS,
      allowCredentials: true,
    },
  }
);
