# Funkcje administratora

Funkcje administratora są narzędziem o kluczowym znaczeniu, ponieważ dostarczają niezbędnych informacji na temat użycia niestandardowych botów i zachowań użytkowników. Bez tych funkcjonalności byłoby niezwykle trudno administratorom zrozumieć, które niestandardowe boty cieszą się popularnością, dlaczego są popularne i kto je wykorzystuje. Te informacje są kluczowe dla optymalizacji podpowiedzi instrukcyjnych, dostosowywania źródeł danych RAG oraz identyfikacji intensywnych użytkowników, którzy mogą stać się influencerami.

## Pętla informacji zwrotnej

Dane wyjściowe z LLM nie zawsze spełniają oczekiwania użytkownika. Czasami nie zaspokaja on potrzeb użytkownika. Aby skutecznie "zintegrować" LLM z operacjami biznesowymi i codziennym życiem, wdrożenie pętli informacji zwrotnej jest niezbędne. Bedrock Claude Chat jest wyposażony w funkcję opinii zaprojektowaną tak, aby umożliwić użytkownikom analizę przyczyn niezadowolenia. Na podstawie wyników analizy użytkownicy mogą odpowiednio dostosować monity, źródła danych RAG i parametry.

![](./imgs/feedback_loop.png)

![](./imgs/feedback-using-claude-chat.png)

Analitycy danych mogą uzyskać dostęp do dzienników rozmów za pomocą [Amazon Athena](https://aws.amazon.com/jp/athena/). Jeśli chcą przeanalizować dane w [Jupyter Notebook](https://jupyter.org/), [ten przykładowy notes](../examples/notebooks/feedback_analysis_example.ipynb) może służyć jako odniesienie.

## Panel administratora

Obecnie zapewnia podstawowy przegląd użycia chatbota i użytkowników, koncentrując się na agregowaniu danych dla każdego bota i użytkownika w określonych przedziałach czasowych oraz sortowaniu wyników według opłat za użycie.

![](./imgs/admin_bot_analytics.png)

> [!Note]
> Analityka użycia użytkowników już wkrótce.

### Wymagania wstępne

Administrator musi być członkiem grupy o nazwie `Admin`, którą można skonfigurować za pośrednictwem konsoli zarządzania > Pule użytkowników Amazon Cognito lub interfejsu wiersza poleceń AWS. Należy pamiętać, że identyfikator puli użytkowników można znaleźć, uzyskując dostęp do CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`.

![](./imgs/group_membership_admin.png)

## Uwagi

- Zgodnie z opisem w [architekturze](../README.md#architecture), funkcje administracyjne będą odwoływać się do bucketu S3 wyeksportowanego z DynamoDB. Należy pamiętać, że ponieważ eksport jest wykonywany co godzinę, najnowsze rozmowy mogą nie być odzwierciedlone natychmiast.

- W publicznych użyciach botów, boty, które w ogóle nie były używane w określonym okresie, nie będą wyświetlane.

- W użyciach użytkowników, użytkownicy, którzy w ogóle nie korzystali z systemu w określonym okresie, nie będą wyświetlani.

> [!Ważne] > **Nazwy Baz Danych dla Wielu Środowisk**
>
> Jeśli używasz wielu środowisk (dev, prod itp.), nazwa bazy danych Athena będzie zawierać prefiks środowiska. Zamiast `bedrockchatstack_usage_analysis`, nazwa bazy danych będzie następująca:
>
> - Dla środowiska domyślnego: `bedrockchatstack_usage_analysis`
> - Dla nazwanych środowisk: `<prefiks-środowiska>_bedrockchatstack_usage_analysis` (np. `dev_bedrockchatstack_usage_analysis`)
>
> Dodatkowo nazwa tabeli będzie zawierać prefiks środowiska:
>
> - Dla środowiska domyślnego: `ddb_export`
> - Dla nazwanych środowisk: `<prefiks-środowiska>_ddb_export` (np. `dev_ddb_export`)
>
> Upewnij się, że odpowiednio dostosowujesz zapytania podczas pracy z wieloma środowiskami.

## Pobieranie danych rozmowy

Możesz przeszukiwać dzienniki rozmów za pomocą Atheny, używając SQL. Aby pobrać dzienniki, otwórz Edytor zapytań Atheny z konsoli zarządzania i uruchom zapytanie SQL. Poniżej znajdują się przykładowe zapytania przydatne do analizy przypadków użycia. Informacje zwrotne można znaleźć w atrybucie `MessageMap`.

### Zapytanie według identyfikatora bota

Edytuj `bot-id` i `datehour`. `bot-id` można znaleźć na ekranie zarządzania botami, do którego można uzyskać dostęp z interfejsów API publikacji bota, wyświetlanych na lewym pasku bocznym. Zwróć uwagę na końcową część adresu URL, np. `https://xxxx.cloudfront.net/admin/bot/<bot-id>`.

```sql
SELECT
    d.newimage.PK.S AS UserId,
    d.newimage.SK.S AS ConversationId,
    d.newimage.MessageMap.S AS MessageMap,
    d.newimage.TotalPrice.N AS TotalPrice,
    d.newimage.CreateTime.N AS CreateTime,
    d.newimage.LastMessageId.S AS LastMessageId,
    d.newimage.BotId.S AS BotId,
    d.datehour AS DateHour
FROM
    bedrockchatstack_usage_analysis.ddb_export d
WHERE
    d.newimage.BotId.S = '<bot-id>'
    AND d.datehour BETWEEN '<yyyy/mm/dd/hh>' AND '<yyyy/mm/dd/hh>'
    AND d.Keys.SK.S LIKE CONCAT(d.Keys.PK.S, '#CONV#%')
ORDER BY
    d.datehour DESC;
```

> [!Uwaga]
> Jeśli używasz środowiska nazwanego (np. "dev"), zastąp `bedrockchatstack_usage_analysis.ddb_export` przez `dev_bedrockchatstack_usage_analysis.dev_ddb_export` w powyższym zapytaniu.

### Zapytanie według identyfikatora użytkownika

Edytuj `user-id` i `datehour`. `user-id` można znaleźć na ekranie zarządzania botami.

> [!Uwaga]
> Analityka użycia użytkownika już wkrótce.

```sql
SELECT
    d.newimage.PK.S AS UserId,
    d.newimage.SK.S AS ConversationId,
    d.newimage.MessageMap.S AS MessageMap,
    d.newimage.TotalPrice.N AS TotalPrice,
    d.newimage.CreateTime.N AS CreateTime,
    d.newimage.LastMessageId.S AS LastMessageId,
    d.newimage.BotId.S AS BotId,
    d.datehour AS DateHour
FROM
    bedrockchatstack_usage_analysis.ddb_export d
WHERE
    d.newimage.PK.S = '<user-id>'
    AND d.datehour BETWEEN '<yyyy/mm/dd/hh>' AND '<yyyy/mm/dd/hh>'
    AND d.Keys.SK.S LIKE CONCAT(d.Keys.PK.S, '#CONV#%')
ORDER BY
    d.datehour DESC;
```

> [!Uwaga]
> Jeśli używasz środowiska nazwanego (np. "dev"), zastąp `bedrockchatstack_usage_analysis.ddb_export` przez `dev_bedrockchatstack_usage_analysis.dev_ddb_export` w powyższym zapytaniu.