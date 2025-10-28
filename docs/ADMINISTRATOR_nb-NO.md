# Administrative funksjoner

## Forutsetninger

Admin-brukeren må være medlem av en gruppe kalt `Admin`, som kan settes opp via administrasjonskonsollen > Amazon Cognito User pools eller aws cli. Merk at bruker-pool-ID-en kan refereres ved å gå til CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`.

![](./imgs/group_membership_admin.png)

## Merk offentlige boter som Essensielle

Offentlige boter kan nå merkes som "Essensielle" av administratorer. Boter som er merket som Essensielle vil bli vist i "Essensielle"-seksjonen i bot-butikken, noe som gjør dem lett tilgjengelige for brukere. Dette lar administratorer feste viktige boter som de ønsker at alle brukere skal bruke.

### Eksempler

- HR Assistent Bot: Hjelper ansatte med HR-relaterte spørsmål og oppgaver.
- IT Support Bot: Gir assistanse for interne tekniske problemer og kontoadministrasjon.
- Intern Policy Guide Bot: Svarer på vanlige spørsmål om oppmøteregler, sikkerhetspolicyer og andre interne forskrifter.
- Onboarding Bot for Nyansatte: Veileder nyansatte gjennom prosedyrer og systembruk på deres første dag.
- Personalfordel Informasjons Bot: Forklarer bedriftens fordelsordninger og velferdstjenester.

![](./imgs/admin_bot_menue.png)
![](./imgs/bot_store.png)

## Tilbakemeldingssløyfe

Resultatet fra LLM møter ikke alltid brukerens forventninger. Noen ganger klarer det ikke å tilfredsstille brukerens behov. For å effektivt "integrere" LLMer i forretningsdrift og dagligliv, er det essensielt å implementere en tilbakemeldingssløyfe. Bedrock Chat er utstyrt med en tilbakemeldingsfunksjon som er designet for å gjøre det mulig for brukere å analysere hvorfor misnøye oppsto. Basert på analyseresultatene kan brukere justere prompts, RAG-datakilder og parametere tilsvarende.

![](./imgs/feedback_loop.png)

![](./imgs/feedback-using-claude-chat.png)

Dataanalytikere kan få tilgang til samtalelogger ved hjelp av [Amazon Athena](https://aws.amazon.com/jp/athena/). Hvis de ønsker å analysere dataene med [Jupyter Notebook](https://jupyter.org/), kan [dette notebook-eksempelet](../examples/notebooks/feedback_analysis_example.ipynb) være en referanse.

## Dashbord

Gir for øyeblikket en grunnleggende oversikt over chatbot- og brukerbruk, med fokus på å aggregere data for hver bot og bruker over spesifikke tidsperioder og sortere resultatene etter bruksavgifter.

![](./imgs/admin_bot_analytics.png)

## Merknader

- Som angitt i [arkitekturen](../README.md#architecture), vil administratorfunksjonene henvise til S3-bøtten som er eksportert fra DynamoDB. Vær oppmerksom på at siden eksporten utføres én gang i timen, vil de nyeste samtalene kanskje ikke gjenspeiles umiddelbart.

- I offentlig bot-bruk vil bots som ikke har vært brukt i det hele tatt i den angitte perioden ikke bli listet.

- I brukerstatistikken vil brukere som ikke har brukt systemet i det hele tatt i den angitte perioden ikke bli listet.

> [!Important]
> Hvis du bruker flere miljøer (dev, prod, osv.), vil Athena-databasenavnet inkludere miljøprefikset. I stedet for `bedrockchatstack_usage_analysis`, vil databasenavnet være:
>
> - For standardmiljø: `bedrockchatstack_usage_analysis`
> - For navngitte miljøer: `<env-prefix>_bedrockchatstack_usage_analysis` (f.eks. `dev_bedrockchatstack_usage_analysis`)
>
> I tillegg vil tabellnavnet inkludere miljøprefikset:
>
> - For standardmiljø: `ddb_export`
> - For navngitte miljøer: `<env-prefix>_ddb_export` (f.eks. `dev_ddb_export`)
>
> Sørg for å justere spørringene dine tilsvarende når du jobber med flere miljøer.

## Last ned samtaledata

Du kan spørre samtaleloggene med Athena ved hjelp av SQL. For å laste ned logger, åpne Athena Query Editor fra administrasjonskonsollen og kjør SQL. Følgende er noen eksempelspørringer som er nyttige for å analysere brukstilfeller. Tilbakemeldinger kan refereres i `MessageMap`-attributtet.

### Spørring per Bot-ID 

Rediger `bot-id` og `datehour`. `bot-id` kan refereres på Bot Management-skjermen, som kan nås fra Bot Publish APIs, som vises i venstre sidepanel. Merk slutten av URL-en som `https://xxxx.cloudfront.net/admin/bot/<bot-id>`.

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

> [!Note]
> Hvis du bruker et navngitt miljø (f.eks. "dev"), erstatt `bedrockchatstack_usage_analysis.ddb_export` med `dev_bedrockchatstack_usage_analysis.dev_ddb_export` i spørringen over.

### Spørring per Bruker-ID

Rediger `user-id` og `datehour`. `user-id` kan refereres på Bot Management-skjermen.

> [!Note]
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

> [!Note]
> Hvis du bruker et navngitt miljø (f.eks. "dev"), erstatt `bedrockchatstack_usage_analysis.ddb_export` med `dev_bedrockchatstack_usage_analysis.dev_ddb_export` i spørringen over.