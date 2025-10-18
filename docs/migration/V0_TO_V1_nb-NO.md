# Migrasjonsveiledning (v0 til v1)

Hvis du allerede bruker Bedrock Chat med en tidligere versjon (~`0.4.x`), må du følge trinnene nedenfor for å migrere.

## Hvorfor må jeg gjøre dette?

Denne store oppdateringen inkluderer viktige sikkerhetsoppdateringer.

- Vektordatabasen (dvs. pgvector på Aurora PostgreSQL) er nå kryptert, noe som utløser en erstatning når den distribueres. Dette betyr at eksisterende vektorelementer vil bli slettet.
- Vi har introdusert Cognito-brukergruppen `CreatingBotAllowed` for å begrense hvilke brukere som kan opprette boter. Nåværende eksisterende brukere er ikke i denne gruppen, så du må legge til tillatelsen manuelt hvis du ønsker at de skal ha mulighet til å opprette boter. Se: [Bot Personalization](../../README.md#bot-personalization)

## Forutsetninger

Les [Database Migration Guide](./DATABASE_MIGRATION_nb-NO.md) og bestem metoden for gjenoppretting av elementer.

## Trinn

### Vektor-lager migrering

- Åpne terminalen din og naviger til prosjektmappen
- Hent grenen du ønsker å distribuere. Følgende er til ønsket gren (i dette tilfellet `v1`) og hent de siste endringene:

```sh
git fetch
git checkout v1
git pull origin v1
```

- Hvis du ønsker å gjenopprette elementer med DMS, IKKE GLEM å deaktivere passordrotasjon og noter passordet for å få tilgang til databasen. Hvis du gjenoppretter med migreringsscriptet ([migrate_v0_v1.py](./migrate_v0_v1.py)), trenger du ikke å notere passordet.
- Fjern alle [publiserte API-er](../PUBLISH_API_nb-NO.md) slik at CloudFormation kan fjerne eksisterende Aurora-cluster.
- Kjør [npx cdk deploy](../README.md#deploy-using-cdk) som utløser Aurora-cluster erstatning og SLETTER ALLE VEKTOR-ELEMENTER.
- Følg [Database Migreringsveiledning](./DATABASE_MIGRATION_nb-NO.md) for å gjenopprette vektor-elementer.
- Verifiser at brukere kan benytte eksisterende boter som har kunnskap, dvs. RAG-boter.

### Legg til CreatingBotAllowed-tillatelse

- Etter distribueringen vil alle brukere være ute av stand til å opprette nye boter.
- Hvis du vil at spesifikke brukere skal kunne opprette boter, legg til disse brukerne i `CreatingBotAllowed`-gruppen ved hjelp av administrasjonskonsollen eller CLI.
- Verifiser om brukeren kan opprette en bot. Merk at brukerne må logge inn på nytt.