# Publicação de API

## Visão Geral

Esta amostra inclui um recurso para publicação de APIs. Embora uma interface de chat possa ser conveniente para validação preliminar, a implementação real depende do caso de uso específico e da experiência do usuário (UX) desejada para o usuário final. Em alguns cenários, uma interface de chat pode ser a escolha preferida, enquanto em outros, uma API independente pode ser mais adequada. Após a validação inicial, esta amostra oferece a capacidade de publicar bots personalizados de acordo com as necessidades do projeto. Ao inserir configurações para cotas, limitação de taxa, origens, etc., um endpoint pode ser publicado junto com uma chave de API, oferecendo flexibilidade para diversas opções de integração.

## Segurança

Usar apenas uma chave de API não é recomendado, conforme descrito em: [Guia do Desenvolvedor do AWS API Gateway](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-api-usage-plans.html). Consequentemente, esta amostra implementa uma simples restrição de endereço IP via AWS WAF. A regra do WAF é aplicada comumente em toda a aplicação devido a considerações de custo, sob a suposição de que as fontes que se deseja restringir provavelmente são as mesmas em todas as APIs emitidas. **Por favor, siga a política de segurança da sua organização para implementação real.** Consulte também a seção [Arquitetura](#architecture).

## Como publicar uma API de bot personalizada

### Pré-requisitos

Por razões de governança, apenas usuários limitados podem publicar bots. Antes de publicar, o usuário deve ser membro do grupo chamado `PublishAllowed`, que pode ser configurado através do console de gerenciamento > Amazon Cognito User pools ou aws cli. Observe que o ID do user pool pode ser referenciado acessando CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`.

![](./imgs/group_membership_publish_allowed.png)

### Configurações de Publicação de API

Após fazer login como um usuário `PublishedAllowed` e criar um bot, escolha `API PublishSettings`. Observe que apenas um bot compartilhado pode ser publicado.
![](./imgs/bot_api_publish_screenshot.png)

Na tela seguinte, podemos configurar vários parâmetros relacionados à limitação de taxa. Para mais detalhes, consulte também: [Limitar solicitações de API para melhor throughput](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html).
![](./imgs/bot_api_publish_screenshot2.png)

Após a implantação, aparecerá a seguinte tela onde você pode obter a URL do endpoint e uma chave de API. Também podemos adicionar e excluir chaves de API.

![](./imgs/bot_api_publish_screenshot3.png)

## Arquitetura

A API é publicada conforme o diagrama a seguir:

![](./imgs/published_arch.png)

O WAF é usado para restrição de endereço IP. O endereço pode ser configurado definindo os parâmetros `publishedApiAllowedIpV4AddressRanges` e `publishedApiAllowedIpV6AddressRanges` no `cdk.json`.

Quando um usuário clica para publicar o bot, o [AWS CodeBuild](https://aws.amazon.com/codebuild/) inicia uma tarefa de implantação do CDK para provisionar a pilha da API (Consulte também: [Definição do CDK](../cdk/lib/api-publishment-stack.ts)) que contém API Gateway, Lambda e SQS. O SQS é usado para desacoplar a solicitação do usuário e a operação do LLM porque a geração de saída pode exceder 30 segundos, que é o limite de cota do API Gateway. Para buscar a saída, é necessário acessar a API de forma assíncrona. Para mais detalhes, consulte [Especificação da API](#api-specification).

O cliente precisa definir `x-api-key` no cabeçalho da solicitação.

## Especificação da API

Veja [aqui](https://aws-samples.github.io/bedrock-chat).