const translation = {
  translation: {
    signIn: {
      button: {
        login: 'Logg inn',
      },
    },
    app: {
      name: 'ACO-gpt',
      nameWithoutClaude: 'ACO-gpt',
      inputMessage: 'Send en melding',
      starredBots: 'Favorittbot',
      recentlyUsedBots: 'Nylig brukte boter',
      conversationHistory: 'Historikk',
      chatWaitingSymbol: '▍',
      adminConsoles: 'Kun administrator',
    },
    agent: {
      label: 'Agent',
      help: {
        overview:
          'Ved å bruke agentfunksjonaliteten kan chatboten din automatisk håndtere mer komplekse oppgaver.',
      },
      hint: `Agenten bestemmer automatisk hvilke verktøy som skal brukes for å svare på brukerens spørsmål. På grunn av tiden som kreves for avgjørelsen, har responsen en tendens til å ta lengre tid. Aktivering av ett eller flere verktøy muliggjør agentens funksjonalitet. Omvendt, hvis ingen verktøy er valgt, blir ikke agentens funksjonalitet brukt. Når agentens funksjonalitet er aktivert, blir også "Kunnskap" behandlet som et av verktøyene. Dette betyr at "Kunnskap" kanskje ikke blir brukt i svar.`,
      progress: {
        label: 'Tenker...',
      },
      progressCard: {
        toolInput: 'Inndata: ',
        toolOutput: 'Utdata: ',
        status: {
          running: 'Kjører...',
          success: 'Suksess',
          error: 'Feil',
        },
        app: {
          name: 'Bedrock Chat',
          inputMessage: 'Send en melding',
          starredBots: 'Favorittbot',
          recentlyUsedBots: 'Nylig brukte boter',
          conversationHistory: 'Historikk',
          chatWaitingSymbol: '▍',
          adminConsoles: 'Kun administrator',
        },
        sql_db_query: {
          name: 'Databaseforespørsel',
          description:
            'Utfør en detaljert og korrekt SQL-forespørsel for å hente resultater fra databasen.',
        },
        sql_db_schema: {
          name: 'Databaseskjema',
          description:
            'Hent skjemaet og eksempelrader for en liste over tabeller.',
        },
        sql_db_list_tables: {
          name: 'List opp databasetabeller',
          description: 'List opp alle tilgjengelige tabeller i databasen.',
        },
        sql_db_query_checker: {
          name: 'Forespørselskontroll',
          description: 'Sjekk om din SQL-forespørsel er korrekt før kjøring.',
        },
        internet_search: {
          name: 'Internett-søk',
          description: 'Søk på internett etter informasjon.',
        },
      },
    },
    bot: {
      label: {
        myBots: 'Mine boter',
        recentlyUsedBots: 'Nylig brukte delte boter',
        knowledge: 'Kunnskap',
        url: 'URL',
        s3url: 'S3-datakilde',
        sitemap: 'Sitemap URL',
        file: 'Fil',
        loadingBot: 'Laster...',
        normalChat: 'Chat',
        notAvailableBot: '[IKKE tilgjengelig]',
        notAvailableBotInputMessage: 'Denne boten er IKKE tilgjengelig.',
        noDescription: 'Ingen beskrivelse',
        notAvailable: 'Denne boten er IKKE tilgjengelig.',
        noBots: 'Ingen boter.',
        noBotsRecentlyUsed: 'Ingen nylig brukte delte boter.',
        retrievingKnowledge: '[Henter kunnskap...]',
        dndFileUpload:
          'Du kan laste opp filer ved å dra og slippe.\nStøttede filer: {{fileExtensions}}',
        uploadError: 'Feilmelding',
        referenceLink: 'Referanselenke',
        syncStatus: {
          queue: 'Venter på synkronisering',
          running: 'Synkroniserer',
          success: 'Synkronisering fullført',
          fail: 'Synkronisering mislyktes',
        },
        fileUploadStatus: {
          uploading: 'Laster opp...',
          uploaded: 'Opplastet',
          error: 'FEIL',
        },
        quickStarter: {
          title: 'Samtale Quick Starter',
          exampleTitle: 'Tittel',
          example: 'Eksempel på samtale',
        },
        citeRetrievedContexts: 'Sitering av hentet kontekst',
        unsupported: 'Ikke støttet, skrivebeskyttet',
      },
      titleSubmenu: {
        edit: 'Rediger',
        copyLink: 'Kopier lenke',
        copiedLink: 'Kopiert',
      },
      help: {
        overview:
          'Boter opererer i henhold til forhåndsdefinerte instruksjoner. Chat fungerer ikke som ønsket med mindre konteksten er definert i meldingen, men med boter er det ikke nødvendig å definere konteksten.',
        instructions:
          'Definer hvordan boten skal oppføre seg. Å gi tvetydige instruksjoner kan føre til uforutsigbar oppførsel, så gi klare og spesifikke instruksjoner.',
        knowledge: {
          overview:
            'Ved å gi ekstern kunnskap til boten, blir den i stand til å håndtere data den ikke er forhåndstrent på.',
          url: 'Informasjonen fra den spesifiserte URL-en vil bli brukt som kunnskap.',
          s3url:
            'Ved å angi S3 URI kan du legge til S3 som en datakilde. Du kan legge til opptil 4 kilder. Det støtter kun bøtter som eksisterer i samme konto og samme region som distribusjonsdestinasjonen.',
          sitemap:
            'Ved å spesifisere URL-en til sitemap, vil informasjonen som hentes gjennom automatisk skraping av nettsteder innenfor den brukes som kunnskap.',
          file: 'De opplastede filene vil bli brukt som kunnskap.',
          citeRetrievedContexts:
            'Konfigurer om du vil vise konteksten som er hentet for å svare på brukerforespørsler som siteringsinformasjon.\nHvis aktivert, kan brukere få tilgang til de opprinnelige kilde-URL-ene eller filene.',
        },
        quickStarter: {
          overview:
            'Når du starter en samtale, gi eksempler. Eksempler illustrerer hvordan man bruker boten.',
        },
      },
      alert: {
        sync: {
          error: {
            title: 'Feil ved synkronisering av kunnskap',
            body: 'En feil oppstod under synkronisering av kunnskap. Vennligst sjekk følgende melding:',
          },
          incomplete: {
            title: 'IKKE klar',
            body: 'Denne boten har ikke fullført kunnskapssynkroniseringen, så kunnskapen før oppdateringen brukes.',
          },
        },
      },
      samples: {
        title: 'Instruksjonseksempler',
        anthropicLibrary: {
          title: 'Anthropic Prompt-bibliotek',
          sentence: 'Trenger du flere eksempler? Besøk: ',
          url: 'https://docs.anthropic.com/claude/prompt-library',
        },
        pythonCodeAssistant: {
          title: 'Python-kodingsassistent',
          prompt: `Skriv et kort og høykvalitets python-skript for den gitte oppgaven, noe en veldig dyktig python-ekspert ville skrevet. Du skriver kode for en erfaren utvikler, så legg kun til kommentarer for ting som ikke er åpenbare. Sørg for å inkludere nødvendige imports. 
ALDRI skriv noe før en \`\`\`python\`\`\` blokk. Etter du er ferdig å generere kode, og etter  \`\`\`python\`\`\` blokken, sjekk over arbeidet nøye for å passe på at det ikek er noen feil, errors, eller inkonsistens. Hvis det er errors, list dem i <error> tags, så generer en ny versjon der disse erroene er fikset. Hvis det ikke er noen feil, skriv "CHECKED: NO ERRORS" i <error> tags.`,
        },
        mailCategorizer: {
          title: 'E-postkategoriserer',
          prompt: `Du er en kundeservicemedarbeider som har i oppgave å klassifisere e-poster etter type. Vennligst gi svaret ditt og rettferdiggjør klassifiseringen din. 

Klassifiseringskategoriene er: 
(A) Før-salg spørsmål 
(B) Ødelagt eller defekt vare 
(C) Fakturaspørsmål 
(D) Annet (vennligst forklar)

Hvordan vil du kategorisere denne e-posten?`,
        },
        fitnessCoach: {
          title: 'Personlig treningscoach',
          prompt: `Du er en entusiastisk personlig treningscoach ved navn Sam. Sam er lidenskapelig opptatt av å hjelpe klienter med å komme i form og leve sunnere livsstiler. Du skriver i en oppmuntrende og vennlig tone og prøver alltid å veilede klientene dine mot bedre treningsmål. Hvis brukeren spør deg om noe som ikke er relatert til trening, bring enten emnet tilbake til trening, eller si at du ikke kan svare.`,
        },
      },
      create: {
        pageTitle: 'Opprett min bot',
      },
      edit: {
        pageTitle: 'Rediger min bot',
      },

      item: {
        title: 'Navn',
        description: 'Beskrivelse',
        instruction: 'Instruksjoner',
      },
      explore: {
        label: {
          pageTitle: 'Botkonsoll',
        },
      },
      apiSettings: {
        pageTitle: 'Innstillinger for publisering av delt bot-API',
        label: {
          endpoint: 'API-endepunkt',
          usagePlan: 'Bruksplan',
          allowOrigins: 'Tillatte opprinnelser',
          apiKeys: 'API-nøkler',
          period: {
            day: 'Per DAG',
            week: 'Per UKE',
            month: 'Per MÅNED',
          },
          apiKeyDetail: {
            creationDate: 'Opprettelsesdato',
            active: 'Aktiv',
            inactive: 'Inaktiv',
            key: 'API-nøkkel',
          },
        },
        item: {
          throttling: 'Gjennomstrømming',
          burstLimit: 'Burst',
          rateLimit: 'Hastighet',
          quota: 'Kvote',
          requestLimit: 'Forespørsler',
          offset: 'Forskyvning',
        },
        help: {
          overview:
            'Å opprette et API gjør at botens funksjoner kan nås av eksterne klienter; API-er muliggjør integrasjon med eksterne applikasjoner.',
          endpoint: 'Klienten kan bruke boten fra dette endepunktet.',
          usagePlan:
            'Bruksplaner spesifiserer antallet eller frekvensen av forespørsler som API-en din godtar fra en klient. Assosier et API med en bruksplan for å spore forespørslene API-en din mottar.',
          throttling: 'Begrens frekvensen brukere kan kalle API-en din.',
          rateLimit:
            'Angi frekvensen, i forespørsler per sekund, som klienter kan kalle API-en din.',
          burstLimit:
            'Angi antall samtidige forespørsler en klient kan gjøre til API-en din.',
          quota:
            'Aktiver kvoter for å begrense antall forespørsler en bruker kan gjøre til API-en din i en gitt tidsperiode.',
          requestLimit:
            'Angi totalt antall forespørsler en bruker kan gjøre i tidsperioden du velger i nedtrekkslisten.',
          allowOrigins:
            'Tillatte klientopprinnelser for tilgang. Hvis opprinnelsen ikke er tillatt, mottar den som kaller en 403 Forbudt-respons og nektes tilgang til API-en. Opprinnelsen må følge formatet: "(http|https)://vert-navn" eller "(http|https)://vert-navn:port", og jokertegn (*) kan brukes.',
          allowOriginsExample:
            'f.eks. https://ditt-vert-navn.com, https://*.ditt-vert-navn.com, http://localhost:8000',
          apiKeys:
            'En API-nøkkel er en alfanumerisk streng som brukes til å identifisere en klient av API-en din. Ellers mottar den som kaller en 403 Forbudt-respons og nektes tilgang til API-en.',
        },
        button: {
          ApiKeyShow: 'Vis',
          ApiKeyHide: 'Skjul',
        },
        alert: {
          botUnshared: {
            title: 'Vennligst del boten',
            body: 'Du kan ikke publisere et API for en bot som ikke er delt.',
          },
          deploying: {
            title: 'API-distribusjonen er UNDER PROSESS',
            body: 'Vennligst vent til distribusjonen er fullført.',
          },
          deployed: {
            title: 'API-en er DISTRIBUERT',
            body: 'Du kan få tilgang til API-en fra klienten ved å bruke API-endepunktet og API-nøkkelen.',
          },
          deployError: {
            title: 'MISLYKTES å distribuere API-en',
            body: 'Vennligst slett API-en og opprett API-en på nytt.',
          },
        },
        deleteApiDaialog: {
          title: 'Slette?',
          content:
            'Er du sikker på at du vil slette API-en? API-endepunktet vil bli slettet, og klienten vil ikke lenger ha tilgang til det.',
        },
        addApiKeyDialog: {
          title: 'Legg til API-nøkkel',
          content: 'Skriv inn et navn for å identifisere API-nøkkelen.',
        },
        deleteApiKeyDialog: {
          title: 'Slette?',
          content:
            'Er du sikker på at du vil slette <Bold>{{title}}</Bold>?\nKlienter som bruker denne API-nøkkelen vil bli nektet tilgang til API-en.',
        },
      },
      button: {
        newBot: 'Opprett ny bot',
        create: 'Opprett',
        edit: 'Rediger',
        delete: 'Slett',
        share: 'Del',
        apiSettings: 'API-publiseringsinnstillinger',
        copy: 'Kopier',
        copied: 'Kopiert',
        instructionsSamples: 'Eksempler',
        chooseFiles: 'Velg filer',
      },
      deleteDialog: {
        title: 'Slette?',
        content: 'Er du sikker på at du vil slette <Bold>{{title}}</Bold>?',
      },
      shareDialog: {
        title: 'Del',
        off: {
          content:
            'Lenkedelingsfunksjonen er av, så kun du kan få tilgang til denne boten gjennom URL-en.',
        },
        on: {
          content:
            'Lenkedelingsfunksjonen er på, så ALLE brukere kan bruke denne lenken til samtale.',
        },
      },
      error: {
        notSupportedFile: 'Denne filen støttes ikke.',
        duplicatedFile: 'En fil med samme navn har blitt lastet opp.',
        failDeleteApi: 'Kunne ikke slette API-en.',
      },
    },
    admin: {
      botAnalytics: {
        label: {
          pageTitle: 'Analyser for delt bot',
          noBotUsages: 'I løpet av beregningsperioden ble ingen boter brukt.',
          published: 'API er publisert.',
          SearchCondition: {
            title: 'Beregningstidspunkt',
            from: 'Fra',
            to: 'Til',
          },
          sortByCost: 'Sorter etter kostnad',
        },
        help: {
          overview: 'Overvåk bruksstatusen for boter og publiserte bot-API-er.',
          calculationPeriod:
            'Hvis beregningsperioden ikke er satt, vil kostnaden for i dag bli vist.',
        },
      },
      apiManagement: {
        label: {
          pageTitle: 'API-administrasjon',
          publishedDate: 'Publiseringsdato',
          noApi: 'Ingen API-er.',
        },
      },
      botManagement: {
        label: {
          pageTitle: 'Botadministrasjon',
          sharedUrl: 'Delt bot-URL',
          apiSettings: 'API-publiseringsinnstillinger',
          noKnowledge: 'Denne boten har ingen kunnskap.',
          notPublishApi: 'Denne botens API er ikke publisert.',
          deployStatus: 'Distribusjonsstatus',
          cfnStatus: 'CloudFormation-status',
          codebuildStatus: 'CodeBuild-status',
          codeBuildId: 'CodeBuild-ID',
          usagePlanOn: 'PÅ',
          usagePlanOff: 'AV',
          rateLimit:
            '<Bold>{{limit}}</Bold> forespørsler per sekund, som klienter kan kalle API-en.',
          burstLimit:
            'Klienten kan gjøre <Bold>{{limit}}</Bold> samtidige forespørsler til API-en.',
          requestsLimit:
            'Du kan gjøre <Bold>{{limit}}</Bold> forespørsler <Bold>{{period}}</Bold>.',
        },
        alert: {
          noApiKeys: {
            title: 'Ingen API-nøkler',
            body: 'Alle klienter kan ikke få tilgang til API-en.',
          },
        },
        button: {
          deleteApi: 'Slett API',
        },
      },
      validationError: {
        period: 'Skriv inn både Fra og Til',
      },
    },
    deleteDialog: {
      title: 'Slette?',
      content: 'Er du sikker på at du vil slette <Bold>{{title}}</Bold>?',
    },
    clearDialog: {
      title: 'Slette ALT?',
      content: 'Er du sikker på at du vil slette ALLE samtaler?',
    },
    languageDialog: {
      title: 'Bytt språk',
    },
    feedbackDialog: {
      title: 'Tilbakemelding',
      content: 'Vennligst gi flere detaljer.',
      categoryLabel: 'Kategori',
      commentLabel: 'Kommentar',
      commentPlaceholder: '(Valgfritt) Skriv inn din kommentar',
      categories: [
        {
          value: 'notFactuallyCorrect',
          label: 'Ikke faktuelt korrekt',
        },
        {
          value: 'notFullyFollowRequest',
          label: 'Følger ikke fullt ut forespørselen min',
        },
        {
          value: 'other',
          label: 'Annet',
        },
      ],
    },
    button: {
      newChat: 'Ny chat',
      botConsole: 'Botkonsoll',
      botAnalytics: 'Analyser for bot',
      apiManagement: 'API-administrasjon',
      userUsages: 'Brukerbruk',
      SaveAndSubmit: 'Lagre og send inn',
      resend: 'Send på nytt',
      regenerate: 'Regenerer',
      delete: 'Slett',
      deleteAll: 'Slett alle',
      done: 'Ferdig',
      ok: 'OK',
      cancel: 'Avbryt',
      back: 'Tilbake',
      menu: 'Meny',
      language: 'Språk',
      clearConversation: 'Slett ALLE samtaler',
      signOut: 'Logg ut',
      close: 'Lukk',
      add: 'Legg til',
      continue: 'Fortsett å generere',
    },
    input: {
      hint: {
        required: '* Obligatorisk',
      },
      validationError: {
        required: 'Dette feltet er obligatorisk.',
        invalidOriginFormat: 'Ugyldig opprinnelsesformat.',
      },
    },
    embeddingSettings: {
      title: 'Innstilling av innebygging',
      description:
        'Du kan konfigurere parameterne for vektorinnebygginger. Ved å justere parameterne kan du endre nøyaktigheten av dokumenthenting.',
      chunkSize: {
        label: 'størrelse på chunk',
        hint: 'Størrelsen på chunk refererer til størrelsen et dokument deles opp i mindre segmenter på',
      },
      chunkOverlap: {
        label: 'overlapp mellom chunks',
        hint: 'Du kan spesifisere antall overlappende tegn mellom tilstøtende chunks.',
      },
      enablePartitionPdf: {
        label:
          'Aktiver detaljert PDF-analyse. Hvis aktivert, vil PDF-en bli analysert i detalj over tid.',
        hint: 'Det er effektivt når du vil forbedre søkenøyaktigheten. Beregningskostnadene øker fordi beregningen tar lengre tid.',
      },
      help: {
        chunkSize:
          'Når chunk-størrelsen er for liten, kan kontekstuell informasjon gå tapt, og når den er for stor, kan ulik kontekstuell informasjon eksistere innenfor samme chunk, noe som potensielt reduserer søkenøyaktigheten.',
        chunkOverlap:
          'Ved å spesifisere chunk-overlapp kan du bevare kontekstuell informasjon rundt chunk-grensene. Å øke chunk-størrelsen kan noen ganger forbedre søkenøyaktigheten. Vær imidlertid oppmerksom på at økt chunk-overlapp kan føre til høyere beregningskostnader.',
      },
      alert: {
        sync: {
          error: {
            title: 'Feil ved setningsdeling',
            body: 'Prøv igjen med mindre chunk-overlappverdi',
          },
        },
      },
    },
    generationConfig: {
      title: 'Generasjonskonfigurasjon',
      description:
        'Du kan konfigurere LLM-inferensparametere for å kontrollere responsen fra modellene.',
      maxTokens: {
        label: 'Maksimal generasjonslengde/maksimalt nye tokens',
        hint: 'Det maksimale antallet tokens tillatt i den genererte responsen',
      },
      temperature: {
        label: 'Temperatur',
        hint: 'Påvirker formen på sannsynlighetsfordelingen for den predikerte output og påvirker sannsynligheten for at modellen velger lavere sannsynlighetsoutputs',
        help: 'Velg en lavere verdi for å påvirke modellen til å velge høyere sannsynlighetsoutputs; Velg en høyere verdi for å påvirke modellen til å velge lavere sannsynlighetsoutputs',
      },
      topK: {
        label: 'Top-k',
        hint: 'Antallet mest sannsynlige kandidater som modellen vurderer for neste token',
        help: 'Velg en lavere verdi for å redusere størrelsen på bassenget og begrense alternativene til mer sannsynlige outputs; Velg en høyere verdi for å øke størrelsen på bassenget og la modellen vurdere mindre sannsynlige outputs',
      },
      topP: {
        label: 'Top-p',
        hint: 'Prosentandelen av de mest sannsynlige kandidatene som modellen vurderer for neste token',
        help: 'Velg en lavere verdi for å redusere størrelsen på bassenget og begrense alternativene til mer sannsynlige outputs; Velg en høyere verdi for å øke størrelsen på bassenget og la modellen vurdere mindre sannsynlige outputs',
      },
      stopSequences: {
        label: 'Slutt token/slutt sekvens',
        hint: 'Spesifiser sekvenser av tegn som stopper modellen fra å generere flere tokens. Bruk komma for å skille flere ord',
      },
    },
    searchSettings: {
      title: 'Søkeinnstillinger',
      description:
        'Du kan konfigurere søkeparametere for å hente relevante dokumenter fra vektorlageret.',
      maxResults: {
        label: 'Maksimalt antall resultater',
        hint: 'Det maksimale antallet poster hentet fra vektorlageret',
      },
      searchType: {
        label: 'Søketype',
        hybrid: {
          label: 'Hybrid søk',
          hint: 'Kombinerer relevansscore fra semantisk og tekstsøk for å gi større nøyaktighet.',
        },
        semantic: {
          label: 'Semantisk søk',
          hint: 'Bruker vektorinnebygginger for å levere relevante resultater.',
        },
      },
    },
    knowledgeBaseSettings: {
      title: 'Detaljerte kunnskapsinnstillinger',
      description:
        'Velg den innebygde modellen for å konfigurere kunnskap, og sett metoden for å dele opp dokumenter som legges til som kunnskap. Disse innstillingene kan ikke endres etter at boten er opprettet.',
      embeddingModel: {
        label: 'Innebyggingsmodell',
        titan_v1: {
          label: 'Titan Embeddings G1 - Tekst v1.2',
        },
        cohere_multilingual_v3: {
          label: 'Embed Multilingual v3',
        },
      },
      chunkingStrategy: {
        label: 'Chunking-strategi',
        default: {
          label: 'Standard chunking',
          hint: 'Deler automatisk opp tekst i biter på omtrent 300 tokens i størrelse som standard. Hvis et dokument er mindre enn eller allerede 300 tokens, deles det ikke ytterligere.',
        },
        fixed_size: {
          label: 'Fast størrelse chunking',
          hint: 'Deler opp tekst i din angitte omtrentlige tokens størrelse.',
        },
        none: {
          label: 'Ingen chunking',
          hint: 'Dokumenter vil ikke bli delt opp.',
        },
      },
      chunkingMaxTokens: {
        label: 'Maksimalt antall tokens',
        hint: 'Det maksimale antallet tokens per chunk',
      },
      chunkingOverlapPercentage: {
        label: 'Overlappingsprosent mellom chunks',
        hint: 'Overlapp mellom overordnede chunks avhenger av den underordnede tokens størrelsen og underordnet prosentvis overlapp du spesifiserer.',
      },
      opensearchAnalyzer: {
        label: 'Analyzer (Tokenisering, Normalisering)',
        hint: 'Du kan spesifisere analyzeren for å tokenisere og normalisere dokumentene som er registrert som kunnskap. Å velge en passende analyzer vil forbedre søkenøyaktigheten. Vennligst velg den optimale analyzeren som matcher språket i din kunnskap.',
        icu: {
          label: 'ICU-analyzer',
          hint: 'For tokenisering brukes {{tokenizer}}, og for normalisering brukes {{normalizer}}.',
        },
        kuromoji: {
          label: 'Japansk (kuromoji) analyzer',
          hint: 'For tokenisering brukes {{tokenizer}}, og for normalisering brukes {{normalizer}}.',
        },
        none: {
          label: 'Systemstandard analyzer',
          hint: 'Standardanalyzeren definert av systemet (OpenSearch) vil bli brukt.',
        },
        tokenizer: 'Tokeniserer:',
        normalizer: 'Normaliserer:',
        token_filter: 'Tokenfilter:',
        not_specified: 'Ikke spesifisert',
      },
    },
    error: {
      answerResponse: 'En feil oppstod under svar.',
      notFoundConversation:
        'Siden den spesifiserte chatten ikke eksisterer, vises en ny chat-skjerm.',
      notFoundPage: 'Siden du leter etter ble ikke funnet.',
      unexpectedError: {
        title: 'En uventet feil har oppstått.',
        restore: 'Gå til TOPP-siden',
      },
      predict: {
        general: 'En feil oppstod under prediksjon.',
        invalidResponse:
          'Uventet respons mottatt. Responsformatet samsvarer ikke med forventet format.',
      },
      notSupportedImage: 'Den valgte modellen støtter ikke bilder.',
      unsupportedFileFormat: 'Det valgte filformatet støttes ikke.',
      totalFileSizeToSendExceeded:
        'Den totale filstørrelsen må ikke overstige {{maxSize}}.',
      attachment: {
        fileSizeExceeded:
          'Hver dokumentstørrelse må ikke overstige {{maxSize}}.',
        fileCountExceeded: 'Kunne ikke laste opp mer enn {{maxCount}} filer.',
      },
    },
    validation: {
      title: 'Validation Error',
      maxRange: {
        message: 'Max verdien som kan bli satt er {{size}}',
      },
      minRange: {
        message: 'Minimum verdien som kan bli satt er {{size}}',
      },
      chunkOverlapLessThanChunkSize: {
        message: 'Chunk overlap må bli satt til mindre enn Chunk size',
      },
      quickStarter: {
        message: 'Vennligst sett inn både Tittel og chat eksempel.',
      },
    },
    helper: {
      shortcuts: {
        title: 'Snarvei taster',
        items: {
          focusInput: 'Bytt fokus til chat input',
          newChat: 'Åpne en ny chat',
        },
      },
    },
    guardrails: {
      title: 'Guardrails',
      label: 'Enable Guardrails for Amazon Bedrock',
      hint: 'Guardrails for Amazon Bedrock are used to implement application-specific safeguards based on your use cases and responsible AI policies.',
      harmfulCategories: {
        label: 'Harmful Categories',
        hint: 'Configure content filters by adjusting the degree of filtering to detect and block harmful user inputs and model responses that violate your usage policies. 0: disable, 1: low, 2: middle, 3: High',
        hate: {
          label: 'Hate',
          hint: 'Describes input prompts and model responses that discriminate, criticize, insult, denounce, or dehumanize a person or group on the basis of an identity (such as race, ethnicity, gender, religion, sexual orientation, ability, and national origin). 0: disable, 1: low, 2: middle, 3: High',
        },
        insults: {
          label: 'Insults',
          hint: 'Describes input prompts and model responses that includes demeaning, humiliating, mocking, insulting, or belittling language. This type of language is also labeled as bullying. 0: disable, 1: low, 2: middle, 3: High',
        },
        sexual: {
          label: 'Sexual',
          hint: 'Describes input prompts and model responses that indicates sexual interest, activity, or arousal using direct or indirect references to body parts, physical traits, or sex. 0: disable, 1: low, 2: middle, 3: High',
        },
        violence: {
          label: 'Violence',
          hint: 'Describes input prompts and model responses that includes glorification of or threats to inflict physical pain, hurt, or injury toward a person, group or thing. 0: disable, 1: low, 2: middle, 3: High ',
        },
        misconduct: {
          label: 'Misconduct',
          hint: 'Describes input prompts and model responses that seeks or provides information about engaging in misconduct activity, or harming, defrauding, or taking advantage of a person, group or institution. 0: disable, 1: low, 2: middle, 3: High',
        },
      },
      contextualGroundingCheck: {
        label: 'Sjekk av kontekstuell forankring',
        hint: 'Bruk denne policyen for å validere om modellens svar er forankret i referansekilden og relevante for brukerens forespørsel for å filtrere modellhallusinasjoner.',
        groundingThreshold: {
          label: 'Forankring',
          hint: 'alider om modellsvarene er forankret og faktisk korrekte basert på informasjonen gitt i referansekilden, og blokker svar som er under den definerte terskelen for forankring. 0: blokkerer ingenting, 0,99: blokkerer nesten alt',
        },
        relevanceThreshold: {
          label: 'Relevans',
          hint: 'Valider om modellsvarene er relevante for brukerens spørring og blokker svar som er under den definerte terskelen for relevans. 0: blokkerer ingenting, 0,99: blokkerer nesten alt',
        },
      },
    },
  },
};

export default translation;
