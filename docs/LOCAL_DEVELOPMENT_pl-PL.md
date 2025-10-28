# Lokalne środowisko programistyczne

## Rozwój Backendu

Zobacz [backend/README](../backend/README_pl-PL.md).

## Rozwój Frontendu

W tym przykładzie możesz lokalnie modyfikować i uruchamiać frontend wykorzystując zasoby AWS (`API Gateway`, `Cognito`, itp.), które zostały wdrożone za pomocą `npx cdk deploy`.

1. Zapoznaj się z [Deploy using CDK](../README.md#deploy-using-cdk), aby wdrożyć w środowisku AWS.
2. Skopiuj `frontend/.env.template` i zapisz go jako `frontend/.env.local`.
3. Wypełnij zawartość `.env.local` na podstawie wyników wyjściowych `npx cdk deploy` (takich jak `BedrockChatStack.AuthUserPoolClientIdXXXXX`).
4. Wykonaj następujące polecenie:

```zsh
cd frontend && npm ci && npm run dev
```

## (Opcjonalne, zalecane) Konfiguracja hooka pre-commit

Wprowadziliśmy przepływy pracy GitHub do sprawdzania typów i lintingu. Są one wykonywane przy tworzeniu Pull Requesta, ale czekanie na zakończenie lintingu przed kontynuowaniem nie jest dobrym doświadczeniem programistycznym. Dlatego te zadania lintingu powinny być wykonywane automatycznie na etapie commita. Wprowadziliśmy [Lefthook](https://github.com/evilmartians/lefthook?tab=readme-ov-file#install) jako mechanizm do osiągnięcia tego celu. Nie jest to obowiązkowe, ale zalecamy jego przyjęcie w celu zapewnienia efektywnego doświadczenia programistycznego. Dodatkowo, chociaż nie wymuszamy formatowania TypeScript za pomocą [Prettier](https://prettier.io/), docenilibyśmy jego stosowanie podczas wnoszenia wkładu, ponieważ pomaga to zapobiec niepotrzebnym różnicom podczas przeglądów kodu.

### Instalacja lefthook

Zobacz [tutaj](https://github.com/evilmartians/lefthook#install). Jeśli jesteś użytkownikiem maca i homebrew, wystarczy uruchomić `brew install lefthook`.

### Instalacja poetry

Jest to wymagane, ponieważ linting kodu pythonowego zależy od `mypy` i `black`.

```sh
cd backend
python3 -m venv .venv  # Opcjonalne (Jeśli nie chcesz instalować poetry w swoim środowisku)
source .venv/bin/activate  # Opcjonalne (Jeśli nie chcesz instalować poetry w swoim środowisku)
pip install poetry
poetry install
```

Aby uzyskać więcej szczegółów, sprawdź [backend README](../backend/README_pl-PL.md).

### Utworzenie hooka pre-commit

Wystarczy uruchomić `lefthook install` w głównym katalogu tego projektu.