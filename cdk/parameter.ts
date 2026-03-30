import { BedrockChatParametersInput } from "./lib/utils/parameter-models";

export const bedrockChatParams = new Map<string, BedrockChatParametersInput>();
// You can define multiple environments and their parameters here
// bedrockChatParams.set("main", {});

// If you define "default" environment here, parameters in cdk.json are ignored
// bedrockChatParams.set("default", {});
bedrockChatParams.set("nma", {
  bedrockRegion: "ap-northeast-1",
  selfSignUpEnabled: false,
  allowedIpV4AddressRanges: [
    "18.176.40.134/32",  // Geco vpn
    "126.249.23.18/32",  // NMA Tokyo Office
    "126.249.75.182/32", // NMA Tokyo Office 10F
  ],
  enableFrontendIpv6: false, // Disabling this property will still create waf rules to allow ipv6 traffic. Workaround set empty array to disable ipv6 traffic.
  allowedIpV6AddressRanges: [],
  enableRagReplicas: false,
  enableBotStoreReplicas: false,
  titleModel: "claude-v4.6-sonnet",   // Model used for generating conversation titles
  defaultModel: "claude-v4.6-sonnet", // Default model for conversations
  enableBedrockGlobalInference: true,
  globalAvailableModels: ["claude-v4.6-opus", "claude-v4.6-sonnet"]
});
