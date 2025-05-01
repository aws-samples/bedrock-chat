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
import { Match } from "aws-cdk-lib/assertions";

describe("Bedrock Chat Stack Test", () => {
  test("Identity Provider Generation", () => {
    const app = new cdk.App();

    const domainPrefix = "test-domain";

    const bedrockRegionResourcesStack = new BedrockRegionResourcesStack(
      app,
      "BedrockRegionResourcesStack",
      {
        env: {
          region: "us-east-1",
        },
        crossRegionReferences: true,
      }
    );

    const hasGoogleProviderStack = new BedrockChatStack(
      app,
      "IdentityProviderGenerateStack",
      {
        env: {
          region: "us-west-2",
        },
        envName: "test",
        envPrefix: "test-",
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
        selfSignUpEnabled: true,
        enableIpV6: true,
        documentBucket: bedrockRegionResourcesStack.documentBucket,
        enableRagReplicas: false,
        enableBedrockCrossRegionInference: false,
        enableLambdaSnapStart: true,
        enableBotStore: true,
        enableBotStoreReplicas: false,
        botStoreLanguage: "en",
        tokenValidMinutes: 60,
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

    const bedrockRegionResourcesStack = new BedrockRegionResourcesStack(
      app,
      "BedrockRegionResourcesStack",
      {
        env: {
          region: "us-east-1",
        },
        crossRegionReferences: true,
      }
    );

    const hasOidcProviderStack = new BedrockChatStack(
      app,
      "OidcProviderGenerateStack",
      {
        env: {
          region: "us-west-2",
        },
        envName: "test",
        envPrefix: "test-",
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
        selfSignUpEnabled: true,
        enableIpV6: true,
        documentBucket: bedrockRegionResourcesStack.documentBucket,
        enableRagReplicas: false,
        enableBedrockCrossRegionInference: false,
        enableLambdaSnapStart: true,
        enableBotStore: true,
        enableBotStoreReplicas: false,
        botStoreLanguage: "en",
        tokenValidMinutes: 60,
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

    const bedrockRegionResourcesStack = new BedrockRegionResourcesStack(
      app,
      "BedrockRegionResourcesStack",
      {
        env: {
          region: "us-east-1",
        },
        crossRegionReferences: true,
      }
    );

    const stack = new BedrockChatStack(app, "MyTestStack", {
      env: {
        region: "us-west-2",
      },
      envName: "test",
      envPrefix: "test-",
      bedrockRegion: "us-east-1",
      crossRegionReferences: true,
      webAclId: "",
      identityProviders: [],
      userPoolDomainPrefix: "",
      publishedApiAllowedIpV4AddressRanges: [""],
      publishedApiAllowedIpV6AddressRanges: [""],
      allowedSignUpEmailDomains: [],
      autoJoinUserGroups: [],
      selfSignUpEnabled: true,
      enableIpV6: true,
      documentBucket: bedrockRegionResourcesStack.documentBucket,
      enableRagReplicas: false,
      enableBedrockCrossRegionInference: false,
      enableLambdaSnapStart: true,
      enableBotStore: true,
      enableBotStoreReplicas: false,
      botStoreLanguage: "en",
      tokenValidMinutes: 60,
    });
    const template = Template.fromStack(stack);

    template.resourceCountIs("AWS::Cognito::UserPoolIdentityProvider", 0);
  });

  test("custom domain configuration", () => {
    const app = new cdk.App();

    const bedrockRegionResourcesStack = new BedrockRegionResourcesStack(
      app,
      "BedrockRegionResourcesStack",
      {
        env: {
          region: "us-east-1",
        },
        crossRegionReferences: true,
      }
    );

    const customDomainStack = new BedrockChatStack(app, "CustomDomainStack", {
      env: {
        region: "us-east-1",
      },
      envName: "test",
      envPrefix: "test-",
      bedrockRegion: "us-east-1",
      crossRegionReferences: true,
      webAclId: "",
      identityProviders: [],
      userPoolDomainPrefix: "",
      publishedApiAllowedIpV4AddressRanges: [""],
      publishedApiAllowedIpV6AddressRanges: [""],
      allowedSignUpEmailDomains: [],
      autoJoinUserGroups: [],
      selfSignUpEnabled: true,
      enableIpV6: true,
      documentBucket: bedrockRegionResourcesStack.documentBucket,
      enableRagReplicas: false,
      enableBedrockCrossRegionInference: false,
      enableLambdaSnapStart: true,
      alternateDomainName: "chat.example.com",
      hostedZoneId: "Z0123456789ABCDEF",
      enableBotStore: true,
      enableBotStoreReplicas: false,
      botStoreLanguage: "en",
      tokenValidMinutes: 60,
    });

    const template = Template.fromStack(customDomainStack);

    // Verify CloudFront distribution has alternate domain name
    template.hasResourceProperties("AWS::CloudFront::Distribution", {
      DistributionConfig: {
        Aliases: ["chat.example.com"],
      },
    });

    // Verify Route53 record is created
    template.hasResourceProperties("AWS::Route53::RecordSet", {
      Name: "chat.example.com.",
      Type: "A",
      AliasTarget: {
        DNSName: {
          "Fn::GetAtt": [Match.anyValue(), "DomainName"],
        },
        HostedZoneId: Match.anyValue(),
      },
      HostedZoneId: "Z0123456789ABCDEF",
    });

    // Verify AAAA record for IPv6
    template.hasResourceProperties("AWS::Route53::RecordSet", {
      Name: "chat.example.com.",
      Type: "AAAA",
      AliasTarget: {
        DNSName: {
          "Fn::GetAtt": [Match.anyValue(), "DomainName"],
        },
        HostedZoneId: Match.anyValue(),
      },
      HostedZoneId: "Z0123456789ABCDEF",
    });
  });

  test("no custom domain configuration", () => {
    const app = new cdk.App();

    const bedrockRegionResourcesStack = new BedrockRegionResourcesStack(
      app,
      "BedrockRegionResourcesStack",
      {
        env: {
          region: "us-east-1",
        },
        crossRegionReferences: true,
      }
    );

    const noDomainStack = new BedrockChatStack(app, "NoDomainStack", {
      env: {
        region: "us-east-1",
      },
      envName: "test",
      envPrefix: "test-",
      bedrockRegion: "us-east-1",
      crossRegionReferences: true,
      webAclId: "",
      identityProviders: [],
      userPoolDomainPrefix: "",
      publishedApiAllowedIpV4AddressRanges: [""],
      publishedApiAllowedIpV6AddressRanges: [""],
      allowedSignUpEmailDomains: [],
      autoJoinUserGroups: [],
      selfSignUpEnabled: true,
      enableIpV6: true,
      documentBucket: bedrockRegionResourcesStack.documentBucket,
      enableRagReplicas: false,
      enableBedrockCrossRegionInference: false,
      enableLambdaSnapStart: true,
      alternateDomainName: "",
      hostedZoneId: "",
      enableBotStore: true,
      enableBotStoreReplicas: false,
      botStoreLanguage: "en",
      tokenValidMinutes: 60,
    });

    const template = Template.fromStack(noDomainStack);

    // Verify no Route53 records are created
    template.resourceCountIs("AWS::Route53::RecordSet", 0);

    // Verify no ACM certificate is created
    template.resourceCountIs("AWS::CertificateManager::Certificate", 0);

    // Verify CloudFront distribution has no aliases
    template.hasResourceProperties("AWS::CloudFront::Distribution", {
      DistributionConfig: {
        Aliases: Match.absent(),
      },
    });
  });

  test("custom domain configuration", () => {
    const app = new cdk.App();

    const bedrockRegionResourcesStack = new BedrockRegionResourcesStack(
      app,
      "BedrockRegionResourcesStack",
      {
        env: {
          region: "us-east-1",
        },
        crossRegionReferences: true,
      }
    );

    const customDomainStack = new BedrockChatStack(app, "CustomDomainStack", {
      env: {
        region: "us-east-1",
      },
      envName: "test",
      envPrefix: "test-",
      bedrockRegion: "us-east-1",
      crossRegionReferences: true,
      webAclId: "",
      identityProviders: [],
      userPoolDomainPrefix: "",
      publishedApiAllowedIpV4AddressRanges: [""],
      publishedApiAllowedIpV6AddressRanges: [""],
      allowedSignUpEmailDomains: [],
      autoJoinUserGroups: [],
      selfSignUpEnabled: true,
      enableIpV6: true,
      documentBucket: bedrockRegionResourcesStack.documentBucket,
      enableRagReplicas: false,
      enableBedrockCrossRegionInference: false,
      enableLambdaSnapStart: true,
      alternateDomainName: "chat.example.com",
      hostedZoneId: "Z0123456789ABCDEF",
      enableBotStore: true,
      enableBotStoreReplicas: false,
      botStoreLanguage: "en",
      tokenValidMinutes: 60,
    });

    const template = Template.fromStack(customDomainStack);

    // Verify CloudFront distribution has alternate domain name
    template.hasResourceProperties("AWS::CloudFront::Distribution", {
      DistributionConfig: {
        Aliases: ["chat.example.com"],
      },
    });

    // Verify Route53 record is created
    template.hasResourceProperties("AWS::Route53::RecordSet", {
      Name: "chat.example.com.",
      Type: "A",
      AliasTarget: {
        DNSName: {
          "Fn::GetAtt": [Match.anyValue(), "DomainName"],
        },
        HostedZoneId: Match.anyValue(),
      },
      HostedZoneId: "Z0123456789ABCDEF",
    });

    // Verify AAAA record for IPv6
    template.hasResourceProperties("AWS::Route53::RecordSet", {
      Name: "chat.example.com.",
      Type: "AAAA",
      AliasTarget: {
        DNSName: {
          "Fn::GetAtt": [Match.anyValue(), "DomainName"],
        },
        HostedZoneId: Match.anyValue(),
      },
      HostedZoneId: "Z0123456789ABCDEF",
    });
  });

  test("no custom domain configuration", () => {
    const app = new cdk.App();

    const bedrockRegionResourcesStack = new BedrockRegionResourcesStack(
      app,
      "BedrockRegionResourcesStack",
      {
        env: {
          region: "us-east-1",
        },
        crossRegionReferences: true,
      }
    );

    const noDomainStack = new BedrockChatStack(app, "NoDomainStack", {
      env: {
        region: "us-east-1",
      },
      envName: "test",
      envPrefix: "test-",
      bedrockRegion: "us-east-1",
      crossRegionReferences: true,
      webAclId: "",
      identityProviders: [],
      userPoolDomainPrefix: "",
      publishedApiAllowedIpV4AddressRanges: [""],
      publishedApiAllowedIpV6AddressRanges: [""],
      allowedSignUpEmailDomains: [],
      autoJoinUserGroups: [],
      selfSignUpEnabled: true,
      enableIpV6: true,
      documentBucket: bedrockRegionResourcesStack.documentBucket,
      enableRagReplicas: false,
      enableBedrockCrossRegionInference: false,
      enableLambdaSnapStart: true,
      alternateDomainName: "",
      hostedZoneId: "",
      enableBotStore: true,
      enableBotStoreReplicas: false,
      botStoreLanguage: "en",
      tokenValidMinutes: 60,
    });

    const template = Template.fromStack(noDomainStack);

    // Verify no Route53 records are created
    template.resourceCountIs("AWS::Route53::RecordSet", 0);

    // Verify no ACM certificate is created
    template.resourceCountIs("AWS::CertificateManager::Certificate", 0);

    // Verify CloudFront distribution has no aliases
    template.hasResourceProperties("AWS::CloudFront::Distribution", {
      DistributionConfig: {
        Aliases: Match.absent(),
      },
    });
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
      knowledgeBase.chunking_strategy.S,
      knowledgeBase.embeddings_model.S
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

    const stack = new BedrockCustomBotStack(app, "BedrockCustomBotStackStack", {
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
      sourceUrls: knowledge.source_urls.L.map((sourceUrl: any) => sourceUrl.S),
      existKnowledgeBaseId: undefined,
    });

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
