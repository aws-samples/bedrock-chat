# 외부 ID 공급자 설정

[원문](https://docs.github.com/en/enterprise-server@3.9/admin/identity-and-access-management/using-saml-for-enterprise-iam/configuring-authentication-and-provisioning-for-your-enterprise-using-azure-ad)

외부 ID 공급자(IdP)를 사용하면 중앙 집중식 사용자 관리가 가능하며 사용자가 여러 애플리케이션에 단일 ID를 사용할 수 있습니다. 

## 전제 조건

- Azure AD 테넌트에 대한 관리자 액세스 권한이 있어야 합니다.
- GitHub Enterprise에 대한 사이트 관리자 권한이 있어야 합니다.

## Azure AD에서 엔터프라이즈 애플리케이션 생성하기

1. Azure AD 관리 포털에서 **엔터프라이즈 애플리케이션**으로 이동합니다.
2. **새 애플리케이션**을 클릭합니다.
3. **GitHub Enterprise Server**를 검색하고 선택합니다.
4. 애플리케이션의 이름을 입력하고 **생성**을 클릭합니다.

## SAML 구성

1. GitHub Enterprise의 관리자 설정에서 **인증**으로 이동합니다.
2. **SAML 구성**을 클릭합니다.
3. Azure AD에서 다음 값을 복사하여 GitHub Enterprise에 입력합니다:
   - 로그인 URL
   - 발급자 URL
   - 공개 인증서
4. **설정 테스트**를 클릭하여 구성을 확인합니다.
5. 성공하면 **설정 저장**을 클릭합니다.

## 사용자 프로비저닝 구성

1. Azure AD에서 **프로비저닝** 탭으로 이동합니다.
2. **프로비저닝 모드**를 **자동**으로 설정합니다.
3. GitHub Enterprise에서 생성한 관리자 토큰을 입력합니다.
4. **연결 테스트**를 클릭하여 구성을 확인합니다.
5. **설정 저장**을 클릭합니다.

이제 사용자들은 Azure AD 자격 증명을 사용하여 GitHub Enterprise에 로그인할 수 있습니다.

## Step 1: OIDC 클라이언트 생성

대상 OIDC 공급자의 절차를 따르고, OIDC 클라이언트 ID와 시크릿 값을 기록해 두십시오. 또한 다음 단계에서 필요한 발급자 URL도 필요합니다. 설정 과정에서 리다이렉트 URI가 필요한 경우, 임시 값을 입력하십시오. 이는 배포가 완료된 후 교체될 것입니다.

## 2단계: AWS Secrets Manager에 자격 증명 저장

1. AWS Management Console로 이동합니다.
2. Secrets Manager로 이동하여 "새 보안 암호 저장"을 선택합니다.
3. "다른 유형의 보안 암호"를 선택합니다.
4. 클라이언트 ID와 클라이언트 시크릿을 키-값 쌍으로 입력합니다.

   - 키: `clientId`, 값: <YOUR_GOOGLE_CLIENT_ID>
   - 키: `clientSecret`, 값: <YOUR_GOOGLE_CLIENT_SECRET>
   - 키: `issuerUrl`, 값: <ISSUER_URL_OF_THE_PROVIDER>

5. 프롬프트에 따라 보안 암호의 이름을 지정하고 설명을 입력합니다. CDK 코드에서 필요하므로 보안 암호 이름을 기록해 두세요(3단계 변수 이름 <YOUR_SECRET_NAME>에서 사용됨).
6. 검토 후 보안 암호를 저장합니다.

### 주의사항

키 이름은 반드시 `clientId`, `clientSecret`, `issuerUrl` 문자열과 정확히 일치해야 합니다.

## Step 3: cdk.json 업데이트

cdk.json 파일에 ID 공급자와 SecretName을 추가하세요.

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

`userPoolDomainPrefix`는 모든 Amazon Cognito 사용자에 대해 전역적으로 고유해야 합니다. 다른 AWS 계정에서 이미 사용 중인 접두사를 선택하면 사용자 풀 도메인 생성이 실패합니다. 고유성을 보장하기 위해 식별자, 프로젝트 이름 또는 환경 이름을 접두사에 포함하는 것이 좋은 방법입니다.

## Step 4: CDK 스택 배포하기

AWS에 CDK 스택을 배포하세요:

```sh
npx cdk deploy --require-approval never --all
```

## Step 5: Cognito 리다이렉트 URI로 OIDC 클라이언트 업데이트

스택 배포 후, CloudFormation 출력에 `AuthApprovedRedirectURI`가 표시됩니다. OIDC 구성으로 돌아가서 올바른 리다이렉트 URI로 업데이트하세요.