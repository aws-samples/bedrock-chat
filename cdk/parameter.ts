import { BedrockChatParametersInput } from "./lib/utils/parameter-models";

export const bedrockChatParams = new Map<string, BedrockChatParametersInput>();
// You can define multiple environments and their parameters here
// bedrockChatParams.set("dev", {});

// If you define "default" environment here, parameters in cdk.json are ignored
// bedrockChatParams.set("default", {});
// 为默认环境定义参数
bedrockChatParams.set("default", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["192.168.0.0/16"],
  selfSignUpEnabled: true,
  enableLambdaSnapStart: false,
  enableBotStore: false,
  enableRagReplicas: false,
  globalAvailableModels: [
      "claude-v3.7-sonnet",
      "claude-v3.5-sonnet",
      "amazon-nova-pro",
      "amazon-nova-lite",
      "llama3-3-70b-instruct"
    ],
});

// 为其他环境定义参数
bedrockChatParams.set("dev", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["10.0.0.0/8"],
  enableRagReplicas: false, // 开发环境节省成本
  enableBotStoreReplicas: false, // 开发环境节省成本
});

bedrockChatParams.set("prod", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["172.16.0.0/12"],
  enableLambdaSnapStart: true,
  enableRagReplicas: true, // 生产环境增强可用性
  enableBotStoreReplicas: true, // 生产环境增强可用性
});