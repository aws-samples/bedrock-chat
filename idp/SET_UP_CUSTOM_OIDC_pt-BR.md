# Configurar provedor de identidade externo

## Etapa 1: Criar um Cliente OIDC

Siga os procedimentos para o provedor OIDC de destino e anote os valores do ID do cliente OIDC e do segredo. Além disso, o URL do emissor é necessário nas etapas seguintes. Se um URI de redirecionamento for necessário durante o processo de configuração, insira um valor fictício, que será substituído após a conclusão da implantação.

## Etapa 2: Armazenar Credenciais no AWS Secrets Manager

1. Acesse o Console de Gerenciamento da AWS.
2. Navegue até o Secrets Manager e escolha "Armazenar novo segredo".
3. Selecione "Outro tipo de segredo".
4. Insira o ID do cliente e o segredo do cliente como pares de chave-valor.

   - Chave: `clientId`, Valor: <SEU_ID_DE_CLIENTE_DO_GOOGLE>
   - Chave: `clientSecret`, Valor: <SEU_SEGREDO_DE_CLIENTE_DO_GOOGLE>
   - Chave: `issuerUrl`, Valor: <URL_DO_EMISSOR_DO_PROVEDOR>

5. Siga os prompts para nomear e descrever o segredo. Anote o nome do segredo, pois você precisará dele no seu código CDK (Usado na Etapa 3 no nome da variável <SEU_NOME_DO_SEGREDO>).
6. Revise e armazene o segredo.

### Atenção

Os nomes das chaves devem corresponder exatamente às strings `clientId`, `clientSecret` e `issuerUrl`.

## Etapa 3: Atualizar cdk.json

No arquivo cdk.json, adicione o Provedor de Identidade e o Nome do Segredo ao arquivo cdk.json.

como a seguir:

```json
{
  "context": {
    // ...
    "identityProviders": [
      {
        "service": "oidc", // Não altere
        "serviceName": "<SEU_NOME_DE_SERVIÇO>", // Defina qualquer valor que desejar
        "secretName": "<SEU_NOME_DE_SEGREDO>"
      }
    ],
    "userPoolDomainPrefix": "<PREFIXO_DE_DOMÍNIO_ÚNICO_PARA_SEU_USER_POOL>"
  }
}
```

### Atenção

#### Unicidade

O `userPoolDomainPrefix` deve ser globalmente único em todos os usuários do Amazon Cognito. Se você escolher um prefixo que já está em uso por outra conta AWS, a criação do domínio do user pool falhará. É uma boa prática incluir identificadores, nomes de projetos ou nomes de ambientes no prefixo para garantir a unicidade.

## Etapa 4: Implantar Sua Stack CDK

Implante sua stack CDK na AWS:

```sh
npx cdk deploy --require-approval never --all
```

## Etapa 5: Atualizar Cliente OIDC com URIs de Redirecionamento do Cognito

Após implantar a pilha, `AuthApprovedRedirectURI` estará visível nos resultados do CloudFormation. Volte para sua configuração OIDC e atualize com os URIs de redirecionamento corretos.