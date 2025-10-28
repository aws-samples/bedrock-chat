# Guia de Migração (v2 para v3)

## TL;DR

- V3 introduz controle de permissões granular e funcionalidade de Bot Store, exigindo mudanças no esquema do DynamoDB
- **Faça backup da sua ConversationTable do DynamoDB antes da migração**
- Atualize a URL do seu repositório de `bedrock-claude-chat` para `bedrock-chat`
- Execute o script de migração para converter seus dados para o novo esquema
- Todos os seus bots e conversas serão preservados com o novo modelo de permissões
- **IMPORTANTE: Durante o processo de migração, a aplicação ficará indisponível para todos os usuários até que a migração seja concluída. Este processo geralmente leva cerca de 60 minutos, dependendo da quantidade de dados e do desempenho do seu ambiente de desenvolvimento.**
- **IMPORTANTE: Todas as APIs Publicadas devem ser excluídas durante o processo de migração.**
- **AVISO: O processo de migração não pode garantir 100% de sucesso para todos os bots. Por favor, documente suas configurações importantes de bot antes da migração caso precise recriá-las manualmente**

## Introdução

### O que há de novo no V3

O V3 introduz melhorias significativas ao Bedrock Chat:

1. **Controle de permissão granular**: Controle o acesso aos seus bots com permissões baseadas em grupos de usuários
2. **Loja de Bots**: Compartilhe e descubra bots através de um marketplace centralizado
3. **Recursos administrativos**: Gerencie APIs, marque bots como essenciais e analise o uso dos bots

Estes novos recursos exigiram mudanças no esquema do DynamoDB, necessitando um processo de migração para usuários existentes.

### Por que esta migração é necessária

O novo modelo de permissões e a funcionalidade da Loja de Bots exigiram a reestruturação da forma como os dados dos bots são armazenados e acessados. O processo de migração converte seus bots e conversas existentes para o novo esquema enquanto preserva todos os seus dados.

> [!WARNING]
> Aviso de Interrupção do Serviço: **Durante o processo de migração, a aplicação ficará indisponível para todos os usuários.** Planeje realizar esta migração durante uma janela de manutenção quando os usuários não precisarem acessar o sistema. A aplicação só voltará a ficar disponível após o script de migração ter sido concluído com sucesso e todos os dados terem sido devidamente convertidos para o novo esquema. Este processo geralmente leva cerca de 60 minutos, dependendo da quantidade de dados e do desempenho do seu ambiente de desenvolvimento.

> [!IMPORTANT]
> Antes de prosseguir com a migração: **O processo de migração não pode garantir 100% de sucesso para todos os bots**, especialmente aqueles criados com versões mais antigas ou com configurações personalizadas. Por favor, documente suas configurações importantes de bot (instruções, fontes de conhecimento, configurações) antes de iniciar o processo de migração caso você precise recriá-las manualmente.

## Processo de Migração

### Aviso Importante Sobre a Visibilidade dos Bots no V3

No V3, **todos os bots v2 com compartilhamento público habilitado serão pesquisáveis na Bot Store.** Se você tiver bots contendo informações sensíveis que não deseja que sejam descobertos, considere torná-los privados antes de migrar para o V3.

### Passo 1: Identificar o nome do seu ambiente

Neste procedimento, `{YOUR_ENV_PREFIX}` é especificado para identificar o nome das suas Stacks do CloudFormation. Se você estiver usando o recurso [Implantando Múltiplos Ambientes](../../README.md#deploying-multiple-environments), substitua pelo nome do ambiente a ser migrado. Caso contrário, substitua por uma string vazia.

### Passo 2: Atualizar URL do Repositório (Recomendado)

O repositório foi renomeado de `bedrock-claude-chat` para `bedrock-chat`. Atualize seu repositório local:

```bash
# Verifique sua URL remota atual
git remote -v

# Atualize a URL remota
git remote set-url origin https://github.com/aws-samples/bedrock-chat.git

# Verifique a alteração
git remote -v
```

### Passo 3: Certifique-se de Estar na Última Versão V2

> [!WARNING]
> Você DEVE atualizar para v2.10.0 antes de migrar para o V3. **Pular esta etapa pode resultar em perda de dados durante a migração.**

Antes de iniciar a migração, certifique-se de estar executando a última versão do V2 (**v2.10.0**). Isso garante que você tenha todas as correções de bugs e melhorias necessárias antes de atualizar para o V3:

```bash
# Busque as últimas tags
git fetch --tags

# Faça checkout da última versão V2
git checkout v2.10.0

# Implante a última versão V2
cd cdk
npm ci
npx cdk deploy --all
```

### Passo 4: Registre o Nome da Sua Tabela DynamoDB V2

Obtenha o nome da ConversationTable V2 das saídas do CloudFormation:

```bash
# Obtenha o nome da ConversationTable V2
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='ConversationTableName'].OutputValue" \
  --stack-name {YOUR_ENV_PREFIX}BedrockChatStack
```

Certifique-se de salvar este nome da tabela em um local seguro, pois você precisará dele para o script de migração posteriormente.

### Passo 5: Faça Backup da Sua Tabela DynamoDB

Antes de prosseguir, crie um backup da sua ConversationTable do DynamoDB usando o nome que você acabou de registrar:

```bash
# Crie um backup da sua tabela V2
aws dynamodb create-backup \
  --no-cli-pager \
  --backup-name "BedrockChatV2Backup-$(date +%Y%m%d)" \
  --table-name YOUR_V2_CONVERSATION_TABLE_NAME

# Verifique se o status do backup está disponível
aws dynamodb describe-backup \
  --no-cli-pager \
  --query BackupDescription.BackupDetails \
  --backup-arn YOUR_BACKUP_ARN
```

### Passo 6: Exclua Todas as APIs Publicadas

> [!IMPORTANT]
> Antes de implantar o V3, você deve excluir todas as APIs publicadas para evitar conflitos de valores de saída do Cloudformation durante o processo de atualização.

1. Faça login em sua aplicação como administrador
2. Navegue até a seção Admin e selecione "API Management"
3. Revise a lista de todas as APIs publicadas
4. Exclua cada API publicada clicando no botão de exclusão ao lado dela

Você pode encontrar mais informações sobre publicação e gerenciamento de APIs na documentação [PUBLISH_API.md](../PUBLISH_API_pt-BR.md), [ADMINISTRATOR.md](../ADMINISTRATOR_pt-BR.md) respectivamente.

### Passo 7: Baixe o V3 e Implante

Baixe o código mais recente do V3 e implante:

```bash
git fetch
git checkout v3
cd cdk
npm ci
npx cdk deploy --all
```

> [!IMPORTANT]
> Depois de implantar o V3, a aplicação ficará indisponível para todos os usuários até que o processo de migração seja concluído. O novo esquema é incompatível com o formato de dados antigo, então os usuários não poderão acessar seus bots ou conversas até que você complete o script de migração nas próximas etapas.

### Passo 8: Registre os Nomes das Suas Tabelas DynamoDB V3

Após implantar o V3, você precisa obter os nomes da nova ConversationTable e BotTable:

```bash
# Obtenha o nome da ConversationTable V3
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='ConversationTableNameV3'].OutputValue" \
  --stack-name {YOUR_ENV_PREFIX}BedrockChatStack

# Obtenha o nome da BotTable V3
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='BotTableNameV3'].OutputValue" \
  --stack-name {YOUR_ENV_PREFIX}BedrockChatStack
```

> [!Important]
> Certifique-se de salvar estes nomes das tabelas V3 junto com o nome da sua tabela V2 previamente salvo, pois você precisará de todos eles para o script de migração.

### Passo 9: Execute o Script de Migração

O script de migração irá converter seus dados V2 para o esquema V3. Primeiro, edite o script de migração `docs/migration/migrate_v2_v3.py` para definir seus nomes de tabelas e região:

```python
# Região onde o dynamodb está localizado
REGION = "ap-northeast-1" # Substitua pela sua região

V2_CONVERSATION_TABLE = "BedrockChatStack-DatabaseConversationTableXXXX" # Substitua pelo valor registrado no Passo 4
V3_CONVERSATION_TABLE = "BedrockChatStack-DatabaseConversationTableV3XXXX" # Substitua pelo valor registrado no Passo 8
V3_BOT_TABLE = "BedrockChatStack-DatabaseBotTableV3XXXXX" # Substitua pelo valor registrado no Passo 8
```

Em seguida, execute o script usando Poetry do diretório backend:

> [!NOTE]
> A versão dos requisitos Python foi alterada para 3.13.0 ou posterior (Possivelmente alterada em desenvolvimento futuro. Veja pyproject.toml). Se você tiver o venv instalado com uma versão diferente do Python, precisará removê-lo uma vez.

```bash
# Navegue até o diretório backend
cd backend

# Instale as dependências se ainda não tiver feito
poetry install

# Execute primeiro uma simulação para ver o que seria migrado
poetry run python ../docs/migration/migrate_v2_v3.py --dry-run

# Se tudo parecer correto, execute a migração real
poetry run python ../docs/migration/migrate_v2_v3.py

# Verifique se a migração foi bem-sucedida
poetry run python ../docs/migration/migrate_v2_v3.py --verify-only
```

O script de migração irá gerar um arquivo de relatório em seu diretório atual com detalhes sobre o processo de migração. Verifique este arquivo para garantir que todos os seus dados foram migrados corretamente.

#### Lidando com Grandes Volumes de Dados

Para ambientes com usuários intensivos ou grandes quantidades de dados, considere estas abordagens:

1. **Migre usuários individualmente**: Para usuários com grandes volumes de dados, migre-os um por vez:

   ```bash
   poetry run python ../docs/migration/migrate_v2_v3.py --users user-id-1 user-id-2
   ```

2. **Considerações de memória**: O processo de migração carrega dados na memória. Se você encontrar erros de Falta de Memória (OOM), tente:

   - Migrar um usuário por vez
   - Executar a migração em uma máquina com mais memória
   - Dividir a migração em lotes menores de usuários

3. **Monitore a migração**: Verifique os arquivos de relatório gerados para garantir que todos os dados sejam migrados corretamente, especialmente para grandes conjuntos de dados.

### Passo 10: Verifique a Aplicação

Após a migração, abra sua aplicação e verifique:

- Todos os seus bots estão disponíveis
- As conversas foram preservadas
- Os novos controles de permissão estão funcionando

### Limpeza (Opcional)

Depois de confirmar que a migração foi bem-sucedida e todos os seus dados estão adequadamente acessíveis no V3, você pode opcionalmente excluir a tabela de conversas V2 para economizar custos:

```bash
# Exclua a tabela de conversas V2 (SOMENTE após confirmar a migração bem-sucedida)
aws dynamodb delete-table --table-name YOUR_V2_CONVERSATION_TABLE_NAME
```

> [!IMPORTANT]
> Exclua a tabela V2 apenas após verificar minuciosamente que todos os seus dados importantes foram migrados com sucesso para o V3. Recomendamos manter o backup criado no Passo 2 por pelo menos algumas semanas após a migração, mesmo que você exclua a tabela original.

## FAQ V3

### Acesso e Permissões do Bot

**P: O que acontece se um bot que estou usando for excluído ou minha permissão de acesso for removida?**
R: A autorização é verificada no momento do chat, então você perderá o acesso imediatamente.

**P: O que acontece se um usuário for excluído (ex: funcionário que saiu)?**
R: Seus dados podem ser completamente removidos deletando todos os itens do DynamoDB que tenham seu ID de usuário como chave de partição (PK).

**P: Posso desativar o compartilhamento de um bot público essencial?**
R: Não, o administrador deve primeiro marcar o bot como não essencial antes de desativar o compartilhamento.

**P: Posso excluir um bot público essencial?**
R: Não, o administrador deve primeiro marcar o bot como não essencial antes de excluí-lo.

### Segurança e Implementação

**P: A segurança em nível de linha (RLS) está implementada para a tabela de bots?**
R: Não, considerando a diversidade de padrões de acesso. A autorização é realizada ao acessar os bots, e o risco de vazamento de metadados é considerado mínimo comparado ao histórico de conversas.

**P: Quais são os requisitos para publicar uma API?**
R: O bot deve ser público.

**P: Haverá uma tela de gerenciamento para todos os bots privados?**
R: Não na versão inicial V3. No entanto, os itens ainda podem ser excluídos consultando o ID do usuário conforme necessário.

**P: Haverá funcionalidade de marcação de bots para melhor UX de busca?**
R: Não na versão inicial V3, mas marcação automática baseada em LLM pode ser adicionada em atualizações futuras.

### Administração

**P: O que os administradores podem fazer?**
R: Os administradores podem:

- Gerenciar bots públicos (incluindo verificação de bots de alto custo)
- Gerenciar APIs
- Marcar bots públicos como essenciais

**P: Posso tornar bots parcialmente compartilhados como essenciais?**
R: Não, apenas suporte a bots públicos.

**P: Posso definir prioridade para bots fixados?**
R: Na versão inicial, não.

### Configuração de Autorização

**P: Como configuro a autorização?**
R:

1. Abra o console do Amazon Cognito e crie grupos de usuários no pool de usuários do BrChat
2. Adicione usuários a esses grupos conforme necessário
3. No BrChat, selecione os grupos de usuários que você deseja permitir acesso ao configurar as configurações de compartilhamento do bot

Nota: Alterações na associação do grupo requerem novo login para ter efeito. As alterações são refletidas na atualização do token, mas não durante o período de validade do token ID (padrão de 30 minutos no V3, configurável por `tokenValidMinutes` em `cdk.json` ou `parameter.ts`).

**P: O sistema verifica com o Cognito toda vez que um bot é acessado?**
R: Não, a autorização é verificada usando o token JWT para evitar operações de E/S desnecessárias.

### Funcionalidade de Busca

**P: A busca de bot suporta busca semântica?**
R: Não, apenas correspondência parcial de texto é suportada. Busca semântica (ex: "automóvel" → "carro", "VE", "veículo") não está disponível devido às atuais restrições do OpenSearch Serverless (Mar 2025).