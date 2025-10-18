# Publikacja API

## Przegląd

Ta przykładowa implementacja zawiera funkcję publikowania interfejsów API. Choć interfejs czatu może być wygodny do wstępnej walidacji, faktyczna implementacja zależy od konkretnego przypadku użycia i pożądanych doświadczeń użytkownika (UX). W niektórych scenariuszach interfejs czatu może być preferowanym wyborem, podczas gdy w innych samodzielne API może być bardziej odpowiednie. Po wstępnej walidacji, ten przykład zapewnia możliwość publikowania dostosowanych botów zgodnie z potrzebami projektu. Poprzez wprowadzenie ustawień dla limitów, throttlingu, dozwolonych źródeł itp., można opublikować endpoint wraz z kluczem API, co zapewnia elastyczność w zakresie różnorodnych opcji integracji.

## Bezpieczeństwo

Używanie wyłącznie klucza API nie jest zalecane, jak opisano w: [AWS API Gateway Developer Guide](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-api-usage-plans.html). W związku z tym, ten przykład implementuje proste ograniczenie adresów IP za pomocą AWS WAF. Ze względu na koszty, reguła WAF jest stosowana wspólnie w całej aplikacji, przy założeniu, że źródła, które chcielibyśmy ograniczyć, są prawdopodobnie takie same dla wszystkich udostępnionych API. **Przy faktycznej implementacji należy przestrzegać polityki bezpieczeństwa swojej organizacji.** Zobacz także sekcję [Architecture](#architecture).

## Jak opublikować spersonalizowane API bota

### Wymagania wstępne

Ze względów bezpieczeństwa tylko ograniczona liczba użytkowników może publikować boty. Przed publikacją użytkownik musi być członkiem grupy o nazwie `PublishAllowed`, którą można skonfigurować poprzez konsolę zarządzania > Amazon Cognito User pools lub aws cli. Należy pamiętać, że id puli użytkowników można sprawdzić w CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`.

![](./imgs/group_membership_publish_allowed.png)

### Ustawienia publikacji API

Po zalogowaniu się jako użytkownik z grupy `PublishedAllowed` i utworzeniu bota, wybierz `API PublishSettings`. Pamiętaj, że tylko bot udostępniony może zostać opublikowany.
![](./imgs/bot_api_publish_screenshot.png)

Na następnym ekranie możemy skonfigurować kilka parametrów dotyczących ograniczania przepustowości. Szczegółowe informacje znajdziesz również w: [Throttle API requests for better throughput](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html).
![](./imgs/bot_api_publish_screenshot2.png)

Po wdrożeniu pojawi się następujący ekran, gdzie można uzyskać adres URL punktu końcowego i klucz API. Możemy również dodawać i usuwać klucze API.

![](./imgs/bot_api_publish_screenshot3.png)

## Architektura

API jest publikowane zgodnie z poniższym diagramem:

![](./imgs/published_arch.png)

WAF służy do ograniczania adresów IP. Adresy można skonfigurować ustawiając parametry `publishedApiAllowedIpV4AddressRanges` i `publishedApiAllowedIpV6AddressRanges` w `cdk.json`.

Gdy użytkownik kliknie publikację bota, [AWS CodeBuild](https://aws.amazon.com/codebuild/) uruchamia zadanie wdrożenia CDK w celu utworzenia stosu API (Zobacz też: [Definicja CDK](../cdk/lib/api-publishment-stack.ts)), który zawiera API Gateway, Lambda i SQS. SQS służy do rozdzielenia żądania użytkownika i operacji LLM, ponieważ generowanie wyjścia może przekroczyć 30 sekund, co jest limitem kwoty API Gateway. Aby pobrać wynik, należy uzyskać dostęp do API asynchronicznie. Więcej szczegółów znajduje się w [Specyfikacji API](#api-specification).

Klient musi ustawić `x-api-key` w nagłówku żądania.

## Specyfikacja API

Zobacz [tutaj](https://aws-samples.github.io/bedrock-chat).