# Guia de Migração (v0 para v1)

Se você já utiliza o Bedrock Chat com uma versão anterior (~`0.4.x`), precisará seguir os passos abaixo para migrar.

## Por que preciso fazer isso?

Esta grande atualização inclui importantes atualizações de segurança.

- O armazenamento do banco de dados vetorial (ou seja, pgvector no Aurora PostgreSQL) agora está criptografado, o que aciona uma substituição quando implantado. Isso significa que os itens vetoriais existentes serão excluídos.
- Introduzimos o grupo de usuários do Cognito `CreatingBotAllowed` para limitar os usuários que podem criar bots. Os usuários existentes atuais não estão neste grupo, portanto, você precisa anexar a permissão manualmente se quiser que eles tenham recursos de criação de bots. Consulte: [Personalização de Bot](../../README.md#bot-personalization)

## Pré-requisitos

Leia o [Guia de Migração de Banco de Dados](./DATABASE_MIGRATION_pt-BR.md) e determine o método para restaurar itens.

## Etapas

### Migração do armazenamento de vetores

- Abra o terminal e navegue até o diretório do projeto
- Faça pull do branch que deseja implantar. A seguir, mude para o branch desejado (neste caso, `v1`) e faça pull das últimas alterações:

```sh
git fetch
git checkout v1
git pull origin v1
```

- Se desejar restaurar itens com DMS, NÃO ESQUEÇA de desabilitar a rotação de senha e anote a senha para acessar o banco de dados. Se estiver restaurando com o script de migração([migrate_v0_v1.py](./migrate_v0_v1.py)), não é necessário anotar a senha.
- Remova todas as [APIs publicadas](../PUBLISH_API_pt-BR.md) para que o CloudFormation possa remover o cluster Aurora existente.
- Execute [npx cdk deploy](../README.md#deploy-using-cdk) que aciona a substituição do cluster Aurora e EXCLUI TODOS OS ITENS DE VETOR.
- Siga o [Guia de Migração de Banco de Dados](./DATABASE_MIGRATION_pt-BR.md) para restaurar itens de vetor.
- Verifique se o usuário pode utilizar os bots existentes que possuem conhecimento, ou seja, bots RAG.

### Anexar permissão CreatingBotAllowed

- Após a implantação, todos os usuários ficarão impossibilitados de criar novos bots.
- Se quiser que usuários específicos possam criar bots, adicione esses usuários ao grupo `CreatingBotAllowed` usando o console de gerenciamento ou CLI.
- Verifique se o usuário pode criar um bot. Observe que os usuários precisam fazer login novamente.