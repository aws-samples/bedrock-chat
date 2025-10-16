# Développement local

## Développement Backend

Voir [backend/README](../backend/README_fr-FR.md).

## Développement Frontend

Dans cet exemple, vous pouvez modifier et lancer localement le frontend en utilisant les ressources AWS (`API Gateway`, `Cognito`, etc.) qui ont été déployées avec `npx cdk deploy`.

1. Consultez [Deploy using CDK](../README.md#deploy-using-cdk) pour le déploiement dans l'environnement AWS.
2. Copiez le fichier `frontend/.env.template` et enregistrez-le sous `frontend/.env.local`.
3. Remplissez le contenu de `.env.local` en vous basant sur les résultats de sortie de `npx cdk deploy` (comme `BedrockChatStack.AuthUserPoolClientIdXXXXX`).
4. Exécutez la commande suivante :

```zsh
cd frontend && npm ci && npm run dev
```

## (Optionnel, recommandé) Configuration du hook pre-commit

Nous avons mis en place des workflows GitHub pour la vérification des types et le linting. Ceux-ci sont exécutés lors de la création d'une Pull Request, mais attendre que le linting se termine avant de poursuivre n'est pas une bonne expérience de développement. Par conséquent, ces tâches de linting devraient être effectuées automatiquement au moment du commit. Nous avons introduit [Lefthook](https://github.com/evilmartians/lefthook?tab=readme-ov-file#install) comme mécanisme pour y parvenir. Ce n'est pas obligatoire, mais nous recommandons son adoption pour une expérience de développement efficace. De plus, bien que nous n'imposions pas le formatage TypeScript avec [Prettier](https://prettier.io/), nous apprécierions que vous l'adoptiez lors de vos contributions, car cela aide à éviter les différences inutiles lors des revues de code.

### Installation de lefthook

Référez-vous à [cette page](https://github.com/evilmartians/lefthook#install). Si vous utilisez Mac et homebrew, exécutez simplement `brew install lefthook`.

### Installation de poetry

Ceci est nécessaire car le linting du code Python dépend de `mypy` et `black`.

```sh
cd backend
python3 -m venv .venv  # Optionnel (Si vous ne voulez pas installer poetry dans votre env)
source .venv/bin/activate  # Optionnel (Si vous ne voulez pas installer poetry dans votre env)
pip install poetry
poetry install
```

Pour plus de détails, veuillez consulter le [README du backend](../backend/README_fr-FR.md).

### Création d'un hook pre-commit

Il suffit d'exécuter `lefthook install` dans le répertoire racine de ce projet.