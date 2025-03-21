# Migrasjonsveiledning (v0 til v1)

Hvis du allerede bruker Bedrock Claude Chat med en tidligere versjon (~`0.4.x`), må du følge trinnene nedenfor for å migrere.

## Hvorfor må jeg gjøre dette?

Denne store oppdateringen inneholder viktige sikkerhetsoppdateringer.

- Vektordatabaselagringen (dvs. pgvector på Aurora PostgreSQL) er nå kryptert, noe som utløser en erstatning ved distribusjon. Dette betyr at eksisterende vektorobjekter vil bli slettet.
- Vi har introdusert Cognito-brukergruppen `CreatingBotAllowed` for å begrense brukere som kan opprette bots. Eksisterende brukere er ikke i denne gruppen, så du må manuelt legge til tillatelsen hvis du vil at de skal ha mulighet til å opprette bots. Se: [Bot Personalization](../../README.md#bot-personalization)

## Forutsetninger

Les [Databasemigrasjonsguide](./DATABASE_MIGRATION_nb-NO.md) og bestem metoden for gjenoppretting av elementer.

## Trinn

### Vektor-lager migrasjon

- Åpne terminalen din og naviger til prosjektkatalogen
- Hent branchen du ønsker å distribuere. Bytt til ønsket branch (i dette tilfellet `v1`) og hent de siste endringene:

```sh
git fetch
git checkout v1
git pull origin v1
```

- Hvis du ønsker å gjenopprette elementer med DMS, IKKE GLEM å deaktivere passordrotering og noter passordet for å få tilgang til databasen. Hvis du gjenoppretter med migrasjonsskriptet([migrate.py](./migrate.py)), trenger du ikke å notere passordet.
- Fjern alle [publiserte APIer](../PUBLISH_API_nb-NO.md) slik at CloudFormation kan fjerne eksisterende Aurora-klynge.
- Kjør [npx cdk deploy](../README.md#deploy-using-cdk) som utløser erstatning av Aurora-klynge og SLETTER ALLE VEKTOR-ELEMENTER.
- Følg [Database Migrasjonsveiledning](./DATABASE_MIGRATION_nb-NO.md) for å gjenopprette vektor-elementer.
- Bekreft at brukeren kan benytte eksisterende bots som har kunnskap, dvs. RAG-bots.

### Legg til CreatingBotAllowed-tillatelse

- Etter distribusjonen vil alle brukere være ute av stand til å opprette nye bots.
- Hvis du vil at spesifikke brukere skal kunne opprette bots, legg til disse brukerne i `CreatingBotAllowed`-gruppen ved hjelp av administrasjonskonsollen eller CLI.
- Bekreft om brukeren kan opprette en bot. Merk at brukerne må logge inn på nytt.