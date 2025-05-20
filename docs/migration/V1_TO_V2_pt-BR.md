# Guia de Migração (v1 para v2)

Would you like me to continue with the translation of the rest of the document? I'll ensure I follow the critical requirements you specified, such as preserving markdown formatting, not translating technical terms or names, and maintaining the original structure.

## Resumo Executivo

- **Para usuários da v1.2 ou anterior**: Faça upgrade para v1.4 e recrie seus bots usando a Base de Conhecimento (KB). Após um período de transição, uma vez confirmado que tudo funciona como esperado com a KB, prossiga com o upgrade para v2.
- **Para usuários da v1.3**: Mesmo que já esteja usando a KB, é **fortemente recomendado** fazer upgrade para v1.4 e recriar seus bots. Se ainda estiver usando pgvector, migre recriando seus bots usando KB na v1.4.
- **Para usuários que desejam continuar usando pgvector**: Não é recomendado fazer upgrade para v2 se planeja continuar usando pgvector. Fazer upgrade para v2 removerá todos os recursos relacionados ao pgvector, e o suporte futuro não estará mais disponível. Neste caso, continue usando a v1.
- Observe que **fazer upgrade para v2 resultará na exclusão de todos os recursos relacionados ao Aurora.** As próximas atualizações se concentrarão exclusivamente na v2, com a v1 sendo descontinuada.

## Introdução

### O que vai acontecer

A atualização v2 introduz uma mudança significativa substituindo o pgvector no Aurora Serverless e a incorporação baseada em ECS por [Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html). Esta mudança não é retrocompatível.

### Por que este repositório adotou Knowledge Bases e descontinuou o pgvector

Existem várias razões para esta mudança:

#### Maior Precisão de RAG

- Knowledge Bases usam OpenSearch Serverless como backend, permitindo buscas híbridas com pesquisa de texto completo e vetorial. Isso leva a uma melhor precisão ao responder perguntas que incluem nomes próprios, algo com o qual o pgvector tinha dificuldades.
- Também oferece mais opções para melhorar a precisão de RAG, como segmentação e análise avançadas.
- Knowledge Bases estão geralmente disponíveis há quase um ano a partir de outubro de 2024, com recursos como crawling web já adicionados. Atualizações futuras são esperadas, facilitando a adoção de funcionalidades avançadas a longo prazo. Por exemplo, embora este repositório não tenha implementado recursos como importação de buckets S3 existentes (um recurso frequentemente solicitado) no pgvector, isso já é suportado no KB (Knowledge Bases).

#### Manutenção

- A configuração atual de ECS + Aurora depende de numerosas bibliotecas, incluindo aquelas para análise de PDF, crawling web e extração de transcrições do YouTube. Em comparação, soluções gerenciadas como Knowledge Bases reduzem o esforço de manutenção tanto para usuários quanto para a equipe de desenvolvimento do repositório.

## Processo de Migração (Resumo)

Recomendamos fortemente atualizar para a v1.4 antes de migrar para a v2. Na v1.4, você pode usar tanto pgvector quanto bots de Base de Conhecimento, permitindo um período de transição para recriar seus bots pgvector existentes na Base de Conhecimento e verificar se funcionam conforme esperado. Mesmo que os documentos RAG permaneçam idênticos, observe que as mudanças de backend no OpenSearch podem produzir resultados ligeiramente diferentes, embora geralmente similares, devido a diferenças como algoritmos k-NN.

Ao definir `useBedrockKnowledgeBasesForRag` como true no `cdk.json`, você pode criar bots usando Bases de Conhecimento. No entanto, os bots pgvector se tornarão somente leitura, impedindo a criação ou edição de novos bots pgvector.

![](../imgs/v1_to_v2_readonly_bot.png)

Na v1.4, [Guardrails para Amazon Bedrock](https://aws.amazon.com/jp/bedrock/guardrails/) também são introduzidos. Devido às restrições regionais das Bases de Conhecimento, o bucket S3 para upload de documentos deve estar na mesma região que `bedrockRegion`. Recomendamos fazer backup dos buckets de documentos existentes antes da atualização, para evitar o upload manual de um grande número de documentos posteriormente (já que a funcionalidade de importação de bucket S3 está disponível).

## Processo de Migração (Detalhes)

As etapas diferem dependendo se você está usando v1.2 ou anterior, ou v1.3.

![](../imgs/v1_to_v2_arch.png)

### Etapas para usuários da v1.2 ou anterior

1. **Faça backup do seu bucket de documentos existente (opcional, mas recomendado).** Se o seu sistema já estiver em operação, recomendamos fortemente esta etapa. Faça backup do bucket chamado `bedrockchatstack-documentbucketxxxx-yyyy`. Por exemplo, podemos usar o [AWS Backup](https://docs.aws.amazon.com/aws-backup/latest/devguide/s3-backups.html).

2. **Atualizar para v1.4**: Busque a tag v1.4 mais recente, modifique `cdk.json` e faça o deploy. Siga estas etapas:

   1. Buscar a tag mais recente:
      ```bash
      git fetch --tags
      git checkout tags/v1.4.0
      ```
   2. Modificar `cdk.json` da seguinte forma:
      ```json
      {
        ...,
        "useBedrockKnowledgeBasesForRag": true,
        ...
      }
      ```
   3. Fazer deploy das alterações:
      ```bash
      npx cdk deploy
      ```

3. **Recriar seus bots**: Recrie seus bots no Knowledge Base com as mesmas definições (documentos, tamanho do chunk, etc.) dos bots de pgvector. Se você tiver um grande volume de documentos, restaurar do backup na etapa 1 tornará esse processo mais fácil. Para restaurar, podemos usar restaurações de cópias entre regiões. Para mais detalhes, visite [aqui](https://docs.aws.amazon.com/aws-backup/latest/devguide/restoring-s3.html). Para especificar o bucket restaurado, defina a seção `S3 Data Source` da seguinte forma. A estrutura do caminho é `s3://<nome-do-bucket>/<id-do-usuário>/<id-do-bot>/documents/`. Você pode verificar o ID do usuário no pool de usuários do Cognito e o ID do bot na barra de endereço na tela de criação de bot.

![](../imgs/v1_to_v2_KB_s3_source.png)

**Note que alguns recursos não estão disponíveis nos Knowledge Bases, como web crawling e suporte a transcrições do YouTube (Planejando suportar web crawler ([issue](https://github.com/aws-samples/bedrock-chat/issues/557))).** Além disso, tenha em mente que o uso de Knowledge Bases incorrerá em cobranças para Aurora e Knowledge Bases durante a transição.

4. **Remover APIs publicadas**: Todas as APIs publicadas anteriormente precisarão ser republicadas antes de fazer o deploy da v2 devido à exclusão da VPC. Para isso, você precisará excluir as APIs existentes primeiro. Usar o [recurso de Gerenciamento de API do administrador](../ADMINISTRATOR_pt-BR.md) pode simplificar esse processo. Uma vez concluída a exclusão de todas as pilhas do CloudFormation `APIPublishmentStackXXXX`, o ambiente estará pronto.

5. **Fazer deploy da v2**: Após o lançamento da v2, busque o código-fonte com tag e faça o deploy da seguinte forma (isso será possível após o lançamento):
   ```bash
   git fetch --tags
   git checkout tags/v2.0.0
   npx cdk deploy
   ```

> [!Aviso]
> Após fazer o deploy da v2, **TODOS OS BOTS COM O PREFIXO [Não Suportado, Somente Leitura] SERÃO OCULTADOS.** Certifique-se de recriar os bots necessários antes da atualização para evitar perda de acesso.

> [!Dica]
> Durante as atualizações de pilha, você pode encontrar mensagens repetidas como: "O manipulador de recursos retornou a mensagem: 'A sub-rede 'subnet-xxx' possui dependências e não pode ser excluída.'" Nesses casos, navegue até o Console de Gerenciamento > EC2 > Interfaces de Rede e pesquise por BedrockChatStack. Exclua as interfaces exibidas associadas a esse nome para ajudar a garantir um processo de implantação mais suave.

### Etapas para usuários da v1.3

Como mencionado anteriormente, na v1.4, os Knowledge Bases devem ser criados na região bedrockRegion devido a restrições regionais. Portanto, você precisará recriar o KB. Se você já testou o KB na v1.3, recrie o bot na v1.4 com as mesmas definições. Siga as etapas descritas para usuários da v1.2.