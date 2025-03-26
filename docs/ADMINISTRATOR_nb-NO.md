# Administratorfunksjoner

Administratorfunksjonene er et avgjørende verktøy som gir vesentlige innsikter i bruk av tilpassede chatbots og brukernes atferd. Uten denne funksjonaliteten ville det være vanskelig for administratorer å forstå hvilke tilpassede chatbots som er populære, hvorfor de er populære, og hvem som bruker dem. Denne informasjonen er avgjørende for å optimalisere instruksjonsprompter, tilpasse RAG-datakilder og identifisere hyppige brukere som potensielt kan være påvirkere.

## Tilbakemeldingssløyfe

Resultatet fra LLM oppfyller ikke alltid brukerens forventninger. Noen ganger klarer den ikke å tilfredsstille brukerens behov. For effektivt å "integrere" LLM-er i forretningsdrift og daglig liv, er det avgjørende å implementere en tilbakemeldingssløyfe. Bedrock Claude Chat er utstyrt med en tilbakemeldingsfunksjon som er designet for å gjøre det mulig for brukere å analysere hvorfor misnøye oppsto. Basert på analyseresultatene kan brukere justere promptene, RAG-datakilder og parametere tilsvarende.

![](./imgs/feedback_loop.png)

![](./imgs/feedback-using-claude-chat.png)

Dataanalytikere kan få tilgang til samtalelogger ved hjelp av [Amazon Athena](https://aws.amazon.com/jp/athena/). Hvis de ønsker å analysere dataene i [Jupyter Notebook](https://jupyter.org/), kan [denne notatbokeksempelet](../examples/notebooks/feedback_analysis_example.ipynb) være en referanse.

## Administratorpanel

Gir for øyeblikket en grunnleggende oversikt over chatbots og brukerbruk, med fokus på å samle data for hver bot og bruker over angitte tidsperioder og sortere resultatene etter bruksgebyrer.

![](./imgs/admin_bot_analytics.png)

> [!Merk]
> Brukerbruksanalyse kommer snart.

### Forutsetninger

Administratorbrukeren må være medlem av gruppen kalt `Admin`, som kan settes opp via administrasjonskonsollen > Amazon Cognito User Pools eller AWS CLI. Merk at brukergruppe-ID-en kan refereres ved å åpne CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`.

![](./imgs/group_membership_admin.png)

## Notater

- Som nevnt i [arkitekturen](../README.md#architecture), vil admin-funksjonene referere til S3-bucketen eksportert fra DynamoDB. Vær oppmerksom på at siden eksporten utføres en gang i timen, kan de nyeste samtalene ikke gjenspeiles umiddelbart.

- I offentlige bot-bruk vil bots som ikke har blitt brukt i det hele tatt i den angitte perioden ikke bli oppført.

- I brukerbruk vil brukere som ikke har brukt systemet i det hele tatt i den angitte perioden ikke bli oppført.

> [!Viktig]
> **Database-navn for flere miljøer**
>
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
> Sørg for å justere dine spørringer tilsvarende når du jobber med flere miljøer.

## Last ned samtaledataene

Du kan søke etter samtalelogger ved hjelp av Athena, ved bruk av SQL. For å laste ned logger, åpne Athena Query Editor fra administrasjonskonsollen og kjør SQL. Følgende er noen eksempelspørringer som er nyttige for å analysere brukstilfeller. Tilbakemelding kan refereres i `MessageMap`-attributtet.

### Spørring per Bot-ID

Rediger `bot-id` og `datehour`. `bot-id` kan refereres på Bot Management-skjermen, som kan nås fra Bot Publish APIs, vist på venstre sidepanel. Legg merke til den siste delen av URL-en som `https://xxxx.cloudfront.net/admin/bot/<bot-id>`.

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