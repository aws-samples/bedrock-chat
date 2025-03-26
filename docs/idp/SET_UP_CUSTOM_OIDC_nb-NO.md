# Sett opp ekstern identitetsleverandør

## Trinn 1: Opprett en OIDC-klient

Følg prosedyrene for den aktuelle OIDC-leverandøren, og noter verdiene for OIDC-klient-ID og hemmelighet. Utgiver-URL er også påkrevd i de påfølgende trinnene. Hvis omdirigerings-URI kreves i oppsettsprosessen, angir du en midlertidig verdi som vil bli erstattet etter at distribusjonen er fullført.

## Trinn 2: Lagre Legitimasjon i AWS Secrets Manager

1. Gå til AWS Management Console.
2. Naviger til Secrets Manager og velg "Store a new secret".
3. Velg "Other type of secrets".
4. Legg inn klient-ID og klient-hemmelighet som nøkkel-verdi-par.

   - Nøkkel: `clientId`, Verdi: <YOUR_GOOGLE_CLIENT_ID>
   - Nøkkel: `clientSecret`, Verdi: <YOUR_GOOGLE_CLIENT_SECRET>
   - Nøkkel: `issuerUrl`, Verdi: <ISSUER_URL_OF_THE_PROVIDER>

5. Følg instruksjonene for å navngi og beskrive hemmeligheten. Merk deg hemmelighetsnavnet, da du vil trenge det i din CDK-kode (Brukt i Trinn 3 variabelnavn <YOUR_SECRET_NAME>).
6. Gjennomgå og lagre hemmeligheten.

### Merk

Nøkkelnavnene må nøyaktig samsvare med strengene `clientId`, `clientSecret` og `issuerUrl`.

## Trinn 3: Oppdater cdk.json

I din cdk.json-fil, legg til ID-leverandøren og hemmelighetsnavnet i cdk.json-filen.

som følger:

```json
{
  "context": {
    // ...
    "identityProviders": [
      {
        "service": "oidc", // Ikke endre
        "serviceName": "<DIN_TJENESTE_NAVN>", // Sett en verdi du vil
        "secretName": "<DITT_HEMMELIGHETSNAVN>"
      }
    ],
    "userPoolDomainPrefix": "<UNIKT_DOMENE_PREFIKS_FOR_DIN_BRUKERGRUPPE>"
  }
}
```

### Oppmerksomhet

#### Unike navn

`userPoolDomainPrefix` må være globalt unikt på tvers av alle Amazon Cognito-brukere. Hvis du velger et prefiks som allerede er i bruk av en annen AWS-konto, vil opprettelsen av brukergruppens domene mislykkes. Det er god praksis å inkludere identifikatorer, prosjektnavn eller miljønavn i prefikset for å sikre unike navn.

## Trinn 4: Distribuer CDK-stakken

Distribuer CDK-stakken til AWS:

```sh
npx cdk deploy --require-approval never --all
```

## Trinn 5: Oppdater OIDC-klient med Cognito Redirect-URI-er

Etter at stakken er distribuert, vil `AuthApprovedRedirectURI` vises i CloudFormation-resultatene. Gå tilbake til OIDC-konfigurasjonen din og oppdater med de riktige redirect-URI-ene.