<h1 align="center">Bedrock Chat (BrChat)</h1>

<p align="center">
  <img src="https://img.shields.io/github/v/release/aws-samples/bedrock-chat?style=flat-square" />
  <img src="https://img.shields.io/github/license/aws-samples/bedrock-chat?style=flat-square" />
  <img src="https://img.shields.io/github/actions/workflow/status/aws-samples/bedrock-chat/cdk.yml?style=flat-square" />
  <a href="https://github.com/aws-samples/bedrock-chat/issues?q=is%3Aissue%20state%3Aopen%20label%3Aroadmap">
    <img src="https://img.shields.io/badge/roadmap-view-blue?style=flat-square" />
  </a>
</p>

[English](https://github.com/aws-samples/bedrock-chat/blob/v3/README.md) | [日本語](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_ja-JP.md) | [한국어](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_ko-KR.md) | [中文](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_zh-CN.md) | [Français](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_fr-FR.md) | [Deutsch](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_de-DE.md) | [Español](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_es-ES.md) | [Italian](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_it-IT.md) | [Norsk](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_nb-NO.md) | [ไทย](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_th-TH.md) | [Bahasa Indonesia](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_id-ID.md) | [Bahasa Melayu](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_ms-MY.md) | [Tiếng Việt](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_vi-VN.md) | [Polski](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_pl-PL.md) | [Português Brasil](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_pt-BR.md)


Uma plataforma de IA generativa multilíngue alimentada por [Amazon Bedrock](https://aws.amazon.com/bedrock/).
Suporta chat, bots personalizados com conhecimento (RAG), compartilhamento de bots através de uma loja de bots e automação de tarefas usando agentes.

![](./imgs/demo.gif)

> [!Aviso]
>
> **V3 lançada. Para atualizar, revise cuidadosamente o [guia de migração](./migration/V2_TO_V3_pt-BR.md).** Sem os devidos cuidados, **OS BOTS DA V2 SE TORNARÃO INUTILIZÁVEIS.**

### Personalização de Bots / Loja de Bots

Adicione suas próprias instruções e conhecimento (também conhecido como [RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)). O bot pode ser compartilhado entre usuários do aplicativo através de um marketplace de loja de bots. O bot personalizado também pode ser publicado como uma API independente (Veja os [detalhes](./PUBLISH_API_pt-BR.md)).

<details>
<summary>Capturas de Tela</summary>

![](./imgs/customized_bot_creation.png)
![](./imgs/fine_grained_permission.png)
![](./imgs/bot_store.png)
![](./imgs/bot_api_publish_screenshot3.png)

Você também pode importar [Bases de Conhecimento existentes do Amazon Bedrock](https://aws.amazon.com/bedrock/knowledge-bases/).

![](./imgs/import_existing_kb.png)

</details>

> [!Importante]
> Por razões de governança, apenas usuários autorizados podem criar bots personalizados. Para permitir a criação de bots personalizados, o usuário deve ser membro de um grupo chamado `CreatingBotAllowed`, que pode ser configurado através do console de gerenciamento > Pools de usuários do Amazon Cognito ou aws cli. Note que o ID do pool de usuários pode ser referenciado acessando CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`.

### Recursos Administrativos

Gerenciamento de API, Marcar bots como essenciais, Analisar uso de bots. [detalhes](./ADMINISTRATOR_pt-BR.md)

<details>
<summary>Capturas de Tela</summary>

![](./imgs/admin_bot_menue.png)
![](./imgs/bot_store.png)
![](./imgs/admn_api_management.png)
![](./imgs/admin_bot_analytics.png))

</details>

### Agente

Usando a [funcionalidade de Agente](./AGENT_pt-BR.md), seu chatbot pode lidar automaticamente com tarefas mais complexas. Por exemplo, para responder a uma pergunta de um usuário, o Agente pode recuperar informações necessárias de ferramentas externas ou dividir a tarefa em várias etapas para processamento.

<details>
<summary>Capturas de Tela</summary>

![](./imgs/agent1.png)
![](./imgs/agent2.png)

</details>

## 🚀 Implantação Super-Fácil

- Na região us-east-1, abra [Acesso ao Modelo Bedrock](https://us-east-1.console.aws.amazon.com/bedrock/home?region=us-east-1#/modelaccess) > `Gerenciar acesso ao modelo` > Marque todos os modelos que deseja usar e depois `Salvar alterações`.

<details>
<summary>Captura de tela</summary>

![](./imgs/model_screenshot.png)

</details>

- Abra o [CloudShell](https://console.aws.amazon.com/cloudshell/home) na região onde deseja implantar
- Execute a implantação através dos seguintes comandos. Se quiser especificar a versão a implantar ou precisar aplicar políticas de segurança, especifique os parâmetros apropriados de [Parâmetros Opcionais](#parâmetros-opcionais).

```sh
git clone https://github.com/aws-samples/bedrock-chat.git
cd bedrock-chat
chmod +x bin.sh
./bin.sh
```

- Você será perguntado se é um novo usuário ou usando v3. Se não for um usuário continuado da v0, digite `y`.

### Parâmetros Opcionais

Você pode especificar os seguintes parâmetros durante a implantação para aprimorar a segurança e personalização:

- **--disable-self-register**: Desabilitar registro próprio (padrão: habilitado). Se esta flag for definida, você precisará criar todos os usuários no Cognito e não permitirá que os usuários se registrem por conta própria.
- **--enable-lambda-snapstart**: Habilitar [Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html) (padrão: desabilitado). Se esta flag for definida, melhora os tempos de inicialização a frio para funções Lambda, fornecendo tempos de resposta mais rápidos para melhor experiência do usuário.
- **--ipv4-ranges**: Lista separada por vírgulas de intervalos IPv4 permitidos. (padrão: permitir todos os endereços ipv4)
- **--ipv6-ranges**: Lista separada por vírgulas de intervalos IPv6 permitidos. (padrão: permitir todos os endereços ipv6)
- **--disable-ipv6**: Desabilitar conexões sobre IPv6. (padrão: habilitado)
- **--allowed-signup-email-domains**: Lista separada por vírgulas de domínios de e-mail permitidos para registro. (padrão: sem restrição de domínio)
- **--bedrock-region**: Definir a região onde o Bedrock está disponível. (padrão: us-east-1)
- **--repo-url**: O repositório personalizado do Bedrock Chat para implantar, se bifurcado ou controle de origem personalizado. (padrão: https://github.com/aws-samples/bedrock-chat.git)
- **--version**: A versão do Bedrock Chat para implantar. (padrão: última versão em desenvolvimento)
- **--cdk-json-override**: Você pode substituir quaisquer valores de contexto CDK durante a implantação usando o bloco JSON de substituição. Isso permite modificar a configuração sem editar diretamente o arquivo cdk.json.

Exemplo de uso:

```bash
./bin.sh --cdk-json-override '{
  "context": {
    "selfSignUpEnabled": false,
    "enableLambdaSnapStart": true,
    "allowedIpV4AddressRanges": ["192.168.1.0/24"],
    "allowedSignUpEmailDomains": ["example.com"]
  }
}'
```

O JSON de substituição deve seguir a mesma estrutura do cdk.json. Você pode substituir quaisquer valores de contexto, incluindo:

- `selfSignUpEnabled`
- `enableLambdaSnapStart`
- `allowedIpV4AddressRanges`
- `allowedIpV6AddressRanges`
- `allowedSignUpEmailDomains`
- `bedrockRegion`
- `enableRagReplicas`
- `enableBedrockCrossRegionInference`
- E outros valores de contexto definidos no cdk.json

> [!Nota]
> Os valores de substituição serão mesclados com a configuração existente do cdk.json durante o tempo de implantação no AWS CodeBuild. Os valores especificados na substituição terão precedência sobre os valores no cdk.json.

#### Exemplo de comando com parâmetros:

```sh
./bin.sh --disable-self-register --ipv4-ranges "192.0.2.0/25,192.0.2.128/25" --ipv6-ranges "2001:db8:1:2::/64,2001:db8:1:3::/64" --allowed-signup-email-domains "example.com,anotherexample.com" --bedrock-region "us-west-2" --version "v1.2.6"
```

- Após cerca de 35 minutos, você receberá a seguinte saída, que pode ser acessada pelo seu navegador

```
Frontend URL: https://xxxxxxxxx.cloudfront.net
```

![](./imgs/signin.png)

A tela de registro será exibida conforme mostrado acima, onde você pode registrar seu e-mail e fazer login.

> [!Importante]
> Sem definir o parâmetro opcional, este método de implantação permite que qualquer pessoa que conheça a URL se registre. Para uso em produção, é altamente recomendado adicionar restrições de endereço IP e desabilitar o registro próprio para mitigar riscos de segurança (você pode definir allowed-signup-email-domains para restringir usuários para que apenas endereços de e-mail do domínio da sua empresa possam se registrar). Use tanto ipv4-ranges quanto ipv6-ranges para restrições de endereço IP e desabilite o registro próprio usando disable-self-register ao executar ./bin.

> [!DICA]
> Se a `Frontend URL` não aparecer ou o Bedrock Chat não funcionar corretamente, pode ser um problema com a versão mais recente. Neste caso, adicione `--version "v3.0.0"` aos parâmetros e tente a implantação novamente.

## Arquitetura

É uma arquitetura construída em serviços gerenciados da AWS, eliminando a necessidade de gerenciamento de infraestrutura. Utilizando o Amazon Bedrock, não há necessidade de comunicação com APIs externas à AWS. Isso permite implantar aplicações escaláveis, confiáveis e seguras.

- [Amazon DynamoDB](https://aws.amazon.com/dynamodb/): Banco de dados NoSQL para armazenamento do histórico de conversas
- [Amazon API Gateway](https://aws.amazon.com/api-gateway/) + [AWS Lambda](https://aws.amazon.com/lambda/): Endpoint de API backend ([AWS Lambda Web Adapter](https://github.com/awslabs/aws-lambda-web-adapter), [FastAPI](https://fastapi.tiangolo.com/))
- [Amazon CloudFront](https://aws.amazon.com/cloudfront/) + [S3](https://aws.amazon.com/s3/): Entrega de aplicação frontend ([React](https://react.dev/), [Tailwind CSS](https://tailwindcss.com/))
- [AWS WAF](https://aws.amazon.com/waf/): Restrição de endereço IP
- [Amazon Cognito](https://aws.amazon.com/cognito/): Autenticação de usuário
- [Amazon Bedrock](https://aws.amazon.com/bedrock/): Serviço gerenciado para utilizar modelos fundamentais via APIs
- [Amazon Bedrock Knowledge Bases](https://aws.amazon.com/bedrock/knowledge-bases/): Fornece uma interface gerenciada para Geração Aumentada por Recuperação ([RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)), oferecendo serviços para incorporação e análise de documentos
- [Amazon EventBridge Pipes](https://aws.amazon.com/eventbridge/pipes/): Recebimento de evento do stream do DynamoDB e inicialização de Step Functions para incorporar conhecimento externo
- [AWS Step Functions](https://aws.amazon.com/step-functions/): Orquestração do pipeline de ingestão para incorporar conhecimento externo nos Bedrock Knowledge Bases
- [Amazon OpenSearch Serverless](https://aws.amazon.com/opensearch-service/features/serverless/): Serve como banco de dados backend para Bedrock Knowledge Bases, fornecendo recursos de busca de texto completo e busca vetorial, permitindo recuperação precisa de informações relevantes
- [Amazon Athena](https://aws.amazon.com/athena/): Serviço de consulta para analisar bucket S3

![](./imgs/arch.png)

## Implantação usando CDK

A Implantação Super-fácil usa [AWS CodeBuild](https://aws.amazon.com/codebuild/) para realizar a implantação com CDK internamente. Esta seção descreve o procedimento para implantação direta com CDK.

- Por favor, tenha um ambiente UNIX, Docker e um ambiente de tempo de execução Node.js. Caso não tenha, você também pode usar [Cloud9](https://github.com/aws-samples/cloud9-setup-for-prototyping)

> [!Importante]
> Se houver espaço de armazenamento insuficiente no ambiente local durante a implantação, o bootstrapping do CDK pode resultar em um erro. Se você estiver executando no Cloud9 etc., recomendamos expandir o tamanho do volume da instância antes da implantação.

- Clone este repositório

```
git clone https://github.com/aws-samples/bedrock-chat
```

- Instale os pacotes npm

```
cd bedrock-chat
cd cdk
npm ci
```

- Se necessário, edite as seguintes entradas em [cdk.json](./cdk/cdk.json) se necessário.

  - `bedrockRegion`: Região onde o Bedrock está disponível. **NOTA: O Bedrock NÃO oferece suporte a todas as regiões no momento.**
  - `allowedIpV4AddressRanges`, `allowedIpV6AddressRanges`: Faixa de Endereço IP permitida.
  - `enableLambdaSnapStart`: Por padrão, é true. Defina como false se estiver implantando em uma [região que não oferece suporte ao Lambda SnapStart para funções Python](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions).

- Antes de implantar o CDK, você precisará realizar o Bootstrap uma vez para a região em que está implantando.

```
npx cdk bootstrap
```

- Implante este projeto de exemplo

```
npx cdk deploy --require-approval never --all
```

- Você receberá uma saída semelhante à seguinte. A URL do aplicativo web será exibida em `BedrockChatStack.FrontendURL`, então acesse-a pelo seu navegador.

```sh
 ✅  BedrockChatStack

✨  Tempo de implantação: 78.57s

Saídas:
BedrockChatStack.AuthUserPoolClientIdXXXXX = xxxxxxx
BedrockChatStack.AuthUserPoolIdXXXXXX = ap-northeast-1_XXXX
BedrockChatStack.BackendApiBackendApiUrlXXXXX = https://xxxxx.execute-api.ap-northeast-1.amazonaws.com
BedrockChatStack.FrontendURL = https://xxxxx.cloudfront.net
```

### Definindo Parâmetros

Você pode definir parâmetros para sua implantação de duas maneiras: usando `cdk.json` ou usando o arquivo `parameter.ts` com tipagem segura.

#### Usando cdk.json (Método Tradicional)

A maneira tradicional de configurar parâmetros é editando o arquivo `cdk.json`. Esta abordagem é simples, mas carece de verificação de tipo:

```json
{
  "app": "npx ts-node --prefer-ts-exts bin/bedrock-chat.ts",
  "context": {
    "bedrockRegion": "us-east-1",
    "allowedIpV4AddressRanges": ["0.0.0.0/1", "128.0.0.0/1"],
    "selfSignUpEnabled": true
  }
}
```

#### Usando parameter.ts (Método Recomendado com Tipagem Segura)

Para maior segurança de tipo e experiência do desenvolvedor, você pode usar o arquivo `parameter.ts` para definir seus parâmetros:

```typescript
// Definir parâmetros para o ambiente padrão
bedrockChatParams.set("default", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["192.168.0.0/16"],
  selfSignUpEnabled: true,
});

// Definir parâmetros para ambientes adicionais
bedrockChatParams.set("dev", {
  bedrockRegion: "us-west-2",
  allowedIpV4AddressRanges: ["10.0.0.0/8"],
  enableRagReplicas: false, // Economia de custos para ambiente de desenvolvimento
  enableBotStoreReplicas: false, // Economia de custos para ambiente de desenvolvimento
});

bedrockChatParams.set("prod", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["172.16.0.0/12"],
  enableLambdaSnapStart: true,
  enableRagReplicas: true, // Disponibilidade aprimorada para produção
  enableBotStoreReplicas: true, // Disponibilidade aprimorada para produção
});
```

> [!Nota]
> Usuários existentes podem continuar usando `cdk.json` sem alterações. A abordagem `parameter.ts` é recomendada para novas implantações ou quando você precisa gerenciar múltiplos ambientes.

### Implantando Múltiplos Ambientes

Você pode implantar múltiplos ambientes a partir do mesmo código-base usando o arquivo `parameter.ts` e a opção `-c envName`.

#### Pré-requisitos

1. Defina seus ambientes em `parameter.ts` como mostrado acima
2. Cada ambiente terá seu próprio conjunto de recursos com prefixos específicos do ambiente

#### Comandos de Implantação

Para implantar um ambiente específico:

```bash
# Implantar o ambiente de desenvolvimento
npx cdk deploy --all -c envName=dev

# Implantar o ambiente de produção
npx cdk deploy --all -c envName=prod
```

Se nenhum ambiente for especificado, o ambiente "default" será usado:

```bash
# Implantar o ambiente padrão
npx cdk deploy --all
```

#### Notas Importantes

1. **Nomenclatura de Pilhas**:

   - As pilhas principais para cada ambiente serão prefixadas com o nome do ambiente (por exemplo, `dev-BedrockChatStack`, `prod-BedrockChatStack`)
   - No entanto, pilhas de bots personalizados (`BrChatKbStack*`) e pilhas de publicação de API (`ApiPublishmentStack*`) não recebem prefixos de ambiente, pois são criadas dinamicamente em tempo de execução

2. **Nomenclatura de Recursos**:

   - Apenas alguns recursos recebem prefixos de ambiente em seus nomes (por exemplo, tabela `dev_ddb_export`, `dev-FrontendWebAcl`)
   - A maioria dos recursos mantém seus nomes originais, mas são isolados por estarem em pilhas diferentes

3. **Identificação de Ambiente**:

   - Todos os recursos são marcados com uma tag `CDKEnvironment` contendo o nome do ambiente
   - Você pode usar essa tag para identificar a qual ambiente um recurso pertence
   - Exemplo: `CDKEnvironment: dev` ou `CDKEnvironment: prod`

4. **Substituição de Ambiente Padrão**: Se você definir um ambiente "default" em `parameter.ts`, ele substituirá as configurações em `cdk.json`. Para continuar usando `cdk.json`, não defina um ambiente "default" em `parameter.ts`.

5. **Requisitos de Ambiente**: Para criar ambientes diferentes de "default", você deve usar `parameter.ts`. A opção `-c envName` sozinha não é suficiente sem definições de ambiente correspondentes.

6. **Isolamento de Recursos**: Cada ambiente cria seu próprio conjunto de recursos, permitindo que você tenha ambientes de desenvolvimento, teste e produção na mesma conta AWS sem conflitos.

## Outros

Você pode definir parâmetros para sua implantação de duas maneiras: usando `cdk.json` ou usando o arquivo `parameter.ts` com tipagem segura.

#### Usando cdk.json (Método Tradicional)

A forma tradicional de configurar parâmetros é editando o arquivo `cdk.json`. Esta abordagem é simples, mas carece de verificação de tipos:

```json
{
  "app": "npx ts-node --prefer-ts-exts bin/bedrock-chat.ts",
  "context": {
    "bedrockRegion": "us-east-1",
    "allowedIpV4AddressRanges": ["0.0.0.0/1", "128.0.0.0/1"],
    "selfSignUpEnabled": true
  }
}
```

#### Usando parameter.ts (Método Recomendado com Tipagem Segura)

Para maior segurança de tipos e experiência do desenvolvedor, você pode usar o arquivo `parameter.ts` para definir seus parâmetros:

```typescript
// Definir parâmetros para o ambiente padrão
bedrockChatParams.set("default", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["192.168.0.0/16"],
  selfSignUpEnabled: true,
});

// Definir parâmetros para ambientes adicionais
bedrockChatParams.set("dev", {
  bedrockRegion: "us-west-2",
  allowedIpV4AddressRanges: ["10.0.0.0/8"],
  enableRagReplicas: false, // Economia de custos para ambiente de desenvolvimento
});

bedrockChatParams.set("prod", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["172.16.0.0/12"],
  enableLambdaSnapStart: true,
  enableRagReplicas: true, // Disponibilidade aprimorada para produção
});
```

> [!Nota]
> Usuários existentes podem continuar usando `cdk.json` sem alterações. A abordagem `parameter.ts` é recomendada para novas implantações ou quando você precisa gerenciar múltiplos ambientes.

### Implantando Múltiplos Ambientes

Você pode implantar múltiplos ambientes a partir do mesmo código-base usando o arquivo `parameter.ts` e a opção `-c envName`.

#### Pré-requisitos

1. Defina seus ambientes em `parameter.ts` como mostrado acima
2. Cada ambiente terá seu próprio conjunto de recursos com prefixos específicos do ambiente

#### Comandos de Implantação

Para implantar um ambiente específico:

```bash
# Implantar o ambiente de desenvolvimento
npx cdk deploy --all -c envName=dev

# Implantar o ambiente de produção
npx cdk deploy --all -c envName=prod
```

Se nenhum ambiente for especificado, o ambiente "default" será usado:

```bash
# Implantar o ambiente padrão
npx cdk deploy --all
```

#### Observações Importantes

1. **Nomenclatura de Pilhas**:

   - As pilhas principais para cada ambiente serão prefixadas com o nome do ambiente (por exemplo, `dev-BedrockChatStack`, `prod-BedrockChatStack`)
   - No entanto, pilhas de bot personalizadas (`BrChatKbStack*`) e pilhas de publicação de API (`ApiPublishmentStack*`) não recebem prefixos de ambiente, pois são criadas dinamicamente em tempo de execução

2. **Nomenclatura de Recursos**:

   - Apenas alguns recursos recebem prefixos de ambiente em seus nomes (por exemplo, tabela `dev_ddb_export`, `dev-FrontendWebAcl`)
   - A maioria dos recursos mantém seus nomes originais, mas são isolados por estarem em pilhas diferentes

3. **Identificação de Ambiente**:

   - Todos os recursos são marcados com uma tag `CDKEnvironment` contendo o nome do ambiente
   - Você pode usar essa tag para identificar a qual ambiente um recurso pertence
   - Exemplo: `CDKEnvironment: dev` ou `CDKEnvironment: prod`

4. **Substituição de Ambiente Padrão**: Se você definir um ambiente "default" em `parameter.ts`, ele substituirá as configurações em `cdk.json`. Para continuar usando `cdk.json`, não defina um ambiente "default" em `parameter.ts`.

5. **Requisitos de Ambiente**: Para criar ambientes diferentes de "default", você deve usar `parameter.ts`. A opção `-c envName` sozinha não é suficiente sem definições de ambiente correspondentes.

6. **Isolamento de Recursos**: Cada ambiente cria seu próprio conjunto de recursos, permitindo que você tenha ambientes de desenvolvimento, teste e produção na mesma conta AWS sem conflitos.

## Outros

### Remover recursos

Se estiver usando CLI e CDK, execute `npx cdk destroy`. Caso contrário, acesse [CloudFormation](https://console.aws.amazon.com/cloudformation/home) e exclua manualmente `BedrockChatStack` e `FrontendWafStack`. Observe que `FrontendWafStack` está na região `us-east-1`.

### Configurações de Idioma

Este recurso detecta automaticamente o idioma usando [i18next-browser-languageDetector](https://github.com/i18next/i18next-browser-languageDetector). Você pode alternar idiomas no menu do aplicativo. Como alternativa, você pode usar Query String para definir o idioma conforme mostrado abaixo.

> `https://example.com?lng=ja`

### Desabilitar autoinscrição

Esta amostra tem autoinscrição habilitada por padrão. Para desabilitar a autoinscrição, abra [cdk.json](./cdk/cdk.json) e altere `selfSignUpEnabled` para `false`. Se você configurar um [provedor de identidade externo](#provedor-de-identidade-externo), o valor será ignorado e automaticamente desabilitado.

### Restringir Domínios para Endereços de E-mail de Inscrição

Por padrão, esta amostra não restringe os domínios para endereços de e-mail de inscrição. Para permitir inscrições apenas de domínios específicos, abra `cdk.json` e especifique os domínios como uma lista em `allowedSignUpEmailDomains`.

```ts
"allowedSignUpEmailDomains": ["example.com"],
```

### Provedor de Identidade Externo

Esta amostra suporta provedor de identidade externo. Atualmente, suportamos [Google](./idp/SET_UP_GOOGLE_pt-BR.md) e [provedor OIDC personalizado](./idp/SET_UP_CUSTOM_OIDC_pt-BR.md).

### Adicionar novos usuários a grupos automaticamente

Esta amostra possui os seguintes grupos para dar permissões aos usuários:

- [`Admin`](./ADMINISTRATOR_pt-BR.md)
- [`CreatingBotAllowed`](#personalizacao-de-bot)
- [`PublishAllowed`](./PUBLISH_API_pt-BR.md)

Se você quiser que usuários recém-criados entrem automaticamente em grupos, pode especificá-los em [cdk.json](./cdk/cdk.json).

```json
"autoJoinUserGroups": ["CreatingBotAllowed"],
```

Por padrão, usuários recém-criados serão adicionados ao grupo `CreatingBotAllowed`.

### Configurar Réplicas RAG

`enableRagReplicas` é uma opção em [cdk.json](./cdk/cdk.json) que controla as configurações de réplica para o banco de dados RAG, especificamente as Bases de Conhecimento usando Amazon OpenSearch Serverless.

- **Padrão**: true
- **true**: Melhora a disponibilidade ao habilitar réplicas adicionais, sendo adequado para ambientes de produção, mas aumentando custos.
- **false**: Reduz custos usando menos réplicas, sendo adequado para desenvolvimento e teste.

Esta é uma configuração de nível de conta/região, afetando toda a aplicação, não apenas bots individuais.

> [!Nota]
> A partir de junho de 2024, o Amazon OpenSearch Serverless suporta 0,5 OCU, reduzindo os custos iniciais para cargas de trabalho em pequena escala. Implantações de produção podem começar com 2 OCUs, enquanto cargas de trabalho de desenvolvimento/teste podem usar 1 OCU. O OpenSearch Serverless escala automaticamente com base nas demandas de carga de trabalho. Para mais detalhes, visite [anúncio](https://aws.amazon.com/jp/about-aws/whats-new/2024/06/amazon-opensearch-serverless-entry-cost-half-collection-types/).

### Configurar Loja de Bots

O recurso de loja de bots permite que os usuários compartilhem e descubram bots personalizados. Você pode configurar a loja de bots através das seguintes configurações em [cdk.json](./cdk/cdk.json):

```json
{
  "context": {
    "enableBotStore": true,
    "enableBotStoreReplicas": false,
    "botStoreLanguage": "en"
  }
}
```

- **enableBotStore**: Controla se o recurso de loja de bots está habilitado (padrão: `true`)
- **botStoreLanguage**: Define o idioma principal para busca e descoberta de bots (padrão: `"en"`). Isso afeta como os bots são indexados e pesquisados na loja de bots, otimizando a análise de texto para o idioma especificado.
- **enableBotStoreReplicas**: Controla se réplicas em standby estão habilitadas para a coleção OpenSearch Serverless usada pela loja de bots (padrão: `false`). Definir como `true` melhora a disponibilidade, mas aumenta custos, enquanto `false` reduz custos, mas pode afetar a disponibilidade.
  > **Importante**: Você não pode atualizar esta propriedade após a coleção já ter sido criada. Se tentar modificar esta propriedade, a coleção continuará usando o valor original.

### Inferência entre regiões

A [inferência entre regiões](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html) permite que o Amazon Bedrock encaminhe dinamicamente solicitações de inferência de modelo entre várias regiões AWS, aprimorando a taxa de transferência e a resiliência durante períodos de pico de demanda. Para configurar, edite `cdk.json`.

```json
"enableBedrockCrossRegionInference": true
```

### Lambda SnapStart

O [Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html) melhora os tempos de inicialização a frio para funções Lambda, proporcionando tempos de resposta mais rápidos para uma melhor experiência do usuário. Por outro lado, para funções Python, há um [custo dependendo do tamanho do cache](https://aws.amazon.com/lambda/pricing/#SnapStart_Pricing) e [não está disponível em algumas regiões](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions) atualmente. Para desabilitar o SnapStart, edite `cdk.json`.

```json
"enableLambdaSnapStart": false
```

### Configurar Domínio Personalizado

Você pode configurar um domínio personalizado para a distribuição CloudFront definindo os seguintes parâmetros em [cdk.json](./cdk/cdk.json):

```json
{
  "alternateDomainName": "chat.example.com",
  "hostedZoneId": "Z0123456789ABCDEF"
}
```

- `alternateDomainName`: O nome de domínio personalizado para seu aplicativo de chat (por exemplo, chat.example.com)
- `hostedZoneId`: O ID da zona hospedada do Route 53 onde os registros de domínio serão criados

Quando esses parâmetros são fornecidos, a implantação automaticamente:

- Criará um certificado ACM com validação DNS na região us-east-1
- Criará os registros DNS necessários em sua zona hospedada do Route 53
- Configurará o CloudFront para usar seu domínio personalizado

> [!Nota]
> O domínio deve ser gerenciado pelo Route 53 em sua conta AWS. O ID da zona hospedada pode ser encontrado no console do Route 53.

### Desenvolvimento Local

Consulte [DESENVOLVIMENTO LOCAL](./LOCAL_DEVELOPMENT_pt-BR.md).

### Contribuição

Obrigado por considerar contribuir para este repositório! Aceitamos correções de bugs, traduções de idiomas (i18n), melhorias de recursos, [ferramentas de agente](./docs/AGENT.md#how-to-develop-your-own-tools) e outros aprimoramentos.

Para melhorias de recursos e outros aprimoramentos, **antes de criar um Pull Request, agradecemos muito se você pudesse criar um Issue de Solicitação de Recurso para discutir a abordagem de implementação e os detalhes. Para correções de bugs e traduções de idiomas (i18n), prossiga diretamente com a criação de um Pull Request.**

Dê uma olhada também nas seguintes diretrizes antes de contribuir:

- [Desenvolvimento Local](./LOCAL_DEVELOPMENT_pt-BR.md)
- [CONTRIBUTING](./CONTRIBUTING_pt-BR.md)

## Contatos

- [Takehiro Suzuki](https://github.com/statefb)
- [Yusuke Wada](https://github.com/wadabee)
- [Yukinobu Mine](https://github.com/Yukinobu-Mine)

## 🏆 Contribuidores Significativos

- [fsatsuki](https://github.com/fsatsuki)
- [k70suK3-k06a7ash1](https://github.com/k70suK3-k06a7ash1)

## Contribuidores

[![contribuidores do bedrock chat](https://contrib.rocks/image?repo=aws-samples/bedrock-chat&max=1000)](https://github.com/aws-samples/bedrock-chat/graphs/contributors)

## Licença

Esta biblioteca é licenciada sob a Licença MIT-0. Consulte [o arquivo de LICENÇA](./LICENSE).