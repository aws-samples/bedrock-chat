import { App } from "aws-cdk-lib";
import { 
  resolveBedrockChatParameters,
  resolveApiPublishParameters,
  resolveBedrockCustomBotParameters
} from "../../lib/utils/parameter-models";
import { ZodError } from "zod";

describe("resolveBedrockChatParameters", () => {
  describe("パラメータソースの選択", () => {
    test("parametersInputが指定されている場合、それが使用される", () => {
      // Arrange
      const app = new App({
        autoSynth: false,
      });
      const inputParams = {
        bedrockRegion: "eu-west-1",
        enableMistral: true,
      };

      // Act
      const result = resolveBedrockChatParameters(app, inputParams);

      // Assert
      expect(result.bedrockRegion).toBe("eu-west-1");
      expect(result.enableMistral).toBe(true);
    });

    test("parametersInputが未指定の場合、コンテキストからパラメータが取得される", () => {
      // Arrange
      const app = new App({
        autoSynth: false,
        context: {
          bedrockRegion: "ap-northeast-1",
          enableMistral: true,
        },
      });

      // Act
      const result = resolveBedrockChatParameters(app);

      // Assert
      expect(result.bedrockRegion).toBe("ap-northeast-1");
      expect(result.enableMistral).toBe(true);
    });
  });

  describe("パラメータのバリデーション", () => {
    test("必須パラメータが欠けている場合でも、デフォルト値が適用される", () => {
      // Arrange
      const app = new App({
        autoSynth: false,
      });

      // Act
      const result = resolveBedrockChatParameters(app);

      // Assert
      expect(result.bedrockRegion).toBe("us-east-1"); // デフォルト値
      expect(result.enableMistral).toBe(false); // デフォルト値
      expect(result.allowedIpV4AddressRanges).toEqual([
        "0.0.0.0/1",
        "128.0.0.0/1",
      ]); // デフォルト値
    });

    test("すべてのパラメータが指定されている場合、正しく解析される", () => {
      // Arrange
      const app = new App({
        autoSynth: false,
      });
      const inputParams = {
        bedrockRegion: "us-west-2",
        enableMistral: true,
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
      };

      // Act
      const result = resolveBedrockChatParameters(app, inputParams);

      // Assert
      expect(result.bedrockRegion).toBe("us-west-2");
      expect(result.enableMistral).toBe(true);
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
    });

    test("無効なパラメータが指定された場合、ZodErrorがスローされる", () => {
      // Arrange
      const app = new App({
        autoSynth: false,
      });
      const invalidParams = {
        bedrockRegion: 123, // 文字列ではなく数値
      };

      // Act & Assert
      expect(() => {
        resolveBedrockChatParameters(app, invalidParams as any);
      }).toThrow(ZodError);
    });
  });

  describe("特殊なパラメータ処理", () => {
    test("配列パラメータが正しく処理される", () => {
      // Arrange
      const app = new App({
        autoSynth: false,
      });
      const inputParams = {
        allowedIpV4AddressRanges: ["192.168.1.0/24", "10.0.0.0/8"],
        allowedSignUpEmailDomains: ["example.com", "test.com"],
      };

      // Act
      const result = resolveBedrockChatParameters(app, inputParams);

      // Assert
      expect(result.allowedIpV4AddressRanges).toEqual([
        "192.168.1.0/24",
        "10.0.0.0/8",
      ]);
      expect(result.allowedSignUpEmailDomains).toEqual([
        "example.com",
        "test.com",
      ]);
    });

    test("ブール値パラメータが正しく処理される", () => {
      // Arrange
      const app = new App({
        autoSynth: false,
      });
      const inputParams = {
        enableMistral: true,
        selfSignUpEnabled: false,
        enableRagReplicas: true,
        enableBedrockCrossRegionInference: false,
        enableLambdaSnapStart: true,
      };

      // Act
      const result = resolveBedrockChatParameters(app, inputParams);

      // Assert
      expect(result.enableMistral).toBe(true);
      expect(result.selfSignUpEnabled).toBe(false);
      expect(result.enableRagReplicas).toBe(true);
      expect(result.enableBedrockCrossRegionInference).toBe(false);
      expect(result.enableLambdaSnapStart).toBe(true);
    });

    test("identityProvidersが配列でない場合、デフォルト値（空配列）が適用される", () => {
      // Arrange
      const app = new App({
        autoSynth: false,
        context: {
          identityProviders: "invalid", // 配列ではなく文字列
        },
      });

      // Act
      const result = resolveBedrockChatParameters(app);

      // Assert
      expect(result.identityProviders).toEqual([]);
    });

    test("identityProvidersが無効なサービスを含む場合でも、バリデーションはパスする", () => {
      // Arrange
      const app = new App({
        autoSynth: false,
      });
      const inputParams = {
        identityProviders: [{ service: "invalid", secretName: "Secret" }],
      };

      // Act
      const result = resolveBedrockChatParameters(app, inputParams);

      // Assert
      expect(result.identityProviders).toEqual([
        { service: "invalid", secretName: "Secret" },
      ]);
      // 注: 実際のバリデーションはidentityProvider関数内で行われる
    });
  });

  test("cdk.jsonのcontextプロパティの値を模倣したテスト", () => {
    // Arrange
    const app = new App({
      autoSynth: false,
      context: {
        enableMistral: false,
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
      },
    });

    // Act
    const result = resolveBedrockChatParameters(app);

    // Assert
    expect(result.bedrockRegion).toBe("us-east-1");
    expect(result.enableMistral).toBe(false);
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
  });
});

describe("resolveApiPublishParameters", () => {
  describe("パラメータソースの選択", () => {
    test("parametersInputが指定されている場合、それが使用される", () => {
      // Arrange
      const app = new App({
        autoSynth: false,
      });
      const inputParams = {
        bedrockRegion: "eu-west-1",
        publishedApiThrottleRateLimit: 100,
        publishedApiAllowedOrigins: '["https://example.com"]',
      };

      // Act
      const result = resolveApiPublishParameters(app, inputParams);

      // Assert
      expect(result.bedrockRegion).toBe("eu-west-1");
      expect(result.publishedApiThrottleRateLimit).toBe(100);
      expect(result.publishedApiAllowedOrigins).toBe('["https://example.com"]');
    });

    test("parametersInputが未指定の場合、コンテキストからパラメータが取得される", () => {
      // Arrange
      const app = new App({
        autoSynth: false,
        context: {
          bedrockRegion: "ap-northeast-1",
          publishedApiThrottleRateLimit: 200,
          publishedApiAllowedOrigins: '["https://test.com"]',
        },
      });

      // Act
      const result = resolveApiPublishParameters(app);

      // Assert
      expect(result.bedrockRegion).toBe("ap-northeast-1");
      expect(result.publishedApiThrottleRateLimit).toBe(200);
      expect(result.publishedApiAllowedOrigins).toBe('["https://test.com"]');
    });
  });

  describe("パラメータのバリデーション", () => {
    test("必須パラメータが欠けている場合でも、デフォルト値が適用される", () => {
      // Arrange
      const app = new App({
        autoSynth: false,
      });

      // Act
      const result = resolveApiPublishParameters(app);

      // Assert
      expect(result.bedrockRegion).toBe("us-east-1"); // デフォルト値
      expect(result.publishedApiAllowedOrigins).toBe('["*"]'); // デフォルト値
      expect(result.publishedApiThrottleRateLimit).toBeUndefined(); // オプショナル
    });

    test("数値パラメータが文字列として提供された場合、数値に変換される", () => {
      // Arrange
      const app = new App({
        autoSynth: false,
        context: {
          publishedApiThrottleRateLimit: "100",
          publishedApiThrottleBurstLimit: "200",
          publishedApiQuotaLimit: "1000",
        },
      });

      // Act
      const result = resolveApiPublishParameters(app);

      // Assert
      expect(result.publishedApiThrottleRateLimit).toBe(100);
      expect(result.publishedApiThrottleBurstLimit).toBe(200);
      expect(result.publishedApiQuotaLimit).toBe(1000);
    });

    test("すべてのパラメータが指定されている場合、正しく解析される", () => {
      // Arrange
      const app = new App({
        autoSynth: false,
      });
      const inputParams = {
        bedrockRegion: "us-west-2",
        publishedApiThrottleRateLimit: 100,
        publishedApiThrottleBurstLimit: 200,
        publishedApiQuotaLimit: 1000,
        publishedApiQuotaPeriod: "DAY" as "DAY" | "WEEK" | "MONTH",
        publishedApiDeploymentStage: "prod",
        publishedApiId: "api123",
        publishedApiAllowedOrigins: '["https://example.com", "https://test.com"]',
      };

      // Act
      const result = resolveApiPublishParameters(app, inputParams);

      // Assert
      expect(result.bedrockRegion).toBe("us-west-2");
      expect(result.publishedApiThrottleRateLimit).toBe(100);
      expect(result.publishedApiThrottleBurstLimit).toBe(200);
      expect(result.publishedApiQuotaLimit).toBe(1000);
      expect(result.publishedApiQuotaPeriod).toBe("DAY");
      expect(result.publishedApiDeploymentStage).toBe("prod");
      expect(result.publishedApiId).toBe("api123");
      expect(result.publishedApiAllowedOrigins).toBe('["https://example.com", "https://test.com"]');
    });

    test("無効なQuotaPeriodが指定された場合、ZodErrorがスローされる", () => {
      // Arrange
      const app = new App({
        autoSynth: false,
      });
      const invalidParams = {
        publishedApiQuotaPeriod: "YEAR" as any, // 無効な値
      };

      // Act & Assert
      expect(() => {
        resolveApiPublishParameters(app, invalidParams as any);
      }).toThrow(ZodError);
    });
  });
});

describe("resolveBedrockCustomBotParameters", () => {
  describe("パラメータソースの選択", () => {
    test("parametersInputが指定されている場合、それが使用される", () => {
      // Arrange
      const app = new App({
        autoSynth: false,
      });
      const inputParams = {
        bedrockRegion: "eu-west-1",
      };

      // Act
      const result = resolveBedrockCustomBotParameters(app, inputParams);

      // Assert
      expect(result.bedrockRegion).toBe("eu-west-1");
    });

    test("parametersInputが未指定の場合、コンテキストからパラメータが取得される", () => {
      // Arrange
      const app = new App({
        autoSynth: false,
        context: {
          bedrockRegion: "ap-northeast-1",
        },
      });

      // Act
      const result = resolveBedrockCustomBotParameters(app);

      // Assert
      expect(result.bedrockRegion).toBe("ap-northeast-1");
    });
  });

  describe("パラメータのバリデーション", () => {
    test("必須パラメータが欠けている場合でも、デフォルト値が適用される", () => {
      // Arrange
      const app = new App({
        autoSynth: false,
      });

      // Act
      const result = resolveBedrockCustomBotParameters(app);

      // Assert
      expect(result.bedrockRegion).toBe("us-east-1"); // デフォルト値
    });

    test("無効なパラメータが指定された場合、ZodErrorがスローされる", () => {
      // Arrange
      const app = new App({
        autoSynth: false,
      });
      const invalidParams = {
        bedrockRegion: 123, // 文字列ではなく数値
      };

      // Act & Assert
      expect(() => {
        resolveBedrockCustomBotParameters(app, invalidParams as any);
      }).toThrow(ZodError);
    });
  });
});