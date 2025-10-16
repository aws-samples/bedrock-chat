# Google용 외부 인증 공급자 설정

## Step 1: Google OAuth 2.0 클라이언트 생성

1. Google Developer Console로 이동합니다.
2. 새 프로젝트를 생성하거나 기존 프로젝트를 선택합니다.
3. "Credentials(자격 증명)"으로 이동한 다음 "Create Credentials(자격 증명 만들기)"를 클릭하고 "OAuth client ID"를 선택합니다.
4. 메시지가 표시되면 동의 화면을 구성합니다.
5. 애플리케이션 유형으로 "Web application(웹 애플리케이션)"을 선택합니다.
6. 리디렉션 URI는 나중에 설정할 수 있도록 지금은 비워두고 임시로 저장합니다.[Step 5 참조](#step-5-update-google-oauth-client-with-cognito-redirect-uris)
7. 생성이 완료되면 클라이언트 ID와 클라이언트 시크릿을 메모해 둡니다.

자세한 내용은 [Google 공식 문서](https://support.google.com/cloud/answer/6158849?hl=en)를 참조하세요.

## 2단계: Google OAuth 자격 증명을 AWS Secrets Manager에 저장

1. AWS Management Console로 이동합니다.
2. Secrets Manager로 이동하여 "Store a new secret"을 선택합니다.
3. "Other type of secrets"를 선택합니다.
4. Google OAuth clientId와 clientSecret을 키-값 쌍으로 입력합니다.

   1. Key: clientId, Value: <YOUR_GOOGLE_CLIENT_ID>
   2. Key: clientSecret, Value: <YOUR_GOOGLE_CLIENT_SECRET>

5. 안내에 따라 시크릿의 이름을 지정하고 설명을 입력합니다. CDK 코드에서 필요하므로 시크릿 이름을 기억해 두세요. 예: googleOAuthCredentials (3단계 변수명 <YOUR_SECRET_NAME>에서 사용)
6. 시크릿을 검토하고 저장합니다.

### 주의사항

키 이름은 반드시 'clientId'와 'clientSecret' 문자열과 정확히 일치해야 합니다.

## Step 3: cdk.json 업데이트

cdk.json 파일에 ID 제공자와 SecretName을 추가하세요.

다음과 같이 작성합니다:

```json
{
  "context": {
    // ...
    "identityProviders": [
      {
        "service": "google",
        "secretName": "<YOUR_SECRET_NAME>"
      }
    ],
    "userPoolDomainPrefix": "<UNIQUE_DOMAIN_PREFIX_FOR_YOUR_USER_POOL>"
  }
}
```

### 주의사항

#### 고유성

userPoolDomainPrefix는 모든 Amazon Cognito 사용자들 사이에서 전역적으로 고유해야 합니다. 다른 AWS 계정에서 이미 사용 중인 접두사를 선택하면 사용자 풀 도메인 생성이 실패합니다. 고유성을 보장하기 위해 식별자, 프로젝트 이름 또는 환경 이름을 접두사에 포함하는 것이 좋습니다.

## Step 4: CDK 스택 배포하기

AWS에 CDK 스택을 배포하세요:

```sh
npx cdk deploy --require-approval never --all
```

## 5단계: Cognito 리다이렉트 URI로 Google OAuth 클라이언트 업데이트

스택 배포 후, CloudFormation 출력에 AuthApprovedRedirectURI가 표시됩니다. Google 개발자 콘솔로 돌아가서 올바른 리다이렉트 URI로 OAuth 클라이언트를 업데이트하세요.