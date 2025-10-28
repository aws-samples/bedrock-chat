# Desarrollo local

## Desarrollo Backend

Ver [backend/README](../backend/README_es-ES.md).

## Desarrollo Frontend

En este ejemplo, puede modificar y lanzar localmente el frontend utilizando recursos de AWS (`API Gateway`, `Cognito`, etc.) que se han desplegado con `npx cdk deploy`.

1. Consulte [Deploy using CDK](../README.md#deploy-using-cdk) para el despliegue en el entorno AWS.
2. Copie `frontend/.env.template` y guárdelo como `frontend/.env.local`.
3. Complete el contenido de `.env.local` basándose en los resultados de salida de `npx cdk deploy` (como `BedrockChatStack.AuthUserPoolClientIdXXXXX`).
4. Ejecute el siguiente comando:

```zsh
cd frontend && npm ci && npm run dev
```

## (Opcional, recomendado) Configurar hook pre-commit

Hemos introducido flujos de trabajo de GitHub para la comprobación de tipos y el linting. Estos se ejecutan cuando se crea una Pull Request, pero esperar a que se complete el linting antes de continuar no es una buena experiencia de desarrollo. Por lo tanto, estas tareas de linting deberían realizarse automáticamente en la etapa de commit. Hemos introducido [Lefthook](https://github.com/evilmartians/lefthook?tab=readme-ov-file#install) como mecanismo para lograr esto. No es obligatorio, pero recomendamos adoptarlo para una experiencia de desarrollo eficiente. Además, aunque no imponemos el formateo de TypeScript con [Prettier](https://prettier.io/), agradeceríamos que lo adoptes al contribuir, ya que ayuda a evitar diferencias innecesarias durante las revisiones de código.

### Instalar lefthook

Consulta [aquí](https://github.com/evilmartians/lefthook#install). Si eres usuario de mac y homebrew, simplemente ejecuta `brew install lefthook`.

### Instalar poetry

Esto es necesario porque el linting del código Python depende de `mypy` y `black`.

```sh
cd backend
python3 -m venv .venv  # Opcional (Si no quieres instalar poetry en tu entorno)
source .venv/bin/activate  # Opcional (Si no quieres instalar poetry en tu entorno)
pip install poetry
poetry install
```

Para más detalles, consulta el [README del backend](../backend/README_es-ES.md).

### Crear un hook pre-commit

Simplemente ejecuta `lefthook install` en el directorio raíz de este proyecto.