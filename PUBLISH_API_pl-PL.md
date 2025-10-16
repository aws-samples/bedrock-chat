# Publikacja API

## Przegląd

Ta przykładowa implementacja zawiera funkcję publikowania API. Chociaż interfejs czatu może być wygodny do wstępnej walidacji, rzeczywista implementacja zależy od konkretnego przypadku użycia i pożądanego doświadczenia użytkownika (UX). W niektórych scenariuszach interfejs czatu może być preferowanym wyborem, podczas gdy w innych samodzielne API może być bardziej odpowiednie. Po wstępnej walidacji, ten przykład zapewnia możliwość publikowania dostosowanych botów zgodnie z potrzebami projektu. Poprzez wprowadzenie ustawień dla limitów, ograniczeń przepustowości, dozwolonych źródeł itp., można opublikować punkt końcowy wraz z kluczem API, oferując elastyczność w zakresie różnorodnych opcji integracji.

## Bezpieczeństwo

Używanie wyłącznie klucza API nie jest zalecane, jak opisano w: [AWS API Gateway Developer Guide](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-api-usage-plans.html). W związku z tym, ten przykład implementuje proste ograniczenie adresów IP za pomocą AWS WAF. Ze względu na koszty, reguła WAF jest stosowana wspólnie w całej aplikacji, przy założeniu, że źródła, które chcielibyśmy ograniczyć, są prawdopodobnie takie same dla wszystkich udostępnionych API. **Przy faktycznym wdrożeniu należy przestrzegać polityki bezpieczeństwa swojej organizacji.** Zobacz także sekcję [Architecture](#architecture).

## Jak opublikować spersonalizowane API bota

### Wymagania wstępne

Ze względów bezpieczeństwa tylko ograniczona liczba użytkowników może publikować boty. Przed publikacją użytkownik musi być członkiem grupy o nazwie `PublishAllowed`, którą można skonfigurować poprzez konsolę zarządzania > Amazon Cognito User pools lub aws cli. Należy pamiętać, że id puli użytkowników można sprawdzić przechodząc do CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`.

![](./imgs/group_membership_publish_allowed.png)

### Ustawienia publikowania API

Po zalogowaniu się jako użytkownik z uprawnieniami `PublishedAllowed` i utworzeniu bota, wybierz `API PublishSettings`. Pamiętaj, że tylko bot udostępniony może zostać opublikowany.
![](./imgs/bot_api_publish_screenshot.png)

Na następnym ekranie możemy skonfigurować kilka parametrów dotyczących ograniczania przepustowości. Szczegółowe informacje można znaleźć w: [Throttle API requests for better throughput](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html).
![](./imgs/bot_api_publish_screenshot2.png)

Po wdrożeniu pojawi się następujący ekran, gdzie można uzyskać adres URL punktu końcowego i klucz API. Możemy również dodawać i usuwać klucze API.

![](./imgs/bot_api_publish_screenshot3.png)

## Architektura

API jest publikowane zgodnie z poniższym diagramem:

![](./imgs/published_arch.png)

WAF służy do ograniczania adresów IP. Adresy można skonfigurować ustawiając parametry `publishedApiAllowedIpV4AddressRanges` i `publishedApiAllowedIpV6AddressRanges` w `cdk.json`.

Gdy użytkownik kliknie przycisk publikacji bota, [AWS CodeBuild](https://aws.amazon.com/codebuild/) uruchamia zadanie wdrożenia CDK w celu utworzenia stosu API (Zobacz też: [Definicja CDK](../cdk/lib/api-publishment-stack.ts)), który zawiera API Gateway, Lambda i SQS. SQS służy do rozdzielenia żądania użytkownika i operacji LLM, ponieważ generowanie wyjścia może przekroczyć 30 sekund, co jest limitem określonym w quotach API Gateway. Aby pobrać wynik, należy uzyskać dostęp do API w sposób asynchroniczny. Więcej szczegółów znajduje się w [Specyfikacji API](#api-specification).

Klient musi ustawić `x-api-key` w nagłówku żądania.

## Specyfikacja API

Zobacz [tutaj](https://aws-samples.github.io/bedrock-chat).