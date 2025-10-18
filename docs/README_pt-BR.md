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


Uma plataforma de IA generativa multilíngue alimentada pelo [Amazon Bedrock](https://aws.amazon.com/bedrock/).
Suporta chat, bots personalizados com conhecimento (RAG), compartilhamento de bots através de uma loja de bots e automação de tarefas usando agentes.

![](./imgs/demo.gif)

> [!Warning]
>
> **V3 lançada. Para atualizar, por favor revise cuidadosamente o [guia de migração](./migration/V2_TO_V3_pt-BR.md).** Sem os devidos cuidados, **OS BOTS DA V2 SE TORNARÃO INUTILIZÁVEIS.**

### Personalização de Bot / Loja de bots

Adicione suas próprias instruções e conhecimento (também conhecido como [RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)). O bot pode ser compartilhado entre os usuários do aplicativo através do marketplace da loja de bots. O bot personalizado também pode ser publicado como uma API independente (Veja os [detalhes](./PUBLISH_API_pt-BR.md)).

<details>
<summary>Capturas de tela</summary>

![](./imgs/customized_bot_creation.png)
![](./imgs/fine_grained_permission.png)
![](./imgs/bot_store.png)
![](./imgs/bot_api_publish_screenshot3.png)

Você também pode importar [Amazon Bedrock's KnowledgeBase](https://aws.amazon.com/bedrock/knowledge-bases/) existentes.

![](./imgs/import_existing_kb.png)

</details>

> [!Important]
> Por razões de governança, apenas usuários autorizados podem criar bots personalizados. Para permitir a criação de bots personalizados, o usuário deve ser membro do grupo chamado `CreatingBotAllowed`, que pode ser configurado através do console de gerenciamento > Amazon Cognito User pools ou aws cli. Observe que o id do pool de usuários pode ser referenciado acessando CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`.

### Recursos administrativos

Gerenciamento de API, Marcação de bots como essenciais, Análise de uso dos bots. [detalhes](./ADMINISTRATOR_pt-BR.md)

<details>
<summary>Capturas de tela</summary>

![](./imgs/admin_bot_menue.png)
![](./imgs/bot_store.png)
![](./imgs/admn_api_management.png)
![](./imgs/admin_bot_analytics.png))

</details>

### Agente

Usando a [funcionalidade de Agente](./AGENT_pt-BR.md), seu chatbot pode automaticamente lidar com tarefas mais complexas. Por exemplo, para responder à pergunta de um usuário, o Agente pode recuperar informações necessárias de ferramentas externas ou dividir a tarefa em múltiplos passos para processamento.

<details>
<summary>Capturas de tela</summary>

![](./imgs/agent1.png)
![](./imgs/agent2.png)

</details>

## 🚀 Implantação Super-fácil

- Na região us-east-1, abra [Bedrock Model access](https://us-east-1.console.aws.amazon.com/bedrock/home?region=us-east-1#/modelaccess) > `Manage model access` > Marque todos os modelos que deseja usar e então clique em `Save changes`.

<details>
<summary>Captura de tela</summary>

![](./imgs/model_screenshot.png)

</details>

### Regiões suportadas

Certifique-se de implantar o Bedrock Chat em uma região [onde OpenSearch Serverless e APIs de Ingestão estejam disponíveis](https://docs.aws.amazon.com/general/latest/gr/opensearch-service.html), se você quiser usar bots e criar bases de conhecimento (OpenSearch Serverless é a escolha padrão). A partir de agosto de 2025, as seguintes regiões são suportadas: us-east-1, us-east-2, us-west-1, us-west-2, ap-south-1, ap-northeast-1, ap-northeast-2, ap-southeast-1, ap-southeast-2, ca-central-1, eu-central-1, eu-west-1, eu-west-2, eu-south-2, eu-north-1, sa-east-1

Para o parâmetro **bedrock-region** você precisa escolher uma região [onde o Bedrock esteja disponível](https://docs.aws.amazon.com/general/latest/gr/bedrock.html).

- Abra o [CloudShell](https://console.aws.amazon.com/cloudshell/home) na região onde você deseja fazer a implantação
- Execute a implantação através dos seguintes comandos. Se você quiser especificar a versão a ser implantada ou precisar aplicar políticas de segurança, especifique os parâmetros apropriados em [Parâmetros Opcionais](#optional-parameters).

```sh
git clone https://github.com/aws-samples/bedrock-chat.git
cd bedrock-chat
chmod +x bin.sh
./bin.sh
```

- Será perguntado se você é um novo usuário ou está usando v3. Se você não é um usuário continuando da v0, digite `y`.

### Parâmetros Opcionais

Você pode especificar os seguintes parâmetros durante a implantação para melhorar a segurança e personalização:

- **--disable-self-register**: Desativa o auto-registro (padrão: ativado). Se esta flag for definida, você precisará criar todos os usuários no cognito e não permitirá que os usuários registrem suas contas por conta própria.
- **--enable-lambda-snapstart**: Ativa o [Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html) (padrão: desativado). Se esta flag for definida, melhora os tempos de início a frio das funções Lambda, proporcionando tempos de resposta mais rápidos para uma melhor experiência do usuário.
- **--ipv4-ranges**: Lista separada por vírgulas de intervalos IPv4 permitidos. (padrão: permite todos os endereços ipv4)
- **--ipv6-ranges**: Lista separada por vírgulas de intervalos IPv6 permitidos. (padrão: permite todos os endereços ipv6)
- **--disable-ipv6**: Desativa conexões via IPv6. (padrão: ativado)
- **--allowed-signup-email-domains**: Lista separada por vírgulas de domínios de email permitidos para registro. (padrão: sem restrição de domínio)
- **--bedrock-region**: Define a região onde o bedrock está disponível. (padrão: us-east-1)
- **--repo-url**: O repositório personalizado do Bedrock Chat para implantar, se bifurcado ou controle de fonte personalizado. (padrão: https://github.com/aws-samples/bedrock-chat.git)
- **--version**: A versão do Bedrock Chat a ser implantada. (padrão: última versão em desenvolvimento)
- **--cdk-json-override**: Você pode substituir quaisquer valores de contexto do CDK durante a implantação usando o bloco JSON de substituição. Isso permite modificar a configuração sem editar diretamente o arquivo cdk.json.

Exemplo de uso:

```bash
./bin.sh --cdk-json-override '{
  "context": {
    "selfSignUpEnabled": false,
    "enableLambdaSnapStart": true,
    "allowedIpV4AddressRanges": ["192.168.1.0/24"],
    "allowedCountries": ["US", "CA"],
    "allowedSignUpEmailDomains": ["example.com"],
    "globalAvailableModels": [
      "claude-v3.7-sonnet",
      "claude-v3.5-sonnet",
      "amazon-nova-pro",
      "amazon-nova-lite",
      "llama3-3-70b-instruct"
    ]
  }
}'
```

O JSON de substituição deve seguir a mesma estrutura do cdk.json. Você pode substituir quaisquer valores de contexto incluindo:

- `selfSignUpEnabled`
- `enableLambdaSnapStart`
- `allowedIpV4AddressRanges`
- `allowedIpV6AddressRanges`
- `allowedCountries`
- `allowedSignUpEmailDomains`
- `bedrockRegion`
- `enableRagReplicas`
- `enableBedrockCrossRegionInference`
- `globalAvailableModels`: aceita uma lista de IDs de modelo para ativar. O valor padrão é uma lista vazia, que ativa todos os modelos.
- `logoPath`: caminho relativo para o ativo do logo dentro do diretório `public/` do frontend que aparece no topo da gaveta de navegação.
- E outros valores de contexto definidos em cdk.json

> [!Note]
> Os valores de substituição serão mesclados com a configuração existente do cdk.json durante o tempo de implantação no AWS code build. Valores especificados na substituição terão precedência sobre os valores no cdk.json.

#### Exemplo de comando com parâmetros:

```sh
./bin.sh --disable-self-register --ipv4-ranges "192.0.2.0/25,192.0.2.128/25" --ipv6-ranges "2001:db8:1:2::/64,2001:db8:1:3::/64" --allowed-signup-email-domains "example.com,anotherexample.com" --bedrock-region "us-west-2" --version "v1.2.6"
```

- Após cerca de 35 minutos, você receberá a seguinte saída, que você pode acessar do seu navegador

```
Frontend URL: https://xxxxxxxxx.cloudfront.net
```

![](./imgs/signin.png)

A tela de registro aparecerá como mostrado acima, onde você pode registrar seu email e fazer login.

> [!Important]
> Sem definir o parâmetro opcional, este método de implantação permite que qualquer pessoa que conheça a URL se registre. Para uso em produção, é fortemente recomendado adicionar restrições de endereço IP e desativar o auto-registro para mitigar riscos de segurança (você pode definir allowed-signup-email-domains para restringir usuários para que apenas endereços de email do domínio da sua empresa possam se registrar). Use tanto ipv4-ranges quanto ipv6-ranges para restrições de endereço IP, e desative o auto-registro usando disable-self-register ao executar ./bin.

> [!TIP]
> Se a `Frontend URL` não aparecer ou o Bedrock Chat não funcionar corretamente, pode ser um problema com a última versão. Neste caso, adicione `--version "v3.0.0"` aos parâmetros e tente a implantação novamente.

## Arquitetura

É uma arquitetura construída sobre serviços gerenciados da AWS, eliminando a necessidade de gerenciamento de infraestrutura. Utilizando o Amazon Bedrock, não há necessidade de comunicação com APIs fora da AWS. Isso permite implantar aplicações escaláveis, confiáveis e seguras.

- [Amazon DynamoDB](https://aws.amazon.com/dynamodb/): Banco de dados NoSQL para armazenamento do histórico de conversas
- [Amazon API Gateway](https://aws.amazon.com/api-gateway/) + [AWS Lambda](https://aws.amazon.com/lambda/): Endpoint da API backend ([AWS Lambda Web Adapter](https://github.com/awslabs/aws-lambda-web-adapter), [FastAPI](https://fastapi.tiangolo.com/))
- [Amazon CloudFront](https://aws.amazon.com/cloudfront/) + [S3](https://aws.amazon.com/s3/): Entrega da aplicação frontend ([React](https://react.dev/), [Tailwind CSS](https://tailwindcss.com/))
- [AWS WAF](https://aws.amazon.com/waf/): Restrição de endereço IP
- [Amazon Cognito](https://aws.amazon.com/cognito/): Autenticação de usuários
- [Amazon Bedrock](https://aws.amazon.com/bedrock/): Serviço gerenciado para utilizar modelos fundamentais via APIs
- [Amazon Bedrock Knowledge Bases](https://aws.amazon.com/bedrock/knowledge-bases/): Fornece uma interface gerenciada para Geração Aumentada por Recuperação ([RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)), oferecendo serviços para incorporação e análise de documentos
- [Amazon EventBridge Pipes](https://aws.amazon.com/eventbridge/pipes/): Recebimento de eventos do stream do DynamoDB e inicialização do Step Functions para incorporar conhecimento externo
- [AWS Step Functions](https://aws.amazon.com/step-functions/): Orquestração do pipeline de ingestão para incorporar conhecimento externo nas Bedrock Knowledge Bases
- [Amazon OpenSearch Serverless](https://aws.amazon.com/opensearch-service/features/serverless/): Serve como banco de dados backend para Bedrock Knowledge Bases, fornecendo busca em texto completo e busca vetorial, permitindo recuperação precisa de informações relevantes
- [Amazon Athena](https://aws.amazon.com/athena/): Serviço de consulta para analisar bucket S3

![](./imgs/arch.png)

## Deploy usando CDK

A implantação super fácil usa o [AWS CodeBuild](https://aws.amazon.com/codebuild/) para realizar a implantação via CDK internamente. Esta seção descreve o procedimento para implantar diretamente com CDK.

- Por favor, tenha UNIX, Docker e um ambiente de execução Node.js.

> [!Important]
> Se houver espaço de armazenamento insuficiente no ambiente local durante a implantação, o bootstrap do CDK pode resultar em erro. Recomendamos aumentar o tamanho do volume da instância antes de implantar.

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

- Se necessário, edite as seguintes entradas em [cdk.json](./cdk/cdk.json).

  - `bedrockRegion`: Região onde o Bedrock está disponível. **NOTA: O Bedrock NÃO suporta todas as regiões por enquanto.**
  - `allowedIpV4AddressRanges`, `allowedIpV6AddressRanges`: Faixa de endereços IP permitidos.
  - `enableLambdaSnapStart`: O padrão é true. Defina como false se estiver implantando em uma [região que não suporta Lambda SnapStart para funções Python](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions).
  - `globalAvailableModels`: O padrão é todos. Se definido (lista de IDs de modelo), permite controlar globalmente quais modelos aparecem nos menus suspensos em todos os chats para todos os usuários e durante a criação de bots no aplicativo Bedrock Chat.
  - `logoPath`: Caminho relativo sob `frontend/public` que aponta para a imagem exibida no topo da gaveta do aplicativo.
Os seguintes IDs de modelo são suportados (certifique-se de que eles também estejam habilitados no console do Bedrock em Model access na sua região de implantação):
- **Modelos Claude:** `claude-v4-opus`, `claude-v4.1-opus`, `claude-v4-sonnet`, `claude-v3.5-sonnet`, `claude-v3.5-sonnet-v2`, `claude-v3.7-sonnet`, `claude-v3.5-haiku`, `claude-v3-haiku`, `claude-v3-opus`
- **Modelos Amazon Nova:** `amazon-nova-pro`, `amazon-nova-lite`, `amazon-nova-micro`
- **Modelos Mistral:** `mistral-7b-instruct`, `mixtral-8x7b-instruct`, `mistral-large`, `mistral-large-2`
- **Modelos DeepSeek:** `deepseek-r1`
- **Modelos Meta Llama:** `llama3-3-70b-instruct`, `llama3-2-1b-instruct`, `llama3-2-3b-instruct`, `llama3-2-11b-instruct`, `llama3-2-90b-instruct`

A lista completa pode ser encontrada em [index.ts](./frontend/src/constants/index.ts).

- Antes de implantar o CDK, você precisará trabalhar com o Bootstrap uma vez para a região em que está implantando.

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

✨  Deployment time: 78.57s

Outputs:
BedrockChatStack.AuthUserPoolClientIdXXXXX = xxxxxxx
BedrockChatStack.AuthUserPoolIdXXXXXX = ap-northeast-1_XXXX
BedrockChatStack.BackendApiBackendApiUrlXXXXX = https://xxxxx.execute-api.ap-northeast-1.amazonaws.com
BedrockChatStack.FrontendURL = https://xxxxx.cloudfront.net
```

### Definindo Parâmetros

Você pode definir parâmetros para sua implantação de duas maneiras: usando `cdk.json` ou usando o arquivo `parameter.ts` com tipagem segura.

#### Usando cdk.json (Método Tradicional)

A maneira tradicional de configurar parâmetros é editando o arquivo `cdk.json`. Esta abordagem é simples mas não possui verificação de tipos:

```json
{
  "app": "npx ts-node --prefer-ts-exts bin/bedrock-chat.ts",
  "context": {
    "bedrockRegion": "us-east-1",
    "allowedIpV4AddressRanges": ["0.0.0.0/1", "128.0.0.0/1"],
    "selfSignUpEnabled": true,
    "globalAvailableModels": [
      "claude-v3.7-sonnet",
      "claude-v3.5-sonnet",
      "amazon-nova-pro",
      "amazon-nova-lite",
      "llama3-3-70b-instruct"
    ],
  }
}
```

#### Usando parameter.ts (Método Recomendado com Tipagem Segura)

Para melhor segurança de tipos e experiência do desenvolvedor, você pode usar o arquivo `parameter.ts` para definir seus parâmetros:

```typescript
// Define parâmetros para o ambiente padrão
bedrockChatParams.set("default", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["192.168.0.0/16"],
  selfSignUpEnabled: true,
  globalAvailableModels: [
      "claude-v3.7-sonnet",
      "claude-v3.5-sonnet",
      "amazon-nova-pro",
      "amazon-nova-lite",
      "llama3-3-70b-instruct"
    ],
});

// Define parâmetros para ambientes adicionais
bedrockChatParams.set("dev", {
  bedrockRegion: "us-west-2",
  allowedIpV4AddressRanges: ["10.0.0.0/8"],
  enableRagReplicas: false, // Economia de custos para ambiente dev
  enableBotStoreReplicas: false, // Economia de custos para ambiente dev
});

bedrockChatParams.set("prod", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["172.16.0.0/12"],
  enableLambdaSnapStart: true,
  enableRagReplicas: true, // Disponibilidade aprimorada para produção
  enableBotStoreReplicas: true, // Disponibilidade aprimorada para produção
});
```

> [!Note]
> Usuários existentes podem continuar usando `cdk.json` sem alterações. A abordagem `parameter.ts` é recomendada para novas implantações ou quando você precisa gerenciar múltiplos ambientes.

### Implantando Múltiplos Ambientes

Você pode implantar múltiplos ambientes do mesmo código-fonte usando o arquivo `parameter.ts` e a opção `-c envName`.

#### Pré-requisitos

1. Defina seus ambientes em `parameter.ts` como mostrado acima
2. Cada ambiente terá seu próprio conjunto de recursos com prefixos específicos do ambiente

#### Comandos de Implantação

Para implantar um ambiente específico:

```bash
# Implantar o ambiente dev
npx cdk deploy --all -c envName=dev

# Implantar o ambiente prod
npx cdk deploy --all -c envName=prod
```

Se nenhum ambiente for especificado, o ambiente "default" é usado:

```bash
# Implantar o ambiente padrão
npx cdk deploy --all
```

#### Notas Importantes

1. **Nomenclatura de Stacks**:

   - As stacks principais para cada ambiente terão prefixo com o nome do ambiente (ex: `dev-BedrockChatStack`, `prod-BedrockChatStack`)
   - No entanto, stacks de bot personalizadas (`BrChatKbStack*`) e stacks de publicação de API (`ApiPublishmentStack*`) não recebem prefixos de ambiente pois são criadas dinamicamente em tempo de execução

2. **Nomenclatura de Recursos**:

   - Apenas alguns recursos recebem prefixos de ambiente em seus nomes (ex: tabela `dev_ddb_export`, `dev-FrontendWebAcl`)
   - A maioria dos recursos mantém seus nomes originais mas são isolados por estarem em stacks diferentes

3. **Identificação de Ambiente**:

   - Todos os recursos são marcados com uma tag `CDKEnvironment` contendo o nome do ambiente
   - Você pode usar esta tag para identificar a qual ambiente um recurso pertence
   - Exemplo: `CDKEnvironment: dev` ou `CDKEnvironment: prod`

4. **Substituição do Ambiente Padrão**: Se você definir um ambiente "default" em `parameter.ts`, ele substituirá as configurações em `cdk.json`. Para continuar usando `cdk.json`, não defina um ambiente "default" em `parameter.ts`.

5. **Requisitos de Ambiente**: Para criar ambientes diferentes de "default", você deve usar `parameter.ts`. A opção `-c envName` sozinha não é suficiente sem as definições correspondentes de ambiente.

6. **Isolamento de Recursos**: Cada ambiente cria seu próprio conjunto de recursos, permitindo que você tenha ambientes de desenvolvimento, teste e produção na mesma conta AWS sem conflitos.

## Outros

Você pode definir parâmetros para sua implantação de duas maneiras: usando `cdk.json` ou usando o arquivo `parameter.ts` com segurança de tipos.

#### Usando cdk.json (Método Tradicional)

A maneira tradicional de configurar parâmetros é editando o arquivo `cdk.json`. Esta abordagem é simples, mas não possui verificação de tipos:

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

#### Usando parameter.ts (Método Recomendado com Segurança de Tipos)

Para melhor segurança de tipos e experiência do desenvolvedor, você pode usar o arquivo `parameter.ts` para definir seus parâmetros:

```typescript
// Define parâmetros para o ambiente padrão
bedrockChatParams.set("default", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["192.168.0.0/16"],
  selfSignUpEnabled: true,
});

// Define parâmetros para ambientes adicionais
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

> [!Note]
> Usuários existentes podem continuar usando `cdk.json` sem alterações. A abordagem `parameter.ts` é recomendada para novas implantações ou quando você precisa gerenciar múltiplos ambientes.

### Implantando Múltiplos Ambientes

Você pode implantar múltiplos ambientes do mesmo código-fonte usando o arquivo `parameter.ts` e a opção `-c envName`.

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

Se nenhum ambiente for especificado, o ambiente "default" é usado:

```bash
# Implantar o ambiente padrão
npx cdk deploy --all
```

#### Notas Importantes

1. **Nomenclatura de Stacks**:

   - As stacks principais para cada ambiente terão prefixo com o nome do ambiente (ex: `dev-BedrockChatStack`, `prod-BedrockChatStack`)
   - No entanto, stacks de bot personalizadas (`BrChatKbStack*`) e stacks de publicação de API (`ApiPublishmentStack*`) não recebem prefixos de ambiente, pois são criadas dinamicamente em tempo de execução

2. **Nomenclatura de Recursos**:

   - Apenas alguns recursos recebem prefixos de ambiente em seus nomes (ex: tabela `dev_ddb_export`, `dev-FrontendWebAcl`)
   - A maioria dos recursos mantém seus nomes originais, mas são isolados por estarem em stacks diferentes

3. **Identificação de Ambiente**:

   - Todos os recursos são marcados com uma tag `CDKEnvironment` contendo o nome do ambiente
   - Você pode usar esta tag para identificar a qual ambiente um recurso pertence
   - Exemplo: `CDKEnvironment: dev` ou `CDKEnvironment: prod`

4. **Substituição do Ambiente Padrão**: Se você definir um ambiente "default" em `parameter.ts`, ele substituirá as configurações em `cdk.json`. Para continuar usando `cdk.json`, não defina um ambiente "default" em `parameter.ts`.

5. **Requisitos de Ambiente**: Para criar ambientes diferentes de "default", você deve usar `parameter.ts`. A opção `-c envName` sozinha não é suficiente sem as definições correspondentes de ambiente.

6. **Isolamento de Recursos**: Cada ambiente cria seu próprio conjunto de recursos, permitindo que você tenha ambientes de desenvolvimento, teste e produção na mesma conta AWS sem conflitos.

## Outros

### Remover recursos

Se estiver usando cli e CDK, execute `npx cdk destroy`. Caso contrário, acesse o [CloudFormation](https://console.aws.amazon.com/cloudformation/home) e exclua manualmente `BedrockChatStack` e `FrontendWafStack`. Observe que `FrontendWafStack` está na região `us-east-1`.

### Configurações de Idioma

Este recurso detecta automaticamente o idioma usando [i18next-browser-languageDetector](https://github.com/i18next/i18next-browser-languageDetector). Você pode alternar idiomas pelo menu da aplicação. Alternativamente, você pode usar Query String para definir o idioma conforme mostrado abaixo.

> `https://example.com?lng=ja`

### Desabilitar auto cadastro

Esta amostra tem o auto cadastro habilitado por padrão. Para desabilitar o auto cadastro, abra [cdk.json](./cdk/cdk.json) e altere `selfSignUpEnabled` para `false`. Se você configurar um [provedor de identidade externo](#external-identity-provider), o valor será ignorado e automaticamente desabilitado.

### Restringir Domínios para E-mails de Cadastro

Por padrão, esta amostra não restringe os domínios para e-mails de cadastro. Para permitir cadastros apenas de domínios específicos, abra `cdk.json` e especifique os domínios como uma lista em `allowedSignUpEmailDomains`.

```ts
"allowedSignUpEmailDomains": ["example.com"],
```

### Provedor de Identidade Externo

Esta amostra suporta provedor de identidade externo. Atualmente suportamos [Google](./idp/SET_UP_GOOGLE_pt-BR.md) e [provedor OIDC personalizado](./idp/SET_UP_CUSTOM_OIDC_pt-BR.md).

### WAF Frontend Opcional

Para distribuições CloudFront, os WebACLs do AWS WAF devem ser criados na região us-east-1. Em algumas organizações, a criação de recursos fora da região principal é restrita por política. Em tais ambientes, a implantação do CDK pode falhar ao tentar provisionar o Frontend WAF em us-east-1.

Para acomodar essas restrições, o stack do Frontend WAF é opcional. Quando desabilitado, a distribuição CloudFront é implantada sem um WebACL. Isso significa que você não terá controles de permissão/negação de IP na borda frontend. Autenticação e todos os outros controles da aplicação continuam funcionando normalmente. Observe que esta configuração afeta apenas o Frontend WAF (escopo CloudFront); o WAF da API Publicada (regional) permanece inalterado.

Para desabilitar o Frontend WAF, defina o seguinte em `parameter.ts` (Método Recomendado com Type-Safe):

```ts
bedrockChatParams.set("default", {
  enableFrontendWaf: false
});
```

Ou se estiver usando o legado `cdk/cdk.json`, defina o seguinte:

```json
"enableFrontendWaf": false
```

### Adicionar novos usuários a grupos automaticamente

Esta amostra tem os seguintes grupos para dar permissões aos usuários:

- [`Admin`](./ADMINISTRATOR_pt-BR.md)
- [`CreatingBotAllowed`](#bot-personalization)
- [`PublishAllowed`](./PUBLISH_API_pt-BR.md)

Se você quiser que os usuários recém-criados entrem automaticamente em grupos, você pode especificá-los em [cdk.json](./cdk/cdk.json).

```json
"autoJoinUserGroups": ["CreatingBotAllowed"],
```

Por padrão, os usuários recém-criados serão adicionados ao grupo `CreatingBotAllowed`.

### Configurar Réplicas RAG

`enableRagReplicas` é uma opção em [cdk.json](./cdk/cdk.json) que controla as configurações de réplica para o banco de dados RAG, especificamente as Bases de Conhecimento usando Amazon OpenSearch Serverless.

- **Padrão**: true
- **true**: Melhora a disponibilidade habilitando réplicas adicionais, tornando-o adequado para ambientes de produção, mas aumentando os custos.
- **false**: Reduz custos usando menos réplicas, tornando-o adequado para desenvolvimento e testes.

Esta é uma configuração em nível de conta/região, afetando toda a aplicação em vez de bots individuais.

> [!Note]
> A partir de junho de 2024, o Amazon OpenSearch Serverless suporta 0,5 OCU, reduzindo os custos iniciais para cargas de trabalho em pequena escala. Implantações de produção podem começar com 2 OCUs, enquanto cargas de trabalho de dev/teste podem usar 1 OCU. O OpenSearch Serverless escala automaticamente com base nas demandas da carga de trabalho. Para mais detalhes, visite o [anúncio](https://aws.amazon.com/jp/about-aws/whats-new/2024/06/amazon-opensearch-serverless-entry-cost-half-collection-types/).

### Configurar Bot Store

O recurso de bot store permite que os usuários compartilhem e descubram bots personalizados. Você pode configurar a bot store através das seguintes configurações em [cdk.json](./cdk/cdk.json):

```json
{
  "context": {
    "enableBotStore": true,
    "enableBotStoreReplicas": false,
    "botStoreLanguage": "en"
  }
}
```

- **enableBotStore**: Controla se o recurso de bot store está habilitado (padrão: `true`)
- **botStoreLanguage**: Define o idioma principal para busca e descoberta de bots (padrão: `"en"`). Isso afeta como os bots são indexados e pesquisados na bot store, otimizando a análise de texto para o idioma especificado.
- **enableBotStoreReplicas**: Controla se as réplicas em standby estão habilitadas para a coleção OpenSearch Serverless usada pela bot store (padrão: `false`). Definir como `true` melhora a disponibilidade mas aumenta os custos, enquanto `false` reduz os custos mas pode afetar a disponibilidade.
  > **Importante**: Você não pode atualizar esta propriedade depois que a coleção já foi criada. Se você tentar modificar esta propriedade, a coleção continuará usando o valor original.

### Inferência Cross-region e Global

[Inferência Cross-region e Global](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html)
permite que o Amazon Bedrock roteie dinamicamente solicitações de inferência de modelo entre
múltiplas regiões AWS, melhorando a taxa de transferência e resiliência durante períodos
de pico de demanda. A inferência global roteia as solicitações para a região ideal com base em
latência e disponibilidade em qualquer lugar do mundo, enquanto a inferência cross-region roteia
solicitações dentro da mesma região AWS, por exemplo, dentro dos EUA. Algumas
SCPs podem restringir uma ou outra ou ambas e, portanto, você pode configurá-las
independentemente. Por padrão, ambas estão habilitadas.

Para configurar, altere as seguintes configurações em `cdk.json` ou `parameters.ts`:

```json
"enableBedrockGlobalInference": false,
"enableBedrockCrossRegionInference": false,
```

### Lambda SnapStart

[Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html) melhora os tempos de inicialização a frio para funções Lambda, fornecendo tempos de resposta mais rápidos para uma melhor experiência do usuário. Por outro lado, para funções Python, há uma [cobrança dependendo do tamanho do cache](https://aws.amazon.com/lambda/pricing/#SnapStart_Pricing) e [não está disponível em algumas regiões](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions) atualmente. Para desabilitar o SnapStart, edite `cdk.json`.

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

- `alternateDomainName`: O nome de domínio personalizado para sua aplicação de chat (ex: chat.example.com)
- `hostedZoneId`: O ID da sua zona hospedada no Route 53 onde os registros de domínio serão criados

Quando estes parâmetros são fornecidos, a implantação irá automaticamente:

- Criar um certificado ACM com validação DNS na região us-east-1
- Criar os registros DNS necessários em sua zona hospedada do Route 53
- Configurar o CloudFront para usar seu domínio personalizado

> [!Note]
> O domínio deve ser gerenciado pelo Route 53 em sua conta AWS. O ID da zona hospedada pode ser encontrado no console do Route 53.

### Configurar países permitidos (restrição geográfica)

Você pode restringir o acesso ao Bedrock-Chat com base no país de onde o cliente está acessando.
Use o parâmetro `allowedCountries` em [cdk.json](./cdk/cdk.json) que aceita uma lista de [Códigos de País ISO-3166](https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes).
Por exemplo, uma empresa baseada na Nova Zelândia pode decidir que apenas endereços IP da Nova Zelândia (NZ) e Austrália (AU) podem acessar o portal e todos os outros devem ter o acesso negado.
Para configurar este comportamento, use a seguinte configuração em [cdk.json](./cdk/cdk.json):

```json
{
  "allowedCountries": ["NZ", "AU"]
}
```

Ou, usando `parameter.ts` (Método Recomendado com Type-Safe):

```ts
// Define parâmetros para o ambiente padrão
bedrockChatParams.set("default", {
  allowedCountries: ["NZ", "AU"],
});
```

### Desabilitar suporte a IPv6

O frontend recebe endereços IP e IPv6 por padrão. Em algumas circunstâncias
raras, você pode precisar desabilitar explicitamente o suporte a IPv6. Para fazer isso, defina
o seguinte parâmetro em [parameter.ts](./cdk/parameter.ts) ou similarmente em [cdk.json](./cdk/cdk.json):

```ts
"enableFrontendIpv6": false
```

Se não for definido, o suporte a IPv6 será habilitado por padrão.

### Desenvolvimento Local

Veja [LOCAL DEVELOPMENT](./LOCAL_DEVELOPMENT_pt-BR.md).

### Contribuição

Obrigado por considerar contribuir com este repositório! Aceitamos correções de bugs, traduções de idiomas (i18n), melhorias de recursos, [ferramentas de agente](./docs/AGENT.md#how-to-develop-your-own-tools) e outras melhorias.

Para melhorias de recursos e outras melhorias, **antes de criar um Pull Request, agradecemos muito se você puder criar uma Issue de Solicitação de Recurso para discutir a abordagem e os detalhes da implementação. Para correções de bugs e traduções de idiomas (i18n), prossiga criando um Pull Request diretamente.**

Por favor, também dê uma olhada nas seguintes diretrizes antes de contribuir:

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

Esta biblioteca está licenciada sob a Licença MIT-0. Consulte [o arquivo LICENSE](./LICENSE).