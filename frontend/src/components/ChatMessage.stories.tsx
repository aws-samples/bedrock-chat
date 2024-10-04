import ChatMessage from './ChatMessage';
import { DisplayMessageContent } from '../@types/conversation';

export const Conversation = () => {
  const messages: DisplayMessageContent[] = [
    {
      id: '1',
      role: 'user',
      content: [
        {
          contentType: 'text',
          body: 'What is RAG?',
        },
        {
          contentType: 'attachment',
          fileName: 'AboutRAG.txt',
          body: btoa('RAG stands for Retrieval-Augmented Generation.'),
        },
        {
          contentType: 'attachment',
          fileName: 'RAG-in-detail.pdf',
          body: '',
        },
      ],
      model: 'claude-v3.5-sonnet',
      feedback: null,
      usedChunks: null,
      parent: null,
      children: [],
      sibling: [],
      thinkingLog: null,
    },
    {
      id: '2',
      role: 'assistant',
      content: [
        {
          contentType: 'text',
          body: "RAG stands for Retrieval-Augmented Generation[^1]. It is an approach in natural language processing (NLP)[^2] that combines the capabilities of large language models with information retrieval from external knowledge sources.\n\nThe key idea behind RAG is to first retrieve relevant information from a knowledge base or corpus of documents, and then use that retrieved information along with the language model's knowledge to generate a final output response.\n\nThe process typically involves:\n\n1) Encoding the input query using the language model.\n\n2) Retrieving relevant documents/passages from a knowledge source based on the encoded query representation.\n\n3) Conditioning the language model on the retrieved knowledge along with the original query to generate the final output.\n\nThis allows language models to go beyond just relying on their pre-trained knowledge and incorporate relevant external information when producing responses. RAG models have shown improved performance on knowledge-intensive NLP tasks like open-domain question answering compared to using just the language model alone.\n\nSome examples of RAG models include RAG from Facebook AI, ColBERT from Stanford, and DPR from Facebook AI Research. The approach is an active area of research aimed at making language models more knowledgeable and factual.",
        },
      ],
      model: 'claude-v3.5-sonnet',
      feedback: null,
      usedChunks: [
        {
          content: 'About RAG',
          contentType: 'url',
          source: 'http://example.com/AboutRAG.txt',
          rank: 1,
        },
        {
          content: 'RAG in detail',
          contentType: 's3',
          source: 's3://example/RAG-in-detail.pdf',
          rank: 2,
        },
      ],
      parent: null,
      children: [],
      sibling: [],
      thinkingLog: null,
    },
  ];
  return (
    <>
      {messages?.map((message, idx) => (
        <div
          key={idx}
          className={`${
            message.role === 'assistant' ? 'bg-aws-squid-ink/5' : ''
          }`}>
          <ChatMessage
            isAgentThinking={false}
            chatContent={message}
            relatedDocuments={message.usedChunks?.map((chunk) => ({
              chunkBody: chunk.content,
              contentType: chunk.contentType,
              sourceLink: chunk.source,
              rank: chunk.rank,
            }))}
          />

          <div className="w-full border-b border-aws-squid-ink/10"></div>
        </div>
      ))}
    </>
  );
};
