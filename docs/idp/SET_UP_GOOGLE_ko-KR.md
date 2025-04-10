# Google 외부 ID 공급자 설정

## 1단계: Google OAuth 2.0 클라이언트 생성

1. Google 개발자 콘솔로 이동합니다.
2. 새 프로젝트를 생성하거나 기존 프로젝트를 선택합니다.
3. "자격 증명"으로 이동한 후 "자격 증명 만들기"를 클릭하고 "OAuth 클라이언트 ID"를 선택합니다.
4. 메시지가 표시되면 동의 화면을 구성합니다.
5. 애플리케이션 유형으로 "웹 애플리케이션"을 선택합니다.
6. 리디렉션 URI는 나중에 설정할 것이므로 지금은 비워둔 채로 임시 저장합니다.[5단계 참조](#step-5-update-google-oauth-client-with-cognito-redirect-uris)
7. 생성된 후 클라이언트 ID와 클라이언트 시크릿을 기록해 둡니다.

자세한 내용은 [Google의 공식 문서](https://support.google.com/cloud/answer/6158849?hl=en)를 참조하세요.

## 2단계: AWS Secrets Manager에 Google OAuth 자격 증명 저장

1. AWS 관리 콘솔로 이동합니다.
2. Secrets Manager로 이동하여 "새 비밀 저장"을 선택합니다.
3. "기타 유형의 비밀"을 선택합니다.
4. Google OAuth clientId와 clientSecret을 키-값 쌍으로 입력합니다.

   1. 키: clientId, 값: <YOUR_GOOGLE_CLIENT_ID>
   2. 키: clientSecret, 값: <YOUR_GOOGLE_CLIENT_SECRET>

5. 프롬프트에 따라 비밀에 이름과 설명을 지정합니다. CDK 코드에서 사용할 비밀 이름을 기록해 두세요. 예를 들어, googleOAuthCredentials. (3단계 변수 이름 <YOUR_SECRET_NAME>에서 사용)
6. 비밀을 검토하고 저장합니다.

### 주의

키 이름은 정확히 'clientId'와 'clientSecret' 문자열과 일치해야 합니다.

## 3단계: cdk.json 업데이트

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

### 주의

#### 고유성

userPoolDomainPrefix는 모든 Amazon Cognito 사용자에서 전역적으로 고유해야 합니다. 이미 다른 AWS 계정에서 사용 중인 접두사를 선택하면 사용자 풀 도메인 생성이 실패합니다. 고유성을 보장하기 위해 식별자, 프로젝트 이름 또는 환경 이름을 접두사에 포함하는 것이 좋습니다.

## 4단계: CDK 스택 배포하기

AWS에 CDK 스택을 배포합니다:

```sh
npx cdk deploy --require-approval never --all
```

## 5단계: Cognito 리디렉션 URI로 Google OAuth 클라이언트 업데이트

스택을 배포한 후, CloudFormation 출력에 AuthApprovedRedirectURI가 표시됩니다. Google 개발자 콘솔로 돌아가서 OAuth 클라이언트를 올바른 리디렉션 URI로 업데이트하세요.