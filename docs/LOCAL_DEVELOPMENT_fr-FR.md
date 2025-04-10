# Développement local

## Développement Backend

Consultez [backend/README](../backend/README_fr-FR.md).

## Développement Frontend

Dans cet exemple, vous pouvez modifier et lancer localement le frontend en utilisant des ressources AWS (`API Gateway`, `Cognito`, etc.) qui ont été déployées avec `npx cdk deploy`.

1. Consultez [Déployer avec CDK](../README.md#deploy-using-cdk) pour le déploiement sur l'environnement AWS.
2. Copiez `frontend/.env.template` et enregistrez-le sous `frontend/.env.local`.
3. Remplissez le contenu de `.env.local` en fonction des résultats de sortie de `npx cdk deploy` (comme `BedrockChatStack.AuthUserPoolClientIdXXXXX`).
4. Exécutez la commande suivante :

```zsh
cd frontend && npm ci && npm run dev
```

## (Optionnel, recommandé) Configuration du hook pre-commit

Nous avons introduit des workflows GitHub pour le type-checking et le linting. Ceux-ci sont exécutés lors de la création d'une Pull Request, mais attendre que le linting soit terminé avant de continuer n'est pas une bonne expérience de développement. Par conséquent, ces tâches de linting doivent être effectuées automatiquement à l'étape du commit. Nous avons introduit [Lefthook](https://github.com/evilmartians/lefthook?tab=readme-ov-file#install) comme mécanisme pour y parvenir. Ce n'est pas obligatoire, mais nous recommandons de l'adopter pour une expérience de développement efficace. De plus, bien que nous n'imposions pas le formatage TypeScript avec [Prettier](https://prettier.io/), nous apprécierions que vous l'adoptiez lors de vos contributions, car cela aide à éviter les différences inutiles lors des revues de code.

### Installer lefthook

Reportez-vous [ici](https://github.com/evilmartians/lefthook#install). Si vous utilisez un Mac avec Homebrew, exécutez simplement `brew install lefthook`.

### Installer poetry

Ceci est requis car le linting du code Python dépend de `mypy` et `black`.

```sh
cd backend
python3 -m venv .venv  # Optionnel (Si vous ne voulez pas installer poetry dans votre environnement)
source .venv/bin/activate  # Optionnel (Si vous ne voulez pas installer poetry dans votre environnement)
pip install poetry
poetry install
```

Pour plus de détails, veuillez consulter le [README du backend](../backend/README_fr-FR.md).

### Créer un hook pre-commit

Exécutez simplement `lefthook install` dans le répertoire racine de ce projet.