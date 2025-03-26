# Funkcje administratora

Funkcje administratora są niezwykle istotnym narzędziem, które zapewnia kluczowe informacje na temat użycia niestandardowych botów i zachowań użytkowników. Bez tej funkcjonalności byłoby bardzo trudno administratorom zrozumieć, które niestandardowe boty są popularne, dlaczego są popularne i kto ich używa. Te informacje są niezmiernie ważne dla optymalizacji instrukcji, dostosowywania źródeł danych RAG oraz identyfikacji intensywnych użytkowników, którzy mogą stać się influencerami.

## Pętla informacji zwrotnej

Dane wyjściowe z LLM nie zawsze mogą spełniać oczekiwania użytkownika. Czasami nie udaje się zaspokoić jego potrzeb. Aby skutecznie "zintegrować" LLM z operacjami biznesowymi i życiem codziennym, wdrożenie pętli informacji zwrotnej jest niezbędne. Bedrock Claude Chat jest wyposażony w funkcję opinii zaprojektowaną tak, aby umożliwić użytkownikom analizę przyczyn niezadowolenia. Na podstawie wyników analizy użytkownicy mogą odpowiednio dostosować polecenia, źródła danych RAG i parametry.

![](./imgs/feedback_loop.png)

![](./imgs/feedback-using-claude-chat.png)

Analitycy danych mogą uzyskać dostęp do dzienników rozmów za pomocą [Amazon Athena](https://aws.amazon.com/jp/athena/). Jeśli chcą przeanalizować dane w [Jupyter Notebook](https://jupyter.org/), [ten przykładowy notes](../examples/notebooks/feedback_analysis_example.ipynb) może służyć jako odniesienie.

## Panel administratora

Aktualnie zapewnia podstawowy przegląd użycia chatbota i użytkowników, koncentrując się na agregowaniu danych dla każdego bota i użytkownika w określonych przedziałach czasowych oraz sortowaniu wyników według opłat za użycie.

![](./imgs/admin_bot_analytics.png)

> [!Note]
> Analityka użycia użytkowników już wkrótce.

### Wymagania wstępne

Administrator musi być członkiem grupy o nazwie `Admin`, którą można skonfigurować za pośrednictwem konsoli zarządzania > Pule użytkowników Amazon Cognito lub interfejsu wiersza poleceń AWS. Należy pamiętać, że identyfikator puli użytkowników można znaleźć, uzyskując dostęp do CloudFormation > BedrockChatStack > Wyjścia > `AuthUserPoolIdxxxx`.

![](./imgs/group_membership_admin.png)

## Uwagi

- Zgodnie z opisem w [architekturze](../README.md#architecture), funkcje administracyjne będą odwoływać się do bucketu S3 wyeksportowanego z DynamoDB. Należy pamiętać, że ponieważ eksport jest wykonywany raz na godzinę, najnowsze rozmowy mogą nie być odzwierciedlone natychmiast.

- W publicznych użyciach botów, boty, które w ogóle nie były używane w określonym okresie, nie zostaną wymienione.

- W użyciach użytkowników, użytkownicy, którzy w ogóle nie korzystali z systemu w określonym okresie, nie zostaną wymienieni.

> [!Ważne] > **Nazwy baz danych w wielu środowiskach**
>
> Jeśli używasz wielu środowisk (dev, prod itp.), nazwa bazy danych Athena będzie zawierać prefiks środowiska. Zamiast `bedrockchatstack_usage_analysis`, nazwa bazy danych będzie następująca:
>
> - Dla domyślnego środowiska: `bedrockchatstack_usage_analysis`
> - Dla nazwanych środowisk: `<prefiks-środowiska>_bedrockchatstack_usage_analysis` (np. `dev_bedrockchatstack_usage_analysis`)
>
> Dodatkowo nazwa tabeli będzie zawierać prefiks środowiska:
>
> - Dla domyślnego środowiska: `ddb_export`
> - Dla nazwanych środowisk: `<prefiks-środowiska>_ddb_export` (np. `dev_ddb_export`)
>
> Upewnij się, że odpowiednio dostosowujesz zapytania podczas pracy z wieloma środowiskami.

## Pobieranie danych z konwersacji

Możesz odpytywać dzienniki konwersacji za pomocą Atheny, używając SQL. Aby pobrać dzienniki, otwórz Edytor zapytań Atheny z konsoli zarządzania i uruchom zapytanie SQL. Poniżej znajdują się przykładowe zapytania przydatne do analizowania przypadków użycia. Opinie można znaleźć w atrybucie `MessageMap`.

### Zapytanie według identyfikatora bota

Edytuj `bot-id` i `datehour`. `bot-id` można znaleźć na ekranie zarządzania botami, do którego można uzyskać dostęp z interfejsów API publikacji botów, wyświetlanych na lewym pasku bocznym. Zwróć uwagę na końcową część adresu URL, np. `https://xxxx.cloudfront.net/admin/bot/<bot-id>`.

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
> Jeśli używasz środowiska o nazwie (np. "dev"), zastąp `bedrockchatstack_usage_analysis.ddb_export` na `dev_bedrockchatstack_usage_analysis.dev_ddb_export` w powyższym zapytaniu.

### Zapytanie według identyfikatora użytkownika

Edytuj `user-id` i `datehour`. `user-id` można znaleźć na ekranie zarządzania botami.

> [!Uwaga]
> Analityka użycia użytkownika jest już wkrótce.

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
> Jeśli używasz środowiska o nazwie (np. "dev"), zastąp `bedrockchatstack_usage_analysis.ddb_export` na `dev_bedrockchatstack_usage_analysis.dev_ddb_export` w powyższym zapytaniu.