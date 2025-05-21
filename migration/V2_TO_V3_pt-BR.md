# Guia de Migração (v2 para v3)

## Resumo Executivo

- A V3 introduz controle de permissões granular e funcionalidade de Loja de Bots, exigindo alterações no esquema do DynamoDB
- **Faça backup da sua ConversationTable do DynamoDB antes da migração**
- Atualize a URL do seu repositório de `bedrock-claude-chat` para `bedrock-chat`
- Execute o script de migração para converter seus dados para o novo esquema
- Todos os seus bots e conversas serão preservados com o novo modelo de permissões
- **IMPORTANTE: Durante o processo de migração, o aplicativo ficará indisponível para todos os usuários até que a migração seja concluída. Este processo normalmente leva cerca de 60 minutos, dependendo da quantidade de dados e do desempenho do seu ambiente de desenvolvimento.**
- **IMPORTANTE: Todas as APIs Publicadas devem ser excluídas durante o processo de migração.**
- **AVISO: O processo de migração não pode garantir 100% de sucesso para todos os bots. Documente as configurações de bots importantes antes da migração, caso precise recriá-los manualmente**

## Introdução

### Novidades na V3

A V3 introduz melhorias significativas no Bedrock Chat:

1. **Controle de permissão granular**: Controle o acesso aos seus bots com permissões baseadas em grupos de usuários
2. **Loja de Bots**: Compartilhe e descubra bots através de um marketplace centralizado
3. **Recursos administrativos**: Gerencie APIs, marque bots como essenciais e analise o uso de bots

Esses novos recursos exigiram alterações no esquema do DynamoDB, necessitando um processo de migração para usuários existentes.

### Por Que Esta Migração É Necessária

O novo modelo de permissões e a funcionalidade da Loja de Bots exigiram uma reestruturação de como os dados de bots são armazenados e acessados. O processo de migração converte seus bots e conversas existentes para o novo esquema, preservando todos os seus dados.

> [!WARNING]
> Aviso de Interrupção de Serviço: **Durante o processo de migração, o aplicativo ficará indisponível para todos os usuários.** Planeje realizar esta migração durante uma janela de manutenção quando os usuários não precisarem acessar o sistema. O aplicativo só ficará disponível novamente após o script de migração ter sido concluído com sucesso e todos os dados terem sido convertidos adequadamente para o novo esquema. Esse processo normalmente leva cerca de 60 minutos, dependendo da quantidade de dados e do desempenho do seu ambiente de desenvolvimento.

> [!IMPORTANT]
> Antes de prosseguir com a migração: **O processo de migração não pode garantir 100% de sucesso para todos os bots**, especialmente aqueles criados com versões mais antigas ou com configurações personalizadas. Documente as configurações importantes dos seus bots (instruções, fontes de conhecimento, configurações) antes de iniciar o processo de migração, caso precise recriá-los manualmente.

## Processo de Migração

### Aviso Importante Sobre a Visibilidade de Bots na V3

Na V3, **todos os bots v2 com compartilhamento público habilitado serão pesquisáveis na Loja de Bots.** Se você tem bots contendo informações sensíveis que não deseja que sejam descobertos, considere torná-los privados antes de migrar para a V3.

### Passo 1: Identificar o nome do seu ambiente

Neste procedimento, `{SEU_PREFIXO_DE_ENV}` é especificado para identificar o nome dos seus CloudFormation Stacks. Se você está usando o recurso de [Implantação de Múltiplos Ambientes](../../README.md#deploying-multiple-environments), substitua pelo nome do ambiente a ser migrado. Se não, substitua por uma string vazia.

### Passo 2: Atualizar URL do Repositório (Recomendado)

O repositório foi renomeado de `bedrock-claude-chat` para `bedrock-chat`. Atualize seu repositório local:

```bash
# Verificar a URL remota atual
git remote -v

# Atualizar a URL remota
git remote set-url origin https://github.com/aws-samples/bedrock-chat.git

# Verificar a mudança
git remote -v
```

### Passo 3: Garantir que Você Está na Última Versão V2

> [!WARNING]
> Você DEVE atualizar para v2.10.0 antes de migrar para V3. **Pular esta etapa pode resultar em perda de dados durante a migração.**

Antes de iniciar a migração, certifique-se de que está executando a versão mais recente da V2 (**v2.10.0**). Isso garante que você tenha todas as correções de bugs e melhorias necessárias antes de atualizar para a V3:

```bash
# Buscar as últimas tags
git fetch --tags

# Fazer checkout da última versão V2
git checkout v2.10.0

# Implantar a última versão V2
cd cdk
npm ci
npx cdk deploy --all
```

### Passo 4: Registrar o Nome da Tabela DynamoDB V2

Obtenha o nome da ConversationTable V2 a partir das saídas do CloudFormation:

```bash
# Obter o nome da ConversationTable V2
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='ConversationTableName'].OutputValue" \
  --stack-name {SEU_PREFIXO_DE_ENV}BedrockChatStack
```

Certifique-se de salvar este nome de tabela em um local seguro, pois você precisará dele para o script de migração posteriormente.

### Passo 5: Fazer Backup da Tabela DynamoDB

Antes de prosseguir, crie um backup da sua ConversationTable DynamoDB usando o nome que acabou de registrar:

```bash
# Criar um backup da tabela V2
aws dynamodb create-backup \
  --no-cli-pager \
  --backup-name "BedrockChatV2Backup-$(date +%Y%m%d)" \
  --table-name SEU_NOME_DE_TABELA_DE_CONVERSAÇÃO_V2

# Verificar se o status do backup está disponível
aws dynamodb describe-backup \
  --no-cli-pager \
  --query BackupDescription.BackupDetails \
  --backup-arn SEU_ARN_DE_BACKUP
```

### Passo 6: Excluir Todas as APIs Publicadas

> [!IMPORTANT]
> Antes de implantar a V3, você deve excluir todas as APIs publicadas para evitar conflitos de valores de saída do Cloudformation durante o processo de atualização.

1. Faça login no seu aplicativo como administrador
2. Navegue até a seção de Administração e selecione "Gerenciamento de API"
3. Revise a lista de todas as APIs publicadas
4. Exclua cada API publicada clicando no botão de exclusão ao lado dela

Você pode encontrar mais informações sobre publicação e gerenciamento de APIs na documentação [PUBLISH_API.md](../PUBLISH_API_pt-BR.md), [ADMINISTRATOR.md](../ADMINISTRATOR_pt-BR.md) respectivamente.

### Passo 7: Puxar V3 e Implantar

Puxe o código V3 mais recente e implante:

```bash
git fetch
git checkout v3
cd cdk
npm ci
npx cdk deploy --all
```

> [!IMPORTANT]
> Após implantar a V3, o aplicativo ficará indisponível para todos os usuários até que o processo de migração seja concluído. O novo esquema é incompatível com o formato de dados antigo, portanto, os usuários não poderão acessar seus bots ou conversas até que você conclua o script de migração nas próximas etapas.

### Passo 8: Registrar os Nomes das Tabelas DynamoDB V3

Após implantar a V3, você precisa obter os nomes da nova ConversationTable e BotTable:

```bash
# Obter o nome da ConversationTable V3
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='ConversationTableNameV3'].OutputValue" \
  --stack-name {SEU_PREFIXO_DE_ENV}BedrockChatStack

# Obter o nome da BotTable V3
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='BotTableNameV3'].OutputValue" \
  --stack-name {SEU_PREFIXO_DE_ENV}BedrockChatStack
```

> [!Important]
> Certifique-se de salvar estes nomes de tabela V3 junto com o nome da tabela V2 que você salvou anteriormente, pois você precisará de todos eles para o script de migração.

### Passo 9: Executar o Script de Migração

O script de migração converterá seus dados V2 para o esquema V3. Primeiro, edite o script de migração `docs/migration/migrate_v2_v3.py` para definir seus nomes de tabela e região:

```python
# Região onde o dynamodb está localizado
REGION = "ap-northeast-1" # Substitua pela sua região

V2_CONVERSATION_TABLE = "BedrockChatStack-DatabaseConversationTableXXXX" # Substitua pelo valor registrado no Passo 4
V3_CONVERSATION_TABLE = "BedrockChatStack-DatabaseConversationTableV3XXXX" # Substitua pelo valor registrado no Passo 8
V3_BOT_TABLE = "BedrockChatStack-DatabaseBotTableV3XXXXX" # Substitua pelo valor registrado no Passo 8
```

Em seguida, execute o script usando Poetry a partir do diretório backend:

> [!NOTE]
> A versão dos requisitos do Python foi alterada para 3.13.0 ou posterior (Possivelmente alterada em desenvolvimento futuro. Consulte pyproject.toml). Se você tiver o venv instalado com uma versão diferente do Python, precisará removê-lo uma vez.

```bash
# Navegar para o diretório backend
cd backend

# Instalar dependências se ainda não o fez
poetry install

# Executar um teste de simulação primeiro para ver o que seria migrado
poetry run python ../docs/migration/migrate_v2_v3.py --dry-run

# Se tudo parecer bom, execute a migração real
poetry run python ../docs/migration/migrate_v2_v3.py

# Verificar se a migração foi bem-sucedida
poetry run python ../docs/migration/migrate_v2_v3.py --verify-only
```

O script de migração irá gerar um arquivo de relatório no seu diretório atual com detalhes sobre o processo de migração. Verifique este arquivo para garantir que todos os seus dados foram migrados corretamente.

#### Lidando com Grandes Volumes de Dados

Para ambientes com usuários intensivos ou grandes quantidades de dados, considere estas abordagens:

1. **Migrar usuários individualmente**: Para usuários com grandes volumes de dados, migre-os um de cada vez:

   ```bash
   poetry run python ../docs/migration/migrate_v2_v3.py --users id-usuario-1 id-usuario-2
   ```

2. **Considerações de memória**: O processo de migração carrega dados na memória. Se você encontrar erros de Memória Insuficiente (OOM), tente:

   - Migrar um usuário de cada vez
   - Executar a migração em uma máquina com mais memória
   - Dividir a migração em lotes menores de usuários

3. **Monitorar a migração**: Verifique os arquivos de relatório gerados para garantir que todos os dados sejam migrados corretamente, especialmente para grandes conjuntos de dados.

### Passo 10: Verificar o Aplicativo

Após a migração, abra seu aplicativo e verifique:

- Todos os seus bots estão disponíveis
- As conversas foram preservadas
- Os novos controles de permissão estão funcionando

### Limpeza (Opcional)

Após confirmar que a migração foi bem-sucedida e todos os seus dados estão corretamente acessíveis na V3, você pode, opcionalmente, excluir a tabela de conversação V2 para reduzir custos:

```bash
# Excluir a tabela de conversação V2 (APENAS após confirmar migração bem-sucedida)
aws dynamodb delete-table --table-name SEU_NOME_DE_TABELA_DE_CONVERSAÇÃO_V2
```

> [!IMPORTANT]
> Exclua a tabela V2 apenas após verificar minuciosamente que todos os seus dados importantes foram migrados com sucesso para a V3. Recomendamos manter o backup criado no Passo 2 por pelo menos algumas semanas após a migração, mesmo que você exclua a tabela original.

## V3 Perguntas Frequentes

### Acesso e Permissões de Bot

**P: O que acontece se um bot que estou usando for excluído ou minha permissão de acesso for removida?**
R: A autorização é verificada no momento do chat, então você perderá o acesso imediatamente.

**P: O que acontece se um usuário for excluído (por exemplo, funcionário sai)?**
R: Seus dados podem ser completamente removidos excluindo todos os itens do DynamoDB com o ID do usuário como chave de partição (PK).

**P: Posso desativar o compartilhamento de um bot público essencial?**
R: Não, o administrador deve primeiro marcar o bot como não essencial antes de desativar o compartilhamento.

**P: Posso excluir um bot público essencial?**
R: Não, o administrador deve primeiro marcar o bot como não essencial antes de excluí-lo.

### Segurança e Implementação

**P: A segurança em nível de linha (RLS) está implementada para a tabela de bots?**
R: Não, considerando a diversidade de padrões de acesso. A autorização é realizada ao acessar bots, e o risco de vazamento de metadados é considerado mínimo em comparação com o histórico de conversas.

**P: Quais são os requisitos para publicar uma API?**
R: O bot deve ser público.

**P: Haverá uma tela de gerenciamento para todos os bots privados?**
R: Não na versão inicial do V3. No entanto, os itens ainda podem ser excluídos consultando com o ID do usuário, conforme necessário.

**P: Haverá funcionalidade de marcação de bots para melhorar a experiência de busca?**
R: Não na versão inicial do V3, mas a marcação automática baseada em LLM pode ser adicionada em futuras atualizações.

### Administração

**P: O que os administradores podem fazer?**
R: Os administradores podem:

- Gerenciar bots públicos (incluindo verificação de bots de alto custo)
- Gerenciar APIs
- Marcar bots públicos como essenciais

**P: Posso tornar bots parcialmente compartilhados como essenciais?**
R: Não, apenas bots públicos são suportados.

**P: Posso definir prioridade para bots fixados?**
R: Na versão inicial, não.

### Configuração de Autorização

**P: Como configuro a autorização?**
R:

1. Abra o console do Amazon Cognito e crie grupos de usuários no pool de usuários do BrChat
2. Adicione usuários a esses grupos conforme necessário
3. No BrChat, selecione os grupos de usuários que deseja permitir acesso ao configurar as definições de compartilhamento de bot

Nota: Alterações na associação de grupos requerem novo login para surtir efeito. As alterações são refletidas na atualização do token, mas não durante o período de validade do token de ID (padrão de 30 minutos no V3, configurável por `tokenValidMinutes` em `cdk.json` ou `parameter.ts`).

**P: O sistema verifica com o Cognito toda vez que um bot é acessado?**
R: Não, a autorização é verificada usando o token JWT para evitar operações de I/O desnecessárias.

### Funcionalidade de Busca

**P: A busca de bots oferece suporte a busca semântica?**
R: Não, apenas correspondência parcial de texto é suportada. Busca semântica (por exemplo, "automóvel" → "carro", "EV", "veículo") não está disponível devido às atuais restrições do OpenSearch Serverless (Mar 2025).