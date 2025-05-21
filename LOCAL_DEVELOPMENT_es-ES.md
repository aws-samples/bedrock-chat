# Desarrollo local

## Desarrollo Backend

Consulte [backend/README](../backend/README_es-ES.md).

## Desarrollo Frontend

En este ejemplo, puede modificar e iniciar localmente el frontend utilizando recursos de AWS (`API Gateway`, `Cognito`, etc.) que se han desplegado con `npx cdk deploy`.

1. Consulte [Desplegar usando CDK](../README.md#deploy-using-cdk) para implementar en el entorno de AWS.
2. Copie `frontend/.env.template` y guárdelo como `frontend/.env.local`.
3. Complete el contenido de `.env.local` basándose en los resultados de salida de `npx cdk deploy` (como `BedrockChatStack.AuthUserPoolClientIdXXXXX`).
4. Ejecute el siguiente comando:

```zsh
cd frontend && npm ci && npm run dev
```

## (Opcional, recomendado) Configurar hook pre-commit

Hemos introducido flujos de trabajo de GitHub para la verificación de tipos y el linting. Estos se ejecutan cuando se crea una Pull Request, pero esperar a que finalice el linting no es una buena experiencia de desarrollo. Por lo tanto, estas tareas de linting deben realizarse automáticamente en la etapa de commit. Hemos introducido [Lefthook](https://github.com/evilmartians/lefthook?tab=readme-ov-file#install) como un mecanismo para lograrlo. No es obligatorio, pero recomendamos adoptarlo para una experiencia de desarrollo eficiente. Además, aunque no imponemos el formato de TypeScript con [Prettier](https://prettier.io/), agradeceríamos que lo adopte al contribuir, ya que ayuda a prevenir diffs innecesarios durante las revisiones de código.

### Instalar lefthook

Consulte [aquí](https://github.com/evilmartians/lefthook#install). Si es usuario de Mac y Homebrew, simplemente ejecute `brew install lefthook`.

### Instalar poetry

Esto es necesario porque el linting de código Python depende de `mypy` y `black`.

```sh
cd backend
python3 -m venv .venv  # Opcional (Si no quiere instalar poetry en su entorno)
source .venv/bin/activate  # Opcional (Si no quiere instalar poetry en su entorno)
pip install poetry
poetry install
```

Para más detalles, consulte el [README del backend](../backend/README_es-ES.md).

### Crear un hook pre-commit

Simplemente ejecute `lefthook install` en el directorio raíz de este proyecto.