# Publikacja API

## Przegląd

Ten przykład zawiera funkcję publikowania interfejsów API. Chociaż interfejs czatu może być wygodny do wstępnej walidacji, rzeczywista implementacja zależy od konkretnego przypadku użycia i pożądanego doświadczenia użytkownika (UX). W niektórych scenariuszach interfejs czatu może być preferowanym wyborem, podczas gdy w innych bardziej odpowiedni może być samodzielny interfejs API. Po wstępnej walidacji ten przykład zapewnia możliwość publikowania dostosowanych botów zgodnie z potrzebami projektu. Wprowadzając ustawienia dla limitów przydziału, ograniczania przepustowości, źródeł itp., można opublikować endpoint wraz z kluczem API, oferując elastyczność dla różnych opcji integracji.

## Bezpieczeństwo

Używanie wyłącznie klucza API nie jest zalecane, zgodnie z opisem w: [Przewodniku dla deweloperów AWS API Gateway](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-api-usage-plans.html). W konsekwencji, ten przykład implementuje prostą restrykcję adresu IP za pomocą AWS WAF. Reguła WAF jest stosowana wspólnie w całej aplikacji ze względu na koszty, przy założeniu, że źródła, które chciałoby się ograniczyć, są prawdopodobnie takie same we wszystkich udostępnionych interfejsach API. **Prosimy o przestrzeganie polityki bezpieczeństwa własnej organizacji podczas faktycznej implementacji.** Zapoznaj się również z sekcją [Architektura](#architektura).

## Jak opublikować niestandardowe API bota

### Wymagania wstępne

Ze względów zarządzania, tylko ograniczona liczba użytkowników może publikować boty. Przed publikacją użytkownik musi być członkiem grupy o nazwie `PublishAllowed`, którą można skonfigurować za pośrednictwem konsoli zarządzania > Amazon Cognito User pools lub interfejsu AWS CLI. Należy pamiętać, że identyfikator puli użytkowników można znaleźć, uzyskując dostęp do CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`.

![](./imgs/group_membership_publish_allowed.png)

### Ustawienia publikacji API

Po zalogowaniu się jako użytkownik `PublishedAllowed` i utworzeniu bota, wybierz `API PublishSettings`. Należy pamiętać, że opublikować można tylko wspólnego bota.
![](./imgs/bot_api_publish_screenshot.png)

Na następnym ekranie można skonfigurować kilka parametrów dotyczących ograniczania przepustowości. Więcej szczegółów można znaleźć pod adresem: [Ograniczanie żądań API w celu poprawy przepustowości](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html).
![](./imgs/bot_api_publish_screenshot2.png)

Po wdrożeniu pojawi się następny ekran, na którym można uzyskać adres URL punktu końcowego i klucz API. Można również dodawać i usuwać klucze API.

![](./imgs/bot_api_publish_screenshot3.png)

## Architektura

API jest publikowane zgodnie z poniższym diagramem:

![](./imgs/published_arch.png)

WAF jest używany do ograniczania adresów IP. Adresy można skonfigurować, ustawiając parametry `publishedApiAllowedIpV4AddressRanges` i `publishedApiAllowedIpV6AddressRanges` w pliku `cdk.json`.

Gdy użytkownik kliknie publikację bota, [AWS CodeBuild](https://aws.amazon.com/codebuild/) uruchamia zadanie wdrożenia CDK w celu udostępnienia stosu API (patrz także: [Definicja CDK](../cdk/lib/api-publishment-stack.ts)), który zawiera API Gateway, Lambda i SQS. SQS jest używany do rozdzielenia żądania użytkownika i operacji LLM, ponieważ generowanie wyniku może przekroczyć 30 sekund, co jest limitem przydziału API Gateway. Aby pobrać wynik, należy uzyskać dostęp do API asynchronicznie. Więcej szczegółów można znaleźć w [Specyfikacji API](#api-specification).

Klient musi ustawić `x-api-key` w nagłówku żądania.

## Specyfikacja API

Sprawdź [tutaj](https://aws-samples.github.io/bedrock-claude-chat).