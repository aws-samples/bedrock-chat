# Rozwój lokalny

## Programowanie backendu

Sprawdź [backend/README](../backend/README_pl-PL.md).

## Programowanie frontendowe

W tym przykładzie możesz lokalnie modyfikować i uruchamiać frontend przy użyciu zasobów AWS (`API Gateway`, `Cognito` itp.), które zostały wdrożone za pomocą `npx cdk deploy`.

1. Zapoznaj się z [Wdrażaniem przy użyciu CDK](../README.md#deploy-using-cdk) w celu wdrożenia w środowisku AWS.
2. Skopiuj `frontend/.env.template` i zapisz jako `frontend/.env.local`.
3. Wypełnij zawartość `.env.local` na podstawie wyników wyjściowych `npx cdk deploy` (takich jak `BedrockChatStack.AuthUserPoolClientIdXXXXX`).
4. Wykonaj następujące polecenie:

```zsh
cd frontend && npm ci && npm run dev
```

## (Opcjonalnie, zalecane) Konfiguracja haka pre-commit

Wprowadziliśmy GitHub workflows do sprawdzania typów i lintowania. Są one wykonywane podczas tworzenia Pull Request, ale czekanie na zakończenie lintowania przed kontynuowaniem nie jest dobrym doświadczeniem podczas programowania. Dlatego zadania związane z lintowaniem powinny być wykonywane automatycznie na etapie commitowania. Wprowadziliśmy [Lefthook](https://github.com/evilmartians/lefthook?tab=readme-ov-file#install) jako mechanizm osiągnięcia tego celu. Nie jest to obowiązkowe, ale zalecamy jego przyjęcie dla wydajnego doświadczenia programistycznego. Dodatkowo, mimo że nie wymuszamy formatowania TypeScriptu za pomocą [Prettier](https://prettier.io/), bylibyśmy wdzięczni, gdybyś go przyjął podczas współpracy, ponieważ pomaga to unikać niepotrzebnych różnic podczas przeglądów kodu.

### Zainstaluj lefthook

Zapoznaj się [tutaj](https://github.com/evilmartians/lefthook#install). Jeśli używasz komputera Mac z homebrew, po prostu uruchom `brew install lefthook`.

### Zainstaluj poetry

Jest to wymagane, ponieważ lintowanie kodu Python zależy od `mypy` i `black`.

```sh
cd backend
python3 -m venv .venv  # Opcjonalne (jeśli nie chcesz instalować poetry w swoim środowisku)
source .venv/bin/activate  # Opcjonalne (jeśli nie chcesz instalować poetry w swoim środowisku)
pip install poetry
poetry install
```

Aby uzyskać więcej szczegółów, sprawdź [backend README](../backend/README_pl-PL.md).

### Utwórz haka pre-commit

Po prostu uruchom `lefthook install` w katalogu głównym tego projektu.