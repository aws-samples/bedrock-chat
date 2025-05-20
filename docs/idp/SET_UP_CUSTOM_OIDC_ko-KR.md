# 외부 ID 공급자 설정

## 1단계: OIDC 클라이언트 생성

대상 OIDC 제공자의 절차를 따르고 OIDC 클라이언트 ID와 비밀키의 값을 기록하세요. 또한 다음 단계에서 발급자 URL이 필요합니다. 설정 과정에서 리디렉션 URI가 필요한 경우, 배포 완료 후 대체될 더미 값을 입력하세요.

## 2단계: AWS Secrets Manager에 자격 증명 저장

1. AWS Management Console으로 이동합니다.
2. Secrets Manager로 이동하여 "새 보안 암호 저장"을 선택합니다.
3. "기타 유형의 보안 암호"를 선택합니다.
4. 클라이언트 ID와 클라이언트 비밀을 키-값 쌍으로 입력합니다.

   - 키: `clientId`, 값: <YOUR_GOOGLE_CLIENT_ID>
   - 키: `clientSecret`, 값: <YOUR_GOOGLE_CLIENT_SECRET>
   - 키: `issuerUrl`, 값: <ISSUER_URL_OF_THE_PROVIDER>

5. 프롬프트에 따라 보안 암호의 이름과 설명을 입력합니다. CDK 코드에서 사용할 보안 암호 이름을 기록해 두세요(3단계 변수 이름 <YOUR_SECRET_NAME>에 사용됨).
6. 보안 암호를 검토하고 저장합니다.

### 주의

키 이름은 정확히 `clientId`, `clientSecret`, `issuerUrl` 문자열과 일치해야 합니다.

## 3단계: cdk.json 업데이트

cdk.json 파일에 ID 제공자와 SecretName을 추가하세요.

다음과 같이 작성합니다:

```json
{
  "context": {
    // ...
    "identityProviders": [
      {
        "service": "oidc", // 변경하지 마세요
        "serviceName": "<YOUR_SERVICE_NAME>", // 원하는 값을 설정하세요
        "secretName": "<YOUR_SECRET_NAME>"
      }
    ],
    "userPoolDomainPrefix": "<UNIQUE_DOMAIN_PREFIX_FOR_YOUR_USER_POOL>"
  }
}
```

### 주의

#### 고유성

`userPoolDomainPrefix`는 모든 Amazon Cognito 사용자에 대해 전역적으로 고유해야 합니다. 이미 다른 AWS 계정에서 사용 중인 접두사를 선택하면 사용자 풀 도메인 생성이 실패합니다. 고유성을 보장하기 위해 식별자, 프로젝트 이름 또는 환경 이름을 접두사에 포함하는 것이 좋습니다.

## 4단계: CDK 스택 배포하기

AWS에 CDK 스택을 배포합니다:

```sh
npx cdk deploy --require-approval never --all
```

## 5단계: Cognito 리디렉션 URI로 OIDC 클라이언트 업데이트

스택을 배포한 후, CloudFormation 출력에 `AuthApprovedRedirectURI`가 표시됩니다. OIDC 구성으로 돌아가서 올바른 리디렉션 URI로 업데이트하세요.