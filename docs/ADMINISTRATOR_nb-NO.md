# Administrative features

(Note: This appears to be a heading section. I've maintained the original markdown formatting and simply translated the heading to Norwegian Bokmål.)

## Forutsetninger

Administratorbrukeren må være medlem av gruppen kalt `Admin`, som kan settes opp via administrasjonskonsollen > Amazon Cognito User pools eller aws cli. Merk at brukergruppe-IDen kan refereres ved å gå til CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`.

![](./imgs/group_membership_admin.png)

## Merk offentlige bots som Essensielle

Offentlige bots kan nå merkes som "Essensielle" av administratorer. Bots som er merket som Essensielle vil bli fremhevet i "Essensielle" seksjonen i bot-butikken, noe som gjør dem lett tilgjengelige for brukere. Dette lar administratorer fremheve viktige bots som de vil at alle brukere skal benytte.

### Eksempler

- HR Assistentbot: Hjelper ansatte med HR-relaterte spørsmål og oppgaver.
- IT Støttebot: Gir assistanse for interne tekniske problemer og kontobehandling.
- Intern Retningslinjebot: Svarer på vanlige spørsmål om oppmøteregler, sikkerhetspolicyer og andre interne retningslinjer.
- Ny Medarbeider Introduksjonsbot: Veileder nyansatte gjennom prosedyrer og systembruk på deres første dag.
- Fordelsinformasjonsbot: Forklarer selskapets fordels- og velferdsprogrammer.

![](./imgs/admin_bot_menue.png)
![](./imgs/bot_store.png)

## Tilbakemeldingssløyfe

Resultatet fra LLM oppfyller ikke alltid brukerens forventninger. Noen ganger klarer den ikke å tilfredsstille brukerens behov. For effektivt å "integrere" LLM-er i forretningsdrift og daglig liv, er det avgjørende å implementere en tilbakemeldingssløyfe. Bedrock Chat er utstyrt med en tilbakemeldingsfunksjon som er designet for å gjøre det mulig for brukere å analysere hvorfor misnøye oppstod. Basert på analyseresultatene kan brukere justere promptene, RAG-datakilder og parametere tilsvarende.

![](./imgs/feedback_loop.png)

![](./imgs/feedback-using-claude-chat.png)

Dataanalytikere kan få tilgang til samtalelogger ved hjelp av [Amazon Athena](https://aws.amazon.com/jp/athena/). Hvis de ønsker å analysere dataene i [Jupyter Notebook](https://jupyter.org/), kan [denne notebook-eksempelet](../examples/notebooks/feedback_analysis_example.ipynb) være en referanse.

## Dashboard

Gir for øyeblikket en grunnleggende oversikt over chatbotens og brukerens bruk, med fokus på å samle inn data for hver bot og bruker over angitte tidsperioder og sortere resultatene etter bruksgebyrer.

![](./imgs/admin_bot_analytics.png)

## Notater

- Som beskrevet i [arkitekturen](../README.md#architecture), vil admin-funksjonene referere til S3-bøtten som er eksportert fra DynamoDB. Vær oppmerksom på at siden eksporten utføres en gang i timen, kan de siste samtalene ikke gjenspeiles umiddelbart.

- I offentlige bot-bruk vil bots som ikke har blitt brukt i det hele tatt i den angitte perioden, ikke bli oppført.

- I brukerbruk vil brukere som ikke har brukt systemet i det hele tatt i den angitte perioden, ikke bli oppført.

> [!Viktig]
> Hvis du bruker flere miljøer (dev, prod, osv.), vil Athena-databasenavnet inkludere miljøprefikset. I stedet for `bedrockchatstack_usage_analysis`, vil databasenavnet være:
>
> - For standard miljø: `bedrockchatstack_usage_analysis`
> - For navngitte miljøer: `<miljø-prefiks>_bedrockchatstack_usage_analysis` (f.eks. `dev_bedrockchatstack_usage_analysis`)
>
> I tillegg vil tabellnavnet inkludere miljøprefikset:
>
> - For standard miljø: `ddb_export`
> - For navngitte miljøer: `<miljø-prefiks>_ddb_export` (f.eks. `dev_ddb_export`)
>
> Sørg for å justere spørringene dine i henhold til dette når du arbeider med flere miljøer.

## Last ned samtaledata

Du kan søke etter samtalelogger med Athena, ved hjelp av SQL. For å laste ned logger, åpne Athena Query Editor fra administrasjonskonsollen og kjør SQL. Følgende er noen eksempelspørringer som er nyttige for å analysere brukstilfeller. Tilbakemelding kan refereres i `MessageMap`-attributtet.

### Spørring per Bot-ID

Rediger `bot-id` og `datehour`. `bot-id` kan refereres på Bot Management-skjermen, som kan nås fra Bot Publish-APIer, vist på venstre sidepanel. Merk den siste delen av URL-en som `https://xxxx.cloudfront.net/admin/bot/<bot-id>`.

```sql
SELECT
    d.newimage.PK.S AS UserId,
    d.newimage.SK.S AS ConversationId,
    d.newimage.MessageMap.S AS MessageMap,
    d.newimage.TotalPrice.N AS TotalPrice,
    d.newimage.CreateTime.N AS CreateTime,
    d.newimage.LastMessageId.S AS LastMessageId,
    d.newimage.BotId.S AS BotId,
    d.datehour AS DateHour
FROM
    bedrockchatstack_usage_analysis.ddb_export d
WHERE
    d.newimage.BotId.S = '<bot-id>'
    AND d.datehour BETWEEN '<yyyy/mm/dd/hh>' AND '<yyyy/mm/dd/hh>'
    AND d.Keys.SK.S LIKE CONCAT(d.Keys.PK.S, '#CONV#%')
ORDER BY
    d.datehour DESC;
```

> [!Merk]
> Hvis du bruker et navngitt miljø (f.eks. "dev"), erstatt `bedrockchatstack_usage_analysis.ddb_export` med `dev_bedrockchatstack_usage_analysis.dev_ddb_export` i spørringen over.

### Spørring per Bruker-ID

Rediger `user-id` og `datehour`. `user-id` kan refereres på Bot Management-skjermen.

> [!Merk]
> Brukerbruksanalyse kommer snart.

```sql
SELECT
    d.newimage.PK.S AS UserId,
    d.newimage.SK.S AS ConversationId,
    d.newimage.MessageMap.S AS MessageMap,
    d.newimage.TotalPrice.N AS TotalPrice,
    d.newimage.CreateTime.N AS CreateTime,
    d.newimage.LastMessageId.S AS LastMessageId,
    d.newimage.BotId.S AS BotId,
    d.datehour AS DateHour
FROM
    bedrockchatstack_usage_analysis.ddb_export d
WHERE
    d.newimage.PK.S = '<user-id>'
    AND d.datehour BETWEEN '<yyyy/mm/dd/hh>' AND '<yyyy/mm/dd/hh>'
    AND d.Keys.SK.S LIKE CONCAT(d.Keys.PK.S, '#CONV#%')
ORDER BY
    d.datehour DESC;
```

> [!Merk]
> Hvis du bruker et navngitt miljø (f.eks. "dev"), erstatt `bedrockchatstack_usage_analysis.ddb_export` med `dev_bedrockchatstack_usage_analysis.dev_ddb_export` i spørringen over.