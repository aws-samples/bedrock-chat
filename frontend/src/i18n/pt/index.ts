const translation = {
    translation: {
      signIn: {
        button: {
          login: 'Entrar',
        },
      },
      app: {
        name: 'Chat Bedrock Claude',
        nameWithoutClaude: 'Chat Bedrock',
        inputMessage: 'Posso te ajudar?',
        starredBots: 'Bots Favoritos',
        recentlyUsedBots: 'Bots Recentemente Usados',
        conversationHistory: 'Histórico',
        chatWaitingSymbol: '▍',
        adminConsoles: 'Somente Administradores',
      },
      model: {
        'claude-v3-haiku': {
          label: 'Claude 3 (Haiku)',
          description:
            'Versão anterior otimizada para velocidade e compacidade, proporcionando respostas quase instantâneas.',
        },
        'claude-v3-sonnet': {
          label: 'Claude 3 (Soneto)',
          description: 'Equilíbrio entre inteligência e velocidade.',
        },
        'claude-v3.5-sonnet': {
          label: 'Claude 3.5 (Soneto) v1',
          description:
            'Versão anterior do Claude 3.5. Suporta uma ampla gama de tarefas, mas a versão v2 oferece maior precisão.',
        },
        'claude-v3.5-sonnet-v2': {
          label: 'Claude 3.5 (Soneto) v2',
          description:
            'A versão mais recente do Claude 3.5. Um modelo aprimorado que melhora o v1 com maior precisão e desempenho.',
        },
        'claude-v3.5-haiku': {
          label: 'Claude 3.5 (Haiku) v1',
          description:
            'A versão mais recente, oferecendo ainda mais rapidez nas respostas e melhorias sobre o Haiku 3.',
        },
        'claude-v3-opus': {
          label: 'Claude 3 (Opus)',
          description: 'Modelo poderoso para tarefas altamente complexas.',
        },
        'mistral-7b-instruct': {
          label: 'Mistral 7B',
          description: 'Suporta tarefas de geração de texto em inglês com capacidades naturais de codificação',
        },
        'mixtral-8x7b-instruct': {
          label: 'Mistral-8x7B',
          description: "Modelo popular e de alta qualidade, Mixture-of-Experts (MoE), ideal para sumarização de textos, perguntas e respostas, classificação de textos, conclusão de textos e geração de código."
        },
        'mistral-large': {
          label: 'Mistral Grande',
          description: "Ideal para tarefas complexas que exigem capacidades substanciais de raciocínio, ou para aquelas altamente especializadas, como Geração de Texto Sintético ou Geração de Código."
        },
        'amazon-nova-pro': {
          label: 'Amazon Nova Pro',
          description:
            'Modelo multimodal altamente capaz, com a melhor combinação de precisão, velocidade e custo para uma ampla gama de tarefas.',
        },
        'amazon-nova-lite': {
          label: 'Amazon Nova Lite',
          description:
            'Modelo multimodal de baixo custo, extremamente rápido para processar entradas de imagem, vídeo e texto.',
        },
        'amazon-nova-micro': {
          label: 'Amazon Nova Micro',
          description:
            'Modelo apenas de texto que oferece respostas com a menor latência dentro da família de modelos Amazon Nova, com um custo muito baixo.',
        },
      },
      agent: {
        label: 'Agente',
        help: {
          overview:
            'Ao usar a funcionalidade de Agente, seu chatbot pode lidar automaticamente com tarefas mais complexas.',
        },
        hint: `O agente determina automaticamente quais ferramentas usar para responder às perguntas do usuário. Devido ao tempo necessário para a decisão, o tempo de resposta tende a ser mais longo. Ativar uma ou mais ferramentas habilita a funcionalidade do agente. Se nenhuma ferramenta for selecionada, a funcionalidade do agente não será utilizada. Quando a funcionalidade do agente está ativada, o uso de "Conhecimento" também é tratado como uma das ferramentas. Isso significa que "Conhecimento" pode não ser usado nas respostas.`,
        progress: {
          label: 'Pensando...',
        },
        progressCard: {
          toolInput: 'Entrada: ',
          toolOutput: 'Saída: ',
          status: {
            running: 'Executando...',
            success: 'Sucesso',
            error: 'Erro',
          },
        },
        tools: {
          get_weather: {
            name: 'Clima Atual',
            description: 'Recupera a previsão do tempo atual.',
          },
          sql_db_query: {
            name: 'Consulta ao Banco de Dados',
            description:
              'Executa uma consulta SQL detalhada e correta para recuperar resultados do banco de dados.',
          },
          sql_db_schema: {
            name: 'Esquema do Banco de Dados',
            description:
              'Recupera o esquema e as linhas de exemplo para uma lista de tabelas.',
          },
          sql_db_list_tables: {
            name: 'Listar Tabelas do Banco de Dados',
            description: 'Lista todas as tabelas disponíveis no banco de dados.',
          },
          sql_db_query_checker: {
            name: 'Verificador de Consultas',
            description: 'Verifique se sua consulta SQL está correta antes de executá-la.',
          },
          internet_search: {
            name: 'Pesquisa na Internet',
            description: 'Pesquise na internet por informações.',
          },
          knowledge_base_tool: {
            name: 'Recuperar Conhecimento',
            description: 'Recupera informações do conhecimento.',
          },
        },
      },
      bot: {
        label: {
          myBots: 'Meus Bots',
          recentlyUsedBots: 'Bots Compartilhados Recentemente Usados',
          knowledge: 'Conhecimento',
          url: 'URL',
          s3url: 'Fonte de Dados S3',
          sitemap: 'URL do Sitemap',
          file: 'Arquivo',
          loadingBot: 'Carregando...',
          normalChat: 'Chat',
          notAvailableBot: '[Não Disponível]',
          notAvailableBotInputMessage: 'Este bot NÃO está disponível.',
          noDescription: 'Sem Descrição',
          notAvailable: 'Este bot NÃO está disponível.',
          noBots: 'Sem Bots.',
          noBotsRecentlyUsed: 'Sem Bots Compartilhados Recentemente Usados.',
          retrievingKnowledge: '[Recuperando Conhecimento...]',
          selectParsingModel: 'Selecionar Modelo de Análise',
          dndFileUpload:
            'Você pode carregar arquivos por arrastar e soltar.\nArquivos suportados: {{fileExtensions}}',
          uploadError: 'Mensagem de Erro',
          referenceLink: 'Link de Referência',
          syncStatus: {
            queue: 'Aguardando Sincronização',
            running: 'Sincronizando',
            success: 'Sincronização Completa',
            fail: 'Falha na Sincronização',
          },
          fileUploadStatus: {
            uploading: 'Carregando...',
            uploaded: 'Carregado',
            error: 'ERRO',
          },
          quickStarter: {
            title: 'Início Rápido da Conversa',
            exampleTitle: 'Título',
            example: 'Exemplo de Conversa',
          },
          citeRetrievedContexts: 'Citação de Contextos Recuperados',
          unsupported: 'Não Suportado, Somente Leitura',
        },
        titleSubmenu: {
          edit: 'Editar',
          copyLink: 'Copiar Link',
          copiedLink: 'Copiado',
        },
        help: {
          overview:
            'Bots operam de acordo com instruções predefinidas. O chat não funciona como esperado, a menos que o contexto seja definido na mensagem, mas com bots, não há necessidade de definir o contexto.',
          instructions:
            'Defina como o bot deve se comportar. Instruções ambíguas podem levar a movimentos imprevisíveis, então forneça instruções claras e específicas.',
          knowledge: {
            overview:
              'Ao fornecer conhecimento externo ao bot, ele se torna capaz de lidar com dados que não foram pré-treinados.',
            url: 'A informação da URL especificada será usada como Conhecimento.',
            s3url:
              'Ao inserir o URI do S3, você pode adicionar o S3 como uma fonte de dados. Você pode adicionar até 4 fontes. Suporta apenas buckets que existem na mesma conta e região que a região Bedrock.',
            sitemap:
              'Ao especificar a URL do sitemap, as informações obtidas por meio da raspagem automática dos sites nele serão usadas como Conhecimento.',
            file: 'Os arquivos carregados serão usados como Conhecimento.',
            citeRetrievedContexts:
              'Configure se os contextos recuperados para responder às perguntas do usuário devem ser exibidos como informações de citação.\nSe ativado, os usuários podem acessar os URLs ou arquivos da fonte original.',
          },
          quickStarter: {
            overview:
              'Ao iniciar uma conversa, forneça exemplos. Os exemplos ilustram como usar o bot.',
          },
        },
        alert: {
          sync: {
            error: {
              title: 'Erro de Sincronização de Conhecimento',
              body: 'Ocorreu um erro ao sincronizar o Conhecimento. Por favor, verifique a mensagem a seguir:',
            },
            incomplete: {
              title: 'NÃO Pronto',
              body: 'Este bot não concluiu a sincronização de conhecimento, então o conhecimento anterior à atualização é usado.',
            },
          },
        },
        samples: {
          title: 'Exemplos de Instruções',
          anthropicLibrary: {
            title: 'Biblioteca de Prompt Antropica',
            sentence: 'Precisa de mais exemplos? Visite: ',
            url: 'https://docs.anthropic.com/claude/prompt-library',
          },
          pythonCodeAssistant: {
            title: 'Assistente de Codificação Python',
            prompt: `Escreva um script Python curto e de alta qualidade para a tarefa fornecida, algo que um especialista muito habilidoso escreveria. Você está escrevendo código para um desenvolvedor experiente, então adicione comentários apenas para coisas que não são óbvias. Certifique-se de incluir quaisquer importações necessárias. 
  NUNCA escreva nada antes do bloco \`\`\`python\`\`\`. Após terminar de gerar o código e depois do bloco \`\`\`python\`\`\`, verifique seu trabalho cuidadosamente para garantir que não haja erros, falhas ou inconsistências. Se houver erros, liste esses erros nas tags <error>, depois gere uma nova versão com esses erros corrigidos. Se não houver erros, escreva "CHECKED: NO ERRORS" nas tags <error>.`,
          },
          mailCategorizer: {
            title: 'Classificador de E-mails',
            prompt: `Você é um agente de atendimento ao cliente encarregado de classificar e-mails por tipo. Por favor, classifique seu e-mail e justifique sua classificação.
  
  As categorias de classificação são: 
  (A) Pergunta pré-venda 
  (B) Item quebrado ou defeituoso 
  (C) Pergunta de cobrança 
  (D) Outro (explique)
  
  Como você classificaria este e-mail?`,
          },
          fitnessCoach: {
            title: 'Personal Fitness Coach',
            prompt: `Você é um personal trainer entusiástico chamado Sam. Sam é apaixonado por ajudar seus clientes a se tornarem mais saudáveis e alcançar suas metas de fitness. Você escreve de forma encorajadora e amigável e sempre tenta guiar seus clientes para alcançar melhores metas de fitness. Se o usuário perguntar algo não relacionado ao fitness, tente trazer o tópico de volta para o fitness ou diga que você não pode responder.`,
          },
        },
        create: {
          pageTitle: 'Criar Meu Bot',
        },
        edit: {
          pageTitle: 'Editar Meu Bot',
        },
  
        item: {
          title: 'Nome',
          description: 'Descrição',
          instruction: 'Instruções',
        },
        explore: {
          label: {
            pageTitle: 'Console do Bot',
          },
        },
        apiSettings: {
          pageTitle: 'Configurações da API de Publicação de Bot Compartilhado',
          label: {
            endpoint: 'Endpoint da API',
            usagePlan: 'Plano de Uso',
            allowOrigins: 'Origens Permitidas',
            apiKeys: 'Chaves da API',
            period: {
              day: 'Por DIA',
              week: 'Por SEMANA',
              month: 'Por MÊS',
            },
            apiKeyDetail: {
              creationDate: 'Data de Criação',
              active: 'Ativo',
              inactive: 'Inativo',
              key: 'Chave da API',
            },
          },
          item: {
            throttling: 'Controle de Taxa',
            burstLimit: 'Limite de Pico',
            rateLimit: 'Limite de Taxa',
            quota: 'Cota',
            requestLimit: 'Limite de Solicitações',
            offset: 'Deslocamento',
          },
          help: {
            overview:
              "Criar uma API permite que as funções do Bot sejam acessadas por clientes externos; APIs permitem integração com aplicativos externos.",
            endpoint: 'O cliente pode usar o Bot a partir deste endpoint.',
            usagePlan:
              'Os planos de uso especificam o número ou a taxa de solicitações que sua API aceita de um cliente. Associe uma API a um plano de uso para acompanhar as solicitações recebidas pela sua API.',
            throttling: 'Limite a taxa em que os usuários podem chamar sua API.',
            rateLimit:
              'Digite a taxa, em solicitações por segundo, que os clientes podem chamar sua API.',
            burstLimit:
              'Digite o número de solicitações simultâneas que um cliente pode fazer à sua API.',
            quota:
              'Ative as cotas para limitar o número de solicitações que um usuário pode fazer à sua API em um período de tempo determinado.',
            requestLimit:
              'Digite o número total de solicitações que um usuário pode fazer no período de tempo selecionado na lista suspensa.',
            allowOrigins:
              'Origens de cliente permitidas para acesso. Se a origem não for permitida, o chamador receberá uma resposta 403 Forbidden e terá acesso negado à API. A Origem deve seguir o formato: "(http|https)://host-name" ou "(http|https)://host-name:port" e curingas(*) podem ser usados.',
            allowOriginsExample:
              'ex: https://your-host-name.com, https://*.your-host-name.com, http://localhost:8000',
            apiKeys:
              'Uma chave de API é uma string alfanumérica usada para identificar um cliente da sua API. Caso contrário, o chamador receberá uma resposta 403 Forbidden e terá acesso negado à API.',
          },
          button: {
            ApiKeyShow: 'Mostrar',
            ApiKeyHide: 'Ocultar',
          },
          alert: {
            botUnshared: {
              title: 'Por Favor, Compartilhe o Bot',
              body: 'Você não pode publicar uma API para um bot que não foi compartilhado.',
            },
            deploying: {
              title: 'A implantação da API está em ANDAMENTO',
              body: 'Aguarde até que a implantação seja concluída.',
            },
            deployed: {
              title: 'A API foi IMPLANTADA',
              body: 'Você pode acessar a API a partir do Cliente usando o Endpoint da API e a Chave da API.',
            },
            deployError: {
              title: 'Falha ao implantar a API',
              body: 'Por favor, exclua a API e recrie-a.',
            },
          },
          deleteApiDaialog: {
            title: 'Excluir?',
            content:
              'Tem certeza de que deseja excluir a API? O endpoint da API será excluído, e o cliente não terá mais acesso a ela.',
          },
          addApiKeyDialog: {
            title: 'Adicionar Chave da API',
            content: 'Digite um nome para identificar a Chave da API.',
          },
          deleteApiKeyDialog: {
            title: 'Excluir?',
            content:
              'Tem certeza de que deseja excluir <Bold>{{title}}</Bold>?\nClientes que utilizam esta chave da API terão acesso negado.',
          },
        },
        button: {
          newBot: 'Criar Novo Bot',
          create: 'Criar',
          edit: 'Editar',
          delete: 'Excluir',
          share: 'Compartilhar',
          apiSettings: 'Configurações de Publicação da API',
          copy: 'Copiar',
          copied: 'Copiado',
          instructionsSamples: 'Amostras',
          chooseFiles: 'Escolher arquivos',
        },
        deleteDialog: {
          title: 'Excluir?',
          content: 'Tem certeza de que deseja excluir <Bold>{{title}}</Bold>?',
        },
        shareDialog: {
          title: 'Compartilhar',
          off: {
            content:
              'O compartilhamento de link está desligado, então apenas você pode acessar este bot através da sua URL.',
          },
          on: {
            content:
              'O compartilhamento de link está ligado, então TODOS os usuários podem usar este link para a conversa.',
          },
        },
        error: {
          notSupportedFile: 'Este arquivo não é suportado.',
          duplicatedFile: 'Um arquivo com o mesmo nome foi carregado.',
          failDeleteApi: 'Falha ao excluir a API.',
        },
        activeModels: {
          title: 'Ativação de Modelo',
          description: 'Configure quais modelos de IA podem ser usados com este bot.',
        },
      },
      admin: {
        sharedBotAnalytics: {
          label: {
            pageTitle: 'Análise de Bot Compartilhado',
            noPublicBotUsages:
              'Durante o Período de Cálculo, nenhum bot público foi utilizado.',
            published: 'API publicada.',
            SearchCondition: {
              title: 'Período de Cálculo',
              from: 'De',
              to: 'Para',
            },
            sortByCost: 'Ordenar por Custo',
          },
          help: {
            overview:
              'Monitore o status de uso de Bots Compartilhados e APIs de Bot Publicadas.',
            calculationPeriod:
              'Se o Período de Cálculo não for definido, o custo de hoje será exibido.',
          },
        },
        apiManagement: {
          label: {
            pageTitle: 'Gerenciamento de API',
            publishedDate: 'Data de Publicação',
            noApi: 'Sem APIs.',
          },
        },
        botManagement: {
          label: {
            pageTitle: 'Gerenciamento de Bot',
            sharedUrl: 'URL do Bot Compartilhado',
            apiSettings: 'Configurações de Publicação de API',
            noKnowledge: 'Este bot não possui Conhecimento.',
            notPublishApi: "A API deste bot não está publicada.",
            deployStatus: 'Status de Implantação',
            cfnStatus: 'Status do CloudFormation',
            codebuildStatus: 'Status do CodeBuild',
            codeBuildId: 'ID do CodeBuild',
            usagePlanOn: 'LIGADO',
            usagePlanOff: 'DESLIGADO',
            rateLimit:
              '<Bold>{{limit}}</Bold> solicitações por segundo, que os clientes podem chamar a API.',
            burstLimit:
              'O cliente pode fazer <Bold>{{limit}}</Bold> solicitações simultâneas à API.',
            requestsLimit:
              'Você pode fazer <Bold>{{limit}}</Bold> solicitações <Bold>{{period}}</Bold>.',
          },
          alert: {
            noApiKeys: {
              title: 'Sem Chaves da API',
              body: 'Todos os clientes não têm acesso à API.',
            },
          },
          button: {
            deleteApi: 'Excluir API',
          },
        },
        validationError: {
          period: 'Digite tanto De quanto Para',
        },
      },
      deleteDialog: {
        title: 'Excluir?',
        content: 'Tem certeza de que deseja excluir <Bold>{{title}}</Bold>?',
      },
      clearDialog: {
        title: 'Excluir TUDO?',
        content: 'Tem certeza de que deseja excluir TODAS as conversas?',
      },
      languageDialog: {
        title: 'Mudar idioma',
      },
      feedbackDialog: {
        title: 'Feedback',
        content: 'Por favor, forneça mais detalhes.',
        categoryLabel: 'Categoria',
        commentLabel: 'Comentário',
        commentPlaceholder: '(Opcional) Digite seu comentário',
        categories: [
          {
            value: 'notFactuallyCorrect',
            label: 'Não é factualmente correto',
          },
          {
            value: 'notFullyFollowRequest',
            label: 'Não seguiu completamente meu pedido',
          },
          {
            value: 'other',
            label: 'Outro',
          },
        ],
      },
      button: {
        newChat: 'Novo Chat',
        botConsole: 'Console do Bot',
        sharedBotAnalytics: 'Análise de Bot Compartilhado',
        apiManagement: 'Gerenciamento de API',
        userUsages: 'Usos de Usuários',
        SaveAndSubmit: 'Salvar e Enviar',
        resend: 'Reenviar',
        regenerate: 'Regenerar',
        delete: 'Excluir',
        deleteAll: 'Excluir Tudo',
        done: 'Feito',
        ok: 'OK',
        cancel: 'Cancelar',
        back: 'Voltar',
        menu: 'Menu',
        language: 'Idioma',
        clearConversation: 'Excluir TODAS as conversas',
        signOut: 'Sair',
        close: 'Fechar',
        add: 'Adicionar',
        continue: 'Continuar gerando',
      },
      input: {
        hint: {
          required: '* Obrigatório',
        },
        validationError: {
          required: 'Este campo é obrigatório.',
          invalidOriginFormat: 'Formato de origem inválido.',
        },
      },
      embeddingSettings: {
        title: 'Configuração de Embedding',
        description:
          'Você pode configurar os parâmetros para embeddings vetoriais. Ajustando os parâmetros, você pode alterar a precisão da recuperação de documentos.',
        chunkSize: {
          label: 'tamanho do pedaço',
          hint: 'O tamanho do pedaço refere-se ao tamanho em que um documento é dividido em segmentos menores',
        },
        chunkOverlap: {
          label: 'sobreposição do pedaço',
          hint: 'Você pode especificar o número de caracteres sobrepostos entre pedaços adjacentes.',
        },
        enablePartitionPdf: {
          label:
            'Habilitar análise detalhada de PDF. Se ativado, o PDF será analisado detalhadamente ao longo do tempo.',
          hint: 'É eficaz quando você deseja melhorar a precisão de pesquisa. O custo de computação aumenta porque a computação leva mais tempo.',
        },
        help: {
          chunkSize:
            "Quando o tamanho do pedaço é muito pequeno, informações contextuais podem ser perdidas, e quando é muito grande, diferentes informações contextuais podem existir dentro do mesmo pedaço, o que pode reduzir a precisão da pesquisa.",
          chunkOverlap:
            'Ao especificar a sobreposição de pedaços, você pode preservar as informações contextuais ao redor das fronteiras dos pedaços. Aumentar o tamanho do pedaço pode, às vezes, melhorar a precisão da pesquisa. No entanto, tenha cuidado, pois aumentar a sobreposição de pedaços pode levar a custos computacionais mais altos.',
          overlapTokens:
            'Você configura o número de tokens para sobrepor, ou repetir, entre pedaços adjacentes. Por exemplo, se você definir sobreposição de tokens para 60, os últimos 60 tokens do primeiro pedaço também serão incluídos no início do segundo pedaço.',
          maxParentTokenSize:
            'Você pode definir o tamanho do pedaço pai. Durante a recuperação, o sistema inicialmente recupera pedaços filhos, mas substitui-os por pedaços pais mais amplos para fornecer ao modelo um contexto mais abrangente',
          maxChildTokenSize:
            'Você pode definir o tamanho do pedaço filho. Durante a recuperação, o sistema inicialmente recupera pedaços filhos, mas substitui-os por pedaços pais mais amplos para fornecer ao modelo um contexto mais abrangente',
          bufferSize:
            'Este parâmetro pode influenciar o quanto de texto é examinado junto para determinar os limites de cada pedaço, impactando a granularidade e coerência dos pedaços resultantes. Um tamanho de buffer maior pode capturar mais contexto, mas também pode introduzir ruído, enquanto um tamanho de buffer menor pode perder contextos importantes, mas garante um pedaçamento mais preciso.',
          breakpointPercentileThreshold:
            'Um limiar mais alto exige que as frases sejam mais distinguíveis para serem divididas em diferentes pedaços. Um limiar mais alto resulta em menos pedaços e, normalmente, um tamanho médio de pedaço maior.',
        },
        alert: {
          sync: {
            error: {
              title: 'Erro no Divisor de Sentença',
              body: 'Tente novamente com um valor menor para a sobreposição de pedaços',
            },
          },
        },
      },
      generationConfig: {
        title: 'Configuração de Geração',
        description:
          'Você pode configurar os parâmetros de inferência do LLM para controlar a resposta dos modelos.',
        maxTokens: {
          label: 'Comprimento máximo da geração/máximo de novos tokens',
          hint: 'O número máximo de tokens permitidos na resposta gerada',
        },
        temperature: {
          label: 'Temperatura',
          hint: 'Afeta a forma da distribuição de probabilidade para a saída prevista e influencia a probabilidade de o modelo selecionar saídas de baixa probabilidade',
          help: 'Escolha um valor baixo para influenciar o modelo a selecionar saídas de alta probabilidade; Escolha um valor mais alto para influenciar o modelo a selecionar saídas de baixa probabilidade',
        },
        topK: {
          label: 'Top-k',
          hint: 'O número de candidatos mais prováveis que o modelo considera para o próximo token',
          help: 'Escolha um valor baixo para diminuir o tamanho do pool e limitar as opções a saídas mais prováveis; Escolha um valor mais alto para aumentar o tamanho do pool e permitir que o modelo considere saídas menos prováveis',
        },
        topP: {
          label: 'Top-p',
          hint: 'A porcentagem de candidatos mais prováveis que o modelo considera para o próximo token',
          help: 'Escolha um valor baixo para diminuir o tamanho do pool e limitar as opções a saídas mais prováveis; Escolha um valor mais alto para aumentar o tamanho do pool e permitir que o modelo considere saídas menos prováveis',
        },
        stopSequences: {
          label: 'Token final/sequência final',
          hint: 'Especifique sequências de caracteres que interrompem a geração de tokens pelo modelo. Use vírgulas para separar várias palavras',
        },
      },
      searchSettings: {
        title: 'Configurações de Pesquisa',
        description:
          'Você pode configurar os parâmetros de pesquisa para buscar documentos relevantes no vetor de armazenamento.',
        maxResults: {
          label: 'Máximo de Resultados',
          hint: 'O número máximo de registros recuperados do vetor de armazenamento',
        },
        searchType: {
          label: 'Tipo de Pesquisa',
          hybrid: {
            label: 'Pesquisa Híbrida',
            hint: 'Combina pontuações de relevância da pesquisa semântica e de texto para fornecer maior precisão.',
          },
          semantic: {
            label: 'Pesquisa Semântica',
            hint: 'Usa embeddings vetoriais para fornecer resultados relevantes.',
          },
        },
      },
      knowledgeBaseSettings: {
        title: 'Configurações de Detalhes do Conhecimento',
        description:
          'Selecione o modelo embutido para configurar o conhecimento e defina o método para dividir documentos adicionados como conhecimento. Essas configurações não podem ser alteradas após criar o bot.',
        embeddingModel: {
          label: 'Modelo de Embedding',
          titan_v2: {
            label: 'Titan Embedding Text v2',
          },
          cohere_multilingual_v3: {
            label: 'Embed Multilingual v3',
          },
        },
        chunkingStrategy: {
          label: 'Estratégia de Pedaçamento',
          default: {
            label: 'Pedaçamento Padrão',
            hint: "Divide automaticamente o texto em pedaços de cerca de 300 tokens por padrão. Se um documento for menor que 300 tokens, ele não será dividido mais.",
          },
          fixed_size: {
            label: 'Pedaçamento de Tamanho Fixo',
            hint: 'Divide o texto no seu tamanho de token aproximado configurado.',
          },
          hierarchical: {
            label: 'Pedaçamento Hierárquico',
            hint: 'Divide o texto em estruturas aninhadas de pedaços pai e filho.',
          },
          semantic: {
            label: 'Pedaçamento Semântico',
            hint: 'Divide o texto em pedaços significativos para melhorar a compreensão e a recuperação de informações.',
          },
          none: {
            label: 'Sem Pedaçamento',
            hint: 'Os documentos não serão divididos.',
          },
        },
        chunkingMaxTokens: {
          label: 'Máximo de Tokens',
          hint: 'O número máximo de tokens por pedaço',
        },
        chunkingOverlapPercentage: {
          label: 'Porcentagem de Sobreposição entre os Pedaços',
          hint: 'A sobreposição do pedaço pai depende do tamanho do token filho e da porcentagem de sobreposição filho que você especificou.',
        },
        overlapTokens: {
          label: 'Tokens de Sobreposição',
          hint: 'O número de tokens a serem repetidos entre pedaços no mesmo nível',
        },
        maxParentTokenSize: {
          label: 'Máximo de Tokens no Pedaço Pai',
          hint: 'O número máximo de tokens que um pedaço pode conter na camada Pai',
        },
        maxChildTokenSize: {
          label: 'Máximo de Tokens no Pedaço Filho',
          hint: 'O número máximo de tokens que um pedaço pode conter na camada Filho',
        },
        bufferSize: {
          label: 'Tamanho do Buffer',
          hint: 'O número de sentenças ao redor que serão adicionadas para a criação de embeddings. Um tamanho de buffer de 1 resulta em 3 sentenças (atual, anterior e próxima) sendo combinadas e embutidas',
        },
        breakpointPercentileThreshold: {
          label: 'Limiar Percentual de Breakpoint',
          hint: 'O limiar percentual de distância/dessemelhança entre sentenças para criar pontos de divisão.',
        },
        opensearchAnalyzer: {
          label: 'Analisador (Tokenização, Normalização)',
          hint: 'Você pode especificar o analisador para tokenizar e normalizar os documentos registrados como conhecimento. Selecionar o analisador apropriado melhorará a precisão da pesquisa. Escolha o analisador ideal que corresponda à língua do seu conhecimento.',
          icu: {
            label: 'Analisador ICU',
            hint: 'Para tokenização, {{tokenizer}} é usado, e para normalização, {{normalizer}} é usado.',
          },
          kuromoji: {
            label: 'Analisador Japonês (kuromoji)',
            hint: 'Para tokenização, {{tokenizer}} é usado, e para normalização, {{normalizer}} é usado.',
          },
          none: {
            label: 'Analisador Padrão do Sistema',
            hint: 'Será usado o analisador padrão definido pelo sistema (OpenSearch).',
          },
          tokenizer: 'Tokenizador:',
          normalizer: 'Normalizador:',
          token_filter: 'Filtro de Token:',
          not_specified: 'Não especificado',
        },
        advancedParsing: {
          label: 'Análise Avançada',
          description:
            'Selecione um modelo para usar as capacidades avançadas de análise de documentos.',
          hint: 'Adequado para analisar mais do que o texto padrão em formatos de documentos compatíveis, incluindo tabelas dentro de PDFs com suas estruturas intactas. Custos adicionais são gerados ao realizar análise usando IA generativa.',
        },
        parsingModel: {
          label: 'Modelo de Análise Avançada',
          none: {
            label: 'Desativado',
            hint: 'Nenhuma análise avançada será aplicada.',
          },
          claude_3_sonnet_v1: {
            label: 'Claude 3 Sonnet v1',
            hint: 'Use o Claude 3 Sonnet v1 para análise avançada de documentos.',
          },
          claude_3_haiku_v1: {
            label: 'Claude 3 Haiku v1',
            hint: 'Use o Claude 3 Haiku v1 para análise avançada de documentos.',
          },
        },
        webCrawlerConfig: {
          title: 'Configuração do Rastreador Web',
          crawlingScope: {
            label: 'Escopo de Rastreamento',
            default: {
              label: 'Padrão',
              hint: 'Limite o rastreamento para páginas da web que pertencem ao mesmo host e têm o mesmo caminho de URL inicial. Por exemplo, com uma URL semente de "https://aws.amazon.com/bedrock/" apenas esse caminho e as páginas da web que se estendem a partir dele serão rastreadas, como "https://aws.amazon.com/bedrock/agents/". URLs irmãs como "https://aws.amazon.com/ec2/" não serão rastreadas, por exemplo.',
            },
            subdomains: {
              label: 'Subdomínios',
              hint: 'Inclua o rastreamento de qualquer página da web que tenha o mesmo domínio principal da URL semente. Por exemplo, com uma URL semente de "https://aws.amazon.com/bedrock/" qualquer página da web que contenha "amazon.com" será rastreada, como "https://www.amazon.com".',
            },
            hostOnly: {
              label: 'Somente Host',
              hint: 'Limite o rastreamento para páginas da web que pertencem ao mesmo host. Por exemplo, com uma URL semente de "https://aws.amazon.com/bedrock/", páginas da web com "https://docs.aws.amazon.com" também serão rastreadas, como "https://aws.amazon.com/ec2".',
            },
          },
          includePatterns: {
            label: 'Incluir Padrões',
            hint: 'Especifique os padrões a serem incluídos no rastreamento da web. Somente URLs que coincidam com esses padrões serão rastreadas.',
          },
          excludePatterns: {
            label: 'Excluir Padrões',
            hint: 'Especifique os padrões a serem excluídos do rastreamento da web. URLs que coincidam com esses padrões não serão rastreadas.',
          },
        },
        advancedConfigration: {
          existKnowledgeBaseId: {
            label: "ID para a Base de Conhecimento do Amazon Bedrock",
            description: "Por favor, especifique o ID da sua base de conhecimento existente no Amazon Bedrock.",
            createNewKb: {
              label: 'Criar Nova Base de Conhecimento',
            },
            existing: {
              label: 'Usar sua base de conhecimento existente',
            }
          }
        },
      },
      error: {
        answerResponse: 'Ocorreu um erro ao responder.',
        notFoundConversation:
          'Como o chat especificado não existe, uma nova tela de chat é exibida.',
        notFoundPage: 'A página que você está procurando não foi encontrada.',
        unexpectedError: {
          title: 'Ocorreu um erro inesperado.',
          restore: 'Ir para a página principal',
        },
        predict: {
          general: 'Ocorreu um erro ao prever.',
          invalidResponse:
            'Resposta inesperada recebida. O formato da resposta não corresponde ao formato esperado.',
        },
        notSupportedImage: 'O modelo selecionado não suporta imagens.',
        unsupportedFileFormat: 'O formato de arquivo selecionado não é suportado.',
        totalFileSizeToSendExceeded:
          'O tamanho total do arquivo deve ser no máximo {{maxSize}}.',
        attachment: {
          fileSizeExceeded:
            'Cada documento deve ter no máximo {{maxSize}}.',
          fileCountExceeded: 'Não foi possível carregar mais de {{maxCount}} arquivos.',
        },
      },
      validation: {
        title: 'Erro de Validação',
        maxRange: {
          message: 'O valor máximo que pode ser definido é {{size}}',
        },
        minRange: {
          message: 'O valor mínimo que pode ser definido é {{size}}',
        },
        chunkOverlapLessThanChunkSize: {
          message: 'A sobreposição do pedaço deve ser definida como menor que o tamanho do pedaço',
        },
        parentTokenRange: {
          message: 'O tamanho do token pai deve ser maior que o tamanho do token filho',
        },
        quickStarter: {
          message: 'Por favor, insira tanto o Título quanto o Exemplo de Conversa.',
        },
      },
      helper: {
        shortcuts: {
          title: 'Teclas de Atalho',
          items: {
            focusInput: 'Focar na entrada do chat',
            newChat: 'Abrir novo chat',
          },
        },
      },
      guardrails: {
        title: 'Guardrails',
        label: 'Ativar Guardrails para o Amazon Bedrock',
        hint: 'Os guardrails para o Amazon Bedrock são usados para implementar salvaguardas específicas de aplicativos com base nos seus casos de uso e políticas de IA responsável.',
        harmfulCategories: {
          label: 'Categorias Prejudiciais',
          hint: 'Configure filtros de conteúdo ajustando o grau de filtragem para detectar e bloquear entradas de usuários e respostas de modelos prejudiciais que violam suas políticas de uso. 0: desabilitado, 1: baixo, 2: médio, 3: alto',
          hate: {
            label: 'Ódio',
            hint: 'Descreve entradas e respostas de modelos que discriminam, criticam, insultam, denunciam ou desumanizam uma pessoa ou grupo com base em uma identidade (como raça, etnia, gênero, religião, orientação sexual, capacidade e origem nacional). 0: desabilitado, 1: baixo, 2: médio, 3: alto',
          },
          insults: {
            label: 'Insultos',
            hint: 'Descreve entradas e respostas de modelos que incluem linguagem humilhante, zombadora, insultante ou desvalorizadora. Esse tipo de linguagem também é rotulado como bullying. 0: desabilitado, 1: baixo, 2: médio, 3: alto',
          },
          sexual: {
            label: 'Sexual',
            hint: 'Descreve entradas e respostas de modelos que indicam interesse sexual, atividade ou excitação usando referências diretas ou indiretas a partes do corpo, características físicas ou sexo. 0: desabilitado, 1: baixo, 2: médio, 3: alto',
          },
          violence: {
            label: 'Violência',
            hint: 'Descreve entradas e respostas de modelos que incluem glorificação ou ameaças de infligir dor, ferir ou lesar uma pessoa, grupo ou coisa. 0: desabilitado, 1: baixo, 2: médio, 3: alto',
          },
          misconduct: {
            label: 'Má Conduta',
            hint: 'Descreve entradas e respostas de modelos que buscam ou fornecem informações sobre como se envolver em atividades impróprias ou prejudicar, fraudar ou tirar proveito de uma pessoa, grupo ou instituição. 0: desabilitado, 1: baixo, 2: médio, 3: alto',
          },
        },
        promptAttacks: {
          hint: 'Descreve prompts de usuário destinados a contornar as capacidades de segurança e moderação de um modelo base para gerar conteúdo prejudicial (também conhecido como jailbreak), e ignorar e substituir instruções especificadas pelo desenvolvedor (conhecido como injeção de prompt). Consulte "Prompt Attack" para mais detalhes e para usá-lo com marcação de entrada.',
        },
        deniedTopics: {
          hint: 'Adicione até 30 tópicos proibidos para bloquear entradas de usuários ou respostas de modelos relacionadas ao tópico.',
        },
        wordFilters: {
          hint: 'Use esses filtros para bloquear certas palavras e frases nas entradas de usuários e respostas de modelos.',
          profanityFilter: {
            hint: 'Ative este recurso para bloquear palavras profanas nas entradas de usuários e respostas de modelos. A lista de palavras é baseada na definição global de profanidade e está sujeita a alterações.',
          },
          customWordsAndPhrases: {
            hint: 'Especifique até 10.000 palavras ou frases (máx. 3 palavras) para serem bloqueadas pelo guardrail. Uma mensagem bloqueada será exibida se as entradas de usuários ou respostas de modelos contiverem essas palavras ou frases.',
          },
        },
        sensitiveInformationFilters: {
          hint: 'Use esses filtros para lidar com quaisquer dados relacionados à privacidade.',
          personallyIdentifiableInformationTypes: {
            PIITypes: {},
            regexPatterns: {},
          },
        },
        contextualGroundingCheck: {
          label: 'Verificação de Contextualização',
          hint: 'Use esta política para validar se as respostas dos modelos estão fundamentadas na fonte de referência e são relevantes para a consulta do usuário para filtrar as alucinações do modelo.',
          groundingThreshold: {
            label: 'Fundamentação',
            hint: 'Valide se as respostas do modelo estão fundamentadas e corretas factualmentes com base nas informações fornecidas na fonte de referência, e bloqueie respostas abaixo do limiar definido de fundamentação. 0: bloqueia nada, 0.99: bloqueia quase tudo',
          },
          relevanceThreshold: {
            label: 'Relevância',
            hint: "Valide se as respostas dos modelos são relevantes para a consulta do usuário e bloqueie respostas abaixo do limiar de relevância definido. 0: bloqueia nada, 0.99: bloqueia quase tudo",
          },
        },
      },
    },
  };
  
  export default translation;  