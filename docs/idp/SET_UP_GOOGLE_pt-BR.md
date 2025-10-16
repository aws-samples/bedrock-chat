# Configurar provedor de identidade externo para o Google

## Passo 1: Criar um Cliente OAuth 2.0 do Google

1. Acesse o Console de Desenvolvedor do Google.
2. Crie um novo projeto ou selecione um existente.
3. Navegue até "Credenciais", clique em "Criar Credenciais" e escolha "ID do cliente OAuth".
4. Configure a tela de consentimento se solicitado.
5. Para o tipo de aplicação, selecione "Aplicação Web".
6. Deixe o URI de redirecionamento em branco por enquanto para configurá-lo depois.[Veja o Passo 5](#step-5-update-google-oauth-client-with-cognito-redirect-uris)
7. Após criar, anote o ID do Cliente e o Segredo do Cliente.

Para mais detalhes, visite [documento oficial do Google](https://support.google.com/cloud/answer/6158849?hl=en)

## Etapa 2: Armazenar Credenciais do Google OAuth no AWS Secrets Manager

1. Acesse o Console de Gerenciamento da AWS.
2. Navegue até o Secrets Manager e escolha "Armazenar um novo segredo".
3. Selecione "Outro tipo de segredos".
4. Insira o clientId e clientSecret do Google OAuth como pares de chave-valor.

   1. Chave: clientId, Valor: <YOUR_GOOGLE_CLIENT_ID>
   2. Chave: clientSecret, Valor: <YOUR_GOOGLE_CLIENT_SECRET>

5. Siga as instruções para nomear e descrever o segredo. Anote o nome do segredo, pois você precisará dele no seu código CDK. Por exemplo, googleOAuthCredentials. (Use na Etapa 3 o nome da variável <YOUR_SECRET_NAME>)
6. Revise e armazene o segredo.

### Atenção

Os nomes das chaves devem corresponder exatamente às strings 'clientId' e 'clientSecret'.

## Etapa 3: Atualizar cdk.json

No seu arquivo cdk.json, adicione o Provedor de ID e o SecretName ao arquivo cdk.json.

desta forma:

```json
{
  "context": {
    // ...
    "identityProviders": [
      {
        "service": "google",
        "secretName": "<YOUR_SECRET_NAME>"
      }
    ],
    "userPoolDomainPrefix": "<UNIQUE_DOMAIN_PREFIX_FOR_YOUR_USER_POOL>"
  }
}
```

### Atenção

#### Exclusividade

O userPoolDomainPrefix deve ser globalmente único entre todos os usuários do Amazon Cognito. Se você escolher um prefixo que já está em uso por outra conta AWS, a criação do domínio do grupo de usuários falhará. É uma boa prática incluir identificadores, nomes de projetos ou nomes de ambiente no prefixo para garantir a exclusividade.

## Etapa 4: Implante Sua Stack CDK

Implante sua stack CDK na AWS:

```sh
npx cdk deploy --require-approval never --all
```

## Passo 5: Atualizar o Cliente OAuth do Google com as URIs de Redirecionamento do Cognito

Após implantar a stack, o AuthApprovedRedirectURI é exibido nas saídas do CloudFormation. Volte ao Console de Desenvolvedor do Google e atualize o cliente OAuth com as URIs de redirecionamento corretas.