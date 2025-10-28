import { type Handler } from 'aws-lambda';

export const handler: Handler = async (event, context) => {
  console.log(`Event: ${JSON.stringify(event)}`);

  const inputFiles = event.inputFiles as any[];

  return {
      outputFiles: inputFiles.flatMap(file => {
        const originalFileLocation = file.originalFileLocation;
        const s3Uri = new URL(originalFileLocation.s3_location.uri);

        const fileName = s3Uri.pathname.match(/^(\/[^/]+)*\/(?<fileName>[^/]+)$/)?.groups?.fileName;
        if (fileName?.startsWith('.')) {
          console.log(`Ignored dotfile '${fileName}'`);
          return [];
        }

        const botId = s3Uri.pathname.match(/^\/(?<userId>[^/]+)\/(?<botId>[^/]+)\/documents\/(?<fileName>[^/]+)$/)?.groups?.botId;
        return [{
          originalFileLocation,
          ...(botId != null ? {
            fileMetadata: {
                tenants: [
                  `BOT#${botId}`,
                ],
            },
          } : undefined),
          contentBatches: file.contentBatches,
        }];
      }),
   };
};
