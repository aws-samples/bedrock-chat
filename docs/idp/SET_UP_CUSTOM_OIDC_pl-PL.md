# Konfiguracja zewnętrznego dostawcy tożsamości

## Krok 1: Utwórz klienta OIDC

Postępuj zgodnie z procedurami dostawcy OIDC i zanotuj wartości identyfikatora klienta OIDC oraz sekretu. W kolejnych krokach wymagany będzie również adres URL wydawcy (issuer URL). Jeśli podczas procesu konfiguracji wymagany jest URI przekierowania, wprowadź tymczasową wartość, która zostanie zastąpiona po zakończeniu wdrożenia.

## Krok 2: Przechowywanie poświadczeń w AWS Secrets Manager

1. Przejdź do konsoli zarządzania AWS.
2. Przejdź do Secrets Manager i wybierz "Store a new secret".
3. Wybierz "Other type of secrets".
4. Wprowadź identyfikator klienta i tajny klucz klienta jako pary klucz-wartość.

   - Klucz: `clientId`, Wartość: <YOUR_GOOGLE_CLIENT_ID>
   - Klucz: `clientSecret`, Wartość: <YOUR_GOOGLE_CLIENT_SECRET>
   - Klucz: `issuerUrl`, Wartość: <ISSUER_URL_OF_THE_PROVIDER>

5. Postępuj zgodnie z instrukcjami, aby nazwać i opisać sekret. Zapamiętaj nazwę sekretu, ponieważ będzie ona potrzebna w kodzie CDK (Używana w kroku 3 jako nazwa zmiennej <YOUR_SECRET_NAME>).
6. Przejrzyj i zapisz sekret.

### Uwaga

Nazwy kluczy muszą dokładnie odpowiadać ciągom znaków `clientId`, `clientSecret` i `issuerUrl`.

## Krok 3: Aktualizacja cdk.json

W pliku cdk.json dodaj ID Dostawcy i SecretName do pliku cdk.json.

w następujący sposób:

```json
{
  "context": {
    // ...
    "identityProviders": [
      {
        "service": "oidc", // Nie zmieniaj
        "serviceName": "<YOUR_SERVICE_NAME>", // Ustaw dowolną wartość
        "secretName": "<YOUR_SECRET_NAME>"
      }
    ],
    "userPoolDomainPrefix": "<UNIQUE_DOMAIN_PREFIX_FOR_YOUR_USER_POOL>"
  }
}
```

### Uwaga

#### Unikalność

`userPoolDomainPrefix` musi być globalnie unikalny wśród wszystkich użytkowników Amazon Cognito. Jeśli wybierzesz prefiks, który jest już używany przez inne konto AWS, utworzenie domeny puli użytkowników nie powiedzie się. Dobrą praktyką jest uwzględnienie identyfikatorów, nazw projektów lub nazw środowisk w prefiksie, aby zapewnić unikalność.

## Krok 4: Wdróż swój stos CDK

Wdróż swój stos CDK na AWS:

```sh
npx cdk deploy --require-approval never --all
```

## Krok 5: Zaktualizuj klienta OIDC o adresy przekierowania Cognito

Po wdrożeniu stosu, `AuthApprovedRedirectURI` jest wyświetlany w wynikach CloudFormation. Wróć do swojej konfiguracji OIDC i zaktualizuj ją o prawidłowe adresy URI przekierowania.