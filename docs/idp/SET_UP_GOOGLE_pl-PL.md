# Konfiguracja zewnętrznego dostawcy tożsamości dla Google

## Krok 1: Utwórz klienta Google OAuth 2.0

1. Przejdź do Konsoli Deweloperskiej Google.
2. Utwórz nowy projekt lub wybierz istniejący.
3. Przejdź do "Credentials" (Poświadczenia), kliknij "Create Credentials" (Utwórz poświadczenia) i wybierz "OAuth client ID".
4. Skonfiguruj ekran zgody, jeśli zostaniesz o to poproszony.
5. Jako typ aplikacji wybierz "Web application" (Aplikacja internetowa).
6. Pozostaw na razie puste pole URI przekierowania, aby ustawić je później.[Zobacz Krok 5](#step-5-update-google-oauth-client-with-cognito-redirect-uris)
7. Po utworzeniu, zapisz identyfikator klienta (Client ID) i tajny klucz klienta (Client Secret).

Aby uzyskać szczegółowe informacje, odwiedź [oficjalną dokumentację Google](https://support.google.com/cloud/answer/6158849?hl=en)

## Krok 2: Przechowywanie poświadczeń Google OAuth w AWS Secrets Manager

1. Przejdź do konsoli zarządzania AWS.
2. Przejdź do Secrets Manager i wybierz "Store a new secret".
3. Wybierz "Other type of secrets".
4. Wprowadź identyfikator clientId i clientSecret OAuth Google jako pary klucz-wartość.

   1. Klucz: clientId, Wartość: <YOUR_GOOGLE_CLIENT_ID>
   2. Klucz: clientSecret, Wartość: <YOUR_GOOGLE_CLIENT_SECRET>

5. Postępuj zgodnie z instrukcjami, aby nazwać i opisać sekret. Zapamiętaj nazwę sekretu, ponieważ będzie ona potrzebna w kodzie CDK. Na przykład: googleOAuthCredentials (Do wykorzystania w kroku 3 jako nazwa zmiennej <YOUR_SECRET_NAME>)
6. Przejrzyj i zapisz sekret.

### Uwaga

Nazwy kluczy muszą dokładnie odpowiadać ciągom znaków 'clientId' i 'clientSecret'.

## Krok 3: Aktualizacja cdk.json

W pliku cdk.json dodaj ID Dostawcy i SecretName do pliku cdk.json.

w następujący sposób:

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

### Uwaga

#### Unikalność

Prefiks userPoolDomainPrefix musi być globalnie unikalny dla wszystkich użytkowników Amazon Cognito. Jeśli wybierzesz prefiks, który jest już używany przez inne konto AWS, utworzenie domeny puli użytkowników nie powiedzie się. Dobrą praktyką jest uwzględnienie w prefiksie identyfikatorów, nazw projektów lub nazw środowisk, aby zapewnić unikalność.

## Krok 4: Wdróż swój stos CDK

Wdróż swój stos CDK na AWS:

```sh
npx cdk deploy --require-approval never --all
```

## Krok 5: Zaktualizuj klienta Google OAuth o URI przekierowania Cognito

Po wdrożeniu stosu, w wynikach CloudFormation wyświetlany jest AuthApprovedRedirectURI. Wróć do Konsoli Deweloperskiej Google i zaktualizuj klienta OAuth o prawidłowe URI przekierowania.