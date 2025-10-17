import { type Handler } from 'aws-lambda';

export const handler: Handler = async (event, context) => {
  console.log(`Event: ${JSON.stringify(event)}`);

  const inputFiles = event.inputFiles as any[];

  return {
      outputFiles: inputFiles.map(file => {
        const originalFileLocation = file.originalFileLocation;
        const s3Uri = new URL(originalFileLocation.s3_location.uri);
        const botId = s3Uri.pathname.match(/^\/(?<userId>[^/]+)\/(?<botId>[^/]+)\/documents\/(?<fileName>[^/]+)$/)?.groups?.botId;
        return {
          originalFileLocation,
          ...(botId != null ? {
            fileMetadata: {
                tenants: [
                  `BOT#${botId}`,
                ],
            },
          } : undefined),
          contentBatches: file.contentBatches,
        };
      }),
   };
};
