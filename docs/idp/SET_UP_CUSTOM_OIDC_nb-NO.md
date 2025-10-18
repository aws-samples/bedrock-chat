# Konfigurer ekstern identitetsleverandør

## Steg 1: Opprett en OIDC-klient

Følg prosedyrene for den valgte OIDC-leverandøren, og noter verdiene for OIDC-klient-ID og hemmelighet. Utsteder-URL er også nødvendig for de følgende trinnene. Hvis redirect URI er nødvendig for oppsettsprosessen, skriv inn en midlertidig verdi som vil bli erstattet etter at distribusjonen er fullført.

## Trinn 2: Lagre påloggingsinformasjon i AWS Secrets Manager

1. Gå til AWS Management Console.
2. Naviger til Secrets Manager og velg "Store a new secret".
3. Velg "Other type of secrets".
4. Legg inn klient-ID og klienthemmelighet som nøkkel-verdi-par.

   - Nøkkel: `clientId`, Verdi: <YOUR_GOOGLE_CLIENT_ID>
   - Nøkkel: `clientSecret`, Verdi: <YOUR_GOOGLE_CLIENT_SECRET>
   - Nøkkel: `issuerUrl`, Verdi: <ISSUER_URL_OF_THE_PROVIDER>

5. Følg instruksjonene for å navngi og beskrive hemmeligheten. Noter deg hemmelighetsnavnet da du vil trenge det i CDK-koden din (Brukt i Trinn 3-variabelnavnet <YOUR_SECRET_NAME>).
6. Gjennomgå og lagre hemmeligheten.

### OBS

Nøkkelnavnene må være nøyaktig like strengene `clientId`, `clientSecret` og `issuerUrl`.

## Trinn 3: Oppdater cdk.json

I cdk.json-filen din, legg til ID-leverandøren og SecretName i cdk.json-filen.

slik som dette:

```json
{
  "context": {
    // ...
    "identityProviders": [
      {
        "service": "oidc", // Ikke endre
        "serviceName": "<YOUR_SERVICE_NAME>", // Sett hvilken verdi du vil
        "secretName": "<YOUR_SECRET_NAME>"
      }
    ],
    "userPoolDomainPrefix": "<UNIKT_DOMENE_PREFIKS_FOR_DIN_USER_POOL>"
  }
}
```

### OBS

#### Unikhet

`userPoolDomainPrefix` må være globalt unikt på tvers av alle Amazon Cognito-brukere. Hvis du velger et prefiks som allerede er i bruk av en annen AWS-konto, vil opprettelsen av brukerbassengets domene mislykkes. Det er god praksis å inkludere identifikatorer, prosjektnavn eller miljønavn i prefikset for å sikre unikhet.

## Steg 4: Distribuer CDK-stakken din

Distribuer CDK-stakken din til AWS:

```sh
npx cdk deploy --require-approval never --all
```

## Steg 5: Oppdater OIDC-klient med Cognito-omdirigeringsadresser

Etter at stacken er distribuert, vises `AuthApprovedRedirectURI` i CloudFormation-utdataene. Gå tilbake til OIDC-konfigurasjonen din og oppdater med de korrekte omdirigeringsadressene.