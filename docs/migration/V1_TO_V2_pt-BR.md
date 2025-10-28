# Guia de Migração (v1 para v2)

## TL;DR

- **Para usuários da v1.2 ou anterior**: Atualize para v1.4 e recrie seus bots usando Knowledge Base (KB). Após um período de transição, depois de confirmar que tudo funciona como esperado com KB, prossiga com a atualização para v2.
- **Para usuários da v1.3**: Mesmo se você já estiver usando KB, é **fortemente recomendado** atualizar para v1.4 e recriar seus bots. Se você ainda estiver usando pgvector, migre recriando seus bots usando KB na v1.4.
- **Para usuários que desejam continuar usando pgvector**: A atualização para v2 não é recomendada se você planeja continuar usando pgvector. A atualização para v2 removerá todos os recursos relacionados ao pgvector, e o suporte futuro não estará mais disponível. Continue usando v1 neste caso.
- Observe que **a atualização para v2 resultará na exclusão de todos os recursos relacionados ao Aurora.** As atualizações futuras serão focadas exclusivamente na v2, com a v1 sendo descontinuada.

## Introdução

### O que vai acontecer

A atualização v2 introduz uma mudança importante ao substituir o pgvector no Aurora Serverless e embeddings baseados em ECS pelo [Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html). Esta mudança não é compatível com versões anteriores.

### Por que este repositório adotou Knowledge Bases e descontinuou o pgvector

Existem várias razões para esta mudança:

#### Melhor Precisão do RAG

- Knowledge Bases usa OpenSearch Serverless como backend, permitindo buscas híbridas com pesquisa tanto textual quanto vetorial. Isso leva a uma melhor precisão ao responder perguntas que incluem substantivos próprios, com os quais o pgvector tinha dificuldades.
- Também suporta mais opções para melhorar a precisão do RAG, como chunking e análise avançados.
- Knowledge Bases está disponível para uso geral há quase um ano desde outubro de 2024, com recursos como rastreamento web já adicionados. Atualizações futuras são esperadas, tornando mais fácil adotar funcionalidades avançadas a longo prazo. Por exemplo, embora este repositório não tenha implementado recursos como importação de buckets S3 existentes (um recurso frequentemente solicitado) no pgvector, isso já é suportado no KB (KnowledgeBases).

#### Manutenção

- A configuração atual de ECS + Aurora depende de várias bibliotecas, incluindo aquelas para análise de PDF, rastreamento web e extração de transcrições do YouTube. Em comparação, soluções gerenciadas como Knowledge Bases reduzem a carga de manutenção tanto para usuários quanto para a equipe de desenvolvimento do repositório.

## Processo de Migração (Resumo)

Recomendamos fortemente atualizar para v1.4 antes de migrar para v2. Na v1.4, você pode usar tanto pgvector quanto bots de Base de Conhecimento, permitindo um período de transição para recriar seus bots pgvector existentes em Base de Conhecimento e verificar se funcionam como esperado. Mesmo que os documentos RAG permaneçam idênticos, observe que as mudanças de backend para OpenSearch podem produzir resultados ligeiramente diferentes, embora geralmente similares, devido a diferenças como algoritmos k-NN.

Ao definir `useBedrockKnowledgeBasesForRag` como true no `cdk.json`, você pode criar bots usando Bases de Conhecimento. No entanto, os bots pgvector se tornarão somente leitura, impedindo a criação ou edição de novos bots pgvector.

![](../imgs/v1_to_v2_readonly_bot.png)

Na v1.4, [Guardrails for Amazon Bedrock](https://aws.amazon.com/jp/bedrock/guardrails/) também são introduzidos. Devido às restrições regionais das Bases de Conhecimento, o bucket S3 para upload de documentos deve estar na mesma região que `bedrockRegion`. Recomendamos fazer backup dos buckets de documentos existentes antes de atualizar, para evitar o upload manual de um grande número de documentos posteriormente (já que a funcionalidade de importação de bucket S3 está disponível).

## Processo de Migração (Detalhado)

Os passos diferem dependendo se você está usando v1.2 ou anterior, ou v1.3.

![](../imgs/v1_to_v2_arch.png)

### Passos para usuários da v1.2 ou anterior

1. **Faça backup do seu bucket de documentos existente (opcional mas recomendado).** Se seu sistema já está em operação, recomendamos fortemente este passo. Faça backup do bucket chamado `bedrockchatstack-documentbucketxxxx-yyyy`. Por exemplo, podemos usar o [AWS Backup](https://docs.aws.amazon.com/aws-backup/latest/devguide/s3-backups.html).

2. **Atualize para v1.4**: Busque a tag mais recente v1.4, modifique o `cdk.json` e faça o deploy. Siga estes passos:

   1. Busque a tag mais recente:
      ```bash
      git fetch --tags
      git checkout tags/v1.4.0
      ```
   2. Modifique o `cdk.json` da seguinte forma:
      ```json
      {
        ...,
        "useBedrockKnowledgeBasesForRag": true,
        ...
      }
      ```
   3. Faça o deploy das alterações:
      ```bash
      npx cdk deploy
      ```

3. **Recrie seus bots**: Recrie seus bots no Knowledge Base com as mesmas definições (documentos, tamanho de chunk, etc.) dos bots pgvector. Se você tiver um grande volume de documentos, restaurar do backup do passo 1 tornará este processo mais fácil. Para restaurar, podemos usar a restauração de cópias entre regiões. Para mais detalhes, visite [aqui](https://docs.aws.amazon.com/aws-backup/latest/devguide/restoring-s3.html). Para especificar o bucket restaurado, configure a seção `S3 Data Source` como a seguir. A estrutura do caminho é `s3://<bucket-name>/<user-id>/<bot-id>/documents/`. Você pode verificar o id do usuário no pool de usuários do Cognito e o id do bot na barra de endereço na tela de criação do bot.

![](../imgs/v1_to_v2_KB_s3_source.png)

**Note que alguns recursos não estão disponíveis no Knowledge Bases, como web crawling e suporte a transcrição do YouTube (Planejamento para suportar web crawler ([issue](https://github.com/aws-samples/bedrock-chat/issues/557))).** Além disso, lembre-se que usar o Knowledge Bases incorrerá em cobranças tanto para Aurora quanto para Knowledge Bases durante a transição.

4. **Remova APIs publicadas**: Todas as APIs previamente publicadas precisarão ser republicadas antes de fazer o deploy da v2 devido à exclusão da VPC. Para isso, você precisará primeiro excluir as APIs existentes. Usar o [recurso de Gerenciamento de API do administrador](../ADMINISTRATOR_pt-BR.md) pode simplificar este processo. Uma vez que a exclusão de todas as stacks CloudFormation `APIPublishmentStackXXXX` estiver completa, o ambiente estará pronto.

5. **Faça deploy da v2**: Após o lançamento da v2, busque o código fonte com tag e faça o deploy da seguinte forma (isso será possível após o lançamento):
   ```bash
   git fetch --tags
   git checkout tags/v2.0.0
   npx cdk deploy
   ```

> [!Warning]
> Após fazer o deploy da v2, **TODOS OS BOTS COM O PREFIXO [Unsupported, Read-only] SERÃO OCULTADOS.** Certifique-se de recriar os bots necessários antes de atualizar para evitar qualquer perda de acesso.

> [!Tip]
> Durante as atualizações da stack, você pode encontrar mensagens repetidas como: Resource handler returned message: "The subnet 'subnet-xxx' has dependencies and cannot be deleted." Nesses casos, navegue até Console de Gerenciamento > EC2 > Interfaces de Rede e procure por BedrockChatStack. Exclua as interfaces exibidas associadas a este nome para ajudar a garantir um processo de implantação mais suave.

### Passos para usuários da v1.3

Como mencionado anteriormente, na v1.4, o Knowledge Bases deve ser criado na bedrockRegion devido a restrições regionais. Portanto, você precisará recriar o KB. Se você já testou o KB na v1.3, recrie o bot na v1.4 com as mesmas definições. Siga os passos descritos para usuários da v1.2.