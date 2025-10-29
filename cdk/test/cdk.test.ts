import * as cdk from "aws-cdk-lib";
import { BedrockChatStack } from "../lib/bedrock-chat-stack";
import { Template } from "aws-cdk-lib/assertions";
import {
  getEmbeddingModel,
  getChunkingStrategy,
  getAnalyzer,
  getKnowledgeBaseType,
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
        allowedIpV4AddressRanges: [""],
        allowedIpV6AddressRanges: [""],
        allowedSignUpEmailDomains: [],
        autoJoinUserGroups: [],
        selfSignUpEnabled: true,
        enableIpV6: true,
        documentBucket: bedrockRegionResourcesStack.documentBucket,
        enableRagReplicas: false,
        enableBedrockGlobalInference: false,
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
        allowedIpV4AddressRanges: [""],
        allowedIpV6AddressRanges: [""],
        selfSignUpEnabled: true,
        enableIpV6: true,
        documentBucket: bedrockRegionResourcesStack.documentBucket,
        enableRagReplicas: false,
        enableBedrockGlobalInference: false,
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
      allowedIpV4AddressRanges: [""],
      allowedIpV6AddressRanges: [""],
      documentBucket: bedrockRegionResourcesStack.documentBucket,
      enableRagReplicas: false,
      enableBedrockGlobalInference: false,
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
      enableBedrockGlobalInference: false,
      enableBedrockCrossRegionInference: false,
      allowedIpV4AddressRanges: [""],
      allowedIpV6AddressRanges: [""],
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
      enableBedrockGlobalInference: false,
      enableBedrockCrossRegionInference: false,
      enableLambdaSnapStart: true,
      alternateDomainName: "",
      allowedIpV4AddressRanges: [""],
      allowedIpV6AddressRanges: [""],
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

  test("Frontend WAF disabled => no WebACLId on CloudFront", () => {
    const app = new cdk.App();

    const bedrockRegionResourcesStack = new BedrockRegionResourcesStack(
      app,
      "BedrockRegionResourcesStackNoWaf",
      {
        env: { region: "us-east-1" },
        crossRegionReferences: true,
      }
    );

    const stack = new BedrockChatStack(app, "NoWafStack", {
      env: { region: "us-west-2" },
      envName: "test",
      envPrefix: "test-",
      bedrockRegion: "us-east-1",
      crossRegionReferences: true,
      // Simulate WAF disabled: no ARN provided from bin
      webAclId: "",
      identityProviders: [],
      userPoolDomainPrefix: "",
      publishedApiAllowedIpV4AddressRanges: [""],
      publishedApiAllowedIpV6AddressRanges: [""],
      allowedIpV4AddressRanges: [""],
      allowedIpV6AddressRanges: [""],
      allowedSignUpEmailDomains: [],
      autoJoinUserGroups: [],
      selfSignUpEnabled: true,
      enableIpV6: true,
      documentBucket: bedrockRegionResourcesStack.documentBucket,
      enableRagReplicas: false,
      enableBedrockGlobalInference: false,
      enableBedrockCrossRegionInference: false,
      enableLambdaSnapStart: true,
      enableBotStore: true,
      enableBotStoreReplicas: false,
      botStoreLanguage: "en",
      tokenValidMinutes: 60,
    });

    const template = Template.fromStack(stack);

    template.hasResourceProperties("AWS::CloudFront::Distribution", {
      DistributionConfig: {
        WebACLId: Match.absent(),
      },
    });
  });

  test("Frontend WAF enabled => WebACLId set on CloudFront", () => {
    const app = new cdk.App();

    const bedrockRegionResourcesStack = new BedrockRegionResourcesStack(
      app,
      "BedrockRegionResourcesStackWaf",
      {
        env: { region: "us-east-1" },
        crossRegionReferences: true,
      }
    );

    const wafArn = "arn:aws:wafv2:us-east-1:123456789012:global/webacl/test/uuid";

    const stack = new BedrockChatStack(app, "WithWafStack", {
      env: { region: "us-west-2" },
      envName: "test",
      envPrefix: "test-",
      bedrockRegion: "us-east-1",
      crossRegionReferences: true,
      webAclId: wafArn,
      identityProviders: [],
      userPoolDomainPrefix: "",
      publishedApiAllowedIpV4AddressRanges: [""],
      publishedApiAllowedIpV6AddressRanges: [""],
      allowedIpV4AddressRanges: [""],
      allowedIpV6AddressRanges: [""],
      allowedSignUpEmailDomains: [],
      autoJoinUserGroups: [],
      selfSignUpEnabled: true,
      enableIpV6: true,
      documentBucket: bedrockRegionResourcesStack.documentBucket,
      enableRagReplicas: false,
      enableBedrockGlobalInference: false,
      enableBedrockCrossRegionInference: false,
      enableLambdaSnapStart: true,
      enableBotStore: true,
      enableBotStoreReplicas: false,
      botStoreLanguage: "en",
      tokenValidMinutes: 60,
    });

    const template = Template.fromStack(stack);

    template.hasResourceProperties("AWS::CloudFront::Distribution", {
      DistributionConfig: {
        WebACLId: wafArn,
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
      enableBedrockGlobalInference: false,
      enableBedrockCrossRegionInference: false,
      enableLambdaSnapStart: true,
      alternateDomainName: "chat.example.com",
      allowedIpV4AddressRanges: [""],
      allowedIpV6AddressRanges: [""],
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
      allowedIpV4AddressRanges: [""],
      allowedIpV6AddressRanges: [""],
      documentBucket: bedrockRegionResourcesStack.documentBucket,
      enableRagReplicas: false,
      enableBedrockGlobalInference: false,
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

    const OWNER_USER_ID: string = "test-user-id";
    const BOT_ID: string = "test-bot-id";
    const KNOWLEDGE = {
      sitemap_urls: [],
      filenames: [
        "test-filename.pdf",
      ],
      source_urls: [
        "https://example.com",
      ],
      s3_urls: params.s3Urls !== undefined ? params.s3Urls : [],
    };

    const KNOWLEDGE_BASE = {
      type: "dedicated",
      chunking_strategy: "fixed_size",
      max_tokens: params.maxTokens,
      instruction: params.instruction,
      overlap_percentage: params.overlapPercentage,
      open_search: {
        analyzer:
          params.analyzer !== undefined
            ? JSON.parse(params.analyzer)
            : {
              character_filters: [
                "icu_normalizer",
              ],
              token_filters: [
                "kuromoji_baseform",
                "kuromoji_part_of_speech",
              ],
              tokenizer: "kuromoji_tokenizer",
            },
      },
      embeddings_model: "titan_v2",
    } as const;

    const BEDROCK_CLAUDE_CHAT_DOCUMENT_BUCKET_NAME =
      "test-document-bucket-name";

    const ownerUserId: string = OWNER_USER_ID;
    const botId: string = BOT_ID;
    const knowledgeBase = KNOWLEDGE_BASE;
    const knowledge = KNOWLEDGE;
    const existingS3Urls: string[] = knowledge.s3_urls;

    const knowledgeBaseType = getKnowledgeBaseType(knowledgeBase.type);
    const embeddingsModel = getEmbeddingModel(knowledgeBase.embeddings_model);
    const chunkingStrategy = getChunkingStrategy(
      knowledgeBase.chunking_strategy,
      knowledgeBase.embeddings_model
    );
    const maxTokens: number | undefined = knowledgeBase.max_tokens;
    const instruction: string | undefined = knowledgeBase.instruction;
    const analyzer = knowledgeBase.open_search.analyzer
      ? getAnalyzer(knowledgeBase.open_search.analyzer)
      : undefined;
    const overlapPercentage: number | undefined = knowledgeBase.overlap_percentage;

    const stack = new BedrockCustomBotStack(app, "BedrockCustomBotStackStack", {
      ownerUserId,
      botId,
      embeddingsModel,
      bedrockClaudeChatDocumentBucketName:
        BEDROCK_CLAUDE_CHAT_DOCUMENT_BUCKET_NAME,
      knowledgeBaseType,
      chunkingStrategy,
      existingS3Urls,
      maxTokens,
      instruction,
      analyzer,
      overlapPercentage,
      filenames: knowledge.filenames,
      sourceUrls: knowledge.source_urls,
      existKnowledgeBaseId: undefined,
    });

    return Template.fromStack(stack);
  };

  test("default kb stack", () => {
    const template = setupStack({
      s3Urls: [
        "s3://test-bucket/test-key",
      ],
      maxTokens: 500,
      instruction: "This is an example instruction.",
      overlapPercentage: 10,
      analyzer: `{
        "character_filters": [
          "icu_normalizer"
        ],
        "token_filters": [
          "kuromoji_baseform",
          "kuromoji_part_of_speech"
        ],
        "tokenizer": "kuromoji_tokenizer"
      }`,
    });
    expect(template).toBeDefined();
  });

  test("kb stack without maxTokens", () => {
    const template = setupStack({
      instruction: "This is an example instruction.",
      overlapPercentage: 10,
      analyzer: `{
        "character_filters": [
          "icu_normalizer"
        ],
        "token_filters": [
          "kuromoji_baseform",
          "kuromoji_part_of_speech"
        ],
        "tokenizer": "kuromoji_tokenizer"
      }`,
    });
    expect(template).toBeDefined();
  });

  test("kb stack without instruction", () => {
    const template = setupStack({
      maxTokens: 500,
      overlapPercentage: 10,
      analyzer: `{
        "character_filters": [
          "icu_normalizer"
        ],
        "token_filters": [
          "kuromoji_baseform",
          "kuromoji_part_of_speech"
        ],
        "tokenizer": "kuromoji_tokenizer"
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
        "character_filters": [
          "icu_normalizer"
        ],
        "token_filters": [
          "kuromoji_baseform",
          "kuromoji_part_of_speech"
        ],
        "tokenizer": "kuromoji_tokenizer"
      }`,
    });
    expect(template).toBeDefined();
  });
});
