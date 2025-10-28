# Lokal utvikling

## Backend-utvikling

Se [backend/README](../backend/README_nb-NO.md).

## Frontend-utvikling

I dette eksempelet kan du lokalt endre og starte frontend ved å bruke AWS-ressurser (`API Gateway`, `Cognito`, osv.) som har blitt distribuert med `npx cdk deploy`.

1. Se [Deploy using CDK](../README.md#deploy-using-cdk) for distribusjon i AWS-miljøet.
2. Kopier `frontend/.env.template` og lagre den som `frontend/.env.local`.
3. Fyll ut innholdet i `.env.local` basert på utdataresultatene fra `npx cdk deploy` (som `BedrockChatStack.AuthUserPoolClientIdXXXXX`).
4. Kjør følgende kommando:

```zsh
cd frontend && npm ci && npm run dev
```

## (Valgfritt, anbefalt) Oppsett av pre-commit hook

Vi har innført GitHub-arbeidsflyter for typekontroll og linting. Disse kjøres når en Pull Request opprettes, men å vente på at lintingen skal fullføres før man går videre gir ikke en god utvikleropplevelse. Derfor bør disse linting-oppgavene utføres automatisk på commit-stadiet. Vi har innført [Lefthook](https://github.com/evilmartians/lefthook?tab=readme-ov-file#install) som en mekanisme for å oppnå dette. Det er ikke obligatorisk, men vi anbefaler å ta det i bruk for en effektiv utvikleropplevelse. I tillegg, selv om vi ikke håndhever TypeScript-formatering med [Prettier](https://prettier.io/), ville vi sette pris på om du kunne bruke det når du bidrar, da det bidrar til å forhindre unødvendige forskjeller under kodegjennomganger.

### Installer lefthook

Se [her](https://github.com/evilmartians/lefthook#install). Hvis du bruker Mac og homebrew, kjør bare `brew install lefthook`.

### Installer poetry

Dette er nødvendig fordi python-kodelinting er avhengig av `mypy` og `black`.

```sh
cd backend
python3 -m venv .venv  # Valgfritt (Hvis du ikke vil installere poetry i ditt miljø)
source .venv/bin/activate  # Valgfritt (Hvis du ikke vil installere poetry i ditt miljø)
pip install poetry
poetry install
```

For mer informasjon, vennligst sjekk [backend README](../backend/README_nb-NO.md).

### Opprett en pre-commit hook

Kjør bare `lefthook install` i rotkatalogen til dette prosjektet.