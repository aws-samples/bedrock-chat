# Funkcje administracyjne

## Wymagania wstępne

Administrator musi być członkiem grupy o nazwie `Admin`, którą można skonfigurować za pośrednictwem konsoli zarządzania > Pule użytkowników Amazon Cognito lub interfejsu wiersza poleceń AWS. Należy pamiętać, że identyfikator puli użytkowników można znaleźć, uzyskując dostęp do CloudFormation > BedrockChatStack > Dane wyjściowe > `AuthUserPoolIdxxxx`.

![](./imgs/group_membership_admin.png)

## Oznacz publiczne boty jako Niezbędne

Administratorzy mogą teraz oznaczyć publiczne boty jako „Niezbędne". Boty oznaczone jako Niezbędne będą wyróżniane w sekcji „Niezbędne" sklepu z botami, dzięki czemu będą łatwo dostępne dla użytkowników. Pozwala to administratorom przypinać ważne boty, które chcą, aby wszyscy użytkownicy używali.

### Przykłady

- Bot Asystent HR: Pomaga pracownikom w pytaniach i zadaniach związanych z zasobami ludzkimi.
- Bot Wsparcia IT: Zapewnia pomoc w zakresie wewnętrznych problemów technicznych i zarządzania kontami.
- Bot Przewodnik po Wewnętrznych Regulacjach: Odpowiada na często zadawane pytania dotyczące zasad obecności, polityki bezpieczeństwa i innych przepisów wewnętrznych.
- Bot Wprowadzenie Nowych Pracowników: Prowadzi nowych pracowników przez procedury i użycie systemów w pierwszym dniu pracy.
- Bot Informacji o Świadczeniach: Wyjaśnia programy świadczeń pracowniczych i usługi socjalne firmy.

![](./imgs/admin_bot_menue.png)
![](./imgs/bot_store.png)

## Pętla informacji zwrotnej

Dane wyjściowe z LLM nie zawsze mogą spełniać oczekiwania użytkownika. Czasami nie udaje się zaspokoić jego potrzeb. Aby skutecznie "zintegrować" LLM z operacjami biznesowymi i codziennym życiem, kluczowe jest wdrożenie pętli informacji zwrotnej. Bedrock Chat jest wyposażony w funkcję opinii zaprojektowaną tak, aby umożliwić użytkownikom analizę przyczyn niezadowolenia. Na podstawie wyników analizy użytkownicy mogą odpowiednio dostosować monity, źródła danych RAG oraz parametry.

![](./imgs/feedback_loop.png)

![](./imgs/feedback-using-claude-chat.png)

Analitycy danych mogą uzyskać dostęp do dzienników rozmów za pomocą [Amazon Athena](https://aws.amazon.com/jp/athena/). Jeśli chcą przeanalizować dane w [Jupyter Notebook](https://jupyter.org/), [ten przykładowy notes](../examples/notebooks/feedback_analysis_example.ipynb) może służyć jako odniesienie.

## Panel główny

Aktualnie zapewnia podstawowy przegląd użycia chatbota i użytkowników, koncentrując się na agregowaniu danych dla każdego bota i użytkownika w określonych przedziałach czasowych oraz sortowaniu wyników według opłat za użycie.

![](./imgs/admin_bot_analytics.png)

## Uwagi

- Jak wspomniano w [architekturze](../README.md#architecture), funkcje administracyjne będą odwoływać się do bucketu S3 wyeksportowanego z DynamoDB. Należy pamiętać, że ponieważ eksport jest wykonywany co godzinę, najnowsze rozmowy mogą nie być odzwierciedlone natychmiast.

- W publicznym użyciu botów, boty, które w ogóle nie były używane w określonym okresie, nie zostaną wymienione.

- W użyciach użytkowników, użytkownicy, którzy w ogóle nie używali systemu w określonym okresie, nie zostaną wymienieni.

> [!Ważne]
> Jeśli używasz wielu środowisk (dev, prod itp.), nazwa bazy danych Athena będzie zawierać prefiks środowiska. Zamiast `bedrockchatstack_usage_analysis`, nazwa bazy danych będzie:
>
> - Dla środowiska domyślnego: `bedrockchatstack_usage_analysis`
> - Dla nazwanych środowisk: `<prefiks-środowiska>_bedrockchatstack_usage_analysis` (np. `dev_bedrockchatstack_usage_analysis`)
>
> Dodatkowo nazwa tabeli będzie zawierać prefiks środowiska:
>
> - Dla środowiska domyślnego: `ddb_export`
> - Dla nazwanych środowisk: `<prefiks-środowiska>_ddb_export` (np. `dev_ddb_export`)
>
> Upewnij się, że odpowiednio dostosujesz zapytania podczas pracy z wieloma środowiskami.

## Pobieranie danych z rozmów

Możesz przeszukiwać dzienniki rozmów za pomocą Atheny, używając SQL. Aby pobrać dzienniki, otwórz Edytor zapytań Atheny z konsoli zarządzania i uruchom zapytanie SQL. Poniżej znajdują się przykładowe zapytania przydatne do analizy przypadków użycia. Opinię można znaleźć w atrybucie `MessageMap`.

### Zapytanie według identyfikatora bota

Edytuj `bot-id` i `datehour`. `bot-id` można znaleźć na ekranie zarządzania botami, do którego można uzyskać dostęp z poziomu interfejsów API publikowania botów, wyświetlanych na lewym pasku bocznym. Zwróć uwagę na końcową część adresu URL, np. `https://xxxx.cloudfront.net/admin/bot/<bot-id>`.

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
> Analityka użycia użytkowników będzie dostępna wkrótce.

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