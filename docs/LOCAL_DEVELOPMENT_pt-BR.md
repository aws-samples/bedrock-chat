# Desenvolvimento local

## Desenvolvimento Backend

Veja [backend/README](../backend/README_pt-BR.md).

## Desenvolvimento Frontend

Nesta amostra, você pode modificar e iniciar localmente o frontend usando recursos da AWS (`API Gateway`, `Cognito`, etc.) que foram implantados com `npx cdk deploy`.

1. Consulte [Deploy using CDK](../README.md#deploy-using-cdk) para implantar no ambiente AWS.
2. Copie o `frontend/.env.template` e salve-o como `frontend/.env.local`.
3. Preencha o conteúdo do `.env.local` com base nos resultados de saída do `npx cdk deploy` (como `BedrockChatStack.AuthUserPoolClientIdXXXXX`).
4. Execute o seguinte comando:

```zsh
cd frontend && npm ci && npm run dev
```

## (Opcional, recomendado) Configurar hook de pre-commit

Introduzimos workflows do GitHub para verificação de tipos e linting. Estes são executados quando um Pull Request é criado, mas esperar pela conclusão do linting antes de prosseguir não é uma boa experiência de desenvolvimento. Portanto, essas tarefas de linting devem ser executadas automaticamente na etapa de commit. Introduzimos o [Lefthook](https://github.com/evilmartians/lefthook?tab=readme-ov-file#install) como mecanismo para alcançar isso. Não é obrigatório, mas recomendamos sua adoção para uma experiência de desenvolvimento eficiente. Além disso, embora não forcemos a formatação TypeScript com [Prettier](https://prettier.io/), apreciaríamos se você pudesse adotá-lo ao contribuir, pois ajuda a evitar diferenças desnecessárias durante as revisões de código.

### Instalar lefthook

Consulte [aqui](https://github.com/evilmartians/lefthook#install). Se você usa Mac e homebrew, basta executar `brew install lefthook`.

### Instalar poetry

Isso é necessário porque o linting do código Python depende do `mypy` e `black`.

```sh
cd backend
python3 -m venv .venv  # Opcional (Se você não quiser instalar o poetry no seu ambiente)
source .venv/bin/activate  # Opcional (Se você não quiser instalar o poetry no seu ambiente)
pip install poetry
poetry install
```

Para mais detalhes, consulte o [README do backend](../backend/README_pt-BR.md).

### Criar um hook de pre-commit

Basta executar `lefthook install` no diretório raiz deste projeto.