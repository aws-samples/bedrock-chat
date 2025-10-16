# 외부 ID 공급자 설정

## Step 1: OIDC 클라이언트 생성

대상 OIDC 공급자의 절차를 따르고, OIDC 클라이언트 ID와 시크릿 값을 기록해 두십시오. 또한 다음 단계에서 발급자 URL이 필요합니다. 설정 과정에서 리디렉션 URI가 필요한 경우, 임시 값을 입력하십시오. 이는 배포가 완료된 후 교체될 것입니다.

## Step 2: AWS Secrets Manager에 자격 증명 저장하기

1. AWS Management Console로 이동합니다.
2. Secrets Manager로 이동하여 "새 보안 암호 저장"을 선택합니다.
3. "다른 유형의 보안 암호"를 선택합니다.
4. 클라이언트 ID와 클라이언트 시크릿을 키-값 쌍으로 입력합니다.

   - Key: `clientId`, Value: <YOUR_GOOGLE_CLIENT_ID>
   - Key: `clientSecret`, Value: <YOUR_GOOGLE_CLIENT_SECRET>
   - Key: `issuerUrl`, Value: <ISSUER_URL_OF_THE_PROVIDER>

5. 안내에 따라 보안 암호의 이름과 설명을 입력합니다. CDK 코드에서 필요하므로 보안 암호 이름을 기억해 두세요(Step 3의 변수명 <YOUR_SECRET_NAME>에서 사용됨).
6. 검토 후 보안 암호를 저장합니다.

### 주의사항

키 이름은 반드시 `clientId`, `clientSecret`, `issuerUrl` 문자열과 정확히 일치해야 합니다.

## 3단계: cdk.json 업데이트

cdk.json 파일에 ID 공급자와 SecretName을 추가하십시오.

다음과 같이 작성합니다:

```json
{
  "context": {
    // ...
    "identityProviders": [
      {
        "service": "oidc", // 변경하지 마세요
        "serviceName": "<YOUR_SERVICE_NAME>", // 원하는 값으로 설정하세요
        "secretName": "<YOUR_SECRET_NAME>"
      }
    ],
    "userPoolDomainPrefix": "<UNIQUE_DOMAIN_PREFIX_FOR_YOUR_USER_POOL>"
  }
}
```

### 주의사항

#### 고유성

`userPoolDomainPrefix`는 모든 Amazon Cognito 사용자 간에 전역적으로 고유해야 합니다. 다른 AWS 계정에서 이미 사용 중인 접두사를 선택하면 사용자 풀 도메인 생성이 실패합니다. 고유성을 보장하기 위해 식별자, 프로젝트 이름 또는 환경 이름을 접두사에 포함하는 것이 좋은 방법입니다.

## Step 4: CDK 스택 배포하기

CDK 스택을 AWS에 배포하세요:

```sh
npx cdk deploy --require-approval never --all
```

## Step 5: Cognito 리다이렉트 URI로 OIDC 클라이언트 업데이트

스택 배포 후, CloudFormation 출력에 `AuthApprovedRedirectURI`가 표시됩니다. OIDC 구성으로 돌아가서 올바른 리다이렉트 URI로 업데이트하세요.