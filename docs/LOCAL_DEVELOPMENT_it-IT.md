# Sviluppo locale

## Sviluppo Backend

Consulta [backend/README](../backend/README_it-IT.md).

## Sviluppo Frontend

In questo esempio, puoi modificare e avviare localmente il frontend utilizzando le risorse AWS (`API Gateway`, `Cognito`, ecc.) che sono state distribuite con `npx cdk deploy`.

1. Fare riferimento a [Distribuzione tramite CDK](../README.md#deploy-using-cdk) per la distribuzione nell'ambiente AWS.
2. Copiare `frontend/.env.template` e salvarlo come `frontend/.env.local`.
3. Compilare il contenuto di `.env.local` in base ai risultati dell'output di `npx cdk deploy` (come `BedrockChatStack.AuthUserPoolClientIdXXXXX`).
4. Eseguire il seguente comando:

```zsh
cd frontend && npm ci && npm run dev
```

## (Facoltativo, consigliato) Configurazione dell'hook pre-commit

Abbiamo introdotto dei workflow GitHub per il controllo dei tipi e il linting. Questi vengono eseguiti quando viene creata una Pull Request, ma attendere il completamento del linting prima di procedere non è una buona esperienza di sviluppo. Pertanto, questi compiti di linting dovrebbero essere eseguiti automaticamente durante la fase di commit. Abbiamo introdotto [Lefthook](https://github.com/evilmartians/lefthook?tab=readme-ov-file#install) come meccanismo per raggiungere questo obiettivo. Non è obbligatorio, ma consigliamo di adottarlo per un'esperienza di sviluppo efficiente. Inoltre, anche se non enforziamo la formattazione TypeScript con [Prettier](https://prettier.io/), apprezzeremmo che lo adottaste quando contribute, in quanto aiuta a prevenire differenze non necessarie durante le revisioni del codice.

### Installare lefthook

Fare riferimento [qui](https://github.com/evilmartians/lefthook#install). Se si è utenti Mac con homebrew, è sufficiente eseguire `brew install lefthook`.

### Installare poetry

Questo è necessario perché il linting del codice Python dipende da `mypy` e `black`.

```sh
cd backend
python3 -m venv .venv  # Facoltativo (se non si vuole installare poetry nell'ambiente)
source .venv/bin/activate  # Facoltativo (se non si vuole installare poetry nell'ambiente)
pip install poetry
poetry install
```

Per maggiori dettagli, consultare il [README del backend](../backend/README_it-IT.md).

### Creare un hook pre-commit

Eseguire semplicemente `lefthook install` nella directory root di questo progetto.