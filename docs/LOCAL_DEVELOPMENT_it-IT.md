# Sviluppo locale

## Sviluppo Backend

Vedi [backend/README](../backend/README_it-IT.md).

## Sviluppo Frontend

In questo esempio, puoi modificare e avviare localmente il frontend utilizzando le risorse AWS (`API Gateway`, `Cognito`, ecc.) che sono state distribuite con `npx cdk deploy`.

1. Fai riferimento a [Deploy using CDK](../README.md#deploy-using-cdk) per la distribuzione nell'ambiente AWS.
2. Copia `frontend/.env.template` e salvalo come `frontend/.env.local`.
3. Compila i contenuti di `.env.local` basandoti sui risultati dell'output di `npx cdk deploy` (come `BedrockChatStack.AuthUserPoolClientIdXXXXX`).
4. Esegui il seguente comando:

```zsh
cd frontend && npm ci && npm run dev
```

## (Opzionale, consigliato) Configurazione hook pre-commit

Abbiamo introdotto dei workflow GitHub per il controllo dei tipi e il linting. Questi vengono eseguiti quando viene creata una Pull Request, ma attendere il completamento del linting prima di procedere non è una buona esperienza di sviluppo. Pertanto, queste attività di linting dovrebbero essere eseguite automaticamente nella fase di commit. Abbiamo introdotto [Lefthook](https://github.com/evilmartians/lefthook?tab=readme-ov-file#install) come meccanismo per raggiungere questo obiettivo. Non è obbligatorio, ma consigliamo di adottarlo per un'esperienza di sviluppo efficiente. Inoltre, sebbene non imponiamo la formattazione TypeScript con [Prettier](https://prettier.io/), apprezzeremmo se poteste adottarlo quando contribuite, poiché aiuta a prevenire differenze non necessarie durante le revisioni del codice.

### Installare lefthook

Fare riferimento a [questo link](https://github.com/evilmartians/lefthook#install). Se sei un utente mac con homebrew, esegui semplicemente `brew install lefthook`.

### Installare poetry

Questo è necessario perché il linting del codice Python dipende da `mypy` e `black`.

```sh
cd backend
python3 -m venv .venv  # Opzionale (Se non vuoi installare poetry nel tuo ambiente)
source .venv/bin/activate  # Opzionale (Se non vuoi installare poetry nel tuo ambiente)
pip install poetry
poetry install
```

Per maggiori dettagli, consulta il [README del backend](../backend/README_it-IT.md).

### Creare un hook pre-commit

Esegui semplicemente `lefthook install` nella directory principale di questo progetto.