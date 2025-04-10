# Migrasjonsguide (v1 til v2)

## TL;DR

- **For brukere av v1.2 eller tidligere**: Oppgrader til v1.4 og gjenskape botene dine ved hjelp av Kunnskapsbase (KB). Etter en overgangsperiode, når du har bekreftet at alt fungerer som forventet med KB, fortsett med å oppgradere til v2.
- **For brukere av v1.3**: Selv om du allerede bruker KB, er det **sterkt anbefalt** å oppgradere til v1.4 og gjenskape botene dine. Hvis du fortsatt bruker pgvector, migrer ved å gjenskape botene dine ved hjelp av KB i v1.4.
- **For brukere som ønsker å fortsette å bruke pgvector**: Oppgradering til v2 anbefales ikke hvis du planlegger å fortsette å bruke pgvector. Oppgradering til v2 vil fjerne alle ressurser relatert til pgvector, og fremtidig støtte vil ikke lenger være tilgjengelig. Fortsett å bruke v1 i dette tilfellet.
- Merk at **oppgradering til v2 vil resultere i sletting av alle Aurora-relaterte ressurser.** Fremtidige oppdateringer vil fokusere utelukkende på v2, med v1 som blir utfaset.

## Introduksjon

### Hva som vil skje

V2-oppdateringen introduserer en stor endring ved å erstatte pgvector på Aurora Serverless og ECS-basert embedding med [Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html). Denne endringen er ikke bakoverkompatibel.

### Hvorfor dette repositoriet har adoptert Knowledge Bases og avsluttet pgvector

Det er flere grunner til denne endringen:

#### Forbedret RAG-nøyaktighet

- Knowledge Bases bruker OpenSearch Serverless som backend, som muliggjør hybride søk med både fulltekst- og vektorsøk. Dette gir bedre nøyaktighet ved besvarelse av spørsmål som inneholder egennavn, noe pgvector strevde med.
- Det støtter også flere alternativer for å forbedre RAG-nøyaktighet, som avansert oppdeling og parsing.
- Knowledge Bases har vært generelt tilgjengelig i nesten ett år per oktober 2024, med funksjoner som nettkravling allerede lagt til. Fremtidige oppdateringer forventes, noe som gjør det enklere å adoptere avansert funksjonalitet på lang sikt. For eksempel, selv om dette repositoriet ikke har implementert funksjoner som import fra eksisterende S3-bøtter (en hyppig etterspurt funksjon) i pgvector, støttes dette allerede i KB (KnowledgeBases).

#### Vedlikehold

- Den nåværende ECS + Aurora-oppsettet er avhengig av tallrike biblioteker, inkludert de for PDF-parsing, nettkravling og uttrekk av YouTube-transkripter. Til sammenligning reduserer administrerte løsninger som Knowledge Bases vedlikeholdsbyrden for både brukere og repositoriets utviklingsteam.

## Migrasjonsprosess (Sammendrag)

Vi anbefaler sterkt å oppgradere til v1.4 før du går over til v2. I v1.4 kan du bruke både pgvector og Knowledge Base-bots, noe som gir en overgangsperiode for å gjenskape eksisterende pgvector-bots i Knowledge Base og verifisere at de fungerer som forventet. Selv om RAG-dokumentene forblir identiske, vær oppmerksom på at backend-endringene til OpenSearch kan produsere litt forskjellige resultater, selv om de generelt er like, på grunn av forskjeller som k-NN-algoritmer.

Ved å sette `useBedrockKnowledgeBasesForRag` til true i `cdk.json`, kan du opprette bots ved hjelp av Knowledge Bases. Imidlertid vil pgvector-bots bli skrivebeskyttet, noe som forhindrer opprettelse eller redigering av nye pgvector-bots.

![](../imgs/v1_to_v2_readonly_bot.png)

I v1.4 introduseres også [Guardrails for Amazon Bedrock](https://aws.amazon.com/jp/bedrock/guardrails/). På grunn av regionale restriksjoner for Knowledge Bases, må S3-bucketen for opplasting av dokumenter være i samme region som `bedrockRegion`. Vi anbefaler å sikkerhetskopiere eksisterende dokumentbøtter før oppdatering, for å unngå manuell opplasting av et stort antall dokumenter senere (da S3-bucket-importfunksjonalitet er tilgjengelig).

## Migrasjonsprosess (Detalj)

Trinnene varierer avhengig av om du bruker v1.2 eller tidligere, eller v1.3.

![](../imgs/v1_to_v2_arch.png)

### Trinn for brukere av v1.2 eller tidligere

1. **Sikkerhetskopier din eksisterende dokumentbøtte (valgfritt, men anbefalt).** Hvis systemet ditt allerede er i drift, anbefaler vi sterkt dette trinnet. Sikkerhetskopier bøtten med navn `bedrockchatstack-documentbucketxxxx-yyyy`. For eksempel kan vi bruke [AWS Backup](https://docs.aws.amazon.com/aws-backup/latest/devguide/s3-backups.html).

2. **Oppdater til v1.4**: Hent den nyeste v1.4-taggen, endre `cdk.json`, og distribuer. Følg disse trinnene:

   1. Hent den nyeste taggen:
      ```bash
      git fetch --tags
      git checkout tags/v1.4.0
      ```
   2. Endre `cdk.json` som følger:
      ```json
      {
        ...,
        "useBedrockKnowledgeBasesForRag": true,
        ...
      }
      ```
   3. Distribuer endringene:
      ```bash
      npx cdk deploy
      ```

3. **Gjenskape botene dine**: Gjenskape botene dine på Knowledge Base med samme definisjoner (dokumenter, chunk-størrelse, osv.) som pgvector-botene. Hvis du har et stort volum av dokumenter, vil gjenoppretting fra sikkerhetskopien i trinn 1 gjøre denne prosessen enklere. For å gjenopprette kan vi bruke gjenoppretting av tverregionale kopier. For mer detaljer, besøk [her](https://docs.aws.amazon.com/aws-backup/latest/devguide/restoring-s3.html). For å angi den gjenopprettede bøtten, sett `S3 Data Source`-seksjonen som følger. Stibstrukturen er `s3://<bucket-name>/<user-id>/<bot-id>/documents/`. Du kan sjekke bruker-ID i Cognito-brukerpuljen og bot-ID i adresselinjen på bot-opprettingsskjermen.

![](../imgs/v1_to_v2_KB_s3_source.png)

**Merk at noen funksjoner ikke er tilgjengelige på Knowledge Bases, som nettcrawling og YouTube-transkriptstøtte (Planlegger å støtte nettcrawler ([issue](https://github.com/aws-samples/bedrock-chat/issues/557))).** Husk også at bruk av Knowledge Bases vil medføre kostnader for både Aurora og Knowledge Bases under overgangen.

4. **Fjern publiserte API-er**: Alle tidligere publiserte API-er må publiseres på nytt før distribusjon av v2 på grunn av VPC-sletting. For å gjøre dette må du slette de eksisterende API-ene først. Bruk av [administrator-API-håndteringsfunksjonen](../ADMINISTRATOR_nb-NO.md) kan forenkle denne prosessen. Når slettingen av alle `APIPublishmentStackXXXX` CloudFormation-stakker er fullført, vil miljøet være klart.

5. **Distribuer v2**: Etter lanseringen av v2, hent den merkede kilden og distribuer som følger (dette vil være mulig når den er lansert):
   ```bash
   git fetch --tags
   git checkout tags/v2.0.0
   npx cdk deploy
   ```

> [!Advarsel]
> Etter distribusjon av v2, **VIL ALLE BOTER MED PREFIKSET [Ikke støttet, Kun lesing] BLI SKJULT.** Sørg for å gjenskape nødvendige boter før oppgradering for å unngå tap av tilgang.

> [!Tips]
> Under stakk-oppdateringer kan du støte på gjentatte meldinger som: Ressurshåndtering returnerte melding: "Undernettet 'subnet-xxx' har avhengigheter og kan ikke slettes." I slike tilfeller, naviger til Management Console > EC2 > Nettverksgrensesnitt og søk etter BedrockChatStack. Slett de viste grensesnittene som er forbundet med dette navnet for å sikre en jevnere distribusjonsprosess.

### Trinn for brukere av v1.3

Som nevnt tidligere, i v1.4 må Knowledge Bases opprettes i bedrockRegion på grunn av regionale begrensninger. Derfor må du gjenskape KB. Hvis du allerede har testet KB i v1.3, gjenskaper du boten i v1.4 med samme definisjoner. Følg trinnene som er beskrevet for v1.2-brukere.