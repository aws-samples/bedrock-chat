import { OsisPipelineConfigProps, Language } from "./bot-store";

/**
 * Generate template content for bot tables
 */
export function genBotTemplateContent(language: Language): string {
  switch (language) {
    case "ja":
      return JSON.stringify({
        template: {
          settings: {
            analysis: {
              analyzer: {
                ja_analyzer: {
                  type: "custom",
                  char_filter: ["icu_normalizer"],
                  tokenizer: "kuromoji_tokenizer",
                  filter: [
                    "kuromoji_baseform",
                    "kuromoji_part_of_speech",
                    "ja_stop",
                    "kuromoji_number",
                    "kuromoji_stemmer",
                  ],
                },
              },
            },
          },
        },
      });

    default:
      throw new Error(`Unsupported language: ${language}`);
  }
}

/**
 * Generate OSIS pipeline settings for bot tables
 */
export function createBotOsisPipelineConfig(props: OsisPipelineConfigProps): any {
  return {
    version: "2",
    "dynamodb-pipeline": {
      source: {
        dynamodb: {
          acknowledgments: true,
          tables: [
            {
              table_arn: props.botTable.tableArn,
              stream: {
                start_position: "LATEST",
              },
              export: {
                s3_bucket: props.bucketName,
                s3_region: props.region,
              },
            },
          ],
          aws: {
            sts_role_arn: props.osisRole.roleArn,
            region: props.region,
          },
        },
      },
      sink: [
        {
          opensearch: {
            hosts: [props.endpoint],
            index: `${props.envPrefix}bot`,
            ...(props.language === "en"
              ? {} // For en, index_type, template_type, template_content are not required
              : {
                  index_type: "custom",
                  template_type: "index-template",
                  template_content: genBotTemplateContent(props.language),
                }),
            document_id: '${getMetadata("primary_key")}',
            action: '${getMetadata("opensearch_action")}',
            document_version: '${getMetadata("document_version")}',
            document_version_type: "external",
            aws: {
              sts_role_arn: props.osisRole.roleArn,
              region: props.region,
              serverless: true,
            },
          },
        },
      ],
    },
  };
}
