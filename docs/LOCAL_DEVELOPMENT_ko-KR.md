# 로컬 개발

## 백엔드 개발

[backend/README](../backend/README_ko-KR.md)를 참조하세요.

## 프론트엔드 개발

이 샘플에서는 `npx cdk deploy`로 배포된 AWS 리소스(`API Gateway`, `Cognito` 등)를 사용하여 프론트엔드를 로컬에서 수정하고 실행할 수 있습니다.

1. AWS 환경에 배포하려면 [CDK로 배포](../README.md#deploy-using-cdk)를 참조하세요.
2. `frontend/.env.template`을 복사하여 `frontend/.env.local`로 저장합니다.
3. `npx cdk deploy`의 출력 결과(예: `BedrockChatStack.AuthUserPoolClientIdXXXXX`)를 기반으로 `.env.local`의 내용을 채웁니다.
4. 다음 명령을 실행합니다:

```zsh
cd frontend && npm ci && npm run dev
```

## (선택사항, 권장) 사전 커밋 훅 설정

GitHub 워크플로우를 통해 타입 검사 및 린팅을 도입했습니다. 이러한 작업은 풀 리퀘스트가 생성될 때 실행되지만, 린팅이 완료될 때까지 기다리는 것은 좋은 개발 경험이 아닙니다. 따라서 이러한 린팅 작업은 커밋 단계에서 자동으로 수행되어야 합니다. [Lefthook](https://github.com/evilmartians/lefthook?tab=readme-ov-file#install)을 이를 달성하기 위한 메커니즘으로 도입했습니다. 필수는 아니지만 효율적인 개발 경험을 위해 채택하는 것을 권장합니다. 또한 [Prettier](https://prettier.io/)로 TypeScript 포맷팅을 강제하지는 않지만, 코드 리뷰 중 불필요한 차이를 방지하기 위해 기여할 때 채택해 주시면 감사하겠습니다.

### Lefthook 설치

[여기](https://github.com/evilmartians/lefthook#install)를 참조하세요. Mac과 Homebrew 사용자라면 `brew install lefthook`을 실행하기만 하면 됩니다.

### Poetry 설치

Python 코드 린팅이 `mypy`와 `black`에 의존하기 때문에 필요합니다.

```sh
cd backend
python3 -m venv .venv  # 선택사항 (poetry를 환경에 설치하고 싶지 않은 경우)
source .venv/bin/activate  # 선택사항 (poetry를 환경에 설치하고 싶지 않은 경우)
pip install poetry
poetry install
```

자세한 내용은 [백엔드 README](../backend/README_ko-KR.md)를 확인하세요.

### 사전 커밋 훅 생성

프로젝트의 루트 디렉토리에서 `lefthook install`을 실행하기만 하면 됩니다.