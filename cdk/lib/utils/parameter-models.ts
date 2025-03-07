import { z } from "zod";
import { TIdentityProvider } from "./identity-provider";

/**
 * Base parameters schema that is common across all entry points
 */
export const BaseParametersSchema = z.object({
  // Bedrock configuration
  bedrockRegion: z.string().default("us-east-1"),
});

/**
 * Parameters schema for the main Bedrock Chat application
 */
export const BedrockChatParametersSchema = BaseParametersSchema.extend({
  // Bedrock configuration
  enableMistral: z.boolean().default(false),
  enableBedrockCrossRegionInference: z.boolean().default(true),

  // IP address restrictions
  allowedIpV4AddressRanges: z
    .array(z.string())
    .default(["0.0.0.0/1", "128.0.0.0/1"]),
  allowedIpV6AddressRanges: z
    .array(z.string())
    .default([
      "0000:0000:0000:0000:0000:0000:0000:0000/1",
      "8000:0000:0000:0000:0000:0000:0000:0000/1",
    ]),
  publishedApiAllowedIpV4AddressRanges: z
    .array(z.string())
    .default(["0.0.0.0/1", "128.0.0.0/1"]),
  publishedApiAllowedIpV6AddressRanges: z
    .array(z.string())
    .default([
      "0000:0000:0000:0000:0000:0000:0000:0000/1",
      "8000:0000:0000:0000:0000:0000:0000:0000/1",
    ]),

  // Authentication and user management
  identityProviders: z.array(z.custom<TIdentityProvider>()).default([]),
  userPoolDomainPrefix: z.string().default(""),
  allowedSignUpEmailDomains: z.array(z.string()).default([]),
  autoJoinUserGroups: z.array(z.string()).default(["CreatingBotAllowed"]),
  selfSignUpEnabled: z.boolean().default(true),

  // Performance and availability
  enableRagReplicas: z.boolean().default(true),
  enableLambdaSnapStart: z.boolean().default(true),

  // Custom domain configuration
  alternateDomainName: z.string().default(""),
  hostedZoneId: z.string().default(""),
});

/**
 * Parameters schema for API publishing
 */
export const ApiPublishParametersSchema = BaseParametersSchema.extend({
  // API publishing configuration
  publishedApiThrottleRateLimit: z.number().optional(),
  publishedApiThrottleBurstLimit: z.number().optional(),
  publishedApiQuotaLimit: z.number().optional(),
  publishedApiQuotaPeriod: z.enum(["DAY", "WEEK", "MONTH"]).optional(),
  publishedApiDeploymentStage: z.string().optional(),
  publishedApiId: z.string().optional(),
  publishedApiAllowedOrigins: z.string().default('["*"]'),
});

/**
 * Parameters schema for Bedrock Custom Bot
 */
export const BedrockCustomBotParametersSchema = BaseParametersSchema;

/**
 * Type definitions for each parameter set
 */
// Input types (for user input, default values are optional)
export type BaseParametersInput = z.input<typeof BaseParametersSchema>;
export type BedrockChatParametersInput = z.input<typeof BedrockChatParametersSchema>;
export type ApiPublishParametersInput = z.input<typeof ApiPublishParametersSchema>;
export type BedrockCustomBotParametersInput = z.input<typeof BedrockCustomBotParametersSchema>;

// Output types (for function returns, all properties are required)
export type BaseParameters = z.infer<typeof BaseParametersSchema>;
export type BedrockChatParameters = z.infer<typeof BedrockChatParametersSchema>;
export type ApiPublishParameters = z.infer<typeof ApiPublishParametersSchema>;
export type BedrockCustomBotParameters = z.infer<typeof BedrockCustomBotParametersSchema>;

/**
 * Parse and validate CDK context parameters for the main Bedrock Chat application
 * @param app CDK App instance
 * @param envName Optional environment name to use for parameter lookup
 * @returns Validated parameters object
 */
export function getBedrockChatParameters(
  app: any,
  envName?: string
): BedrockChatParameters {
  // Use 'default' if envName is undefined
  const environment = envName || "default";

  // Import bedrockChatParams from parameter.ts
  const { bedrockChatParams } = require("../../parameter");

  // If environment parameters exist in bedrockChatParams, use them
  if (bedrockChatParams.has(environment)) {
    return BedrockChatParametersSchema.parse(bedrockChatParams.get(environment)!);
  }

  // If environment is 'default' and not found in bedrockChatParams, use context values
  if (environment === "default") {
    const contextParams = {
      bedrockRegion: app.node.tryGetContext("bedrockRegion"),
      enableMistral: app.node.tryGetContext("enableMistral"),
      allowedIpV4AddressRanges: app.node.tryGetContext(
        "allowedIpV4AddressRanges"
      ),
      allowedIpV6AddressRanges: app.node.tryGetContext(
        "allowedIpV6AddressRanges"
      ),
      identityProviders: app.node.tryGetContext("identityProviders"),
      userPoolDomainPrefix: app.node.tryGetContext("userPoolDomainPrefix"),
      allowedSignUpEmailDomains: app.node.tryGetContext(
        "allowedSignUpEmailDomains"
      ),
      autoJoinUserGroups: app.node.tryGetContext("autoJoinUserGroups"),
      selfSignUpEnabled: app.node.tryGetContext("selfSignUpEnabled"),
      publishedApiAllowedIpV4AddressRanges: app.node.tryGetContext(
        "publishedApiAllowedIpV4AddressRanges"
      ),
      publishedApiAllowedIpV6AddressRanges: app.node.tryGetContext(
        "publishedApiAllowedIpV6AddressRanges"
      ),
      enableRagReplicas: app.node.tryGetContext("enableRagReplicas"),
      enableBedrockCrossRegionInference: app.node.tryGetContext(
        "enableBedrockCrossRegionInference"
      ),
      enableLambdaSnapStart: app.node.tryGetContext("enableLambdaSnapStart"),
      alternateDomainName: app.node.tryGetContext("alternateDomainName"),
      hostedZoneId: app.node.tryGetContext("hostedZoneId"),
    };

    return BedrockChatParametersSchema.parse(contextParams);
  }

  // If environment is not 'default' and not found in bedrockChatParams, throw an error
  throw new Error(
    `Environment '${environment}' not found in bedrockChatParams`
  );
}

/**
 * Parse and validate CDK context parameters for API publishing
 * @param app CDK App instance
 * @returns Validated parameters object
 */
export function getApiPublishParameters(app: any): ApiPublishParameters {
  const contextParams = {
    bedrockRegion: app.node.tryGetContext("bedrockRegion"),
    publishedApiThrottleRateLimit: app.node.tryGetContext(
      "publishedApiThrottleRateLimit"
    )
      ? Number(app.node.tryGetContext("publishedApiThrottleRateLimit"))
      : undefined,
    publishedApiThrottleBurstLimit: app.node.tryGetContext(
      "publishedApiThrottleBurstLimit"
    )
      ? Number(app.node.tryGetContext("publishedApiThrottleBurstLimit"))
      : undefined,
    publishedApiQuotaLimit: app.node.tryGetContext("publishedApiQuotaLimit")
      ? Number(app.node.tryGetContext("publishedApiQuotaLimit"))
      : undefined,
    publishedApiQuotaPeriod: app.node.tryGetContext("publishedApiQuotaPeriod"),
    publishedApiDeploymentStage: app.node.tryGetContext(
      "publishedApiDeploymentStage"
    ),
    publishedApiId: app.node.tryGetContext("publishedApiId"),
    publishedApiAllowedOrigins: app.node.tryGetContext(
      "publishedApiAllowedOrigins"
    ),
  };

  return ApiPublishParametersSchema.parse(contextParams);
}

/**
 * Parse and validate CDK context parameters for Bedrock Custom Bot
 * @param app CDK App instance
 * @returns Validated parameters object
 */
export function getBedrockCustomBotParameters(
  app: any
): BedrockCustomBotParameters {
  const contextParams = {
    bedrockRegion: app.node.tryGetContext("bedrockRegion"),
  };

  return BedrockCustomBotParametersSchema.parse(contextParams);
}