import { z } from "zod";
import { TIdentityProvider } from "./identity-provider";
import { App } from "aws-cdk-lib";

/**
 * Base parameters schema that is common across all entry points
 */
const BaseParametersSchema = z.object({
  // Bedrock configuration
  bedrockRegion: z.string().default("us-east-1"),
});

/**
 * Parameters schema for the main Bedrock Chat application
 */
const BedrockChatParametersSchema = BaseParametersSchema.extend({
  // CDK Environments
  envName: z.string().default("default"),
  envPrefix: z.string().default(""),

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
const ApiPublishParametersSchema = BaseParametersSchema.extend({
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
const BedrockCustomBotParametersSchema = BaseParametersSchema;

/**
 * Type definitions for each parameter set
 */
// Input types (for user input, default values are optional)
export type BaseParametersInput = z.input<typeof BaseParametersSchema>;
export type BedrockChatParametersInput = z.input<
  typeof BedrockChatParametersSchema
>;
export type ApiPublishParametersInput = z.input<
  typeof ApiPublishParametersSchema
>;
export type BedrockCustomBotParametersInput = z.input<
  typeof BedrockCustomBotParametersSchema
>;

// Output types (for function returns, all properties are required)
export type BaseParameters = z.infer<typeof BaseParametersSchema>;
export type BedrockChatParameters = z.infer<typeof BedrockChatParametersSchema>;
export type ApiPublishParameters = z.infer<typeof ApiPublishParametersSchema>;
export type BedrockCustomBotParameters = z.infer<
  typeof BedrockCustomBotParametersSchema
>;

/**
 * Parse and validate parameters for the main Bedrock Chat application.
 * If you omit parametersInput, context parameters are used.
 * @param app CDK App instance
 * @param parametersInput (optional) Input parameters that should be used instead of context parameters
 * @returns Validated parameters object
 */
export function resolveBedrockChatParameters(
  app: App,
  parametersInput?: BedrockChatParametersInput
): BedrockChatParameters {
  // If parametersInput is provided, use it directly
  if (parametersInput) {
    return BedrockChatParametersSchema.parse(parametersInput);
  }

  // Otherwise, get parameters from context
  const identityProviders = app.node.tryGetContext("identityProviders");

  const contextParams = {
    envName: "default",
    envPrefix: "",
    bedrockRegion: app.node.tryGetContext("bedrockRegion"),
    enableMistral: app.node.tryGetContext("enableMistral"),
    allowedIpV4AddressRanges: app.node.tryGetContext(
      "allowedIpV4AddressRanges"
    ),
    allowedIpV6AddressRanges: app.node.tryGetContext(
      "allowedIpV6AddressRanges"
    ),
    // 配列でない場合は空配列を使用
    identityProviders: Array.isArray(identityProviders)
      ? identityProviders
      : [],
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

/**
 * Get Bedrock Chat parameters based on environment name.
 * If you omit envName, "default" is used.
 * If you omit parametersInput, context parameters are used.
 * @param app CDK App instance
 * @param envName (optional) Environment name. Used as map key if provided
 * @param paramsMap (optional) Map of parameters. If not provided, use context parameters
 * @returns Validated parameters object
 */
export function getBedrockChatParameters(
  app: App,
  envName: string | undefined,
  paramsMap: Map<string, BedrockChatParametersInput>
): BedrockChatParameters {
  if (envName == undefined) {
    if (paramsMap.has("default")) {
      // Use parameter.ts instead of context parameters
      const params = paramsMap.get("default") || {};
      return resolveBedrockChatParameters(app, {
        envName: "default",
        envPrefix: "",
        ...params,
      });
    } else {
      // Use CDK context parameters (cdk.json or -c options)
      return resolveBedrockChatParameters(app);
    }
  } else {
    // Lookup envName in parameter.ts
    if (!paramsMap.has(envName)) {
      throw new Error(`Environment ${envName} not found in parameter.ts`);
    }

    const params = paramsMap.get(envName) || {};
    const envPrefix = envName === "default" ? "" : envName;

    return resolveBedrockChatParameters(app, {
      envName,
      envPrefix,
      ...params,
    });
  }
}

/**
 * Parse and validate parameters for API publishing
 * @param app CDK App instance
 * @param parametersInput Optional input parameters that override context values
 * @returns Validated parameters object
 */
export function resolveApiPublishParameters(
  app: App,
  parametersInput?: ApiPublishParametersInput
): ApiPublishParameters {
  // If parametersInput is provided, use it directly
  if (parametersInput) {
    return ApiPublishParametersSchema.parse(parametersInput);
  }

  // Otherwise, get parameters from context
  const publishedApiThrottleRateLimit = app.node.tryGetContext(
    "publishedApiThrottleRateLimit"
  );
  const publishedApiThrottleBurstLimit = app.node.tryGetContext(
    "publishedApiThrottleBurstLimit"
  );
  const publishedApiQuotaLimit = app.node.tryGetContext(
    "publishedApiQuotaLimit"
  );
  const publishedApiAllowedOrigins = app.node.tryGetContext(
    "publishedApiAllowedOrigins"
  );

  const contextParams = {
    bedrockRegion: app.node.tryGetContext("bedrockRegion"),
    publishedApiThrottleRateLimit: publishedApiThrottleRateLimit
      ? Number(publishedApiThrottleRateLimit)
      : undefined,
    publishedApiThrottleBurstLimit: publishedApiThrottleBurstLimit
      ? Number(publishedApiThrottleBurstLimit)
      : undefined,
    publishedApiQuotaLimit: publishedApiQuotaLimit
      ? Number(publishedApiQuotaLimit)
      : undefined,
    publishedApiQuotaPeriod: app.node.tryGetContext("publishedApiQuotaPeriod"),
    publishedApiDeploymentStage: app.node.tryGetContext(
      "publishedApiDeploymentStage"
    ),
    publishedApiId: app.node.tryGetContext("publishedApiId"),
    publishedApiAllowedOrigins: publishedApiAllowedOrigins || '["*"]',
  };

  return ApiPublishParametersSchema.parse(contextParams);
}

/**
 * Parse and validate parameters for Bedrock Custom Bot
 * @param app CDK App instance
 * @param parametersInput Optional input parameters that override context values
 * @returns Validated parameters object
 */
export function resolveBedrockCustomBotParameters(
  app: App,
  parametersInput?: BedrockCustomBotParametersInput
): BedrockCustomBotParameters {
  // If parametersInput is provided, use it directly
  if (parametersInput) {
    return BedrockCustomBotParametersSchema.parse(parametersInput);
  }

  // Otherwise, get parameters from context
  const contextParams = {
    bedrockRegion: app.node.tryGetContext("bedrockRegion"),
  };

  return BedrockCustomBotParametersSchema.parse(contextParams);
}
