#!/usr/bin/env node
import "source-map-support/register";
import * as cdk from "aws-cdk-lib";
import { ApiPublishmentStack } from "../lib/api-publishment-stack";
import * as apigateway from "aws-cdk-lib/aws-apigateway";
import { resolveApiPublishParameters } from "../lib/utils/parameter-models";

const app = new cdk.App();

// Get parameters specific to API publishing
const params = resolveApiPublishParameters();
const sepHyphen = params.envPrefix ? "-" : "";

// Parse allowed origins
const publishedApiAllowedOrigins = JSON.parse(
  params.publishedApiAllowedOrigins || '["*"]'
);

// Log all parameters at once for debugging
console.log("API Publish Parameters:", JSON.stringify(params));

const webAclArn = cdk.Fn.importValue(
  `${params.envPrefix}${sepHyphen}PublishedApiWebAclArn`
);

const conversationTableName = cdk.Fn.importValue(
  `${params.envPrefix}${sepHyphen}BedrockClaudeChatConversationTableName`
);
const botTableName = cdk.Fn.importValue(
  `${params.envPrefix}${sepHyphen}BedrockClaudeChatBotTableNameV3`
);
const tableAccessRoleArn = cdk.Fn.importValue(
  `${params.envPrefix}${sepHyphen}BedrockClaudeChatTableAccessRoleArn`
);
const largeMessageBucketName = cdk.Fn.importValue(
  `${params.envPrefix}${sepHyphen}BedrockClaudeChatLargeMessageBucketName`
);

// NOTE: DO NOT change the stack id naming rule.
new ApiPublishmentStack(app, `ApiPublishmentStack${params.publishedApiId}`, {
  env: {
    region: process.env.CDK_DEFAULT_REGION,
  },
  bedrockRegion: params.bedrockRegion,
  conversationTableName: conversationTableName,
  botTableName: botTableName,
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
});

cdk.Tags.of(app).add("CDKEnvironment", params.envName);
