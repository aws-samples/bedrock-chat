# Recursos administrativos

## Pré-requisitos

O usuário administrador deve ser membro do grupo chamado `Admin`, que pode ser configurado através do console de gerenciamento > Amazon Cognito User pools ou aws cli. Observe que o ID do grupo de usuários pode ser consultado acessando CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`.

![](./imgs/group_membership_admin.png)

## Marcar bots públicos como Essenciais

Agora os bots públicos podem ser marcados como "Essenciais" pelos administradores. Os bots marcados como Essenciais serão destacados na seção "Essenciais" da loja de bots, tornando-os facilmente acessíveis aos usuários. Isso permite que os administradores fixem bots importantes que desejam que todos os usuários utilizem.

### Exemplos

- Bot Assistente de RH: Ajuda funcionários com questões e tarefas relacionadas a recursos humanos.
- Bot de Suporte de TI: Fornece assistência para problemas técnicos internos e gerenciamento de contas.
- Bot Guia de Políticas Internas: Responde perguntas frequentes sobre regras de presença, políticas de segurança e outros regulamentos internos.
- Bot de Integração de Novos Funcionários: Orienta novos contratados sobre procedimentos e uso de sistemas em seu primeiro dia.
- Bot de Informações sobre Benefícios: Explica os programas de benefícios e serviços de bem-estar da empresa.

![](./imgs/admin_bot_menue.png)
![](./imgs/bot_store.png)

## Loop de feedback

A saída do LLM nem sempre pode atender às expectativas do usuário. Às vezes, ela falha em satisfazer as necessidades do usuário. Para "integrar" efetivamente os LLMs nas operações de negócios e na vida diária, é essencial implementar um loop de feedback. O Bedrock Chat está equipado com um recurso de feedback projetado para permitir que os usuários analisem por que surgiu a insatisfação. Com base nos resultados da análise, os usuários podem ajustar os prompts, as fontes de dados RAG e os parâmetros adequadamente.

![](./imgs/feedback_loop.png)

![](./imgs/feedback-using-claude-chat.png)

Os analistas de dados podem acessar os logs de conversação usando o [Amazon Athena](https://aws.amazon.com/jp/athena/). Se eles quiserem analisar os dados usando [Jupyter Notebook](https://jupyter.org/), [este exemplo de notebook](../examples/notebooks/feedback_analysis_example.ipynb) pode servir como referência.

## Painel de Controle

Atualmente fornece uma visão geral básica do uso dos chatbots e usuários, focando na agregação de dados para cada bot e usuário durante períodos específicos e classificando os resultados por taxas de uso.

![](./imgs/admin_bot_analytics.png)

## Notas

- Como indicado na [arquitetura](../README.md#architecture), os recursos administrativos farão referência ao bucket S3 exportado do DynamoDB. Por favor, observe que como a exportação é realizada uma vez por hora, as conversas mais recentes podem não ser refletidas imediatamente.

- Nos usos públicos do bot, os bots que não foram utilizados durante o período especificado não serão listados.

- Nos usos por usuário, os usuários que não utilizaram o sistema durante o período especificado não serão listados.

> [!Important]
> Se você estiver usando múltiplos ambientes (dev, prod, etc.), o nome do banco de dados Athena incluirá o prefixo do ambiente. Em vez de `bedrockchatstack_usage_analysis`, o nome do banco de dados será:
>
> - Para ambiente padrão: `bedrockchatstack_usage_analysis`
> - Para ambientes nomeados: `<env-prefix>_bedrockchatstack_usage_analysis` (ex: `dev_bedrockchatstack_usage_analysis`)
>
> Além disso, o nome da tabela incluirá o prefixo do ambiente:
>
> - Para ambiente padrão: `ddb_export`
> - Para ambientes nomeados: `<env-prefix>_ddb_export` (ex: `dev_ddb_export`)
>
> Certifique-se de ajustar suas consultas adequadamente quando trabalhar com múltiplos ambientes.

## Download dos dados de conversação

Você pode consultar os logs de conversação usando Athena, através de SQL. Para baixar os logs, abra o Editor de Consultas do Athena no console de gerenciamento e execute SQL. A seguir estão alguns exemplos de consultas úteis para analisar casos de uso. O feedback pode ser consultado no atributo `MessageMap`.

### Consulta por ID do Bot

Edite `bot-id` e `datehour`. O `bot-id` pode ser consultado na tela de Gerenciamento de Bot, que pode ser acessada através das APIs de Publicação de Bot, mostrada na barra lateral esquerda. Observe a parte final da URL como `https://xxxx.cloudfront.net/admin/bot/<bot-id>`.

```sql
SELECT
    d.newimage.PK.S AS UserId,
    d.newimage.SK.S AS ConversationId,
    d.newimage.MessageMap.S AS MessageMap,
    d.newimage.TotalPrice.N AS TotalPrice,
    d.newimage.CreateTime.N AS CreateTime,
    d.newimage.LastMessageId.S AS LastMessageId,
    d.newimage.BotId.S AS BotId,
    d.datehour AS DateHour
FROM
    bedrockchatstack_usage_analysis.ddb_export d
WHERE
    d.newimage.BotId.S = '<bot-id>'
    AND d.datehour BETWEEN '<yyyy/mm/dd/hh>' AND '<yyyy/mm/dd/hh>'
    AND d.Keys.SK.S LIKE CONCAT(d.Keys.PK.S, '#CONV#%')
ORDER BY
    d.datehour DESC;
```

> [!Note]
> Se estiver usando um ambiente nomeado (ex: "dev"), substitua `bedrockchatstack_usage_analysis.ddb_export` por `dev_bedrockchatstack_usage_analysis.dev_ddb_export` na consulta acima.

### Consulta por ID do Usuário

Edite `user-id` e `datehour`. O `user-id` pode ser consultado na tela de Gerenciamento de Bot.

> [!Note]
> Análise de uso por usuário em breve.

```sql
SELECT
    d.newimage.PK.S AS UserId,
    d.newimage.SK.S AS ConversationId,
    d.newimage.MessageMap.S AS MessageMap,
    d.newimage.TotalPrice.N AS TotalPrice,
    d.newimage.CreateTime.N AS CreateTime,
    d.newimage.LastMessageId.S AS LastMessageId,
    d.newimage.BotId.S AS BotId,
    d.datehour AS DateHour
FROM
    bedrockchatstack_usage_analysis.ddb_export d
WHERE
    d.newimage.PK.S = '<user-id>'
    AND d.datehour BETWEEN '<yyyy/mm/dd/hh>' AND '<yyyy/mm/dd/hh>'
    AND d.Keys.SK.S LIKE CONCAT(d.Keys.PK.S, '#CONV#%')
ORDER BY
    d.datehour DESC;
```

> [!Note]
> Se estiver usando um ambiente nomeado (ex: "dev"), substitua `bedrockchatstack_usage_analysis.ddb_export` por `dev_bedrockchatstack_usage_analysis.dev_ddb_export` na consulta acima.