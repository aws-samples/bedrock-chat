# Funkcje administracyjne

## Wymagania wstępne

Użytkownik administracyjny musi być członkiem grupy o nazwie `Admin`, którą można skonfigurować poprzez konsolę zarządzania > Amazon Cognito User pools lub aws cli. Należy pamiętać, że identyfikator puli użytkowników można sprawdzić poprzez CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`.

![](./imgs/group_membership_admin.png)

## Oznaczanie botów publicznych jako Niezbędne

Administratorzy mogą teraz oznaczać boty publiczne jako "Niezbędne". Boty oznaczone jako Niezbędne będą wyświetlane w sekcji "Niezbędne" w sklepie z botami, co ułatwia użytkownikom dostęp do nich. Pozwala to administratorom przypiąć ważne boty, z których chcą, aby korzystali wszyscy użytkownicy.

### Przykłady

- Bot Asystent HR: Pomaga pracownikom w kwestiach i zadaniach związanych z HR.
- Bot Wsparcia IT: Zapewnia pomoc w wewnętrznych kwestiach technicznych i zarządzaniu kontami.
- Bot Przewodnika po Zasadach Wewnętrznych: Odpowiada na często zadawane pytania dotyczące zasad obecności, polityki bezpieczeństwa i innych regulacji wewnętrznych.
- Bot Wdrażający Nowych Pracowników: Przeprowadza nowych pracowników przez procedury i obsługę systemów w ich pierwszym dniu pracy.
- Bot Informacji o Świadczeniach: Wyjaśnia programy świadczeń pracowniczych i usługi socjalne.

![](./imgs/admin_bot_menue.png)
![](./imgs/bot_store.png)

## Pętla informacji zwrotnej

Wynik z LLM może nie zawsze spełniać oczekiwania użytkownika. Czasami nie zaspokaja potrzeb użytkownika. Aby skutecznie "zintegrować" LLM z działalnością biznesową i codziennym życiem, niezbędne jest wdrożenie pętli informacji zwrotnej. Bedrock Chat jest wyposażony w funkcję feedbacku zaprojektowaną tak, aby umożliwić użytkownikom analizę przyczyn niezadowolenia. Na podstawie wyników analizy użytkownicy mogą odpowiednio dostosować prompty, źródła danych RAG i parametry.

![](./imgs/feedback_loop.png)

![](./imgs/feedback-using-claude-chat.png)

Analitycy danych mogą uzyskać dostęp do logów konwersacji za pomocą [Amazon Athena](https://aws.amazon.com/jp/athena/). Jeśli chcą analizować dane przy użyciu [Jupyter Notebook](https://jupyter.org/), [ten przykładowy notebook](../examples/notebooks/feedback_analysis_example.ipynb) może służyć jako punkt odniesienia.

## Panel główny

Aktualnie zapewnia podstawowy przegląd wykorzystania chatbotów i użytkowników, koncentrując się na agregowaniu danych dla każdego bota i użytkownika w określonych przedziałach czasowych oraz sortowaniu wyników według opłat za użytkowanie.

![](./imgs/admin_bot_analytics.png)

## Uwagi

- Jak określono w [architekturze](../README.md#architecture), funkcje administracyjne będą odwoływać się do bucketu S3 wyeksportowanego z DynamoDB. Należy pamiętać, że ponieważ eksport jest wykonywany raz na godzinę, najnowsze rozmowy mogą nie być widoczne natychmiast.

- W przypadku publicznego wykorzystania botów, boty które nie były w ogóle używane w określonym okresie nie będą wyświetlane na liście.

- W przypadku wykorzystania przez użytkowników, użytkownicy którzy w ogóle nie korzystali z systemu w określonym okresie nie będą wyświetlani na liście.

> [!Important]
> Jeśli korzystasz z wielu środowisk (dev, prod, itp.), nazwa bazy danych Athena będzie zawierać prefiks środowiska. Zamiast `bedrockchatstack_usage_analysis`, nazwa bazy danych będzie:
>
> - Dla domyślnego środowiska: `bedrockchatstack_usage_analysis`
> - Dla nazwanych środowisk: `<env-prefix>_bedrockchatstack_usage_analysis` (np. `dev_bedrockchatstack_usage_analysis`)
>
> Dodatkowo, nazwa tabeli będzie zawierać prefiks środowiska:
>
> - Dla domyślnego środowiska: `ddb_export`
> - Dla nazwanych środowisk: `<env-prefix>_ddb_export` (np. `dev_ddb_export`)
>
> Upewnij się, że odpowiednio dostosujesz swoje zapytania podczas pracy z wieloma środowiskami.

## Pobieranie danych konwersacji

Możesz przeszukiwać logi konwersacji za pomocą Atheny, używając SQL. Aby pobrać logi, otwórz Edytor Zapytań Athena z konsoli zarządzania i uruchom zapytanie SQL. Poniżej znajdują się przykładowe zapytania przydatne do analizy przypadków użycia. Informacje zwrotne można znaleźć w atrybucie `MessageMap`.

### Zapytanie według ID bota

Edytuj `bot-id` i `datehour`. `bot-id` można znaleźć na ekranie Bot Management, do którego można uzyskać dostęp z Bot Publish APIs, wyświetlanych na lewym pasku bocznym. Zwróć uwagę na końcową część adresu URL, np. `https://xxxx.cloudfront.net/admin/bot/<bot-id>`.

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

> [!Note]
> Jeśli używasz nazwanego środowiska (np. "dev"), zamień `bedrockchatstack_usage_analysis.ddb_export` na `dev_bedrockchatstack_usage_analysis.dev_ddb_export` w powyższym zapytaniu.

### Zapytanie według ID użytkownika

Edytuj `user-id` i `datehour`. `user-id` można znaleźć na ekranie Bot Management.

> [!Note]
> Analityka użytkowania użytkowników będzie dostępna wkrótce.

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

> [!Note]
> Jeśli używasz nazwanego środowiska (np. "dev"), zamień `bedrockchatstack_usage_analysis.ddb_export` na `dev_bedrockchatstack_usage_analysis.dev_ddb_export` w powyższym zapytaniu.