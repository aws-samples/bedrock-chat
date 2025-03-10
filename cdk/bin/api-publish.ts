#!/usr/bin/env node
import "source-map-support/register";
import * as cdk from "aws-cdk-lib";
import { ApiPublishmentStack } from "../lib/api-publishment-stack";
import * as apigateway from "aws-cdk-lib/aws-apigateway";
import { resolveApiPublishParameters } from "../lib/utils/parameter-models";

const app = new cdk.App();

// Get parameters specific to API publishing
const params = resolveApiPublishParameters(app);

// Parse allowed origins
const publishedApiAllowedOrigins = JSON.parse(
  params.publishedApiAllowedOrigins || '["*"]'
);

console.log(
  `PUBLISHED_API_THROTTLE_RATE_LIMIT: ${params.publishedApiThrottleRateLimit}`
);
console.log(
  `PUBLISHED_API_THROTTLE_BURST_LIMIT: ${params.publishedApiThrottleBurstLimit}`
);
console.log(`PUBLISHED_API_QUOTA_LIMIT: ${params.publishedApiQuotaLimit}`);
console.log(`PUBLISHED_API_QUOTA_PERIOD: ${params.publishedApiQuotaPeriod}`);
console.log(
  `PUBLISHED_API_DEPLOYMENT_STAGE: ${params.publishedApiDeploymentStage}`
);
console.log(`PUBLISHED_API_ID: ${params.publishedApiId}`);
console.log(`PUBLISHED_API_ALLOWED_ORIGINS: ${publishedApiAllowedOrigins}`);

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
  `ApiPublishmentStack${params.publishedApiId}`,
  {
    env: {
      region: process.env.CDK_DEFAULT_REGION,
    },
    bedrockRegion: params.bedrockRegion,
    conversationTableName: conversationTableName,
    tableAccessRoleArn: tableAccessRoleArn,
    webAclArn: webAclArn,
    largeMessageBucketName: largeMessageBucketName,
    usagePlan: {
      throttle:
        params.publishedApiThrottleRateLimit !== undefined &&
        params.publishedApiThrottleBurstLimit !== undefined
          ? {
              rateLimit: params.publishedApiThrottleRateLimit,
              burstLimit: params.publishedApiThrottleBurstLimit,
            }
          : undefined,
      quota:
        params.publishedApiQuotaLimit !== undefined &&
        params.publishedApiQuotaPeriod !== undefined
          ? {
              limit: params.publishedApiQuotaLimit,
              period: apigateway.Period[params.publishedApiQuotaPeriod],
            }
          : undefined,
    },
    deploymentStage: params.publishedApiDeploymentStage,
    corsOptions: {
      allowOrigins: publishedApiAllowedOrigins,
      allowMethods: apigateway.Cors.ALL_METHODS,
      allowHeaders: apigateway.Cors.DEFAULT_HEADERS,
      allowCredentials: true,
    },
  }
);
