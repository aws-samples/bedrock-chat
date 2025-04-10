# Lokal utvikling

## Backend-utvikling

Se [backend/README](../backend/README_nb-NO.md).

## Frontend-utvikling

I denne eksempelen kan du lokalt modifisere og starte frontend-en ved hjelp av AWS-ressurser (`API Gateway`, `Cognito`, osv.) som er distribuert med `npx cdk deploy`.

1. Se [Distribuer ved hjelp av CDK](../README.md#deploy-using-cdk) for distribusjon i AWS-miljøet.
2. Kopier `frontend/.env.template` og lagre den som `frontend/.env.local`.
3. Fyll ut innholdet i `.env.local` basert på resultatene fra `npx cdk deploy` (som `BedrockChatStack.AuthUserPoolClientIdXXXXX`).
4. Kjør følgende kommando:

```zsh
cd frontend && npm ci && npm run dev
```

## (Valgfritt, anbefalt) Sett opp pre-commit hook

Vi har introdusert GitHub-arbeidsflyter for type-sjekking og linting. Disse blir utført når en Pull Request opprettes, men å vente på at linting skal fullføres før man fortsetter er ikke en god utviklingsopplevelse. Derfor bør disse linting-oppgavene utføres automatisk på commit-stadiet. Vi har introdusert [Lefthook](https://github.com/evilmartians/lefthook?tab=readme-ov-file#install) som en mekanisme for å oppnå dette. Det er ikke obligatorisk, men vi anbefaler å ta det i bruk for en effektiv utviklingsopplevelse. I tillegg, selv om vi ikke håndhever TypeScript-formatering med [Prettier](https://prettier.io/), setter vi pris på om du kan ta det i bruk ved bidrag, da det hjelper med å forhindre unødvendige forskjeller under kodegjennomganger.

### Installer lefthook

Se [her](https://github.com/evilmartians/lefthook#install). Hvis du er Mac- og Homebrew-bruker, kjør ganske enkelt `brew install lefthook`.

### Installer poetry

Dette er nødvendig fordi python-kode linting avhenger av `mypy` og `black`.

```sh
cd backend
python3 -m venv .venv  # Valgfritt (Hvis du ikke vil installere poetry i miljøet ditt)
source .venv/bin/activate  # Valgfritt (Hvis du ikke vil installere poetry i miljøet ditt)
pip install poetry
poetry install
```

For mer detaljer, sjekk [backend README](../backend/README_nb-NO.md).

### Opprett en pre-commit hook

Kjør ganske enkelt `lefthook install` i prosjektets rotmappe.