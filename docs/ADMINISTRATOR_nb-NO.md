# Administratorfunksjoner

Administratorfunksjonene er et avgjørende verktøy som gir vesentlige innsikter i bruk av tilpassede chatbots og brukeratferd. Uten denne funksjonaliteten ville det være vanskelig for administratorer å forstå hvilke tilpassede chatbots som er populære, hvorfor de er populære, og hvem som bruker dem. Denne informasjonen er avgjørende for å optimalisere instruksjonsprompts, tilpasse RAG-datakilder og identifisere tunge brukere som potensielt kan bli påvirkere.

## Tilbakemeldingssløyfe

Utdata fra LLM oppfyller ikke alltid brukerens forventninger. Noen ganger klarer den ikke å tilfredsstille brukerens behov. For effektivt å "integrere" LLM-er i forretningsdrift og dagligliv, er det avgjørende å implementere en tilbakemeldingssløyfe. Bedrock Claude Chat er utstyrt med en tilbakemeldingsfunksjon som er designet for å gjøre det mulig for brukere å analysere hvorfor misnøye oppstod. Basert på analyseresultatene kan brukere justere promptene, RAG-datakildene og parameterne deretter.

![](./imgs/feedback_loop.png)

![](./imgs/feedback-using-claude-chat.png)

Dataanalytikere kan få tilgang til samtalelogger ved hjelp av [Amazon Athena](https://aws.amazon.com/jp/athena/). Hvis de ønsker å analysere dataene i [Jupyter Notebook](https://jupyter.org/), kan [denne notatbokeksempelet](../examples/notebooks/feedback_analysis_example.ipynb) være en referanse.

## Administratorpanel

Gir for øyeblikket en grunnleggende oversikt over chatbots og brukerbruk, med fokus på å aggregere data for hver bot og bruker over spesifiserte tidsperioder og sortere resultatene etter bruksgebyrer.

![](./imgs/admin_bot_analytics.png)

> [!Merk]
> Brukerbruksanalyse kommer snart.

### Forutsetninger

Administratorbrukeren må være medlem av gruppen kalt `Admin`, som kan settes opp via administrasjonskonsollen > Amazon Cognito User Pools eller AWS CLI. Merk at brukergruppe-ID-en kan refereres ved å åpne CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`.

![](./imgs/group_membership_admin.png)

## Notater

- Som nevnt i [arkitekturen](../README.md#architecture), vil administratorfunksjonene referere til S3-bucketen som er eksportert fra DynamoDB. Vær oppmerksom på at siden eksporten utføres én gang i timen, vil de nyeste samtalene kanskje ikke umiddelbart gjenspeiles.

- I offentlige bot-bruk vil bots som ikke har blitt brukt i det hele tatt i løpet av den angitte perioden, ikke bli listet.

- I brukerbruk vil brukere som ikke har brukt systemet i det hele tatt i løpet av den angitte perioden, ikke bli listet.

## Last ned samtaledata

Du kan spørre samtaleloggene til Athena ved hjelp av SQL. For å laste ned logger, åpne Athena Query Editor fra administrasjonskonsollen og kjør SQL. Følgende er noen eksempelspørringer som er nyttige for å analysere brukstilfeller. Tilbakemelding kan refereres i `MessageMap`-attributtet.

### Spørring per Bot-ID

Rediger `bot-id` og `datehour`. `bot-id` kan refereres på Bot Management-skjermen, som kan nås fra Bot Publish APIs, vist på venstre sidepanel. Merk den siste delen av URL-en som `https://xxxx.cloudfront.net/admin/bot/<bot-id>`.

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