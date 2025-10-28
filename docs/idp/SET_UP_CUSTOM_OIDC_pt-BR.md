# Configurar provedor de identidade externo

## Passo 1: Criar um Cliente OIDC

Siga os procedimentos para o provedor OIDC de destino e anote os valores do ID do cliente OIDC e do segredo. A URL do emissor também é necessária nas etapas seguintes. Se a URI de redirecionamento for necessária durante o processo de configuração, insira um valor temporário, que será substituído após a conclusão da implantação.

## Etapa 2: Armazenar Credenciais no AWS Secrets Manager

1. Acesse o Console de Gerenciamento da AWS.
2. Navegue até o Secrets Manager e escolha "Armazenar um novo segredo".
3. Selecione "Outro tipo de segredos".
4. Insira o ID do cliente e o segredo do cliente como pares de chave-valor.

   - Chave: `clientId`, Valor: <YOUR_GOOGLE_CLIENT_ID>
   - Chave: `clientSecret`, Valor: <YOUR_GOOGLE_CLIENT_SECRET>
   - Chave: `issuerUrl`, Valor: <ISSUER_URL_OF_THE_PROVIDER>

5. Siga as instruções para nomear e descrever o segredo. Anote o nome do segredo, pois você precisará dele no seu código CDK (Usado na variável da Etapa 3 <YOUR_SECRET_NAME>).
6. Revise e armazene o segredo.

### Atenção

Os nomes das chaves devem corresponder exatamente às strings `clientId`, `clientSecret` e `issuerUrl`.

## Passo 3: Atualizar cdk.json

No seu arquivo cdk.json, adicione o ID Provider e o SecretName ao arquivo cdk.json.

desta forma:

```json
{
  "context": {
    // ...
    "identityProviders": [
      {
        "service": "oidc", // Não altere
        "serviceName": "<SEU_NOME_DE_SERVICO>", // Defina qualquer valor que desejar
        "secretName": "<SEU_NOME_DO_SEGREDO>"
      }
    ],
    "userPoolDomainPrefix": "<PREFIXO_DE_DOMINIO_UNICO_PARA_SEU_POOL_DE_USUARIOS>"
  }
}
```

### Atenção

#### Exclusividade

O `userPoolDomainPrefix` deve ser globalmente único entre todos os usuários do Amazon Cognito. Se você escolher um prefixo que já esteja em uso por outra conta AWS, a criação do domínio do pool de usuários falhará. É uma boa prática incluir identificadores, nomes de projetos ou nomes de ambiente no prefixo para garantir a exclusividade.

## Etapa 4: Implante Sua Stack CDK

Implante sua stack CDK na AWS:

```sh
npx cdk deploy --require-approval never --all
```

## Etapa 5: Atualizar o Cliente OIDC com os URIs de Redirecionamento do Cognito

Após implantar a stack, o `AuthApprovedRedirectURI` é exibido nas saídas do CloudFormation. Volte para sua configuração OIDC e atualize com os URIs de redirecionamento corretos.