const translation = {
  translation: {
    signIn: {
      button: {
        login: 'Iniciar sesión',
      },
    },
    app: {
      name: 'Bedrock Claude Chat',
      nameWithoutClaude: 'Bedrock Chat',
      inputMessage: 'Enviar un mensaje',
      starredBots: 'Bots Favoritos',
      recentlyUsedBots: 'Bots Usados Recientemente',
      conversationHistory: 'Historial',
      chatWaitingSymbol: '▍',
      adminConsoles: 'Solo Administrador',
    },
    agent: {
      label: 'Agente',
      help: {
        overview:
          'Al utilizar la funcionalidad de Agente, tu chatbot puede manejar automáticamente tareas más complejas.',
      },
      hint: 'El agente determina automáticamente qué herramientas usar para responder las preguntas del usuario. Debido al tiempo necesario para tomar decisiones, el tiempo de respuesta tiende a ser más largo. Activar una o más herramientas habilita la funcionalidad del agente. Por el contrario, si no se seleccionan herramientas, no se utiliza la funcionalidad del agente. Cuando la funcionalidad del agente está habilitada, el uso de "Conocimiento" también se trata como una de las herramientas. Esto significa que "Conocimiento" puede no ser utilizado en las respuestas.',
      progress: {
        label: 'Pensando...',
      },
      progressCard: {
        toolInput: 'Entrada: ',
        toolOutput: 'Salida: ',
        status: {
          running: 'En ejecución...',
          success: 'Éxito',
          error: 'Error',
        },
      },
      tools: {
        get_weather: {
          name: 'Clima Actual',
          description: 'Recupera el pronóstico del clima actual.',
        },
        sql_db_query: {
          name: 'Consulta de Base de Datos',
          description:
            'Ejecuta una consulta SQL detallada y correcta para recuperar resultados de la base de datos.',
        },
        sql_db_schema: {
          name: 'Esquema de Base de Datos',
          description:
            'Recupera el esquema y las filas de ejemplo para una lista de tablas.',
        },
        sql_db_list_tables: {
          name: 'Listar Tablas de la Base de Datos',
          description: 'Lista todas las tablas disponibles en la base de datos.',
        },
        sql_db_query_checker: {
          name: 'Verificador de Consultas',
          description: 'Verifica si tu consulta SQL es correcta antes de ejecutarla.',
        },
        internet_search: {
          name: 'Búsqueda en Internet',
          description: 'Busca información en internet.',
        },
      },
    },
    bot: {
      label: {
        myBots: 'Mis Bots',
        recentlyUsedBots: 'Bots Compartidos Usados Recientemente',
        knowledge: 'Conocimiento',
        url: 'URL',
        s3url: 'Fuente de Datos S3',
        sitemap: 'URL del Sitemap',
        file: 'Archivo',
        loadingBot: 'Cargando...',
        normalChat: 'Chat',
        notAvailableBot: '[NO Disponible]',
        notAvailableBotInputMessage: 'Este bot NO está disponible.',
        noDescription: 'Sin Descripción',
        notAvailable: 'Este bot NO está disponible.',
        noBots: 'No hay Bots.',
        noBotsRecentlyUsed: 'No hay Bots Compartidos Usados Recientemente.',
        retrievingKnowledge: '[Recuperando Conocimiento...]',
        dndFileUpload:
          'Puedes cargar archivos arrastrándolos y soltándolos.\nArchivos soportados: {{fileExtensions}}',
        uploadError: 'Mensaje de Error',
        referenceLink: 'Enlace de Referencia',
        syncStatus: {
          queue: 'Esperando Sincronización',
          running: 'Sincronizando',
          success: 'Sincronización Completada',
          fail: 'Error en la Sincronización',
        },
        fileUploadStatus: {
          uploading: 'Cargando...',
          uploaded: 'Cargado',
          error: 'ERROR',
        },
        quickStarter: {
          title: 'Inicio Rápido de Conversación',
          exampleTitle: 'Título',
          example: 'Ejemplo de Conversación',
        },
        citeRetrievedContexts: 'Cita de Contexto Recuperado',
        unsupported: 'No Compatible, Solo Lectura',
      },
      titleSubmenu: {
        edit: 'Editar',
        copyLink: 'Copiar Enlace',
        copiedLink: 'Enlace Copiado',
      },
      help: {
        overview:
          'Los bots operan de acuerdo con instrucciones predefinidas. El chat no funciona como se espera a menos que se defina el contexto en el mensaje, pero con los bots, no es necesario definir el contexto.',
        instructions:
          'Define cómo debe comportarse el bot. Dar instrucciones ambiguas puede llevar a movimientos impredecibles, por lo que debes proporcionar instrucciones claras y específicas.',
        knowledge: {
          overview:
            'Al proporcionar conocimiento externo al bot, se vuelve capaz de manejar datos con los que no ha sido preentrenado.',
          url: 'La información de la URL especificada será utilizada como Conocimiento.',
          s3url:
            'Al ingresar la URI de S3, puedes agregar S3 como una fuente de datos. Puedes agregar hasta 4 fuentes. Solo soporta buckets que existan en la misma cuenta y región que Bedrock.',
          sitemap:
            'Al especificar la URL del sitemap, la información obtenida a través de la extracción automática de los sitios web será utilizada como Conocimiento.',
          file: 'Los archivos cargados serán utilizados como Conocimiento.',
          citeRetrievedContexts:
            'Configura si deseas mostrar el contexto recuperado para responder consultas del usuario como información de cita.\nSi está habilitado, los usuarios podrán acceder a las URLs o archivos originales.',
        },
        quickStarter: {
          overview:
            'Al iniciar una conversación, proporciona ejemplos. Los ejemplos ilustran cómo usar el bot.',
        },
      },
      alert: {
        sync: {
          error: {
            title: 'Error de Sincronización de Conocimiento',
            body: 'Ocurrió un error mientras se sincronizaba el Conocimiento. Por favor revisa el siguiente mensaje:',
          },
          incomplete: {
            title: 'NO Listo',
            body: 'Este bot no ha completado la sincronización del conocimiento, por lo que se utiliza el conocimiento anterior a la actualización.',
          },
        },
      },
      samples: {
        title: 'Ejemplos de Instrucciones',
        anthropicLibrary: {
          title: 'Biblioteca de Prompts de Anthropic',
          sentence: '¿Necesitas más ejemplos? Visita: ',
          url: 'https://docs.anthropic.com/claude/prompt-library',
        },
        pythonCodeAssistant: {
          title: 'Asistente de Código Python',
          prompt: `Escribe un script corto y de alta calidad en Python para la tarea dada, algo que escribiría un experto muy hábil en Python. Estás escribiendo código para un desarrollador experimentado, así que solo añade comentarios para cosas que no sean obvias. Asegúrate de incluir cualquier importación requerida. 
          NUNCA escribas nada antes del bloque \`\`\`python\`\`\`. Después de que hayas terminado de generar el código y después del bloque \`\`\`python\`\`\`, revisa tu trabajo cuidadosamente para asegurarte de que no haya errores, fallos o inconsistencias. Si hay errores, enumera esos errores en etiquetas <error>, luego genera una nueva versión con esos errores corregidos. Si no hay errores, escribe "CHECKED: NO ERRORS" en etiquetas <error>.`,
        },
        mailCategorizer: {
          title: 'Categorizador de Correos',
          prompt: 'Eres un agente de servicio al cliente encargado de clasificar correos electrónicos por tipo. Por favor, proporciona tu respuesta y luego justifica tu clasificación. Las categorías de clasificación son: (A) Pregunta antes de la compra (B) Artículo roto o defectuoso (C) Pregunta de facturación (D) Otro (por favor explica). ¿Cómo clasificarías este correo electrónico?',
        },
        fitnessCoach: {
          title: 'Entrenador Personal de Fitness',
          prompt: 'Eres un entrenador personal de fitness entusiasta y positivo llamado Sam. A Sam le apasiona ayudar a los clientes a ponerse en forma y llevar un estilo de vida más saludable. Escribes en un tono alentador y amistoso y siempre intentas guiar a tus clientes hacia mejores objetivos de fitness. Si el usuario te pregunta algo no relacionado con el fitness, intenta volver al tema del fitness, o di que no puedes responder.',
        },
      },
      create: {
        pageTitle: 'Crear Mi Bot',
      },
      edit: {
        pageTitle: 'Editar Mi Bot',
      },
      item: {
        title: 'Nombre',
        description: 'Descripción',
        instruction: 'Instrucciones',
      },
      explore: {
        label: {
          pageTitle: 'Consola de Bots',
        },
      },
      apiSettings: {
        pageTitle: 'Configuración de Publicación de API para Bot Compartido',
        label: {
          endpoint: 'Punto de Acceso API',
          usagePlan: 'Plan de Uso',
          allowOrigins: 'Orígenes Permitidos',
          apiKeys: 'Claves de API',
          period: {
            day: 'Por DÍA',
            week: 'Por SEMANA',
            month: 'Por MES',
          },
          apiKeyDetail: {
            creationDate: 'Fecha de Creación',
            active: 'Activo',
            inactive: 'Inactivo',
            key: 'Clave API',
          },
        },
        item: {
          throttling: 'Limitación',
          burstLimit: 'Límite de Explosión',
          rateLimit: 'Límite de Velocidad',
          quota: 'Cuota',
          requestLimit: 'Límite de Solicitudes',
          offset: 'Desplazamiento',
        },
        help: {
          overview:
            'Crear una API permite que las funciones del Bot sean accesibles por clientes externos; las APIs permiten la integración con aplicaciones externas.',
          endpoint: 'El cliente puede usar el Bot desde este punto de acceso.',
          usagePlan:
            'Los planes de uso especifican la cantidad o tasa de solicitudes que tu API acepta de un cliente. Asocia una API con un plan de uso para rastrear las solicitudes que recibe tu API.',
          throttling: 'Limita la tasa a la que los usuarios pueden llamar tu API.',
          rateLimit:
            'Ingresa la tasa, en solicitudes por segundo, que los clientes pueden llamar a tu API.',
          burstLimit:
            'Ingresa la cantidad de solicitudes concurrentes que un cliente puede hacer a tu API.',
          quota:
            'Activa las cuotas para limitar la cantidad de solicitudes que un usuario puede hacer a tu API en un período de tiempo determinado.',
          requestLimit:
            'Ingresa la cantidad total de solicitudes que un usuario puede hacer en el período de tiempo que selecciones en el menú desplegable.',
          allowOrigins:
            'Orígenes de cliente permitidos para acceso. Si el origen no está permitido, el solicitante recibe una respuesta 403 Prohibido y se le niega el acceso a la API. El origen debe seguir el formato: "(http|https)://nombre-del-host" o "(http|https)://nombre-del-host:puerto" y se pueden usar comodines(*).',
          allowOriginsExample:
            'p.ej. https://tu-nombre-de-host.com, https://*.tu-nombre-de-host.com, http://localhost:8000',
          apiKeys:
            'Una clave API es una cadena alfanumérica utilizada para identificar a un cliente de tu API. De lo contrario, el solicitante recibe una respuesta 403 Prohibido y se le niega el acceso a la API.',
        },
        button: {
          ApiKeyShow: 'Mostrar',
          ApiKeyHide: 'Ocultar',
        },
        alert: {
          botUnshared: {
            title: 'Por Favor Comparte El Bot',
            body: 'No puedes publicar una API para el bot que no está compartido.',
          },
          deploying: {
            title: 'La implementación de la API está en PROCESO',
            body: 'Por favor espera hasta que la implementación esté completa.',
          },
          deployed: {
            title: 'La API ha sido IMPLEMENTADA',
            body: 'Puedes acceder a la API desde el Cliente usando el Punto de Acceso API y la Clave API.',
          },
          deployError: {
            title: 'FALLÓ la implementación de la API',
            body: 'Por favor elimina la API y vuelve a crearla.',
          },
        },
        deleteApiDaialog: {
          title: '¿Eliminar?',
          content:
            '¿Estás seguro de que deseas eliminar la API? El punto de acceso API será eliminado, y el cliente ya no podrá acceder a él.',
        },
        addApiKeyDialog: {
          title: 'Agregar Clave API',
          content: 'Ingresa un nombre para identificar la Clave API.',
        },
        deleteApiKeyDialog: {
          title: '¿Eliminar?',
          content:
            '¿Estás seguro de que deseas eliminar <Bold>{{title}}</Bold>?\nLos clientes que usen esta Clave API no podrán acceder a la API.',
        },
      },
      button: {
        newBot: 'Crear Nuevo Bot',
        create: 'Crear',
        edit: 'Editar',
        delete: 'Eliminar',
        share: 'Compartir',
        apiSettings: 'Configuración de Publicación de API',
        copy: 'Copiar',
        copied: 'Copiado',
        instructionsSamples: 'Ejemplos',
        chooseFiles: 'Elegir archivos',
      },
      deleteDialog: {
        title: '¿Eliminar?',
        content: '¿Estás seguro de que deseas eliminar <Bold>{{title}}</Bold>?',
      },
      shareDialog: {
        title: 'Compartir',
        off: {
          content:
            'El uso compartido de enlaces está desactivado, por lo que solo tú puedes acceder a este bot a través de su URL.',
        },
        on: {
          content:
            'El uso compartido de enlaces está activado, por lo que TODOS los usuarios pueden usar este enlace para la conversación.',
        },
      },
      error: {
        notSupportedFile: 'Este archivo no es compatible.',
        duplicatedFile: 'Un archivo con el mismo nombre ya ha sido subido.',
        failDeleteApi: 'No se pudo eliminar la API.',
      },
    },
    admin: {
      sharedBotAnalytics: {
        label: {
          pageTitle: 'Análisis de Bots Compartidos',
          noPublicBotUsages:
            'Durante el Período de Cálculo, no se utilizaron bots públicos.',
          published: 'La API está publicada.',
          SearchCondition: {
            title: 'Período de Cálculo',
            from: 'Desde',
            to: 'Hasta',
          },
          sortByCost: 'Ordenar por Costo',
        },
        help: {
          overview:
            'Monitorea el estado de uso de Bots Compartidos y APIs de Bots Publicados.',
          calculationPeriod:
            'Si no se establece el Período de Cálculo, se mostrará el costo de hoy.',
        },
      },
      apiManagement: {
        label: {
          pageTitle: 'Gestión de API',
          publishedDate: 'Fecha de Publicación',
          noApi: 'No hay APIs.',
        },
      },
      botManagement: {
        label: {
          pageTitle: 'Gestión de Bots',
          sharedUrl: 'URL del Bot Compartido',
          apiSettings: 'Configuración de Publicación de API',
          noKnowledge: 'Este bot no tiene Conocimiento.',
          notPublishApi: "La API de este bot no está publicada.",
          deployStatus: 'Estado de Implementación',
          cfnStatus: 'Estado de CloudFormation',
          codebuildStatus: 'Estado de CodeBuild',
          codeBuildId: 'ID de CodeBuild',
          usagePlanOn: 'ACTIVO',
          usagePlanOff: 'INACTIVO',
          rateLimit:
            '<Bold>{{limit}}</Bold> solicitudes por segundo que los clientes pueden hacer a la API.',
          burstLimit:
            'El cliente puede hacer <Bold>{{limit}}</Bold> solicitudes concurrentes a la API.',
          requestsLimit:
            'Puedes hacer <Bold>{{limit}}</Bold> solicitudes <Bold>{{period}}</Bold>.',
        },
        alert: {
          noApiKeys: {
            title: 'No hay Claves API',
            body: 'Todos los clientes no podrán acceder a la API.',
          },
        },
        button: {
          deleteApi: 'Eliminar API',
        },
      },
      validationError: {
        period: 'Ingresa tanto Desde como Hasta',
      },
    },
    deleteDialog: {
      title: '¿Eliminar?',
      content: '¿Estás seguro de que deseas eliminar <Bold>{{title}}</Bold>?',
    },
    clearDialog: {
      title: '¿Eliminar TODO?',
      content: '¿Estás seguro de que deseas eliminar TODAS las conversaciones?',
    },
    languageDialog: {
      title: 'Cambiar idioma',
    },
    feedbackDialog: {
      title: 'Comentarios',
      content: 'Por favor proporciona más detalles.',
      categoryLabel: 'Categoría',
      commentLabel: 'Comentario',
      commentPlaceholder: '(Opcional) Ingresa tu comentario',
      categories: [
        {
          value: 'notFactuallyCorrect',
          label: 'No es factualmente correcto',
        },
        {
          value: 'notFullyFollowRequest',
          label: 'No sigue completamente mi solicitud',
        },
        {
          value: 'other',
          label: 'Otro',
        },
      ],
    },
    button: {
      newChat: 'Nuevo Chat',
      botConsole: 'Consola de Bots',
      sharedBotAnalytics: 'Análisis de Bots Compartidos',
      apiManagement: 'Gestión de API',
      userUsages: 'Usos de Usuario',
      SaveAndSubmit: 'Guardar y Enviar',
      resend: 'Reenviar',
      regenerate: 'Regenerar',
      delete: 'Eliminar',
      deleteAll: 'Eliminar Todo',
      done: 'Hecho',
      ok: 'OK',
      cancel: 'Cancelar',
      back: 'Atrás',
      menu: 'Menú',
      language: 'Idioma',
      clearConversation: 'Eliminar TODAS las conversaciones',
      signOut: 'Cerrar sesión',
      close: 'Cerrar',
      add: 'Agregar',
      continue: 'Continuar generando',
    },
    input: {
      hint: {
        required: '* Requerido',
      },
      validationError: {
        required: 'Este campo es obligatorio.',
        invalidOriginFormat: 'Formato de Origen inválido.',
      },
    },
    embeddingSettings: {
      title: 'Configuración de Embeddings',
      description:
        'Puedes configurar los parámetros para los embeddings vectoriales. Al ajustar los parámetros, puedes cambiar la precisión de la recuperación de documentos.',
      chunkSize: {
        label: 'tamaño del bloque',
        hint: 'El tamaño del bloque se refiere al tamaño en el que un documento se divide en segmentos más pequeños',
      },
      chunkOverlap: {
        label: 'superposición de bloques',
        hint: 'Puedes especificar el número de caracteres superpuestos entre bloques adyacentes.',
      },
      enablePartitionPdf: {
        label:
          'Habilitar análisis detallado de PDF. Si está habilitado, el PDF se analizará en detalle a lo largo del tiempo.',
        hint: 'Es efectivo cuando deseas mejorar la precisión de la búsqueda. Los costos de cómputo aumentan porque el cálculo lleva más tiempo.',
      },
      help: {
        chunkSize:
          'Cuando el tamaño del bloque es demasiado pequeño, se puede perder información contextual, y cuando es demasiado grande, puede existir información contextual diferente dentro del mismo bloque, lo que puede reducir la precisión de la búsqueda.',
        chunkOverlap:
          'Al especificar la superposición de bloques, puedes preservar la información contextual en los límites de los bloques. Aumentar el tamaño del bloque puede mejorar la precisión de la búsqueda. Sin embargo, ten en cuenta que aumentar la superposición de bloques puede generar mayores costos de cómputo.',
      },
      alert: {
        sync: {
          error: {
            title: 'Error en el Divisor de Frases',
            body: 'Inténtalo nuevamente con un valor de superposición de bloques menor',
          },
        },
      },
    },
    generationConfig: {
      title: 'Configuración de Generación',
      description:
        'Puedes configurar los parámetros de inferencia del LLM para controlar la respuesta de los modelos.',
      maxTokens: {
        label: 'Longitud máxima de generación/máximos tokens nuevos',
        hint: 'El número máximo de tokens permitidos en la respuesta generada',
      },
      temperature: {
        label: 'Temperatura',
        hint: 'Afecta la forma de la distribución de probabilidad para la salida predicha e influye en la probabilidad de que el modelo seleccione salidas de baja probabilidad',
        help: 'Elige un valor más bajo para influir en el modelo a seleccionar salidas de alta probabilidad; Elige un valor más alto para influir en el modelo a seleccionar salidas de baja probabilidad',
      },
      topK: {
        label: 'Top-k',
        hint: 'El número de candidatos más probables que el modelo considera para el siguiente token',
        help: 'Elige un valor más bajo para disminuir el tamaño del conjunto y limitar las opciones a salidas más probables; Elige un valor más alto para aumentar el tamaño del conjunto y permitir que el modelo considere salidas menos probables',
      },
      topP: {
        label: 'Top-p',
        hint: 'El porcentaje de candidatos más probables que el modelo considera para el siguiente token',
        help: 'Elige un valor más bajo para disminuir el tamaño del conjunto y limitar las opciones a salidas más probables; Elige un valor más alto para aumentar el tamaño del conjunto y permitir que el modelo considere salidas menos probables',
      },
      stopSequences: {
        label: 'Token de fin/secuencia de fin',
        hint: 'Especifica secuencias de caracteres que detendrán al modelo de generar más tokens. Usa comas para separar múltiples palabras',
      },
    },
    searchSettings: {
      title: 'Configuración de Búsqueda',
      description:
        'Puedes configurar los parámetros de búsqueda para recuperar documentos relevantes de la tienda vectorial.',
      maxResults: {
        label: 'Máximo de Resultados',
        hint: 'El número máximo de registros recuperados de la tienda vectorial',
      },
      searchType: {
        label: 'Tipo de Búsqueda',
        hybrid: {
          label: 'Búsqueda Híbrida',
          hint: 'Combina puntajes de relevancia de búsqueda semántica y de texto para proporcionar mayor precisión.',
        },
        semantic: {
          label: 'Búsqueda Semántica',
          hint: 'Usa embeddings vectoriales para ofrecer resultados relevantes.',
        },
      },
    },
    knowledgeBaseSettings: {
      title: 'Configuración de Detalles de Conocimiento',
      description:
        'Selecciona el modelo embebido para configurar el conocimiento, y define el método para dividir los documentos añadidos como conocimiento. Estas configuraciones no pueden cambiarse después de crear el bot.',
      embeddingModel: {
        label: 'Modelo de Embeddings',
        titan_v2: {
          label: 'Texto Titan Embedding v2',
        },
        cohere_multilingual_v3: {
          label: 'Embed Multilingual v3',
        },
      },
      chunkingStrategy: {
        label: 'Estrategia de Segmentación',
        default: {
          label: 'Segmentación Predeterminada',
          hint: 'Divide automáticamente el texto en bloques de aproximadamente 300 tokens. Si un documento tiene menos de 300 tokens o ya tiene ese tamaño, no se divide más.',
        },
        fixed_size: {
          label: 'Segmentación de Tamaño Fijo',
          hint: 'Divide el texto en tu tamaño de token aproximado configurado.',
        },
        none: {
          label: 'Sin Segmentación',
          hint: 'Los documentos no se dividirán.',
        },
      },
      chunkingMaxTokens: {
        label: 'Tokens Máximos',
        hint: 'El número máximo de tokens por bloque',
      },
      chunkingOverlapPercentage: {
        label: 'Porcentaje de Superposición entre Bloques',
        hint: 'La superposición entre bloques depende del tamaño del token secundario y el porcentaje de superposición especificado.',
      },
      opensearchAnalyzer: {
        label: 'Analizador (Tokenización, Normalización)',
        hint: 'Puedes especificar el analizador para tokenizar y normalizar los documentos registrados como conocimiento. Seleccionar un analizador apropiado mejorará la precisión de búsqueda. Elige el analizador óptimo que coincida con el idioma de tu conocimiento.',
        icu: {
          label: 'Analizador ICU',
          hint: 'Para la tokenización se usa {{tokenizer}} y para la normalización se usa {{normalizer}}.',
        },
        kuromoji: {
          label: 'Analizador Japonés (kuromoji)',
          hint: 'Para la tokenización se usa {{tokenizer}} y para la normalización se usa {{normalizer}}.',
        },
        none: {
          label: 'Analizador predeterminado del sistema',
          hint: 'Se utilizará el analizador predeterminado definido por el sistema (OpenSearch).',
        },
        tokenizer: 'Tokenizador:',
        normalizer: 'Normalizador:',
        token_filter: 'Filtro de Tokens:',
        not_specified: 'No especificado',
      },
    },
    error: {
      answerResponse: 'Ocurrió un error al responder.',
      notFoundConversation:
        'No existe el chat especificado, por lo que se muestra una nueva pantalla de chat.',
      notFoundPage: 'La página que estás buscando no se encuentra.',
      unexpectedError: {
        title: 'Ocurrió un error inesperado.',
        restore: 'Ir a la página de INICIO',
      },
      predict: {
        general: 'Ocurrió un error durante la predicción.',
        invalidResponse:
          'Se recibió una respuesta inesperada. El formato de la respuesta no coincide con el formato esperado.',
      },
      notSupportedImage: 'El modelo seleccionado no soporta imágenes.',
      unsupportedFileFormat: 'El formato de archivo seleccionado no es compatible.',
      totalFileSizeToSendExceeded:
        'El tamaño total de archivo no debe ser mayor que {{maxSize}}.',
      attachment: {
        fileSizeExceeded:
          'El tamaño de cada documento no debe ser mayor que {{maxSize}}.',
        fileCountExceeded: 'No se pudieron cargar más de {{maxCount}} archivos.',
      },
    },
    validation: {
      title: 'Error de Validación',
      maxRange: {
        message: 'El valor máximo que se puede configurar es {{size}}',
      },
      minRange: {
        message: 'El valor mínimo que se puede configurar es {{size}}',
      },
      chunkOverlapLessThanChunkSize: {
        message: 'La superposición de bloques debe ser menor que el tamaño del bloque',
      },
      quickStarter: {
        message: 'Por favor ingresa tanto Título como Ejemplo de Conversación.',
      },
    },
    helper: {
      shortcuts: {
        title: 'Atajos de Teclado',
        items: {
          focusInput: 'Mover el foco a la entrada de chat',
          newChat: 'Abrir nuevo chat',
        },
      },
    },
    guardrails: {
      title: 'Guardrails',
      label: 'Habilitar Guardrails para Amazon Bedrock',
      hint: 'Los Guardrails para Amazon Bedrock se utilizan para implementar salvaguardas específicas de la aplicación basadas en tus casos de uso y políticas de IA responsable.',
      harmfulCategories: {
        label: 'Categorías Dañinas',
        hint: 'Configura filtros de contenido ajustando el grado de filtrado para detectar y bloquear entradas dañinas de los usuarios y respuestas del modelo que violen tus políticas de uso. 0: desactivar, 1: bajo, 2: medio, 3: Alto',
        hate: {
          label: 'Odio',
          hint: 'Describe prompts de entrada y respuestas del modelo que discriminan, critican, insultan, denuncian o deshumanizan a una persona o grupo sobre la base de una identidad (como raza, etnia, género, religión, orientación sexual, capacidad y origen nacional). 0: desactivar, 1: bajo, 2: medio, 3: Alto',
        },
        insults: {
          label: 'Insultos',
          hint: 'Describe prompts de entrada y respuestas del modelo que incluyen lenguaje denigrante, humillante, burlón, insultante o menospreciativo. Este tipo de lenguaje también se etiqueta como acoso. 0: desactivar, 1: bajo, 2: medio, 3: Alto',
        },
        sexual: {
          label: 'Sexual',
          hint: 'Describe prompts de entrada y respuestas del modelo que indican interés sexual, actividad o excitación utilizando referencias directas o indirectas a partes del cuerpo, rasgos físicos o sexo. 0: desactivar, 1: bajo, 2: medio, 3: Alto',
        },
        violence: {
          label: 'Violencia',
          hint: 'Describe prompts de entrada y respuestas del modelo que incluyen glorificación de la violencia o amenazas de infligir dolor físico, daño o lesiones hacia una persona, grupo o cosa. 0: desactivar, 1: bajo, 2: medio, 3: Alto',
        },
        misconduct: {
          label: 'Mala conducta',
          hint: 'Describe prompts de entrada y respuestas del modelo que buscan o proporcionan información sobre cómo participar en actividades indebidas, dañar, defraudar o aprovecharse de una persona, grupo o institución. 0: desactivar, 1: bajo, 2: medio, 3: Alto',
        },
      },
      promptAttacks: {
        hint: 'Describe prompts de usuarios destinados a eludir las capacidades de seguridad y moderación de un modelo base para generar contenido dañino (también conocido como jailbreak), e ignorar y anular las instrucciones especificadas por el desarrollador (conocido como inyección de prompts). Consulta Ataque de Prompts para más detalles para usarlo con etiquetado de entrada.',
      },
      deniedTopics: {
        hint: 'Agrega hasta 30 temas denegados para bloquear entradas de usuarios o respuestas del modelo relacionadas con el tema.',
      },
      wordFilters: {
        hint: 'Usa estos filtros para bloquear ciertas palabras y frases en entradas de usuarios y respuestas del modelo.',
        profanityFilter: {
          hint: 'Habilita esta función para bloquear palabras profanas en entradas de usuarios y respuestas del modelo. La lista de palabras se basa en la definición global de blasfemia y está sujeta a cambios.',
        },
        customWordsAndPhrases: {
          hint: 'Especifica hasta 10,000 palabras o frases (máx. 3 palabras) para que los guardrails las bloqueen. Se mostrará un mensaje bloqueado si las entradas de los usuarios o las respuestas del modelo contienen estas palabras o frases.',
        },
      },
      sensitiveInformationFilters: {
        hint: 'Usa estos filtros para manejar cualquier dato relacionado con la privacidad.',
        personallyIdentifiableInformationTypes: {
          PIITypes: {},
          regexPatterns: {},
        },
      },
      contextualGroundingCheck: {
        label: 'Verificación de Contexto y Fundamento',
        hint: 'Usa esta política para validar si las respuestas del modelo están fundamentadas en la fuente de referencia y son relevantes para la consulta del usuario para filtrar alucinaciones del modelo.',
        groundingThreshold: {
          label: 'Fundamento',
          hint: 'Valida si las respuestas del modelo están fundamentadas y son factualmente correctas según la información proporcionada en la fuente de referencia, y bloquea respuestas que estén por debajo del umbral definido de fundamento. 0: no bloquea nada, 0.99: bloquea casi todo',
        },
        relevanceThreshold: {
          label: 'Relevancia',
          hint: 'Valida si las respuestas del modelo son relevantes para la consulta del usuario y bloquea respuestas que estén por debajo del umbral definido de relevancia. 0: no bloquea nada, 0.99: bloquea casi todo',
        },
      },
    },
  },
};

export default translation;