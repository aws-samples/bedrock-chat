# 로컬 개발

## 백엔드 개발

[backend/README](../backend/README_ko-KR.md)를 참조하세요.

## 프론트엔드 개발

이 예제에서는 `npx cdk deploy`로 배포된 AWS 리소스(`API Gateway`, `Cognito` 등)를 사용하여 프론트엔드를 로컬에서 수정하고 실행할 수 있습니다.

1. AWS 환경에 배포하는 방법은 [Deploy using CDK](../README.md#deploy-using-cdk)를 참조하세요.
2. `frontend/.env.template`를 복사하여 `frontend/.env.local`로 저장하세요.
3. `npx cdk deploy`의 출력 결과(예: `BedrockChatStack.AuthUserPoolClientIdXXXXX`)를 바탕으로 `.env.local`의 내용을 채우세요.
4. 다음 명령어를 실행하세요:

```zsh
cd frontend && npm ci && npm run dev
```

## (선택사항, 권장) pre-commit 훅 설정하기

GitHub workflows를 통해 타입 체크와 린팅을 도입했습니다. 이러한 검사는 Pull Request가 생성될 때 실행되지만, 린팅이 완료될 때까지 기다리는 것은 좋은 개발 경험이 아닙니다. 따라서 이러한 린팅 작업은 커밋 단계에서 자동으로 수행되어야 합니다. 이를 위해 [Lefthook](https://github.com/evilmartians/lefthook?tab=readme-ov-file#install)을 도입했습니다. 필수는 아니지만, 효율적인 개발 경험을 위해 이를 채택하는 것을 권장합니다. 또한, [Prettier](https://prettier.io/)를 사용한 TypeScript 포맷팅을 강제하지는 않지만, 코드 리뷰 중 불필요한 차이를 방지하기 위해 기여할 때 이를 채택해 주시면 감사하겠습니다.

### Lefthook 설치하기

[여기](https://github.com/evilmartians/lefthook#install)를 참조하세요. Mac과 homebrew 사용자라면 간단히 `brew install lefthook`를 실행하면 됩니다.

### Poetry 설치하기

Python 코드 린팅이 `mypy`와 `black`에 의존하기 때문에 이 설치가 필요합니다.

```sh
cd backend
python3 -m venv .venv  # 선택사항 (자신의 환경에 poetry를 설치하고 싶지 않은 경우)
source .venv/bin/activate  # 선택사항 (자신의 환경에 poetry를 설치하고 싶지 않은 경우)
pip install poetry
poetry install
```

자세한 내용은 [backend README](../backend/README_ko-KR.md)를 확인해 주세요.

### pre-commit 훅 생성하기

이 프로젝트의 루트 디렉토리에서 `lefthook install`을 실행하기만 하면 됩니다.