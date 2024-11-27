import {
  SimpleMessage,
  RelatedDocument,
} from '../../../@types/conversation';
import { AgentToolUse, AgentToolsProps } from '../xstates/agentThink';

export const convertThinkingLogToAgentToolProps = (
  thinkingLog: SimpleMessage[],
  relatedDocuments?: RelatedDocument[],
): AgentToolsProps[] => {
  const toolResults = Object.fromEntries(thinkingLog.flatMap(message => message.content.flatMap(content => {
    if (content.contentType === 'toolResult') {
      return [[content.body.toolUseId, content.body]];
    } else {
      return [];
    }
  })));
  return thinkingLog.flatMap(message => {
    const thoughts = message.content.flatMap(content => {
      if (content.contentType === 'text') {
        return [content.body];
      } else {
        return [];
      }
    });
    const tools: Record<string, AgentToolUse> = Object.fromEntries(message.content.flatMap(content => {
      if (content.contentType === 'toolUse') {
        if (content.body.toolUseId in toolResults) {
          const result = toolResults[content.body.toolUseId];
          return [[content.body.toolUseId, {
            name: content.body.name,
            input: content.body.input,
            status: result.status,
            resultContents: result.content,
            relatedDocuments: getRelatedDocumentsOfToolUse(relatedDocuments, content.body.toolUseId)
          }]];
        } else {
          return [[content.body.toolUseId, {
            name: content.body.name,
            input: content.body.input,
            status: 'running',
          }]];
        }
      } else {
        return [] as [string, AgentToolUse][];
      }
    }));
    if (Object.keys(tools).length > 0) {
      return [{
        thought: (thoughts.length > 0 ? thoughts.join('\n') : undefined),
        tools: tools,
      }];
    } else {
      return [] as AgentToolsProps[];
    }
  });
};

export const getRelatedDocumentsOfToolUse = (relatedDocuments: RelatedDocument[] | undefined, toolUseId: string) => {
  if (relatedDocuments == null) {
    return undefined;
  }

  const filteredWithToolUseId = relatedDocuments.filter(document => document.sourceId === toolUseId);
  if (filteredWithToolUseId.length > 0) {
    return filteredWithToolUseId;
  }

  const relatedDocumentsSortedByRank =  relatedDocuments.flatMap(document => {
    const match = document.sourceId.match(/(?<sourceId>.+?)@(?<rank>[\d]+?)$/);
    if (match == null || match.groups!.sourceId !== toolUseId) {
      return [];
    }

    return [
      {
        rank: Number(match.groups!.rank),
        ...document,
      },
    ];
  }).sort((lhs, rhs) => lhs.rank - rhs.rank);
  if (relatedDocumentsSortedByRank.length > 0) {
    return relatedDocumentsSortedByRank;
  }

  return undefined;
};
