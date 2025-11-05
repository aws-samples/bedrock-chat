import { type Handler } from "aws-lambda";

/**
 * Custom transformation function used in the S3 data source of a shared Knowledge Base.
 * https://docs.aws.amazon.com/bedrock/latest/userguide/kb-custom-transformation.html
 */
export const handler: Handler = async (event, context) => {
  console.log(`Event: ${JSON.stringify(event)}`);

  const inputFiles = event.inputFiles as any[];

  return {
    outputFiles: inputFiles.flatMap((file) => {
      const originalFileLocation = file.originalFileLocation;
      const s3Uri = new URL(originalFileLocation.s3_location.uri);

      // Ignore files that do not exist in the directory for bots.
      const groups = s3Uri.pathname.match(
        /^\/(?<userId>[^/]+)\/(?<botId>[^/]+)\/documents\/(?<fileName>[^/]+)$/
      )?.groups;
      const userId = groups?.userId;
      const botId = groups?.botId;
      // Note: `.temp` is used for distributed lock
      if (groups == null || botId == null || userId === ".temp") {
        return [];
      }

      // For files uploaded by bots, set the bot's ID in the metadata field named 'tenants'.
      return [
        {
          originalFileLocation,
          contentBatches: file.contentBatches,
          fileMetadata: {
            tenants: [`BOT#${botId}`],
          },
        },
      ];
    }),
  };
};
