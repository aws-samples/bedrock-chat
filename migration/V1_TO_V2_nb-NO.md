# Migrasjonsveiledning (v1 til v2)

## TL;DR

- **For brukere av v1.2 eller tidligere**: Oppgrader til v1.4 og opprett botene dine på nytt ved hjelp av Knowledge Base (KB). Etter en overgangsperiode, når du har bekreftet at alt fungerer som forventet med KB, fortsett med oppgradering til v2.
- **For brukere av v1.3**: Selv om du allerede bruker KB, er det **sterkt anbefalt** å oppgradere til v1.4 og opprette botene på nytt. Hvis du fortsatt bruker pgvector, migrer ved å opprette botene dine på nytt med KB i v1.4.
- **For brukere som ønsker å fortsette å bruke pgvector**: Oppgradering til v2 anbefales ikke hvis du planlegger å fortsette å bruke pgvector. Oppgradering til v2 vil fjerne alle ressurser relatert til pgvector, og fremtidig støtte vil ikke lenger være tilgjengelig. Fortsett å bruke v1 i dette tilfellet.
- Merk at **oppgradering til v2 vil resultere i sletting av alle Aurora-relaterte ressurser.** Fremtidige oppdateringer vil fokusere utelukkende på v2, mens v1 blir utfaset.

## Introduksjon

### Hva som vil skje

V2-oppdateringen introduserer en stor endring ved å erstatte pgvector på Aurora Serverless og ECS-basert embedding med [Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html). Denne endringen er ikke bakoverkompatibel.

### Hvorfor dette repositoriet har adoptert Knowledge Bases og avviklet pgvector

Det er flere grunner til denne endringen:

#### Forbedret RAG-nøyaktighet

- Knowledge Bases bruker OpenSearch Serverless som backend, som muliggjør hybride søk med både fulltekst- og vektorsøk. Dette fører til bedre nøyaktighet ved besvarelse av spørsmål som inneholder egennavn, noe pgvector hadde problemer med.
- Det støtter også flere alternativer for å forbedre RAG-nøyaktighet, som avansert oppdeling og parsing.
- Knowledge Bases har vært allment tilgjengelig i nesten ett år per oktober 2024, med funksjoner som nettkryping allerede lagt til. Fremtidige oppdateringer er forventet, noe som gjør det enklere å ta i bruk avansert funksjonalitet på lang sikt. For eksempel, mens dette repositoriet ikke har implementert funksjoner som import fra eksisterende S3-bøtter (en ofte etterspurt funksjon) i pgvector, er det allerede støttet i KB (KnowledgeBases).

#### Vedlikehold

- Den nåværende ECS + Aurora-oppsettet er avhengig av mange biblioteker, inkludert de for PDF-parsing, nettkryping og utvinning av YouTube-transkripsjoner. Til sammenligning reduserer administrerte løsninger som Knowledge Bases vedlikeholdsbyrden for både brukere og repositoriets utviklingsteam.

## Migrasjonsprosess (Sammendrag)

Vi anbefaler sterkt å oppgradere til v1.4 før overgang til v2. I v1.4 kan du bruke både pgvector og Knowledge Base-boter, noe som gir en overgangsperiode for å gjenskape dine eksisterende pgvector-boter i Knowledge Base og verifisere at de fungerer som forventet. Selv om RAG-dokumentene forblir identiske, merk at backend-endringene til OpenSearch kan gi litt forskjellige resultater, selv om de generelt er like, på grunn av forskjeller som k-NN-algoritmer.

Ved å sette `useBedrockKnowledgeBasesForRag` til true i `cdk.json`, kan du opprette boter ved hjelp av Knowledge Bases. Imidlertid vil pgvector-boter bli skrivebeskyttet, noe som forhindrer opprettelse eller redigering av nye pgvector-boter.

![](../imgs/v1_to_v2_readonly_bot.png)

I v1.4 introduseres også [Guardrails for Amazon Bedrock](https://aws.amazon.com/jp/bedrock/guardrails/). På grunn av regionale begrensninger i Knowledge Bases, må S3-bøtten for opplasting av dokumenter være i samme region som `bedrockRegion`. Vi anbefaler å sikkerhetskopiere eksisterende dokumentbøtter før oppdatering, for å unngå manuell opplasting av store mengder dokumenter senere (ettersom S3-bøtte importfunksjonalitet er tilgjengelig).

## Migrasjonsprosess (Detaljer)

Trinnene varierer avhengig av om du bruker v1.2 eller tidligere, eller v1.3.

![](../imgs/v1_to_v2_arch.png)

### Trinn for brukere av v1.2 eller tidligere

1. **Sikkerhetskopier din eksisterende dokumentbucket (valgfritt, men anbefalt).** Hvis systemet ditt allerede er i drift, anbefaler vi sterkt dette trinnet. Sikkerhetskopier bucketen med navnet `bedrockchatstack-documentbucketxxxx-yyyy`. For eksempel kan vi bruke [AWS Backup](https://docs.aws.amazon.com/aws-backup/latest/devguide/s3-backups.html).

2. **Oppdater til v1.4**: Hent den nyeste v1.4-taggen, modifiser `cdk.json`, og deploy. Følg disse trinnene:

   1. Hent den nyeste taggen:
      ```bash
      git fetch --tags
      git checkout tags/v1.4.0
      ```
   2. Modifiser `cdk.json` som følger:
      ```json
      {
        ...,
        "useBedrockKnowledgeBasesForRag": true,
        ...
      }
      ```
   3. Deploy endringene:
      ```bash
      npx cdk deploy
      ```

3. **Gjenskap botene dine**: Gjenskap botene dine på Knowledge Base med de samme definisjonene (dokumenter, chunk-størrelse, etc.) som pgvector-botene. Hvis du har et stort volum av dokumenter, vil gjenoppretting fra sikkerhetskopien i trinn 1 gjøre denne prosessen enklere. For å gjenopprette kan vi bruke gjenoppretting av kopier på tvers av regioner. For mer detaljer, besøk [her](https://docs.aws.amazon.com/aws-backup/latest/devguide/restoring-s3.html). For å spesifisere den gjenopprettede bucketen, sett `S3 Data Source`-seksjonen som følger. Bane-strukturen er `s3://<bucket-name>/<user-id>/<bot-id>/documents/`. Du kan sjekke bruker-ID i Cognito user pool og bot-ID i adresselinjen på bot-opprettelsesskjermen.

![](../imgs/v1_to_v2_KB_s3_source.png)

**Merk at noen funksjoner ikke er tilgjengelige på Knowledge Bases, som nettkryping og YouTube-transkriptstøtte (Planlegger å støtte nettkryper ([issue](https://github.com/aws-samples/bedrock-chat/issues/557))).** Husk også at bruk av Knowledge Bases vil medføre kostnader for både Aurora og Knowledge Bases under overgangen.

4. **Fjern publiserte API-er**: Alle tidligere publiserte API-er må republiseres før v2 deployes på grunn av VPC-sletting. For å gjøre dette må du først slette de eksisterende API-ene. Bruk av [administrators API Management-funksjon](../ADMINISTRATOR_nb-NO.md) kan forenkle denne prosessen. Når slettingen av alle `APIPublishmentStackXXXX` CloudFormation-stacks er fullført, vil miljøet være klart.

5. **Deploy v2**: Etter utgivelsen av v2, hent den taggede kilden og deploy som følger (dette vil være mulig når den er utgitt):
   ```bash
   git fetch --tags
   git checkout tags/v2.0.0
   npx cdk deploy
   ```

> [!Warning]
> Etter deploying av v2, **VIL ALLE BOTER MED PREFIKSET [Unsupported, Read-only] BLI SKJULT.** Sørg for at du gjenskaper nødvendige boter før oppgradering for å unngå tap av tilgang.

> [!Tip]
> Under stack-oppdateringer kan du møte gjentatte meldinger som: Resource handler returned message: "The subnet 'subnet-xxx' has dependencies and cannot be deleted." I slike tilfeller, gå til Management Console > EC2 > Network Interfaces og søk etter BedrockChatStack. Slett de viste grensesnittene tilknyttet dette navnet for å bidra til en smidigere deployeringsprosess.

### Trinn for brukere av v1.3

Som nevnt tidligere, i v1.4 må Knowledge Bases opprettes i bedrockRegion på grunn av regionale begrensninger. Derfor må du gjenopprette KB. Hvis du allerede har testet KB i v1.3, gjenskap boten i v1.4 med de samme definisjonene. Følg trinnene som er skissert for v1.2-brukere.