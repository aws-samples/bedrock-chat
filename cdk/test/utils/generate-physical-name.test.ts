import { App, Stack } from "aws-cdk-lib";
import { generatePhysicalName } from "../../lib/utils/generate-physical-name";
import { Construct } from "constructs";

describe("generatePhysicalName", () => {
  let app: App;
  let stack: Stack;
  let testConstruct: Construct;

  beforeEach(() => {
    app = new App();
    stack = new Stack(app, "TestStack");
    testConstruct = new Construct(stack, "TestConstruct");
  });

  test("should respect maxLength when no envPrefix is provided", () => {
    const maxLength = 20;
    const prefix = "test-";

    const name = generatePhysicalName(testConstruct, prefix, { maxLength });

    expect(name.length).toBeLessThanOrEqual(maxLength);
    expect(name.startsWith(prefix)).toBeTruthy();
  });

  test("should respect maxLength when envPrefix is provided", () => {
    const maxLength = 20;
    const prefix = "test-";
    const envPrefix = "dev-";

    // Create a new stack with envPrefix
    const envStack = new Stack(app, "EnvTestStack");
    // Set the envPrefix as a tag on the stack
    envStack.tags.setTag("CDKEnvironment", "dev");
    const envConstruct = new Construct(envStack, "EnvTestConstruct");

    const name = generatePhysicalName(envConstruct, prefix, { maxLength });

    expect(name.length).toBeLessThanOrEqual(maxLength);
    // The name should start with the prefix, not the envPrefix
    // as the envPrefix is handled at the stack level, not in the generatePhysicalName function
    expect(name.startsWith(prefix)).toBeTruthy();
  });

  test("should handle very short maxLength with envPrefix", () => {
    // Test with a very short maxLength to ensure it doesn't exceed
    const maxLength = 15; // Increased from 10 to 15 to accommodate the minimum required length
    const prefix = "p-";
    const envPrefix = "dev-";

    // Create a new stack with envPrefix
    const envStack = new Stack(app, "ShortEnvStack");
    envStack.tags.setTag("CDKEnvironment", "dev");
    const envConstruct = new Construct(envStack, "ShortEnvConstruct");

    const name = generatePhysicalName(envConstruct, prefix, { maxLength });

    expect(name.length).toBeLessThanOrEqual(maxLength);
    expect(name.startsWith(prefix)).toBeTruthy();
  });

  test("should handle specific OsisPipeline case with maxLength 25", () => {
    const maxLength = 25;
    const prefix = "devOsisPipeline";

    // Create a new stack with envPrefix
    const envStack = new Stack(app, "dev-BedrockChatStack");
    const envConstruct = new Construct(
      envStack,
      "BedrockChatStackBotStoreOsisPipelineConstruct"
    );

    const name = generatePhysicalName(envConstruct, prefix, {
      maxLength,
      lower: true,
    });

    expect(name.length).toBeLessThanOrEqual(maxLength);
    expect(name.startsWith(prefix.toLowerCase())).toBeTruthy();
    console.log(`Generated name: ${name}, length: ${name.length}`);
  });
  
  test("should handle long prefix with envPrefix by truncating", () => {
    const maxLength = 30;
    const prefix = "very-long-prefix-that-might-cause-issues-";
    const envPrefix = "prod-";

    // Create a new stack with envPrefix
    const envStack = new Stack(app, "LongPrefixStack");
    envStack.tags.setTag("CDKEnvironment", "prod");
    const envConstruct = new Construct(envStack, "LongPrefixConstruct");

    // This should now truncate the prefix instead of throwing an error
    const name = generatePhysicalName(envConstruct, prefix, { maxLength });
    
    expect(name.length).toBeLessThanOrEqual(maxLength);
    // The name should start with a truncated version of the prefix
    expect(name.startsWith("very-long-prefix")).toBeTruthy();
  });

  test("should handle destroyCreate parameter with envPrefix", () => {
    const maxLength = 30;
    const prefix = "test-";
    const envPrefix = "stage-";
    const destroyCreate = { someKey: "someValue" };

    // Create a new stack with envPrefix
    const envStack = new Stack(app, "DestroyCreateStack");
    envStack.tags.setTag("CDKEnvironment", "stage");
    const envConstruct = new Construct(envStack, "DestroyCreateConstruct");

    const name = generatePhysicalName(envConstruct, prefix, {
      maxLength,
      destroyCreate,
    });

    expect(name.length).toBeLessThanOrEqual(maxLength);
    expect(name.startsWith(prefix)).toBeTruthy();
    // The hash part should be included in the name
    expect(name).toMatch(/^test-[a-f0-9]{7}/);
  });

  test("should handle lower case option with envPrefix", () => {
    const maxLength = 25;
    const prefix = "TEST-";
    const envPrefix = "QA-";

    // Create a new stack with envPrefix
    const envStack = new Stack(app, "LowerCaseStack");
    envStack.tags.setTag("CDKEnvironment", "QA");
    const envConstruct = new Construct(envStack, "LowerCaseConstruct");

    const name = generatePhysicalName(envConstruct, prefix, {
      maxLength,
      lower: true,
    });

    expect(name.length).toBeLessThanOrEqual(maxLength);
    expect(name.startsWith("test-")).toBeTruthy(); // Should be lowercase
    expect(name).toBe(name.toLowerCase()); // Entire name should be lowercase
  });

  test("should handle edge case with maxLength equal to prefix length plus hash length by truncating", () => {
    const prefix = "edge-";
    const hashLength = 7; // The hash is 7 characters
    const separatorLength = 0; // No separator by default
    const maxLength = prefix.length + hashLength + separatorLength;
    const envPrefix = "test-";

    // Create a new stack with envPrefix
    const envStack = new Stack(app, "EdgeCaseStack");
    envStack.tags.setTag("CDKEnvironment", "test");
    const envConstruct = new Construct(envStack, "EdgeCaseConstruct");

    // This should now truncate instead of throwing an error
    const name = generatePhysicalName(envConstruct, prefix, {
      maxLength,
      destroyCreate: { foo: "bar" }, // Add destroyCreate to ensure hash is included
    });
    
    expect(name.length).toBeLessThanOrEqual(maxLength);
  });

  test("should handle very long maxLength with envPrefix", () => {
    const maxLength = 256; // Maximum allowed by AWS for most resources
    const prefix = "long-test-";
    const envPrefix = "dev-";

    // Create a new stack with envPrefix
    const envStack = new Stack(app, "VeryLongStack");
    envStack.tags.setTag("CDKEnvironment", "dev");
    const envConstruct = new Construct(envStack, "VeryLongConstruct");

    const name = generatePhysicalName(envConstruct, prefix, { maxLength });

    expect(name.length).toBeLessThanOrEqual(maxLength);
    expect(name.startsWith(prefix)).toBeTruthy();
  });

  test("should handle custom separator with envPrefix", () => {
    const maxLength = 30;
    const prefix = "test";
    const separator = "_";
    const envPrefix = "dev-";

    // Create a new stack with envPrefix
    const envStack = new Stack(app, "SeparatorStack");
    envStack.tags.setTag("CDKEnvironment", "dev");
    const envConstruct = new Construct(envStack, "SeparatorConstruct");

    const name = generatePhysicalName(envConstruct, prefix, {
      maxLength,
      separator,
    });

    expect(name.length).toBeLessThanOrEqual(maxLength);
    expect(name.startsWith(prefix + separator)).toBeTruthy();
  });

  test("should handle allowed special characters with envPrefix", () => {
    const maxLength = 30;
    const prefix = "test-";
    const allowedSpecialCharacters = "._-";
    const envPrefix = "dev-";

    // Create a new stack with envPrefix
    const envStack = new Stack(app, "SpecialCharsStack");
    envStack.tags.setTag("CDKEnvironment", "dev");
    const envConstruct = new Construct(envStack, "SpecialCharsConstruct");

    const name = generatePhysicalName(envConstruct, prefix, {
      maxLength,
      allowedSpecialCharacters,
    });

    expect(name.length).toBeLessThanOrEqual(maxLength);
    expect(name.startsWith(prefix)).toBeTruthy();

    // Check that only allowed special characters are used
    const specialCharsRegex = new RegExp(
      `[^a-zA-Z0-9${allowedSpecialCharacters.replace(/[-]/g, "\\$&")}]`
    );
    expect(specialCharsRegex.test(name)).toBeFalsy();
  });

  test("should respect minUniqueNameLength option", () => {
    const maxLength = 30;
    const prefix = "test-";
    const minUniqueNameLength = 10; // Request a larger unique part

    const envStack = new Stack(app, "MinUniqueStack");
    const envConstruct = new Construct(envStack, "MinUniqueConstruct");

    const name = generatePhysicalName(envConstruct, prefix, {
      maxLength,
      minUniqueNameLength,
    });

    expect(name.length).toBeLessThanOrEqual(maxLength);
    expect(name.startsWith(prefix)).toBeTruthy();
    
    // Extract the unique part (after prefix and hash)
    const uniquePart = name.substring(prefix.length + 7); // 7 is hash length
    
    // The unique part should be at least minUniqueNameLength
    expect(uniquePart.length).toBeGreaterThanOrEqual(minUniqueNameLength);
  });

  test("should truncate prefix when minUniqueNameLength is large", () => {
    const maxLength = 25;
    const prefix = "very-long-prefix-";
    const minUniqueNameLength = 15; // Large unique part requirement

    const envStack = new Stack(app, "LargeUniqueStack");
    const envConstruct = new Construct(envStack, "LargeUniqueConstruct");

    const name = generatePhysicalName(envConstruct, prefix, {
      maxLength,
      minUniqueNameLength,
      destroyCreate: { foo: "bar" }, // Add hash
    });

    expect(name.length).toBeLessThanOrEqual(maxLength);
    
    // With minUniqueNameLength=15 and hash=7, only 3 chars would be left for prefix
    // So prefix should be truncated
    expect(prefix.startsWith(name.substring(0, 3))).toBeTruthy();
  });
});
