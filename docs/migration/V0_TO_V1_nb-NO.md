# Migreringsguide (v0 til v1)

Hvis du allerede bruker Bedrock Claude Chat med en tidligere versjon (~`0.4.x`), må du følge trinnene nedenfor for å migrere.

## Hvorfor må jeg gjøre dette?

Denne store oppdateringen inkluderer viktige sikkerhetsoppdateringer.

- Vektordatabaselagringen (dvs. pgvector på Aurora PostgreSQL) er nå kryptert, noe som utløser en erstatning ved distribusjon. Dette betyr at eksisterende vektorobjekter vil bli slettet.
- Vi introduserte `CreatingBotAllowed` Cognito-brukergruppe for å begrense brukere som kan opprette bots. Eksisterende brukere er ikke i denne gruppen, så du må manuelt legge til tillatelsen hvis du vil at de skal ha mulighet til å opprette bots. Se: [Bot Personalization](../../README.md#bot-personalization)

## Forutsetninger

Les [Databasemigrasjonsguide](./DATABASE_MIGRATION_nb-NO.md) og bestem metoden for gjenoppretting av elementer.

## Trinn

### Vektorbutikk-migrasjon

- Åpne terminalen din og naviger til prosjektkatalogen
- Hent branchen du ønsker å distribuere. Bytt til ønsket branch (i dette tilfellet `v1`) og hent de siste endringene:

```sh
git fetch
git checkout v1
git pull origin v1
```

- Hvis du ønsker å gjenopprette elementer med DMS, IKKE GLEM å deaktivere passordrotering og noter passordet for å få tilgang til databasen. Hvis du gjenoppretter med migreringsscriptet([migrate.py](./migrate.py)), trenger du ikke å notere passordet.
- Fjern alle [publiserte API-er](../PUBLISH_API_nb-NO.md) slik at CloudFormation kan fjerne eksisterende Aurora-klynge.
- Kjør [npx cdk deploy](../README.md#deploy-using-cdk) som utløser erstatning av Aurora-klynge og SLETTER ALLE VEKTORELEMENTER.
- Følg [Database Migration Guide](./DATABASE_MIGRATION_nb-NO.md) for å gjenopprette vektorelementer.
- Bekreft at brukeren kan benytte eksisterende bots med kunnskap, dvs. RAG-bots.

### Legg til CreatingBotAllowed-tillatelse

- Etter distribusjonen vil ingen brukere kunne opprette nye bots.
- Hvis du vil at bestemte brukere skal kunne opprette bots, legg disse brukerne til i `CreatingBotAllowed`-gruppen ved hjelp av administrasjonskonsollen eller CLI.
- Bekreft om brukeren kan opprette en bot. Merk at brukerne må logge inn på nytt.