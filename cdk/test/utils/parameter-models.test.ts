import { App } from "aws-cdk-lib";
import {
  resolveBedrockChatParameters,
  resolveApiPublishParameters,
  resolveBedrockCustomBotParameters,
  BedrockChatParametersInput,
  getBedrockChatParameters,
} from "../../lib/utils/parameter-models";
import { ZodError } from "zod";

/**
 * Test helper function: create CDK App instance
 */
function createTestApp(context = {}) {
  return new App({
    autoSynth: false,
    context,
  });
}

describe("BaseParametersSchema", () => {
  describe("Parameter Validation", () => {
    describe("envName", () => {
      // set any values for required fields
      const commonParams = {
        bedrockRegion: "eu-west-1",
      };

      test("should not throw ZodError when not set", () => {
        // Given
        const app = createTestApp();
        const inputParams = {
          ...commonParams,
          envName: "",
        };

        // When/Then
        expect(() => {
          resolveBedrockChatParameters(app, inputParams);
        }).not.toThrow();
      });

      test("should not throw ZodError when set 10 characters and Upper case at first character", () => {
        // Given
        const app = createTestApp();
        const inputParams = {
          ...commonParams,
          envName: "Env4567890",
        };

        // When/Then
        expect(() => {
          resolveBedrockChatParameters(app, inputParams);
        }).not.toThrow();
      });

      test("should not throw ZodError when lower case at first character", () => {
        // Given
        const app = createTestApp();
        const inputParams = {
          ...commonParams,
          envName: "env",
        };

        // When/Then
        expect(() => {
          resolveBedrockChatParameters(app, inputParams);
        }).not.toThrow();
      });

      test("should throw ZodError when set 11 characters", () => {
        // Given
        const app = createTestApp();
        const inputParams = {
          ...commonParams,
          envName: "env45678901",
        };

        // When/Then
        expect(() => {
          resolveBedrockChatParameters(app, inputParams);
        }).toThrow();
      });

      test("should throw ZodError when set number at first character", () => {
        // Given
        const app = createTestApp();
        const inputParams = {
          ...commonParams,
          envName: "1env",
        };

        // When/Then
        expect(() => {
          resolveBedrockChatParameters(app, inputParams);
        }).toThrow();
      });

      test("should throw ZodError when set non-alphanumeric character", () => {
        // Given
        const app = createTestApp();
        const inputParams = {
          ...commonParams,
          envName: "!",
        };

        // When/Then
        expect(() => {
          resolveBedrockChatParameters(app, inputParams);
        }).toThrow();
      });
    });
  });
});

describe("resolveBedrockChatParameters", () => {
  describe("Parameter Source Selection", () => {
    test("should use parametersInput when provided", () => {
      // Given
      const app = createTestApp();
      const inputParams = {
        bedrockRegion: "eu-west-1",
      };

      // When
      const result = resolveBedrockChatParameters(app, inputParams);

      // Then
      expect(result.bedrockRegion).toBe("eu-west-1");
    });

    test("should get parameters from context when parametersInput is not provided", () => {
      // Given
      const app = createTestApp({
        bedrockRegion: "ap-northeast-1",
      });

      // When
      const result = resolveBedrockChatParameters(app);

      // Then
      expect(result.bedrockRegion).toBe("ap-northeast-1");
    });
  });

  describe("Parameter Validation", () => {
    test("should apply default values when required parameters are missing", () => {
      // Given
      const app = createTestApp();

      // When
      const result = resolveBedrockChatParameters(app);

      // Then
      expect(result.bedrockRegion).toBe("us-east-1"); // default value
      expect(result.allowedIpV4AddressRanges).toEqual([
        "0.0.0.0/1",
        "128.0.0.0/1",
      ]); // default value
    });

    test("should correctly parse all parameters when specified", () => {
      // Given
      const app = createTestApp();
      const inputParams = {
        bedrockRegion: "us-west-2",
        allowedIpV4AddressRanges: ["192.168.0.0/16"],
        allowedIpV6AddressRanges: ["2001:db8::/32"],
        identityProviders: [{ service: "google", secretName: "GoogleSecret" }],
        userPoolDomainPrefix: "my-app",
        allowedSignUpEmailDomains: ["example.com"],
        autoJoinUserGroups: ["Users"],
        selfSignUpEnabled: false,
        publishedApiAllowedIpV4AddressRanges: ["10.0.0.0/8"],
        publishedApiAllowedIpV6AddressRanges: ["2001:db8:1::/48"],
        enableRagReplicas: false,
        enableBedrockCrossRegionInference: false,
        enableLambdaSnapStart: false,
        alternateDomainName: "chat.example.com",
        hostedZoneId: "Z1234567890",
        devAccessIamRoleArn: "arn:aws:iam::123456789012:role/Admin",
      };

      // When
      const result = resolveBedrockChatParameters(app, inputParams);

      // Then
      expect(result.bedrockRegion).toBe("us-west-2");
      expect(result.allowedIpV4AddressRanges).toEqual(["192.168.0.0/16"]);
      expect(result.allowedIpV6AddressRanges).toEqual(["2001:db8::/32"]);
      expect(result.identityProviders).toEqual([
        { service: "google", secretName: "GoogleSecret" },
      ]);
      expect(result.userPoolDomainPrefix).toBe("my-app");
      expect(result.allowedSignUpEmailDomains).toEqual(["example.com"]);
      expect(result.autoJoinUserGroups).toEqual(["Users"]);
      expect(result.selfSignUpEnabled).toBe(false);
      expect(result.publishedApiAllowedIpV4AddressRanges).toEqual([
        "10.0.0.0/8",
      ]);
      expect(result.publishedApiAllowedIpV6AddressRanges).toEqual([
        "2001:db8:1::/48",
      ]);
      expect(result.enableRagReplicas).toBe(false);
      expect(result.enableBedrockCrossRegionInference).toBe(false);
      expect(result.enableLambdaSnapStart).toBe(false);
      expect(result.alternateDomainName).toBe("chat.example.com");
      expect(result.hostedZoneId).toBe("Z1234567890");
      expect(result.devAccessIamRoleArn).toBe("arn:aws:iam::123456789012:role/Admin")
    });

    test("should throw ZodError when invalid parameter is specified", () => {
      // Given
      const app = createTestApp();
      const invalidParams = {
        bedrockRegion: 123, // number instead of string
      };

      // When/Then
      expect(() => {
        resolveBedrockChatParameters(app, invalidParams as any);
      }).toThrow(ZodError);
    });
  });

  describe("Special Parameter Handling", () => {
    test("should correctly process array parameters", () => {
      // Given
      const app = createTestApp();
      const inputParams = {
        allowedIpV4AddressRanges: ["192.168.1.0/24", "10.0.0.0/8"],
        allowedSignUpEmailDomains: ["example.com", "test.com"],
      };

      // When
      const result = resolveBedrockChatParameters(app, inputParams);

      // Then
      expect(result.allowedIpV4AddressRanges).toEqual([
        "192.168.1.0/24",
        "10.0.0.0/8",
      ]);
      expect(result.allowedSignUpEmailDomains).toEqual([
        "example.com",
        "test.com",
      ]);
    });

    test("should correctly process boolean parameters", () => {
      // Given
      const app = createTestApp();
      const inputParams = {
        selfSignUpEnabled: false,
        enableRagReplicas: true,
        enableBedrockCrossRegionInference: false,
        enableLambdaSnapStart: true,
      };

      // When
      const result = resolveBedrockChatParameters(app, inputParams);

      // Then
      expect(result.selfSignUpEnabled).toBe(false);
      expect(result.enableRagReplicas).toBe(true);
      expect(result.enableBedrockCrossRegionInference).toBe(false);
      expect(result.enableLambdaSnapStart).toBe(true);
    });

    test("should apply default value (empty array) when identityProviders is not an array", () => {
      // Given
      const app = createTestApp({
        identityProviders: "invalid", // string instead of array
      });

      // When
      const result = resolveBedrockChatParameters(app);

      // Then
      expect(result.identityProviders).toEqual([]);
    });

    test("should pass validation even when identityProviders contains invalid service", () => {
      // Given
      const app = createTestApp();
      const inputParams = {
        identityProviders: [{ service: "invalid", secretName: "Secret" }],
      };

      // When
      const result = resolveBedrockChatParameters(app, inputParams);

      // Then
      expect(result.identityProviders).toEqual([
        { service: "invalid", secretName: "Secret" },
      ]);
      // Note: Actual validation is performed in identityProvider function
    });
  });

  test("should correctly parse parameters mimicking cdk.json context properties", () => {
    // Given
    const app = createTestApp({
      bedrockRegion: "us-east-1",
      allowedIpV4AddressRanges: ["0.0.0.0/1", "128.0.0.0/1"],
      allowedIpV6AddressRanges: [
        "0000:0000:0000:0000:0000:0000:0000:0000/1",
        "8000:0000:0000:0000:0000:0000:0000:0000/1",
      ],
      identityProviders: [],
      userPoolDomainPrefix: "",
      allowedSignUpEmailDomains: [],
      autoJoinUserGroups: ["CreatingBotAllowed"],
      selfSignUpEnabled: true,
      publishedApiAllowedIpV4AddressRanges: ["0.0.0.0/1", "128.0.0.0/1"],
      publishedApiAllowedIpV6AddressRanges: [
        "0000:0000:0000:0000:0000:0000:0000:0000/1",
        "8000:0000:0000:0000:0000:0000:0000:0000/1",
      ],
      enableRagReplicas: true,
      enableBedrockCrossRegionInference: true,
      enableLambdaSnapStart: true,
      alternateDomainName: "",
      hostedZoneId: "",
      devAccessIamRoleArn: "",
    });

    // When
    const result = resolveBedrockChatParameters(app);

    // Then
    expect(result.bedrockRegion).toBe("us-east-1");
    expect(result.allowedIpV4AddressRanges).toEqual([
      "0.0.0.0/1",
      "128.0.0.0/1",
    ]);
    expect(result.allowedIpV6AddressRanges).toEqual([
      "0000:0000:0000:0000:0000:0000:0000:0000/1",
      "8000:0000:0000:0000:0000:0000:0000:0000/1",
    ]);
    expect(result.identityProviders).toEqual([]);
    expect(result.userPoolDomainPrefix).toBe("");
    expect(result.allowedSignUpEmailDomains).toEqual([]);
    expect(result.autoJoinUserGroups).toEqual(["CreatingBotAllowed"]);
    expect(result.selfSignUpEnabled).toBe(true);
    expect(result.publishedApiAllowedIpV4AddressRanges).toEqual([
      "0.0.0.0/1",
      "128.0.0.0/1",
    ]);
    expect(result.publishedApiAllowedIpV6AddressRanges).toEqual([
      "0000:0000:0000:0000:0000:0000:0000:0000/1",
      "8000:0000:0000:0000:0000:0000:0000:0000/1",
    ]);
    expect(result.enableRagReplicas).toBe(true);
    expect(result.enableBedrockCrossRegionInference).toBe(true);
    expect(result.enableLambdaSnapStart).toBe(true);
    expect(result.alternateDomainName).toBe("");
    expect(result.hostedZoneId).toBe("");
    expect(result.devAccessIamRoleArn).toBe("");
  });
});

describe("getBedrockChatParameters", () => {
  let app: App;
  let paramsMap: Map<string, BedrockChatParametersInput>;

  beforeEach(() => {
    app = createTestApp();
    paramsMap = new Map<string, BedrockChatParametersInput>();
  });

  describe("Environment Name Handling", () => {
    test("should use params from paramsMap when default exists and envName is undefined", () => {
      // Given
      const defaultParams: BedrockChatParametersInput = {
        bedrockRegion: "us-west-2",
      };
      paramsMap.set("default", defaultParams);

      // When
      const result = getBedrockChatParameters(app, undefined, paramsMap);

      // Then
      expect(result.envName).toBe("default");
      expect(result.envPrefix).toBe("");
      expect(result.bedrockRegion).toBe("us-west-2");
    });

    test("should use CDK context when default doesn't exist in paramsMap and envName is undefined", () => {
      // Given
      app = createTestApp({
        bedrockRegion: "eu-west-1",
      });

      // When
      const result = getBedrockChatParameters(app, undefined, paramsMap);

      // Then
      expect(result.envName).toBe("default");
      expect(result.envPrefix).toBe("");
      expect(result.bedrockRegion).toBe("eu-west-1");
    });

    test("should throw error when envName doesn't exist in paramsMap", () => {
      // Given
      const nonExistentEnvName = "nonexistent";

      // When/Then
      expect(() => {
        getBedrockChatParameters(app, nonExistentEnvName, paramsMap);
      }).toThrow(`Environment ${nonExistentEnvName} not found in parameter.ts`);
    });

    test("should use params with empty envPrefix when envName is default", () => {
      // Given
      const defaultParams: BedrockChatParametersInput = {
        bedrockRegion: "ap-northeast-1",
      };
      paramsMap.set("default", defaultParams);

      // When
      const result = getBedrockChatParameters(app, "default", paramsMap);

      // Then
      expect(result.envName).toBe("default");
      expect(result.envPrefix).toBe("");
      expect(result.bedrockRegion).toBe("ap-northeast-1");
    });

    test("should use params with envName as envPrefix for non-default env", () => {
      // Given
      const devParams: BedrockChatParametersInput = {
        bedrockRegion: "ap-southeast-1",
      };
      paramsMap.set("dev", devParams);

      // When
      const result = getBedrockChatParameters(app, "dev", paramsMap);

      // Then
      expect(result.envName).toBe("dev");
      expect(result.envPrefix).toBe("dev");
      expect(result.bedrockRegion).toBe("ap-southeast-1");
    });
  });

  describe("Parameter Validation", () => {
    test("should apply default values for optional parameters", () => {
      // Given
      const minimalParams: BedrockChatParametersInput = {
        bedrockRegion: "us-east-1",
      };
      paramsMap.set("minimal", minimalParams);

      // When
      const result = getBedrockChatParameters(app, "minimal", paramsMap);

      // Then
      expect(result.bedrockRegion).toBe("us-east-1");
      expect(result.enableBedrockCrossRegionInference).toBe(true);
      expect(result.enableRagReplicas).toBe(true);
      expect(result.enableLambdaSnapStart).toBe(true);
      expect(result.selfSignUpEnabled).toBe(true);
      expect(result.autoJoinUserGroups).toEqual(["CreatingBotAllowed"]);
      expect(result.allowedSignUpEmailDomains).toEqual([]);
      expect(result.identityProviders).toEqual([]);
    });

    test("should override default values with provided values", () => {
      // Given
      const customParams: BedrockChatParametersInput = {
        bedrockRegion: "us-east-2",
        enableBedrockCrossRegionInference: false,
        enableRagReplicas: false,
        enableLambdaSnapStart: false,
        selfSignUpEnabled: false,
        autoJoinUserGroups: ["CustomGroup"],
        allowedSignUpEmailDomains: ["example.com"],
      };
      paramsMap.set("custom", customParams);

      // When
      const result = getBedrockChatParameters(app, "custom", paramsMap);

      // Then
      expect(result.bedrockRegion).toBe("us-east-2");
      expect(result.enableBedrockCrossRegionInference).toBe(false);
      expect(result.enableRagReplicas).toBe(false);
      expect(result.enableLambdaSnapStart).toBe(false);
      expect(result.selfSignUpEnabled).toBe(false);
      expect(result.autoJoinUserGroups).toEqual(["CustomGroup"]);
      expect(result.allowedSignUpEmailDomains).toEqual(["example.com"]);
    });

    test("should use default values when CDK context is empty", () => {
      // Given
      const emptyParamsMap = new Map();

      // When
      const result = getBedrockChatParameters(app, undefined, emptyParamsMap);

      // Then
      expect(result.bedrockRegion).toBe("us-east-1");
      expect(result.enableBedrockCrossRegionInference).toBe(true);
      expect(result.enableRagReplicas).toBe(true);
      expect(result.enableLambdaSnapStart).toBe(true);
    });
  });
});

describe("resolveApiPublishParameters", () => {
  describe("Parameter Source Selection", () => {
    test("should get parameters from environment variables", () => {
      // Given
      // Mock environment variables
      const originalEnv = process.env;
      process.env = {
        ...originalEnv,
        BEDROCK_REGION: "us-east-1",
        PUBLISHED_API_THROTTLE_RATE_LIMIT: "200",
        PUBLISHED_API_ALLOWED_ORIGINS: '["https://test.com"]',
      };

      try {
        // When
        const result = resolveApiPublishParameters();

        // Then
        expect(result.bedrockRegion).toBe("us-east-1");
        expect(result.publishedApiThrottleRateLimit).toBe(200);
        expect(result.publishedApiAllowedOrigins).toBe('["https://test.com"]');
      } finally {
        // Restore original environment
        process.env = originalEnv;
      }
    });
  });

  describe("Parameter Validation", () => {
    test("should apply default values when required parameters are missing", () => {
      // Given
      // When
      const result = resolveApiPublishParameters();

      // Then
      expect(result.bedrockRegion).toBe("us-east-1"); // default value
      expect(result.publishedApiAllowedOrigins).toBe('["*"]'); // default value
      expect(result.publishedApiThrottleRateLimit).toBeUndefined(); // optional
    });

    test("should convert string numeric parameters to numbers", () => {
      // Given
      // Mock environment variables
      const originalEnv = process.env;
      process.env = {
        ...originalEnv,
        PUBLISHED_API_THROTTLE_RATE_LIMIT: "100",
        PUBLISHED_API_THROTTLE_BURST_LIMIT: "200",
        PUBLISHED_API_QUOTA_LIMIT: "1000",
      };

      try {
        // When
        const result = resolveApiPublishParameters();

        // Then
        expect(result.publishedApiThrottleRateLimit).toBe(100);
        expect(result.publishedApiThrottleBurstLimit).toBe(200);
        expect(result.publishedApiQuotaLimit).toBe(1000);
      } finally {
        // Restore original environment
        process.env = originalEnv;
      }
    });

    test("should correctly parse all parameters when specified", () => {
      // Given
      // Mock environment variables
      const originalEnv = process.env;
      process.env = {
        ...originalEnv,
        BEDROCK_REGION: "us-west-2",
        PUBLISHED_API_THROTTLE_RATE_LIMIT: "100",
        PUBLISHED_API_THROTTLE_BURST_LIMIT: "200",
        PUBLISHED_API_QUOTA_LIMIT: "1000",
      };

      try {
        // When
        const result = resolveApiPublishParameters();

        // Then
        expect(result.publishedApiThrottleRateLimit).toBe(100);
        expect(result.publishedApiThrottleBurstLimit).toBe(200);
        expect(result.publishedApiQuotaLimit).toBe(1000);
      } finally {
        // Restore original environment
        process.env = originalEnv;
      }
    });

    test("should correctly parse all parameters when specified", () => {
      // Given
      // Mock environment variables
      const originalEnv = process.env;
      process.env = {
        ...originalEnv,
        BEDROCK_REGION: "us-west-2",
        PUBLISHED_API_THROTTLE_RATE_LIMIT: "100",
        PUBLISHED_API_THROTTLE_BURST_LIMIT: "200",
        PUBLISHED_API_QUOTA_LIMIT: "1000",
        PUBLISHED_API_QUOTA_PERIOD: "DAY",
        PUBLISHED_API_DEPLOYMENT_STAGE: "prod",
        PUBLISHED_API_ID: "api123",
        PUBLISHED_API_ALLOWED_ORIGINS:
          '["https://example.com", "https://test.com"]',
      };

      try {
        // When
        const result = resolveApiPublishParameters();

        // Then
        expect(result.bedrockRegion).toBe("us-west-2");
        expect(result.publishedApiThrottleRateLimit).toBe(100);
        expect(result.publishedApiThrottleBurstLimit).toBe(200);
        expect(result.publishedApiQuotaLimit).toBe(1000);
        expect(result.publishedApiQuotaPeriod).toBe("DAY");
        expect(result.publishedApiDeploymentStage).toBe("prod");
        expect(result.publishedApiId).toBe("api123");
        expect(result.publishedApiAllowedOrigins).toBe(
          '["https://example.com", "https://test.com"]'
        );
      } finally {
        // Restore original environment
        process.env = originalEnv;
      }
    });

    test("should throw ZodError when invalid QuotaPeriod is specified", () => {
      // Given
      // Mock environment variables
      const originalEnv = process.env;
      process.env = {
        ...originalEnv,
        PUBLISHED_API_QUOTA_PERIOD: "YEAR", // invalid value
      };

      try {
        // When/Then
        expect(() => {
          resolveApiPublishParameters();
        }).toThrow(ZodError);
      } finally {
        // Restore original environment
        process.env = originalEnv;
      }
    });

    test("should handle invalid publishedApiAllowedOrigins format", () => {
      // Given
      // Mock environment variables
      const originalEnv = process.env;
      process.env = {
        ...originalEnv,
        PUBLISHED_API_ALLOWED_ORIGINS: "invalid json format",
      };

      try {
        // When
        const result = resolveApiPublishParameters();

        // Then
        // Note: The function doesn't validate JSON format, it just passes the string through
        expect(result.publishedApiAllowedOrigins).toBe("invalid json format");
      } finally {
        // Restore original environment
        process.env = originalEnv;
      }
    });
  });
});

describe("resolveBedrockCustomBotParameters", () => {
  describe("Parameter Source Selection", () => {
    test("should get parameters from environment variables", () => {
      // Given
      // Mock environment variables
      const originalEnv = process.env;
      process.env = {
        ...originalEnv,
        ENV_NAME: "testEnv",
        ENV_PREFIX: "test-prefix",
        BEDROCK_REGION: "us-east-1",
        PK: "env-pk",
        SK: "env-sk",
        BEDROCK_CLAUDE_CHAT_DOCUMENT_BUCKET_NAME: "env-bucket",
        KNOWLEDGE: '{"env": "knowledge"}',
        BEDROCK_KNOWLEDGE_BASE: '{"env": "kb"}',
        BEDROCK_GUARDRAILS: '{"env": "guardrails"}',
        ENABLE_RAG_REPLICAS: "true",
      };

      try {
        // When
        const result = resolveBedrockCustomBotParameters();

        // Then
        expect(result.bedrockRegion).toBe("us-east-1");
        expect(result.envName).toBe("testEnv");
        expect(result.envPrefix).toBe("test-prefix");
        expect(result.pk).toBe("env-pk");
        expect(result.sk).toBe("env-sk");
        expect(result.documentBucketName).toBe("env-bucket");
        expect(result.knowledge).toBe('{"env": "knowledge"}');
        expect(result.knowledgeBase).toBe('{"env": "kb"}');
        expect(result.guardrails).toBe('{"env": "guardrails"}');
        expect(result.enableRagReplicas).toBe(true);
      } finally {
        // Restore original environment
        process.env = originalEnv;
      }
    });
  });

  describe("Parameter Validation", () => {
    test("should throw ZodError when required parameters are missing", () => {
      // Given
      // When/Then
      expect(() => {
        resolveBedrockCustomBotParameters();
      }).toThrow();
    });

    test("should throw ZodError when invalid parameter is specified", () => {
      // Given
      // Mock environment variables with invalid type
      const originalEnv = process.env;
      // Clear all environment variables to ensure required ones are missing
      process.env = {};

      try {
        // When/Then
        expect(() => {
          resolveBedrockCustomBotParameters();
        }).toThrow();
      } finally {
        // Restore original environment
        process.env = originalEnv;
      }
    });
  });
});
