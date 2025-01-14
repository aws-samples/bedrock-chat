# Local development

## Backend Development

See [backend/README](../backend/README.md).

## Frontend Development

In this sample, you can locally modify and launch the frontend using AWS resources (`API Gateway`, `Cognito`, etc.) that have been deployed with `npx cdk deploy`.

1. Refer to [Deploy using CDK](../README.md#deploy-using-cdk) for deploying on the AWS environment.
2. Copy the `frontend/.env.template` and save it as `frontend/.env.local`.
3. Fill in the contents of `.env.local` based on the output results of `npx cdk deploy` (such as `BedrockChatStack.AuthUserPoolClientIdXXXXX`).
4. Execute the following command:

```zsh
cd frontend && npm ci && npm run dev
```

## (Optional, recommended) Setup pre-commit hook

We have introduced a GitHub workflows for type-checking and linting. These are executed when a Pull Request is created, but waiting for the linting to complete before proceeding is not a good development experience. Therefore, these linting tasks should be performed automatically at the commit stage. We have introduced [Lefthook](https://github.com/evilmartians/lefthook?tab=readme-ov-file#install) as a mechanism to achieve this. It's not mandatory, but we recommend adopting it for an efficient development experience. Additionally, while we don't enforce TypeScript formatting with [Prettier](https://prettier.io/), we would appreciate it if you could adopt it when contributing, as it helps prevent unnecessary diffs during code reviews.

### Install lefthook

Refer [here](https://github.com/evilmartians/lefthook#install). If you are a mac and homebrew user, just run `brew install lefthook`.

### Install poetry

This is required because python code linting depends on `mypy` and `black`.

```sh
cd backend
python3 -m venv .venv  # Optional (If you don't want to install poetry on your env)
source .venv/bin/activate  # Optional (If you don't want to install poetry on your env)
pip install poetry
poetry install
```

For more detail, please check [backend README](../backend/README.md).

### Create a pre-commit hook

Just run `lefthook install` on the root directory of this project.
