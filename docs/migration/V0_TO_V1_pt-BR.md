# Guia de Migração (v0 para v1)

Se você já usa o Bedrock Chat com uma versão anterior (~`0.4.x`), você precisa seguir os passos abaixo para migrar.

## Por que preciso fazer isso?

Esta atualização importante inclui atualizações de segurança essenciais.

- O armazenamento do banco de dados vetorial (ou seja, pgvector no Aurora PostgreSQL) agora está criptografado, o que aciona uma substituição quando implantado. Isso significa que os itens vetoriais existentes serão excluídos.
- Introduzimos o grupo de usuários Cognito `CreatingBotAllowed` para limitar os usuários que podem criar bots. Os usuários existentes atualmente não estão neste grupo, então você precisa anexar a permissão manualmente se quiser que eles tenham capacidades de criação de bots. Veja: [Personalização de Bot](../../README.md#bot-personalization)

## Pré-requisitos

Leia o [Guia de Migração de Banco de Dados](./DATABASE_MIGRATION_pt-BR.md) e determine o método para restauração dos itens.

## Etapas

### Migração do armazenamento de vetores

- Abra seu terminal e navegue até o diretório do projeto
- Faça o pull da branch que você deseja implantar. A seguir, vá para a branch desejada (neste caso, `v1`) e faça pull das últimas alterações:

```sh
git fetch
git checkout v1
git pull origin v1
```

- Se você deseja restaurar itens com DMS, NÃO SE ESQUEÇA de desabilitar a rotação de senha e anotar a senha para acessar o banco de dados. Se estiver restaurando com o script de migração ([migrate_v0_v1.py](./migrate_v0_v1.py)), você não precisa anotar a senha.
- Remova todas as [APIs publicadas](../PUBLISH_API_pt-BR.md) para que o CloudFormation possa remover o cluster Aurora existente.
- Execute [npx cdk deploy](../README.md#deploy-using-cdk) para acionar a substituição do cluster Aurora e DELETAR TODOS OS ITENS VETORIAIS.
- Siga o [Guia de Migração de Banco de Dados](./DATABASE_MIGRATION_pt-BR.md) para restaurar os itens vetoriais.
- Verifique se o usuário pode utilizar os bots existentes que possuem conhecimento, ou seja, bots RAG.

### Anexar permissão CreatingBotAllowed

- Após a implantação, todos os usuários ficarão impossibilitados de criar novos bots.
- Se você quiser que usuários específicos possam criar bots, adicione esses usuários ao grupo `CreatingBotAllowed` usando o console de gerenciamento ou CLI.
- Verifique se o usuário pode criar um bot. Observe que os usuários precisam fazer login novamente.