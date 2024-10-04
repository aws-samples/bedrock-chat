import * as cdk from "aws-cdk-lib";
import { BedrockChatStack } from "../lib/bedrock-chat-stack";
import { Template } from "aws-cdk-lib/assertions";
import { AwsPrototypingChecks } from "@aws-prototyping-sdk/pdk-nag";
import {
  getEmbeddingModel,
  getChunkingStrategy,
  getAnalyzer,
} from "../lib/utils/bedrock-knowledge-base-args";
import { BedrockCustomBotStack } from "../lib/bedrock-custom-bot-stack";
import { BedrockRegionResourcesStack } from "../lib/bedrock-region-resources";
import { Analyzer } from "@cdklabs/generative-ai-cdk-constructs/lib/cdk-lib/opensearch-vectorindex";

describe("Bedrock Chat Stack Test", () => {
  test("Identity Provider Generation", () => {
    const app = new cdk.App();

    const domainPrefix = "test-domain";

    const bedrockRegionResourcesStack = new BedrockRegionResourcesStack(app, "BedrockRegionResourcesStack", {
      env: {
        region: "us-east-1",
      },
      crossRegionReferences: true,
    })

    const hasGoogleProviderStack = new BedrockChatStack(
      app,
      "IdentityProviderGenerateStack",
      {
        env: {
          region: "us-west-2",
        },
        bedrockRegion: "us-east-1",
        crossRegionReferences: true,
        webAclId: "",
        identityProviders: [
          {
            secretName: "MyTestSecret",
            service: "google",
          },
        ],
        userPoolDomainPrefix: domainPrefix,
        publishedApiAllowedIpV4AddressRanges: [""],
        publishedApiAllowedIpV6AddressRanges: [""],
        allowedSignUpEmailDomains: [],
        autoJoinUserGroups: [],
        rdsSchedules: {
          stop: {},
          start: {},
        },
        enableMistral: false,
        enableKB: false,
        selfSignUpEnabled: true,
        embeddingContainerVcpu: 1024,
        embeddingContainerMemory: 2048,
        natgatewayCount: 2,
        enableIpV6: true,
        documentBucket: bedrockRegionResourcesStack.documentBucket,
      }
    );
    const hasGoogleProviderTemplate = Template.fromStack(
      hasGoogleProviderStack
    );

    hasGoogleProviderTemplate.hasResourceProperties(
      "AWS::Cognito::UserPoolDomain",
      {
        Domain: domainPrefix,
      }
    );
    hasGoogleProviderTemplate.hasResourceProperties(
      "AWS::Cognito::UserPoolClient",
      {
        SupportedIdentityProviders: ["Google", "COGNITO"],
      }
    );
    hasGoogleProviderTemplate.hasResourceProperties(
      "AWS::Cognito::UserPoolIdentityProvider",
      {
        ProviderName: "Google",
        ProviderType: "Google",
      }
    );
  });

  test("Custom OIDC Provider Generation", () => {
    const app = new cdk.App();
    const domainPrefix = "test-domain";

    const bedrockRegionResourcesStack = new BedrockRegionResourcesStack(app, "BedrockRegionResourcesStack", {
      env: {
        region: "us-east-1",
      },
      crossRegionReferences: true,
    })

    const hasOidcProviderStack = new BedrockChatStack(
      app,
      "OidcProviderGenerateStack",
      {
        env: {
          region: "us-west-2",
        },
        bedrockRegion: "us-east-1",
        crossRegionReferences: true,
        webAclId: "",
        identityProviders: [
          {
            secretName: "MyOidcTestSecret",
            service: "oidc",
            serviceName: "MyOidcProvider",
          },
        ],
        userPoolDomainPrefix: domainPrefix,
        publishedApiAllowedIpV4AddressRanges: [""],
        publishedApiAllowedIpV6AddressRanges: [""],
        allowedSignUpEmailDomains: [],
        autoJoinUserGroups: [],
        rdsSchedules: {
          stop: {},
          start: {},
        },
        enableMistral: false,
        enableKB: false,
        selfSignUpEnabled: true,
        embeddingContainerVcpu: 1024,
        embeddingContainerMemory: 2048,
        natgatewayCount: 2,
        enableIpV6: true,
        documentBucket: bedrockRegionResourcesStack.documentBucket,
      }
    );
    const hasOidcProviderTemplate = Template.fromStack(hasOidcProviderStack);

    hasOidcProviderTemplate.hasResourceProperties(
      "AWS::Cognito::UserPoolDomain",
      {
        Domain: domainPrefix,
      }
    );

    hasOidcProviderTemplate.hasResourceProperties(
      "AWS::Cognito::UserPoolClient",
      {
        SupportedIdentityProviders: ["MyOidcProvider", "COGNITO"],
      }
    );
    hasOidcProviderTemplate.hasResourceProperties(
      "AWS::Cognito::UserPoolIdentityProvider",
      {
        ProviderType: "OIDC",
      }
    );
  });

  test("default stack", () => {
    const app = new cdk.App();
    // Security check
    cdk.Aspects.of(app).add(new AwsPrototypingChecks());

    const bedrockRegionResourcesStack = new BedrockRegionResourcesStack(app, "BedrockRegionResourcesStack", {
      env: {
        region: "us-east-1",
      },
      crossRegionReferences: true,
    })

    const stack = new BedrockChatStack(app, "MyTestStack", {
      env: {
        region: "us-west-2",
      },
      bedrockRegion: "us-east-1",
      crossRegionReferences: true,
      webAclId: "",
      identityProviders: [],
      userPoolDomainPrefix: "",
      publishedApiAllowedIpV4AddressRanges: [""],
      publishedApiAllowedIpV6AddressRanges: [""],
      allowedSignUpEmailDomains: [],
      autoJoinUserGroups: [],
      rdsSchedules: {
        stop: {},
        start: {},
      },
      enableMistral: false,
      enableKB: false,
      selfSignUpEnabled: true,
      embeddingContainerVcpu: 1024,
      embeddingContainerMemory: 2048,
      natgatewayCount: 2,
      enableIpV6: true,
      documentBucket: bedrockRegionResourcesStack.documentBucket,
    });
    const template = Template.fromStack(stack);

    template.resourceCountIs("AWS::Cognito::UserPoolIdentityProvider", 0);
    // verify the stack has environment variable VITE_APP_ENABLE_MISTRAL is set to "false"
    template.hasResourceProperties("Custom::CDKNodejsBuild", {
      environment: {
        VITE_APP_ENABLE_MISTRAL: "false",
      },
    });
  });
});

describe("Scheduler Test", () => {
  test("has schedules", () => {
    const app = new cdk.App();

    const bedrockRegionResourcesStack = new BedrockRegionResourcesStack(app, "BedrockRegionResourcesStack", {
      env: {
        region: "us-east-1",
      },
      crossRegionReferences: true,
    })

    const hasScheduleStack = new BedrockChatStack(app, "HasSchedulesStack", {
      env: {
        region: "us-west-2",
      },
      bedrockRegion: "us-east-1",
      crossRegionReferences: true,
      webAclId: "",
      identityProviders: [],
      userPoolDomainPrefix: "",
      publishedApiAllowedIpV4AddressRanges: [""],
      publishedApiAllowedIpV6AddressRanges: [""],
      allowedSignUpEmailDomains: [],
      autoJoinUserGroups: [],
      rdsSchedules: {
        stop: {
          minute: "00",
          hour: "22",
          day: "*",
          month: "*",
          year: "*",
        },
        start: {
          minute: "00",
          hour: "7",
          day: "*",
          month: "*",
          year: "*",
        },
      },
      enableMistral: false,
      enableKB: false,
      selfSignUpEnabled: true,
      embeddingContainerVcpu: 1024,
      embeddingContainerMemory: 2048,
      natgatewayCount: 2,
      enableIpV6: true,
      documentBucket: bedrockRegionResourcesStack.documentBucket,
    });
    const template = Template.fromStack(hasScheduleStack);
    template.hasResourceProperties("AWS::Scheduler::Schedule", {
      ScheduleExpression: "cron(00 22 * * ? *)",
    });

    template.hasResourceProperties("AWS::Scheduler::Schedule", {
      ScheduleExpression: "cron(00 7 * * ? *)",
    });
  });
  test("has'nt schedules", () => {
    const app = new cdk.App();

    const bedrockRegionResourcesStack = new BedrockRegionResourcesStack(app, "BedrockRegionResourcesStack", {
      env: {
        region: "us-east-1",
      },
      crossRegionReferences: true,
    })

    const defaultStack = new BedrockChatStack(app, "DefaultStack", {
      env: {
        region: "us-west-2",
      },
      bedrockRegion: "us-east-1",
      crossRegionReferences: true,
      webAclId: "",
      identityProviders: [],
      userPoolDomainPrefix: "",
      publishedApiAllowedIpV4AddressRanges: [""],
      publishedApiAllowedIpV6AddressRanges: [""],
      allowedSignUpEmailDomains: [],
      autoJoinUserGroups: [],
      rdsSchedules: {
        stop: {},
        start: {},
      },
      enableMistral: false,
      enableKB: false,
      selfSignUpEnabled: true,
      embeddingContainerVcpu: 1024,
      embeddingContainerMemory: 2048,
      natgatewayCount: 2,
      enableIpV6: true,
      documentBucket: bedrockRegionResourcesStack.documentBucket,
    });
    const template = Template.fromStack(defaultStack);
    // The stack should have only 1 rule for exporting the data from ddb to s3
    template.resourceCountIs("AWS::Events::Rule", 1);
  });
});

describe("Bedrock Knowledge Base Stack", () => {
  const setupStack = (params: any = {}) => {
    const app = new cdk.App();
    // Security check
    cdk.Aspects.of(app).add(new AwsPrototypingChecks());

    const PK: string = "test-user-id";
    const SK: string = "test-user-id#BOT#test-bot-id";
    const KNOWLEDGE = {
      sitemap_urls: {
        L: [],
      },
      filenames: {
        L: [
          {
            S: "test-filename.pdf",
          },
        ],
      },
      source_urls: {
        L: [
          {
            S: "https://example.com",
          },
        ],
      },
      s3_urls: params.s3Urls !== undefined ? params.s3Urls : { L: [] },
    };

    const BEDROCK_KNOWLEDGE_BASE = {
      chunking_strategy: {
        S: "fixed_size",
      },
      max_tokens:
        params.maxTokens !== undefined
          ? { N: String(params.maxTokens) }
          : undefined,
      instruction:
        params.instruction !== undefined
          ? { S: params.instruction }
          : undefined,
      overlap_percentage:
        params.overlapPercentage !== undefined
          ? { N: String(params.overlapPercentage) }
          : undefined,
      open_search: {
        M: {
          analyzer:
            params.analyzer !== undefined
              ? JSON.parse(params.analyzer)
              : {
                  character_filters: {
                    L: [
                      {
                        S: "icu_normalizer",
                      },
                    ],
                  },
                  token_filters: {
                    L: [
                      {
                        S: "kuromoji_baseform",
                      },
                      {
                        S: "kuromoji_part_of_speech",
                      },
                    ],
                  },
                  tokenizer: {
                    S: "kuromoji_tokenizer",
                  },
                },
        },
      },
      embeddings_model: {
        S: "titan_v2",
      },
    };

    const BEDROCK_CLAUDE_CHAT_DOCUMENT_BUCKET_NAME =
      "test-document-bucket-name";

    const ownerUserId: string = PK;
    const botId: string = SK.split("#")[2];
    const knowledgeBase = BEDROCK_KNOWLEDGE_BASE;
    const knowledge = KNOWLEDGE;
    const existingS3Urls: string[] = knowledge.s3_urls.L.map(
      (s3Url: any) => s3Url.S
    );

    const embeddingsModel = getEmbeddingModel(knowledgeBase.embeddings_model.S);
    const chunkingStrategy = getChunkingStrategy(
      knowledgeBase.chunking_strategy.S
    );
    const maxTokens: number | undefined = knowledgeBase.max_tokens
      ? Number(knowledgeBase.max_tokens.N)
      : undefined;
    const instruction: string | undefined = knowledgeBase.instruction
      ? knowledgeBase.instruction.S
      : undefined;
    const analyzer = knowledgeBase.open_search.M.analyzer
      ? getAnalyzer(knowledgeBase.open_search.M.analyzer)
      : undefined;
    const overlapPercentage: number | undefined =
      knowledgeBase.overlap_percentage
        ? Number(knowledgeBase.overlap_percentage.N)
        : undefined;

    const stack = new BedrockCustomBotStack(
      app,
      "BedrockCustomBotStackStack",
      {
        ownerUserId,
        botId,
        embeddingsModel,
        bedrockClaudeChatDocumentBucketName:
          BEDROCK_CLAUDE_CHAT_DOCUMENT_BUCKET_NAME,
        chunkingStrategy,
        existingS3Urls,
        maxTokens,
        instruction,
        analyzer,
        overlapPercentage,
      }
    );

    return Template.fromStack(stack);
  };

  test("default kb stack", () => {
    const template = setupStack({
      s3Urls: {
        L: [
          {
            S: "s3://test-bucket/test-key",
          },
        ],
      },
      maxTokens: 500,
      instruction: "This is an example instruction.",
      overlapPercentage: 10,
      analyzer: `{
        "character_filters": {
          "L": [
            {
              "S": "icu_normalizer"
            }
          ]
        },
        "token_filters": {
          "L": [
            {
              "S": "kuromoji_baseform"
            },
            {
              "S": "kuromoji_part_of_speech"
            }
          ]
        },
        "tokenizer": {
          "S": "kuromoji_tokenizer"
        }
      }`,
    });
    expect(template).toBeDefined();
  });

  test("kb stack without maxTokens", () => {
    const template = setupStack({
      instruction: "This is an example instruction.",
      overlapPercentage: 10,
      analyzer: `{
        "character_filters": {
          "L": [
            {
              "S": "icu_normalizer"
            }
          ]
        },
        "token_filters": {
          "L": [
            {
              "S": "kuromoji_baseform"
            },
            {
              "S": "kuromoji_part_of_speech"
            }
          ]
        },
        "tokenizer": {
          "S": "kuromoji_tokenizer"
        }
      }`,
    });
    expect(template).toBeDefined();
  });

  test("kb stack without instruction", () => {
    const template = setupStack({
      maxTokens: 500,
      overlapPercentage: 10,
      analyzer: `{
        "character_filters": {
          "L": [
            {
              "S": "icu_normalizer"
            }
          ]
        },
        "token_filters": {
          "L": [
            {
              "S": "kuromoji_baseform"
            },
            {
              "S": "kuromoji_part_of_speech"
            }
          ]
        },
        "tokenizer": {
          "S": "kuromoji_tokenizer"
        }
      }`,
    });
    expect(template).toBeDefined();
  });

  test("kb stack without analyzer", () => {
    const template = setupStack({
      maxTokens: 500,
      instruction: "This is an example instruction.",
      overlapPercentage: 10,
    });
    expect(template).toBeDefined();
  });

  test("kb stack without overlapPercentage", () => {
    const template = setupStack({
      maxTokens: 500,
      instruction: "This is an example instruction.",
      analyzer: `{
        "character_filters": {
          "L": [
            {
              "S": "icu_normalizer"
            }
          ]
        },
        "token_filters": {
          "L": [
            {
              "S": "kuromoji_baseform"
            },
            {
              "S": "kuromoji_part_of_speech"
            }
          ]
        },
        "tokenizer": {
          "S": "kuromoji_tokenizer"
        }
      }`,
    });
    expect(template).toBeDefined();
  });
});
