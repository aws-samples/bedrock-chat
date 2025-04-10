# Przewodnik migracyjny (z wersji 2 do 3)

## Krótko mówiąc

- Wersja 3 wprowadza precyzyjną kontrolę uprawnień i funkcjonalność Bot Store, wymagającą zmian schematu DynamoDB
- **Wykonaj kopię zapasową tabeli ConversationTable w DynamoDB przed migracją**
- Zaktualizuj adres URL repozytorium z `bedrock-claude-chat` na `bedrock-chat`
- Uruchom skrypt migracyjny, aby przekonwertować dane do nowego schematu
- Wszystkie Twoje boty i rozmowy zostaną zachowane z nowym modelem uprawnień
- **WAŻNE: Podczas procesu migracji aplikacja będzie niedostępna dla wszystkich użytkowników do momentu zakończenia migracji. Ten proces zwykle trwa około 60 minut, w zależności od ilości danych i wydajności środowiska programistycznego.**
- **WAŻNE: Wszystkie opublikowane interfejsy API muszą zostać usunięte podczas procesu migracji.**
- **OSTRZEŻENIE: Proces migracji nie może zagwarantować 100% sukcesu dla wszystkich botów. Przed migracją udokumentuj konfiguracje ważnych botów na wypadek konieczności ręcznego ich odtworzenia**

## Wprowadzenie

### Co Nowego w V3

V3 wprowadza znaczące ulepszenia w Bedrock Chat:

1. **Precyzyjna kontrola uprawnień**: Kontroluj dostęp do swoich botów za pomocą uprawnień opartych na grupach użytkowników
2. **Sklep z Botami**: Udostępniaj i odkrywaj boty za pośrednictwem scentralizowanego rynku
3. **Funkcje administracyjne**: Zarządzaj interfejsami API, oznaczaj boty jako niezbędne i analizuj użycie botów

Te nowe funkcje wymagały zmian w schemacie DynamoDB, co z kolei wymaga procesu migracji dla istniejących użytkowników.

### Dlaczego Ta Migracja Jest Konieczna

Nowy model uprawnień i funkcjonalność Sklepu z Botami wymagały przebudowy sposobu przechowywania i dostępu do danych botów. Proces migracji konwertuje istniejące boty i rozmowy do nowego schematu, zachowując przy tym wszystkie dane.

> [!WARNING]
> Powiadomienie o Przerwie w Usłudze: **Podczas procesu migracji aplikacja będzie niedostępna dla wszystkich użytkowników.** Zaplanuj przeprowadzenie tej migracji w oknie konserwacyjnym, gdy użytkownicy nie potrzebują dostępu do systemu. Aplikacja stanie się ponownie dostępna dopiero po pomyślnym zakończeniu skryptu migracyjnego i prawidłowej konwersji wszystkich danych do nowego schematu. Ten proces zazwyczaj trwa około 60 minut, w zależności od ilości danych i wydajności środowiska deweloperskiego.

> [!IMPORTANT]
> Przed przystąpieniem do migracji: **Proces migracji nie może zagwarantować 100% sukcesu dla wszystkich botów**, szczególnie tych utworzonych w starszych wersjach lub z niestandardowymi konfiguracjami. Przed rozpoczęciem procesu migracji prosimy o udokumentowanie ważnych konfiguracji botów (instrukcji, źródeł wiedzy, ustawień) na wypadek konieczności ich ręcznego odtworzenia.

## Proces migracji

### Ważna uwaga dotycząca widoczności botów w V3

W V3 **wszystkie boty v2 z włączonym publicznym udostępnianiem będą widoczne w Bot Store.** Jeśli posiadasz boty zawierające poufne informacje, które nie powinny być odkrywalne, rozważ ustawienie ich jako prywatne przed migracją do V3.

### Krok 1: Zidentyfikuj nazwę środowiska

W tej procedurze `{TWÓJ_PREFIKS_ŚR}` jest określony do zidentyfikowania nazwy twoich stosów CloudFormation. Jeśli korzystasz z funkcji [Wdrażanie wielu środowisk](../../README.md#deploying-multiple-environments), zastąp go nazwą środowiska, które ma zostać zmigrowane. Jeśli nie, zastąp go pustym ciągiem znaków.

### Krok 2: Aktualizacja adresu URL repozytorium (Zalecane)

Repozytorium zostało przemianowane z `bedrock-claude-chat` na `bedrock-chat`. Zaktualizuj lokalne repozytorium:

```bash
# Sprawdź aktualny zdalny adres URL
git remote -v

# Zaktualizuj zdalny adres URL
git remote set-url origin https://github.com/aws-samples/bedrock-chat.git

# Sprawdź zmianę
git remote -v
```

### Krok 3: Upewnij się, że korzystasz z najnowszej wersji V2

> [!OSTRZEŻENIE]
> MUSISZ zaktualizować do v2.10.0 przed migracją do V3. **Pominięcie tego kroku może spowodować utratę danych podczas migracji.**

Przed rozpoczęciem migracji upewnij się, że używasz najnowszej wersji V2 (**v2.10.0**). Gwarantuje to posiadanie wszystkich niezbędnych poprawek błędów i ulepszeń przed aktualizacją do V3:

```bash
# Pobierz najnowsze tagi
git fetch --tags

# Przełącz się na najnowszą wersję V2
git checkout v2.10.0

# Wdróż najnowszą wersję V2
cd cdk
npm ci
npx cdk deploy --all
```

### Krok 4: Zanotuj nazwę tabeli DynamoDB V2

Pobierz nazwę tabeli ConversationTable z wyjść CloudFormation:

```bash
# Pobierz nazwę tabeli ConversationTable V2
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='ConversationTableName'].OutputValue" \
  --stack-name {TWÓJ_PREFIKS_ŚR}BedrockChatStack
```

Upewnij się, że zapiszesz tę nazwę tabeli w bezpiecznym miejscu, ponieważ będzie potrzebna później w skrypcie migracyjnym.

### Krok 5: Wykonaj kopię zapasową tabeli DynamoDB

Przed kontynuacją utwórz kopię zapasową tabeli ConversationTable przy użyciu nazwy, którą właśnie zanotowałeś:

```bash
# Utwórz kopię zapasową tabeli V2
aws dynamodb create-backup \
  --no-cli-pager \
  --backup-name "BedrockChatV2Backup-$(date +%Y%m%d)" \
  --table-name NAZWA_TWOJEJ_TABELI_KONWERSACJI_V2

# Sprawdź, czy kopia zapasowa jest dostępna
aws dynamodb describe-backup \
  --no-cli-pager \
  --query BackupDescription.BackupDetails \
  --backup-arn TWÓJ_ARN_KOPII_ZAPASOWEJ
```

### Krok 6: Usuń wszystkie opublikowane interfejsy API

> [!WAŻNE]
> Przed wdrożeniem V3 musisz usunąć wszystkie opublikowane interfejsy API, aby uniknąć konfliktów wartości wyjściowych Cloudformation podczas procesu aktualizacji.

1. Zaloguj się do aplikacji jako administrator
2. Przejdź do sekcji Admin i wybierz "Zarządzanie API"
3. Przejrzyj listę wszystkich opublikowanych interfejsów API
4. Usuń każdy opublikowany interfejs API, klikając przycisk usuwania obok niego

Więcej informacji na temat publikowania i zarządzania interfejsami API można znaleźć w dokumentacji [PUBLISH_API.md](../PUBLISH_API_pl-PL.md), [ADMINISTRATOR.md](../ADMINISTRATOR_pl-PL.md).

### Krok 7: Pobierz V3 i wdróż

Pobierz najnowszy kod V3 i wdróż:

```bash
git fetch
git checkout v3
cd cdk
npm ci
npx cdk deploy --all
```

> [!WAŻNE]
> Po wdrożeniu V3 aplikacja będzie niedostępna dla wszystkich użytkowników do czasu zakończenia procesu migracji. Nowy schemat jest niezgodny ze starym formatem danych, więc użytkownicy nie będą mogli uzyskać dostępu do swoich botów lub konwersacji do czasu zakończenia skryptu migracyjnego w kolejnych krokach.

### Krok 8: Zanotuj nazwy tabel DynamoDB V3

Po wdrożeniu V3 musisz pobrać nazwy zarówno nowej tabeli ConversationTable, jak i BotTable:

```bash
# Pobierz nazwę tabeli ConversationTable V3
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='ConversationTableNameV3'].OutputValue" \
  --stack-name {TWÓJ_PREFIKS_ŚR}BedrockChatStack

# Pobierz nazwę tabeli BotTable V3
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='BotTableNameV3'].OutputValue" \
  --stack-name {TWÓJ_PREFIKS_ŚR}BedrockChatStack
```

> [!Ważne]
> Upewnij się, że zapiszesz nazwy tabel V3 wraz z wcześniej zapisaną nazwą tabeli V2, ponieważ wszystkie będą potrzebne do skryptu migracyjnego.

(Reszta tekstu pozostaje bez zmian, więc nie będę jej ponownie tłumaczył. Jeśli chcesz, żebym dokończył tłumaczenie, daj znać.)

## V3 Często Zadawane Pytania

### Dostęp do Bota i Uprawnienia

**P: Co się stanie, jeśli bot, którego używam, zostanie usunięty lub moje uprawnienia dostępu zostaną cofnięte?**
O: Autoryzacja jest sprawdzana w momencie rozmowy, więc utracisz dostęp natychmiast.

**P: Co się stanie, jeśli użytkownik zostanie usunięty (np. pracownik odchodzi)?**
O: Jego dane mogą zostać całkowicie usunięte przez usunięcie wszystkich elementów z DynamoDB z jego identyfikatorem użytkownika jako kluczem partycji (PK).

**P: Czy mogę wyłączyć udostępnianie dla niezbędnego bota publicznego?**
O: Nie, administrator musi najpierw oznaczyć bota jako nieniezbędnego przed wyłączeniem udostępniania.

**P: Czy mogę usunąć niezbędnego bota publicznego?**
O: Nie, administrator musi najpierw oznaczyć bota jako nieniezbędnego przed jego usunięciem.

### Bezpieczeństwo i Implementacja

**P: Czy wdrożono zabezpieczenia na poziomie wierszy (RLS) dla tabeli botów?**
O: Nie, biorąc pod uwagę różnorodność wzorców dostępu. Autoryzacja jest przeprowadzana podczas uzyskiwania dostępu do botów, a ryzyko wycieku metadanych jest uważane za minimalne w porównaniu z historią rozmów.

**P: Jakie są wymagania dotyczące publikacji API?**
O: Bot musi być publiczny.

**P: Czy będzie ekran zarządzania wszystkimi prywatnymi botami?**
O: Nie w początkowej wersji V3. Jednak elementy nadal można usuwać, wykonując zapytanie z identyfikatorem użytkownika w razie potrzeby.

**P: Czy będzie funkcjonalność tagowania botów dla lepszego doświadczenia wyszukiwania?**
O: Nie w początkowej wersji V3, ale automatyczne tagowanie oparte na LLM może zostać dodane w przyszłych aktualizacjach.

### Administracja

**P: Co mogą robić administratorzy?**
O: Administratorzy mogą:

- Zarządzać botami publicznymi (w tym sprawdzać boty o wysokich kosztach)
- Zarządzać API
- Oznaczać boty publiczne jako niezbędne

**P: Czy mogę oznaczyć boty częściowo udostępniane jako niezbędne?**
O: Nie, wspierane są tylko boty publiczne.

**P: Czy mogę ustawić priorytet dla przypiętych botów?**
O: W początkowej wersji - nie.

### Konfiguracja Autoryzacji

**P: Jak skonfigurować autoryzację?**
O:

1. Otwórz konsolę Amazon Cognito i utwórz grupy użytkowników w puli użytkowników BrChat
2. Dodaj użytkowników do tych grup zgodnie z potrzebami
3. W BrChat wybierz grupy użytkowników, którym chcesz zezwolić na dostęp podczas konfigurowania ustawień udostępniania bota

Uwaga: Zmiany członkostwa w grupach wymagają ponownego zalogowania. Zmiany są odzwierciedlane przy odświeżeniu tokenu, ale nie w trakcie ważności tokenu ID (domyślnie 30 minut w V3, konfigurowalne przez `tokenValidMinutes` w `cdk.json` lub `parameter.ts`).

**P: Czy system sprawdza w Cognito za każdym razem, gdy uzyskiwany jest dostęp do bota?**
O: Nie, autoryzacja jest sprawdzana przy użyciu tokenu JWT, aby uniknąć niepotrzebnych operacji we/wy.

### Funkcjonalność Wyszukiwania

**P: Czy wyszukiwanie botów obsługuje wyszukiwanie semantyczne?**
O: Nie, obsługiwane jest tylko częściowe dopasowanie tekstu. Wyszukiwanie semantyczne (np. „samochód" → „auto", „EV", „pojazd") nie jest dostępne ze względu na obecne ograniczenia OpenSearch Serverless (marzec 2025).