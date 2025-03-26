# Lokale Entwicklung

## Backend-Entwicklung

Lesen Sie [backend/README](../backend/README_de-DE.md).

## Frontend-Entwicklung

In diesem Beispiel können Sie das Frontend lokal modifizieren und starten und dabei AWS-Ressourcen (`API Gateway`, `Cognito` usw.) verwenden, die mit `npx cdk deploy` bereitgestellt wurden.

1. Informieren Sie sich unter [Bereitstellung mit CDK](../README.md#deploy-using-cdk) zur Bereitstellung in der AWS-Umgebung.
2. Kopieren Sie `frontend/.env.template` und speichern Sie es als `frontend/.env.local`.
3. Füllen Sie den Inhalt von `.env.local` basierend auf den Ausgabeergebnissen von `npx cdk deploy` aus (wie z.B. `BedrockChatStack.AuthUserPoolClientIdXXXXX`).
4. Führen Sie den folgenden Befehl aus:

```zsh
cd frontend && npm ci && npm run dev
```

## (Optional, empfohlen) Einrichten eines Pre-Commit-Hooks

Wir haben GitHub-Workflows für Typenüberprüfung und Linting eingeführt. Diese werden ausgeführt, wenn ein Pull Request erstellt wird, aber darauf zu warten, dass das Linting abgeschlossen ist, bevor man fortfährt, ist keine gute Entwicklungserfahrung. Daher sollten diese Linting-Aufgaben automatisch in der Commit-Phase durchgeführt werden. Wir haben [Lefthook](https://github.com/evilmartians/lefthook?tab=readme-ov-file#install) als Mechanismus eingeführt, um dies zu erreichen. Es ist nicht obligatorisch, aber wir empfehlen, es für eine effiziente Entwicklungserfahrung zu übernehmen. Zusätzlich erzwingen wir keine TypeScript-Formatierung mit [Prettier](https://prettier.io/), aber wir würden uns freuen, wenn Sie es bei Ihren Beiträgen übernehmen könnten, da es hilft, unnötige Unterschiede bei Code-Reviews zu vermeiden.

### Lefthook installieren

Weitere Informationen finden Sie [hier](https://github.com/evilmartians/lefthook#install). Wenn Sie Mac- und Homebrew-Benutzer sind, führen Sie einfach `brew install lefthook` aus.

### Poetry installieren

Dies ist erforderlich, da das Python-Code-Linting von `mypy` und `black` abhängt.

```sh
cd backend
python3 -m venv .venv  # Optional (Wenn Sie Poetry nicht in Ihrer Umgebung installieren möchten)
source .venv/bin/activate  # Optional (Wenn Sie Poetry nicht in Ihrer Umgebung installieren möchten)
pip install poetry
poetry install
```

Weitere Details finden Sie in der [Backend-README](../backend/README_de-DE.md).

### Einen Pre-Commit-Hook erstellen

Führen Sie einfach `lefthook install` im Stammverzeichnis dieses Projekts aus.