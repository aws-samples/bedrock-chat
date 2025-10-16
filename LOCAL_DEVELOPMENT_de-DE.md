# Lokale Entwicklung

## Backend-Entwicklung

Siehe [backend/README](../backend/README_de-DE.md).

## Frontend-Entwicklung

In diesem Beispiel können Sie das Frontend lokal modifizieren und starten, wobei AWS-Ressourcen (`API Gateway`, `Cognito` etc.) verwendet werden, die mit `npx cdk deploy` bereitgestellt wurden.

1. Informationen zur Bereitstellung in der AWS-Umgebung finden Sie unter [Deploy using CDK](../README.md#deploy-using-cdk).
2. Kopieren Sie `frontend/.env.template` und speichern Sie es als `frontend/.env.local`.
3. Füllen Sie den Inhalt von `.env.local` basierend auf den Ausgabeergebnissen von `npx cdk deploy` aus (wie z.B. `BedrockChatStack.AuthUserPoolClientIdXXXXX`).
4. Führen Sie den folgenden Befehl aus:

```zsh
cd frontend && npm ci && npm run dev
```

## (Optional, empfohlen) Einrichten des Pre-Commit-Hooks

Wir haben GitHub-Workflows für Typenprüfung und Linting eingeführt. Diese werden ausgeführt, wenn ein Pull Request erstellt wird, aber auf den Abschluss des Linting zu warten ist keine gute Entwicklungserfahrung. Daher sollten diese Linting-Aufgaben automatisch in der Commit-Phase durchgeführt werden. Wir haben [Lefthook](https://github.com/evilmartians/lefthook?tab=readme-ov-file#install) als Mechanismus dafür eingeführt. Es ist nicht verpflichtend, aber wir empfehlen die Nutzung für eine effiziente Entwicklungserfahrung. Zusätzlich erzwingen wir zwar keine TypeScript-Formatierung mit [Prettier](https://prettier.io/), würden uns aber freuen, wenn Sie diese bei Ihren Beiträgen verwenden würden, da dies unnötige Unterschiede während Code-Reviews verhindert.

### Lefthook installieren

Siehe [hier](https://github.com/evilmartians/lefthook#install). Wenn Sie Mac und Homebrew-Nutzer sind, führen Sie einfach `brew install lefthook` aus.

### Poetry installieren

Dies ist erforderlich, da die Python-Code-Linting von `mypy` und `black` abhängt.

```sh
cd backend
python3 -m venv .venv  # Optional (Wenn Sie poetry nicht in Ihrer Umgebung installieren möchten)
source .venv/bin/activate  # Optional (Wenn Sie poetry nicht in Ihrer Umgebung installieren möchten)
pip install poetry
poetry install
```

Weitere Details finden Sie in der [Backend README](../backend/README_de-DE.md).

### Pre-Commit-Hook erstellen

Führen Sie einfach `lefthook install` im Hauptverzeichnis dieses Projekts aus.