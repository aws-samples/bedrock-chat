# Configurar provedor de identidade externo para o Google

## Etapa 1: Criar um Cliente OAuth 2.0 do Google

1. Acesse o Console de Desenvolvedores do Google.
2. Crie um novo projeto ou selecione um existente.
3. Navegue até "Credenciais", depois clique em "Criar Credenciais" e escolha "ID de cliente OAuth".
4. Configure a tela de consentimento se solicitado.
5. Para o tipo de aplicativo, selecione "Aplicativo web".
6. Deixe o URI de redirecionamento em branco por enquanto para definir posteriormente.[Consulte a Etapa 5](#step-5-update-google-oauth-client-with-cognito-redirect-uris)
7. Após a criação, anote o ID do Cliente e o Segredo do Cliente.

Para mais detalhes, visite [documento oficial do Google](https://support.google.com/cloud/answer/6158849?hl=en)

## Etapa 2: Armazenar Credenciais do Google OAuth no AWS Secrets Manager

1. Acesse o Console de Gerenciamento da AWS.
2. Navegue até o Secrets Manager e escolha "Armazenar um novo segredo".
3. Selecione "Outro tipo de segredos".
4. Insira o clientId e o clientSecret do Google OAuth como pares de chave-valor.

   1. Chave: clientId, Valor: <SEU_ID_DE_CLIENTE_GOOGLE>
   2. Chave: clientSecret, Valor: <SEU_SEGREDO_DE_CLIENTE_GOOGLE>

5. Siga os prompts para nomear e descrever o segredo. Anote o nome do segredo, pois você precisará dele no seu código CDK. Por exemplo, googleOAuthCredentials. (Use na Etapa 3 o nome da variável <SEU_NOME_DO_SEGREDO>)
6. Revise e armazene o segredo.

### Atenção

Os nomes das chaves devem corresponder exatamente às strings 'clientId' e 'clientSecret'.

## Etapa 3: Atualizar cdk.json

No arquivo cdk.json, adicione o Provedor de Identidade e o Nome do Segredo ao arquivo cdk.json.

como no exemplo:

```json
{
  "context": {
    // ...
    "identityProviders": [
      {
        "service": "google",
        "secretName": "<SEU_NOME_DE_SEGREDO>"
      }
    ],
    "userPoolDomainPrefix": "<PREFIXO_DE_DOMÍNIO_ÚNICO_PARA_SEU_USER_POOL>"
  }
}
```

### Atenção

#### Unicidade

O userPoolDomainPrefix deve ser globalmente único em todos os usuários do Amazon Cognito. Se você escolher um prefixo que já esteja em uso por outra conta AWS, a criação do domínio do user pool falhará. É uma boa prática incluir identificadores, nomes de projetos ou nomes de ambientes no prefixo para garantir a unicidade.

## Etapa 4: Implantar Seu Stack CDK

Implante seu stack CDK na AWS:

```sh
npx cdk deploy --require-approval never --all
```

## Etapa 5: Atualizar o Cliente OAuth do Google com URIs de Redirecionamento do Cognito

Após implantar a pilha, AuthApprovedRedirectURI será exibido nas saídas do CloudFormation. Volte para o Console de Desenvolvedores do Google e atualize o cliente OAuth com os URIs de redirecionamento corretos.