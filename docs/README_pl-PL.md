# Bedrock Claude Chat (Nova)

![](https://img.shields.io/github/v/release/aws-samples/bedrock-claude-chat?style=flat-square)
![](https://img.shields.io/github/license/aws-samples/bedrock-claude-chat?style=flat-square)
![](https://img.shields.io/github/actions/workflow/status/aws-samples/bedrock-claude-chat/cdk.yml?style=flat-square)
[![](https://img.shields.io/badge/roadmap-view-blue)](https://github.com/aws-samples/bedrock-claude-chat/issues?q=is%3Aissue%20state%3Aopen%20label%3Aroadmap)

[English](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/README.md) | [日本語](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_ja-JP.md) | [한국어](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_ko-KR.md) | [中文](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_zh-CN.md) | [Français](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_fr-FR.md) | [Deutsch](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_de-DE.md) | [Español](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_es-ES.md) | [Italian](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_it-IT.md) | [Norsk](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_nb-NO.md) | [ไทย](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_th-TH.md) | [Bahasa Indonesia](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_id-ID.md) | [Bahasa Melayu](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_ms-MY.md) | [Tiếng Việt](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_vi-VN.md) | [Polski](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_pl-PL.md)

> [!Ostrzeżenie]
>
> **Wydano wersję V2. Aby zaktualizować, prosimy dokładnie zapoznać się z [przewodnikiem migracji](./migration/V1_TO_V2_pl-PL.md).** Bez należytej staranności **BOTY Z WERSJI V1 STANĄ SIĘ BEZUŻYTECZNE.**

Wielojęzyczny chatbot wykorzystujący modele LLM dostarczane przez [Amazon Bedrock](https://aws.amazon.com/bedrock/) do generatywnej sztucznej inteligencji.

### Obejrzyj przegląd i instalację na YouTube

[![Przegląd](https://img.youtube.com/vi/PDTGrHlaLCQ/hq1.jpg)](https://www.youtube.com/watch?v=PDTGrHlaLCQ)

### Podstawowa rozmowa

![](./imgs/demo.gif)

### Personalizacja Bota

Dodaj własną instrukcję i udostępnij wiedzę zewnętrzną poprzez adres URL lub pliki (tzw. [RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/). Bot może być współdzielony między użytkownikami aplikacji. Dostosowany bot może również zostać opublikowany jako autonomiczne API (Patrz [szczegóły](./PUBLISH_API_pl-PL.md)).

![](./imgs/bot_creation.png)
![](./imgs/bot_chat.png)
![](./imgs/bot_api_publish_screenshot3.png)

> [!Ważne]
> Ze względów zarządzania, tylko uprawnieni użytkownicy mogą tworzyć dostosowane boty. Aby zezwolić na tworzenie dostosowanych botów, użytkownik musi być członkiem grupy o nazwie `CreatingBotAllowed`, którą można skonfigurować za pośrednictwem konsoli zarządzania > Pule użytkowników Amazon Cognito lub interfejsu wiersza poleceń AWS. Należy pamiętać, że identyfikator puli użytkowników można sprawdzić, uzyskując dostęp do CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`.

### Panel administratora

<details>
<summary>Panel administratora</summary>

Analizuj użycie dla każdego użytkownika / bota na panelu administratora. [szczegóły](./ADMINISTRATOR_pl-PL.md)

![](./imgs/admin_bot_analytics.png)

</details>

### Agent napędzany przez LLM

<details>
<summary>Agent napędzany przez LLM</summary>

Korzystając z [funkcjonalności Agenta](./AGENT_pl-PL.md), Twój chatbot może automatycznie obsługiwać bardziej złożone zadania. Na przykład, aby odpowiedzieć na pytanie użytkownika, Agent może pobrać niezbędne informacje z narzędzi zewnętrznych lub podzielić zadanie na wiele kroków do przetworzenia.

![](./imgs/agent1.png)
![](./imgs/agent2.png)

</details>

## 🚀 Super-proste Wdrożenie

- W regionie us-east-1 otwórz [Dostęp do modeli Bedrock](https://us-east-1.console.aws.amazon.com/bedrock/home?region=us-east-1#/modelaccess) > `Zarządzaj dostępem do modeli` > Zaznacz wszystkie opcje `Anthropic / Claude 3`, wszystkie opcje `Amazon / Nova`, `Amazon / Titan Text Embeddings V2` oraz `Cohere / Embed Multilingual`, a następnie `Zapisz zmiany`.

<details>
<summary>Zrzut ekranu</summary>

![](./imgs/model_screenshot.png)

</details>

- Otwórz [CloudShell](https://console.aws.amazon.com/cloudshell/home) w regionie, w którym chcesz wdrożyć
- Uruchom wdrożenie za pomocą następujących poleceń. Jeśli chcesz określić wersję do wdrożenia lub musisz zastosować zasady bezpieczeństwa, określ odpowiednie parametry z [Parametrów opcjonalnych](#opcjonalne-parametry).

```sh
git clone https://github.com/aws-samples/bedrock-claude-chat.git
cd bedrock-claude-chat
chmod +x bin.sh
./bin.sh
```

- Zostaniesz zapytany, czy jesteś nowym użytkownikiem, czy korzystasz z wersji 2. Jeśli nie jesteś użytkownikiem kontynuującym z wersji 0, wprowadź `y`.

### Parametry opcjonalne

Podczas wdrażania możesz określić następujące parametry w celu zwiększenia bezpieczeństwa i dostosowania:

- **--disable-self-register**: Wyłącz samodzielną rejestrację (domyślnie: włączone). Jeśli ta flaga jest ustawiona, musisz utworzyć wszystkich użytkowników w Cognito i nie zezwoli na samodzielną rejestrację kont.
- **--enable-lambda-snapstart**: Włącz [Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html) (domyślnie: wyłączone). Jeśli ta flaga jest ustawiona, poprawia czasy zimnego startu dla funkcji Lambda, zapewniając szybsze czasy odpowiedzi dla lepszego doświadczenia użytkownika.
- **--ipv4-ranges**: Rozdzielona przecinkami lista dozwolonych zakresów IPv4. (domyślnie: zezwalaj na wszystkie adresy IPv4)
- **--ipv6-ranges**: Rozdzielona przecinkami lista dozwolonych zakresów IPv6. (domyślnie: zezwalaj na wszystkie adresy IPv6)
- **--disable-ipv6**: Wyłącz połączenia przez IPv6. (domyślnie: włączone)
- **--allowed-signup-email-domains**: Rozdzielona przecinkami lista dozwolonych domen poczty elektronicznej do rejestracji. (domyślnie: brak ograniczeń domen)
- **--bedrock-region**: Zdefiniuj region, w którym dostępny jest Bedrock. (domyślnie: us-east-1)
- **--repo-url**: Niestandardowe repozytorium Bedrock Claude Chat do wdrożenia, jeśli zostało rozwidlone lub użyto niestandardowego systemu kontroli źródła. (domyślnie: https://github.com/aws-samples/bedrock-claude-chat.git)
- **--version**: Wersja Bedrock Claude Chat do wdrożenia. (domyślnie: najnowsza wersja w fazie rozwoju)
- **--cdk-json-override**: Możesz zastąpić dowolne wartości kontekstu CDK podczas wdrażania, używając bloku zastępowania JSON. Pozwala to na modyfikację konfiguracji bez bezpośredniej edycji pliku cdk.json.

Przykład użycia:

```bash
./bin.sh --cdk-json-override '{
  "context": {
    "selfSignUpEnabled": false,
    "enableLambdaSnapStart": true,
    "allowedIpV4AddressRanges": ["192.168.1.0/24"],
    "allowedSignUpEmailDomains": ["example.com"]
  }
}'
```

Zastępujący JSON musi mieć taką samą strukturę jak cdk.json. Możesz zastąpić dowolne wartości kontekstu, w tym:

- `selfSignUpEnabled`
- `enableLambdaSnapStart`
- `allowedIpV4AddressRanges`
- `allowedIpV6AddressRanges`
- `allowedSignUpEmailDomains`
- `bedrockRegion`
- `enableRagReplicas`
- `enableBedrockCrossRegionInference`
- I inne wartości kontekstu zdefiniowane w cdk.json

> [!Uwaga]
> Wartości zastępujące zostaną scalone z istniejącą konfiguracją cdk.json podczas wdrażania w AWS code build. Wartości określone w zastępowaniu będą miały pierwszeństwo przed wartościami w cdk.json.

#### Przykładowe polecenie z parametrami:

```sh
./bin.sh --disable-self-register --ipv4-ranges "192.0.2.0/25,192.0.2.128/25" --ipv6-ranges "2001:db8:1:2::/64,2001:db8:1:3::/64" --allowed-signup-email-domains "example.com,anotherexample.com" --bedrock-region "us-west-2" --version "v1.2.6"
```

- Po około 35 minutach otrzymasz następujące dane wyjściowe, które możesz otworzyć w przeglądarce

```
Frontend URL: https://xxxxxxxxx.cloudfront.net
```

![](./imgs/signin.png)

Pojawi się ekran rejestracji, jak pokazano powyżej, gdzie możesz zarejestrować swój adres e-mail i zalogować się.

> [!Ważne]
> Bez ustawienia parametru opcjonalnego ta metoda wdrażania pozwala każdemu, kto zna adres URL, na rejestrację. W przypadku użycia produkcyjnego zdecydowanie zaleca się dodanie ograniczeń adresów IP i wyłączenie samodzielnej rejestracji, aby ograniczyć ryzyko bezpieczeństwa (możesz zdefiniować allowed-signup-email-domains, aby ograniczyć użytkowników tylko do adresów e-mail z domeny Twojej firmy). Użyj zarówno ipv4-ranges, jak i ipv6-ranges do ograniczenia adresów IP i wyłącz samodzielną rejestrację, używając disable-self-register podczas wykonywania ./bin.

> [!WSKAZÓWKA]
> Jeśli `Frontend URL` nie pojawia się lub Bedrock Claude Chat nie działa poprawnie, może to być problem z najnowszą wersją. W takim przypadku dodaj `--version "v1.2.6"` do parametrów i spróbuj wdrożyć ponownie.

## Architektura

Jest to architektura zbudowana w oparciu o zarządzane usługi AWS, eliminująca potrzebę zarządzania infrastrukturą. Wykorzystanie Amazon Bedrock eliminuje konieczność komunikacji z interfejsami API spoza AWS. Umożliwia to wdrażanie skalowalnych, niezawodnych i bezpiecznych aplikacji.

- [Amazon DynamoDB](https://aws.amazon.com/dynamodb/): Baza danych NoSQL do przechowywania historii rozmów
- [Amazon API Gateway](https://aws.amazon.com/api-gateway/) + [AWS Lambda](https://aws.amazon.com/lambda/): Endpoint API zaplecza ([AWS Lambda Web Adapter](https://github.com/awslabs/aws-lambda-web-adapter), [FastAPI](https://fastapi.tiangolo.com/))
- [Amazon CloudFront](https://aws.amazon.com/cloudfront/) + [S3](https://aws.amazon.com/s3/): Dostarczanie aplikacji frontendowej ([React](https://react.dev/), [Tailwind CSS](https://tailwindcss.com/))
- [AWS WAF](https://aws.amazon.com/waf/): Ograniczanie adresów IP
- [Amazon Cognito](https://aws.amazon.com/cognito/): Uwierzytelnianie użytkowników
- [Amazon Bedrock](https://aws.amazon.com/bedrock/): Usługa zarządzana do wykorzystania modeli bazowych za pośrednictwem interfejsów API
- [Amazon Bedrock Knowledge Bases](https://aws.amazon.com/bedrock/knowledge-bases/): Zapewnia zarządzany interfejs dla Generowania Wspomaganego Wyszukiwaniem ([RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)), oferujący usługi osadzania i parsowania dokumentów
- [Amazon EventBridge Pipes](https://aws.amazon.com/eventbridge/pipes/): Odbieranie zdarzeń ze strumienia DynamoDB i uruchamianie Step Functions do osadzania wiedzy zewnętrznej
- [AWS Step Functions](https://aws.amazon.com/step-functions/): Orkiestracja potoku pozyskiwania w celu osadzenia wiedzy zewnętrznej w Bedrock Knowledge Bases
- [Amazon OpenSearch Serverless](https://aws.amazon.com/opensearch-service/features/serverless/): Służy jako baza danych zaplecza dla Bedrock Knowledge Bases, zapewniająca możliwości wyszukiwania pełnotekstowego i wektorowego, umożliwiająca dokładne wyszukiwanie istotnych informacji
- [Amazon Athena](https://aws.amazon.com/athena/): Usługa zapytań do analizowania zasobów w S3

![](./imgs/arch.png)

## Wdrażanie przy użyciu CDK

Super-łatwe wdrażanie używa [AWS CodeBuild](https://aws.amazon.com/codebuild/) do wykonywania wdrożenia wewnętrznie za pomocą CDK. Ta sekcja opisuje procedurę bezpośredniego wdrożenia przy użyciu CDK.

- Proszę mieć środowisko UNIX, Docker i środowisko uruchomieniowe Node.js. Jeśli nie, możesz również użyć [Cloud9](https://github.com/aws-samples/cloud9-setup-for-prototyping)

> [!Ważne]
> Jeśli podczas wdrażania jest niewystarczająca przestrzeń dyskowa w środowisku lokalnym, bootstrap CDK może zakończyć się błędem. Jeśli korzystasz z Cloud9 itp., zalecamy powiększenie rozmiaru woluminu instancji przed wdrożeniem.

- Sklonuj to repozytorium

```
git clone https://github.com/aws-samples/bedrock-claude-chat
```

- Zainstaluj pakiety npm

```
cd bedrock-claude-chat
cd cdk
npm ci
```

- W razie potrzeby edytuj następujące wpisy w [cdk.json](./cdk/cdk.json):

  - `bedrockRegion`: Region, w którym Bedrock jest dostępny. **UWAGA: Bedrock NIE obsługuje jeszcze wszystkich regionów.**
  - `allowedIpV4AddressRanges`, `allowedIpV6AddressRanges`: Dozwolony zakres adresów IP.
  - `enableLambdaSnapStart`: Domyślnie ustawione na true. Ustaw na false, jeśli wdrażasz w [regionie, który nie obsługuje Lambda SnapStart dla funkcji Python](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions).

- Przed wdrożeniem CDK musisz wykonać Bootstrap jeden raz dla regionu, w którym wdrażasz.

```
npx cdk bootstrap
```

- Wdróż ten przykładowy projekt

```
npx cdk deploy --require-approval never --all
```

- Otrzymasz dane wyjściowe podobne do następujących. Adres URL aplikacji internetowej zostanie wyświetlony w `BedrockChatStack.FrontendURL`, więc proszę uzyskać do niego dostęp przez przeglądarkę.

```sh
 ✅  BedrockChatStack

✨  Czas wdrożenia: 78.57s

Dane wyjściowe:
BedrockChatStack.AuthUserPoolClientIdXXXXX = xxxxxxx
BedrockChatStack.AuthUserPoolIdXXXXXX = ap-northeast-1_XXXX
BedrockChatStack.BackendApiBackendApiUrlXXXXX = https://xxxxx.execute-api.ap-northeast-1.amazonaws.com
BedrockChatStack.FrontendURL = https://xxxxx.cloudfront.net
```

### Definiowanie parametrów

Parametry wdrożenia można zdefiniować na dwa sposoby: używając `cdk.json` lub używając pliku `parameter.ts` z bezpiecznym typowaniem.

#### Używanie cdk.json (Tradycyjna metoda)

Tradycyjny sposób konfiguracji parametrów to edycja pliku `cdk.json`. To podejście jest proste, ale pozbawione sprawdzania typów:

```json
{
  "app": "npx ts-node --prefer-ts-exts bin/bedrock-chat.ts",
  "context": {
    "bedrockRegion": "us-east-1",
    "allowedIpV4AddressRanges": ["0.0.0.0/1", "128.0.0.0/1"],
    "selfSignUpEnabled": true
  }
}
```

#### Używanie parameter.ts (Zalecana metoda z bezpiecznym typowaniem)

Dla lepszego bezpieczeństwa typów i doświadczenia programisty możesz użyć pliku `parameter.ts` do zdefiniowania parametrów:

```typescript
// Zdefiniuj parametry dla środowiska domyślnego
bedrockChatParams.set("default", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["192.168.0.0/16"],
  selfSignUpEnabled: true,
});

// Zdefiniuj parametry dla dodatkowych środowisk
bedrockChatParams.set("dev", {
  bedrockRegion: "us-west-2",
  allowedIpV4AddressRanges: ["10.0.0.0/8"],
  enableRagReplicas: false, // Oszczędzanie kosztów dla środowiska deweloperskiego
});

bedrockChatParams.set("prod", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["172.16.0.0/12"],
  enableLambdaSnapStart: true,
  enableRagReplicas: true, // Zwiększona dostępność dla produkcji
});
```

> [!Uwaga]
> Istniejący użytkownicy mogą nadal używać `cdk.json` bez żadnych zmian. Podejście `parameter.ts` jest zalecane dla nowych wdrożeń lub gdy trzeba zarządzać wieloma środowiskami.

### Wdrażanie wielu środowisk

Możesz wdrażać wiele środowisk z tego samego kodu źródłowego przy użyciu pliku `parameter.ts` i opcji `-c envName`.

#### Wymagania wstępne

1. Zdefiniuj swoje środowiska w `parameter.ts` jak pokazano powyżej
2. Każde środowisko będzie miało własny zestaw zasobów z prefiksami specyficznymi dla środowiska

#### Polecenia wdrożenia

Aby wdrożyć konkretne środowisko:

```bash
# Wdróż środowisko deweloperskie
npx cdk deploy --all -c envName=dev

# Wdróż środowisko produkcyjne
npx cdk deploy --all -c envName=prod
```

Jeśli nie określono środowiska, używane jest środowisko "default":

```bash
# Wdróż środowisko domyślne
npx cdk deploy --all
```

#### Ważne uwagi

1. **Nazewnictwo stosów**:

   - Główne stosy dla każdego środowiska będą miały prefiks nazwy środowiska (np. `dev-BedrockChatStack`, `prod-BedrockChatStack`)
   - Jednak stosy niestandardowych botów (`BrChatKbStack*`) i stosy publikacji API (`ApiPublishmentStack*`) nie otrzymują prefiksów środowiska, ponieważ są tworzone dynamicznie w czasie wykonania

2. **Nazewnictwo zasobów**:

   - Tylko niektóre zasoby otrzymują prefiksy środowiska w nazwach (np. tabela `dev_ddb_export`, `dev-FrontendWebAcl`)
   - Większość zasobów zachowuje oryginalne nazwy, ale jest izolowana poprzez umieszczenie ich w różnych stosach

3. **Identyfikacja środowiska**:

   - Wszystkie zasoby są oznaczone tagiem `CDKEnvironment` zawierającym nazwę środowiska
   - Możesz użyć tego tagu do identyfikacji, do jakiego środowiska należy zasób
   - Przykład: `CDKEnvironment: dev` lub `CDKEnvironment: prod`

4. **Zastępowanie środowiska domyślnego**: Jeśli zdefiniujesz środowisko "default" w `parameter.ts`, zastąpi ono ustawienia w `cdk.json`. Aby kontynuować korzystanie z `cdk.json`, nie definiuj środowiska "default" w `parameter.ts`.

5. **Wymagania środowiska**: Aby utworzyć środowiska inne niż "default", musisz użyć `parameter.ts`. Sama opcja `-c envName` nie jest wystarczająca bez odpowiednich definicji środowisk.

6. **Izolacja zasobów**: Każde środowisko tworzy własny zestaw zasobów, umożliwiając posiadanie środowisk deweloperskich, testowych i produkcyjnych w tym samym koncie AWS bez konfliktów.

## Inne

### Konfiguracja domyślnej generacji tekstu

Użytkownicy mogą dostosować [parametry generacji tekstu](https://docs.anthropic.com/claude/reference/complete_post) z ekranu tworzenia niestandardowego bota. Jeśli bot nie jest używany, zostaną użyte domyślne parametry ustawione w [config.py](./backend/app/config.py).

```py
DEFAULT_GENERATION_CONFIG = {
    "max_tokens": 2000,
    "top_k": 250,
    "top_p": 0.999,
    "temperature": 0.6,
    "stop_sequences": ["Human: ", "Assistant: "],
}
```

### Usuwanie zasobów

Jeśli używasz CLI i CDK, użyj `npx cdk destroy`. Jeśli nie, przejdź do [CloudFormation](https://console.aws.amazon.com/cloudformation/home) i ręcznie usuń `BedrockChatStack` oraz `FrontendWafStack`. Pamiętaj, że `FrontendWafStack` znajduje się w regionie us-east-1.

### Ustawienia języka

Ten zasób automatycznie wykrywa język za pomocą [i18next-browser-languageDetector](https://github.com/i18next/i18next-browser-languageDetector). Możesz przełączać języki z menu aplikacji. Alternatywnie możesz użyć ciągu zapytania, aby ustawić język, jak pokazano poniżej.

> `https://example.com?lng=ja`

### Wyłączenie samodzielnej rejestracji

Ten przykład domyślnie ma włączoną samodzielną rejestrację. Aby ją wyłączyć, otwórz [cdk.json](./cdk/cdk.json) i zmień `selfSignUpEnabled` na `false`. Jeśli skonfigurujesz [zewnętrznego dostawcę tożsamości](#external-identity-provider), wartość zostanie zignorowana i automatycznie wyłączona.

### Ograniczenie domen dla adresów e-mail rejestracji

Domyślnie ten przykład nie ogranicza domen dla adresów e-mail rejestracji. Aby zezwolić na rejestrację tylko z określonych domen, otwórz `cdk.json` i określ domeny jako listę w `allowedSignUpEmailDomains`.

```ts
"allowedSignUpEmailDomains": ["example.com"],
```

### Zewnętrzny dostawca tożsamości

Ten przykład obsługuje zewnętrznego dostawcę tożsamości. Obecnie wspieramy [Google](./idp/SET_UP_GOOGLE_pl-PL.md) i [niestandardowego dostawcę OIDC](./idp/SET_UP_CUSTOM_OIDC_pl-PL.md).

### Automatyczne dodawanie nowych użytkowników do grup

Ten przykład posiada następujące grupy do nadawania uprawnień użytkownikom:

- [`Admin`](./ADMINISTRATOR_pl-PL.md)
- [`CreatingBotAllowed`](#bot-personalization)
- [`PublishAllowed`](./PUBLISH_API_pl-PL.md)

Jeśli chcesz, aby nowo utworzeni użytkownicy automatycznie dołączali do grup, możesz je określić w [cdk.json](./cdk/cdk.json).

```json
"autoJoinUserGroups": ["CreatingBotAllowed"],
```

Domyślnie nowo utworzeni użytkownicy zostaną dołączeni do grupy `CreatingBotAllowed`.

### Konfiguracja replik RAG

`enableRagReplicas` to opcja w [cdk.json](./cdk/cdk.json), która kontroluje ustawienia replik dla bazy danych RAG, w szczególności Bazy Wiedzy korzystające z Amazon OpenSearch Serverless.

- **Domyślnie**: true
- **true**: Zwiększa dostępność przez włączenie dodatkowych replik, odpowiednie dla środowisk produkcyjnych, ale zwiększa koszty.
- **false**: Zmniejsza koszty przez użycie mniejszej liczby replik, odpowiednie dla rozwoju i testowania.

Jest to ustawienie na poziomie konta/regionu, wpływające na całą aplikację, a nie na poszczególne boty.

> [!Uwaga]
> Według stanu na czerwiec 2024, Amazon OpenSearch Serverless obsługuje 0,5 OCU, obniżając koszty wejścia dla małych obciążeń. Wdrożenia produkcyjne mogą zaczynać się od 2 OCU, podczas gdy obciążenia dev/test mogą używać 1 OCU. OpenSearch Serverless automatycznie skaluje się w zależności od zapotrzebowania. Więcej szczegółów znajdziesz w [komunikacie](https://aws.amazon.com/jp/about-aws/whats-new/2024/06/amazon-opensearch-serverless-entry-cost-half-collection-types/).

### Wnioskowanie międzyregionowe

[Wnioskowanie międzyregionowe](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html) pozwala Amazon Bedrock na dynamiczne kierowanie żądań wnioskowania modelu między wieloma regionami AWS, zwiększając przepustowość i odporność podczas szczytowych okresów popytu. Aby skonfigurować, edytuj `cdk.json`.

```json
"enableBedrockCrossRegionInference": true
```

### Lambda SnapStart

[Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html) poprawia czasy zimnego startu dla funkcji Lambda, zapewniając szybsze czasy odpowiedzi dla lepszego doświadczenia użytkownika. Z drugiej strony, dla funkcji Python istnieje [opłata zależna od rozmiaru pamięci podręcznej](https://aws.amazon.com/lambda/pricing/#SnapStart_Pricing) i [nie jest dostępna we wszystkich regionach](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions) obecnie. Aby wyłączyć SnapStart, edytuj `cdk.json`.

```json
"enableLambdaSnapStart": false
```

### Konfiguracja domeny niestandardowej

Możesz skonfigurować domenę niestandardową dla dystrybucji CloudFront, ustawiając następujące parametry w [cdk.json](./cdk/cdk.json):

```json
{
  "alternateDomainName": "chat.example.com",
  "hostedZoneId": "Z0123456789ABCDEF"
}
```

- `alternateDomainName`: Niestandardowa nazwa domeny dla Twojej aplikacji czatu (np. chat.example.com)
- `hostedZoneId`: Identyfikator strefy hostowanej Route 53, w której zostaną utworzone rekordy DNS

Gdy te parametry są podane, wdrożenie automatycznie:

- Utworzy certyfikat ACM z walidacją DNS w regionie us-east-1
- Utworzy niezbędne rekordy DNS w Twojej strefie Route 53
- Skonfiguruje CloudFront do używania Twojej domeny niestandardowej

> [!Uwaga]
> Domena musi być zarządzana przez Route 53 w Twoim koncie AWS. Identyfikator strefy hostowanej można znaleźć w konsoli Route 53.

### Rozwój lokalny

Sprawdź [ROZWÓJ LOKALNY](./LOCAL_DEVELOPMENT_pl-PL.md).

### Wkład

Dziękujemy za rozważenie przyczynienia się do tego repozytorium! Witamy poprawki błędów, tłumaczenia języków (i18n), ulepszenia funkcji, [narzędzia agenta](./docs/AGENT.md#how-to-develop-your-own-tools) i inne usprawnienia.

W przypadku ulepszeń funkcji i innych ulepszeń, **przed utworzeniem Pull Request, bardzo docenilibyśmy utworzenie Issue z prośbą o funkcję, aby omówić podejście i szczegóły implementacji. W przypadku poprawek błędów i tłumaczeń języków (i18n) można od razu utworzyć Pull Request.**

Przed przyczynieniem się zapoznaj się również z poniższymi wytycznymi:

- [Rozwój lokalny](./LOCAL_DEVELOPMENT_pl-PL.md)
- [WKŁAD](./CONTRIBUTING_pl-PL.md)

## Kontakty

- [Takehiro Suzuki](https://github.com/statefb)
- [Yusuke Wada](https://github.com/wadabee)
- [Yukinobu Mine](https://github.com/Yukinobu-Mine)

## 🏆 Znaczący Współtwórcy

- [k70suK3-k06a7ash1](https://github.com/k70suK3-k06a7ash1)
- [fsatsuki](https://github.com/fsatsuki)

## Współtwórcy

[![bedrock claude chat współtwórcy](https://contrib.rocks/image?repo=aws-samples/bedrock-claude-chat&max=1000)](https://github.com/aws-samples/bedrock-claude-chat/graphs/contributors)

## Licencja

Ta biblioteka jest licencjonowana na warunkach licencji MIT-0. Zapoznaj się z [plikiem LICENSE](./LICENSE).