# Przewodnik migracyjny (z wersji 2 do 3)

## Krótko mówiąc

- V3 wprowadza kontrolę uprawnień na poziomie szczegółowym oraz funkcjonalność Bot Store, wymagając zmian schematu DynamoDB
- **Wykonaj kopię zapasową tabeli ConversationTable w DynamoDB przed migracją**
- Zaktualizuj adres URL repozytorium z `bedrock-claude-chat` na `bedrock-chat`
- Uruchom skrypt migracyjny, aby przekonwertować dane do nowego schematu
- Wszystkie Twoje boty i rozmowy zostaną zachowane z nowym modelem uprawnień
- **WAŻNE: Podczas procesu migracji aplikacja będzie niedostępna dla wszystkich użytkowników do czasu zakończenia migracji. Ten proces zazwyczaj trwa około 60 minut, w zależności od ilości danych i wydajności środowiska deweloperskiego.**
- **WAŻNE: Wszystkie opublikowane interfejsy API muszą zostać usunięte podczas procesu migracji.**
- **OSTRZEŻENIE: Proces migracji nie może zagwarantować 100% sukcesu dla wszystkich botów. Prosimy o udokumentowanie konfiguracji ważnych botów przed migracją na wypadek konieczności ich ręcznego odtworzenia**

## Wprowadzenie

### Co Nowego w Wersji 3

Wersja 3 wprowadza znaczące ulepszenia w Bedrock Chat:

1. **Szczegółowa kontrola uprawnień**: Kontroluj dostęp do botów za pomocą uprawnień opartych na grupach użytkowników
2. **Sklep z Botami**: Udostępniaj i odkrywaj boty za pośrednictwem scentralizowanego rynku
3. **Funkcje administracyjne**: Zarządzaj interfejsami API, oznaczaj boty jako niezbędne i analizuj użycie botów

Te nowe funkcje wymagały zmian w schemacie DynamoDB, co wiąże się z koniecznością przeprowadzenia procesu migracji dla istniejących użytkowników.

### Dlaczego Ta Migracja Jest Konieczna

Nowy model uprawnień i funkcjonalność Sklepu z Botami wymagały przestrukturyzowania sposobu przechowywania i dostępu do danych botów. Proces migracji konwertuje istniejące boty i rozmowy na nowy schemat, zachowując wszystkie dane.

> [!WARNING]
> Powiadomienie o Przerwie w Usłudze: **Podczas procesu migracji aplikacja będzie niedostępna dla wszystkich użytkowników.** Zaplanuj przeprowadzenie tej migracji w oknie konserwacyjnym, gdy użytkownicy nie potrzebują dostępu do systemu. Aplikacja stanie się ponownie dostępna dopiero po pomyślnym zakończeniu skryptu migracyjnego i prawidłowej konwersji wszystkich danych do nowego schematu. Proces ten zazwyczaj trwa około 60 minut, w zależności od ilości danych i wydajności środowiska deweloperskiego.

> [!IMPORTANT]
> Przed przystąpieniem do migracji: **Proces migracji nie może zagwarantować 100% powodzenia dla wszystkich botów**, szczególnie tych utworzonych w starszych wersjach lub z niestandardowymi konfiguracjami. Przed rozpoczęciem procesu migracji udokumentuj ważne konfiguracje botów (instrukcje, źródła wiedzy, ustawienia) na wypadek konieczności ich ręcznego odtworzenia.

## Proces migracji

### Ważna informacja o widoczności botów w wersji 3

W wersji 3 **wszystkie boty v2 z włączonym udostępnianiem publicznym będą widoczne w sklepie Bot Store.** Jeśli masz boty zawierające poufne informacje, które nie powinny być odkrywalne, rozważ ustawienie ich jako prywatne przed migracją do wersji 3.

### Krok 1: Zidentyfikuj nazwę środowiska

W tej procedurze `{YOUR_ENV_PREFIX}` jest określony do identyfikacji nazwy twoich stosów CloudFormation. Jeśli używasz funkcji [Wdrażanie wielu środowisk](../../README.md#deploying-multiple-environments), zastąp go nazwą środowiska do migracji. Jeśli nie, zastąp go pustym ciągiem.

### Krok 2: Zaktualizuj adres URL repozytorium (Zalecane)

Repozytorium zostało przemianowane z `bedrock-claude-chat` na `bedrock-chat`. Zaktualizuj lokalne repozytorium:

```bash
# Sprawdź aktualny zdalny adres URL
git remote -v

# Zaktualizuj zdalny adres URL
git remote set-url origin https://github.com/aws-samples/bedrock-chat.git

# Sprawdź zmianę
git remote -v
```

### Krok 3: Upewnij się, że jesteś na najnowszej wersji V2

> [!WARNING]
> Musisz zaktualizować do wersji v2.10.0 przed migracją do V3. **Pominięcie tego kroku może spowodować utratę danych podczas migracji.**

Przed rozpoczęciem migracji upewnij się, że używasz najnowszej wersji V2 (**v2.10.0**). Gwarantuje to posiadanie wszystkich niezbędnych poprawek i ulepszeń przed aktualizacją do V3:

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
  --stack-name {YOUR_ENV_PREFIX}BedrockChatStack
```

Upewnij się, że zachowasz tę nazwę tabeli w bezpiecznym miejscu, ponieważ będzie potrzebna później do skryptu migracji.

### Krok 5: Wykonaj kopię zapasową tabeli DynamoDB

Przed kontynuacją utwórz kopię zapasową tabeli ConversationTable przy użyciu nazwy, którą właśnie zanotowałeś:

```bash
# Utwórz kopię zapasową tabeli V2
aws dynamodb create-backup \
  --no-cli-pager \
  --backup-name "BedrockChatV2Backup-$(date +%Y%m%d)" \
  --table-name YOUR_V2_CONVERSATION_TABLE_NAME

# Sprawdź, czy kopia zapasowa jest dostępna
aws dynamodb describe-backup \
  --no-cli-pager \
  --query BackupDescription.BackupDetails \
  --backup-arn YOUR_BACKUP_ARN
```

### Krok 6: Usuń wszystkie opublikowane interfejsy API

> [!IMPORTANT]
> Przed wdrożeniem V3 musisz usunąć wszystkie opublikowane interfejsy API, aby uniknąć konfliktów wartości wyjściowych CloudFormation podczas procesu aktualizacji.

1. Zaloguj się do aplikacji jako administrator
2. Przejdź do sekcji Administracja i wybierz "Zarządzanie API"
3. Przejrzyj listę wszystkich opublikowanych interfejsów API
4. Usuń każdy opublikowany interfejs API, klikając przycisk usuwania obok niego

Więcej informacji o publikowaniu i zarządzaniu interfejsami API można znaleźć w dokumentacji [PUBLISH_API.md](../PUBLISH_API_pl-PL.md), [ADMINISTRATOR.md](../ADMINISTRATOR_pl-PL.md).

### Krok 7: Pobierz V3 i wdróż

Pobierz najnowszy kod V3 i wdróż:

```bash
git fetch
git checkout v3
cd cdk
npm ci
npx cdk deploy --all
```

> [!IMPORTANT]
> Po wdrożeniu V3 aplikacja będzie niedostępna dla wszystkich użytkowników do czasu zakończenia procesu migracji. Nowy schemat jest niezgodny ze starym formatem danych, więc użytkownicy nie będą mogli uzyskać dostępu do swoich botów lub rozmów do czasu zakończenia skryptu migracji w kolejnych krokach.

### Krok 8: Zanotuj nazwy tabel DynamoDB V3

Po wdrożeniu V3 musisz pobrać nazwy zarówno nowej tabeli ConversationTable, jak i BotTable:

```bash
# Pobierz nazwę tabeli ConversationTable V3
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='ConversationTableNameV3'].OutputValue" \
  --stack-name {YOUR_ENV_PREFIX}BedrockChatStack

# Pobierz nazwę tabeli BotTable V3
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='BotTableNameV3'].OutputValue" \
  --stack-name {YOUR_ENV_PREFIX}BedrockChatStack
```

> [!Important]
> Upewnij się, że zachowasz nazwy tabel V3 wraz z wcześniej zapisaną nazwą tabeli V2, ponieważ będą potrzebne do skryptu migracji.

### Krok 9: Uruchom skrypt migracji

Skrypt migracji przekształci dane V2 do schematu V3. Najpierw edytuj skrypt migracji `docs/migration/migrate_v2_v3.py`, aby ustawić nazwy tabel i region:

```python
# Region, w którym znajduje się dynamodb
REGION = "ap-northeast-1" # Zastąp swoim regionem

V2_CONVERSATION_TABLE = "BedrockChatStack-DatabaseConversationTableXXXX" # Zastąp zanotowaną wartością z kroku 4
V3_CONVERSATION_TABLE = "BedrockChatStack-DatabaseConversationTableV3XXXX" # Zastąp zanotowaną wartością z kroku 8
V3_BOT_TABLE = "BedrockChatStack-DatabaseBotTableV3XXXXX" # Zastąp zanotowaną wartością z kroku 8
```

Następnie uruchom skrypt za pomocą Poetry z katalogu backend:

> [!NOTE]
> Wersja wymagań Python została zmieniona na 3.13.0 lub nowszą (Możliwe, że zostanie zmieniona w przyszłym rozwoju. Patrz pyproject.toml). Jeśli masz zainstalowane venv z inną wersją Python, będziesz musiał je usunąć.

```bash
# Przejdź do katalogu backend
cd backend

# Zainstaluj zależności, jeśli jeszcze tego nie zrobiłeś
poetry install

# Najpierw wykonaj próbę suchego uruchomienia, aby zobaczyć, co zostanie zmigrowane
poetry run python ../docs/migration/migrate_v2_v3.py --dry-run

# Jeśli wszystko wygląda dobrze, wykonaj faktyczną migrację
poetry run python ../docs/migration/migrate_v2_v3.py

# Sprawdź, czy migracja zakończyła się sukcesem
poetry run python ../docs/migration/migrate_v2_v3.py --verify-only
```

Skrypt migracji wygeneruje plik raportu w bieżącym katalogu ze szczegółami procesu migracji. Sprawdź ten plik, aby upewnić się, że wszystkie dane zostały poprawnie zmigrowane.

#### Obsługa dużych wolumenów danych

Dla środowisk z aktywnymi użytkownikami lub dużymi ilościami danych rozważ następujące podejścia:

1. **Migracja użytkowników indywidualnie**: Dla użytkowników z dużymi wolumenami danych, migruj ich po kolei:

   ```bash
   poetry run python ../docs/migration/migrate_v2_v3.py --users user-id-1 user-id-2
   ```

2. **Uwagi dotyczące pamięci**: Proces migracji ładuje dane do pamięci. Jeśli napotkasz błędy Out-Of-Memory (OOM), spróbuj:

   - Migracji jednego użytkownika na raz
   - Uruchomienia migracji na maszynie z większą ilością pamięci
   - Podzielenia migracji na mniejsze partie użytkowników

3. **Monitoruj migrację**: Sprawdź wygenerowane pliki raportów, aby upewnić się, że wszystkie dane są poprawnie zmigrowane, szczególnie dla dużych zbiorów danych.

### Krok 10: Sprawdź aplikację

Po migracji otwórz swoją aplikację i sprawdź:

- Wszystkie twoje boty są dostępne
- Rozmowy są zachowane
- Nowe kontrole uprawnień działają

### Czyszczenie (opcjonalne)

Po potwierdzeniu, że migracja zakończyła się sukcesem i wszystkie ważne dane są prawidłowo dostępne w V3, możesz opcjonalnie usunąć tabelę konwersacji V2, aby zaoszczędzić koszty:

```bash
# Usuń tabelę konwersacji V2 (TYLKO po potwierdzeniu udanej migracji)
aws dynamodb delete-table --table-name YOUR_V2_CONVERSATION_TABLE_NAME
```

> [!IMPORTANT]
> Usuń tabelę V2 dopiero po dokładnym sprawdzeniu, czy wszystkie ważne dane zostały pomyślnie zmigrowane do V3. Zalecamy zachowanie kopii zapasowej utworzonej w kroku 2 przez co najmniej kilka tygodni po migracji, nawet jeśli usuniesz oryginalną tabelę.

## Często zadawane pytania V3

### Dostęp do bota i uprawnienia

**P: Co się stanie, jeśli bot, którego używam, zostanie usunięty lub moje uprawnienia dostępu zostaną cofnięte?**
O: Autoryzacja jest sprawdzana w momencie rozmowy, więc utracisz dostęp natychmiast.

**P: Co się stanie, jeśli użytkownik zostanie usunięty (np. pracownik odchodzi)?**
O: Jego dane mogą zostać całkowicie usunięte poprzez usunięcie wszystkich elementów z DynamoDB z jego identyfikatorem użytkownika jako kluczem partycji (PK).

**P: Czy mogę wyłączyć udostępnianie dla niezbędnego bota publicznego?**
O: Nie, administrator musi najpierw oznaczyć bota jako nieniezbędny, zanim będzie można wyłączyć udostępnianie.

**P: Czy mogę usunąć niezbędnego bota publicznego?**
O: Nie, administrator musi najpierw oznaczyć bota jako nieniezbędny, zanim będzie można go usunąć.

### Bezpieczeństwo i implementacja

**P: Czy zaimplementowano bezpieczeństwo na poziomie wierszy (RLS) dla tabeli botów?**
O: Nie, biorąc pod uwagę różnorodność wzorców dostępu. Autoryzacja jest przeprowadzana podczas uzyskiwania dostępu do botów, a ryzyko wycieku metadanych jest uznawane za minimalne w porównaniu z historią rozmów.

**P: Jakie są wymagania dotyczące publikacji API?**
O: Bot musi być publiczny.

**P: Czy będzie ekran zarządzania wszystkimi prywatnymi botami?**
O: Nie w początkowej wersji V3. Jednak elementy można nadal usuwać, wykonując zapytania z identyfikatorem użytkownika w razie potrzeby.

**P: Czy będzie funkcja tagowania botów dla lepszego doświadczenia wyszukiwania?**
O: Nie w początkowej wersji V3, ale automatyczne tagowanie oparte na LLM może zostać dodane w przyszłych aktualizacjach.

### Administracja

**P: Co mogą robić administratorzy?**
O: Administratorzy mogą:

- Zarządzać botami publicznymi (w tym sprawdzać boty o wysokich kosztach)
- Zarządzać API
- Oznaczać boty publiczne jako niezbędne

**P: Czy mogę oznaczyć boty częściowo udostępniane jako niezbędne?**
O: Nie, obsługiwane są tylko boty publiczne.

**P: Czy mogę ustawić priorytet dla przypiętych botów?**
O: W początkowej wersji - nie.

### Konfiguracja autoryzacji

**P: Jak skonfigurować autoryzację?**
O:

1. Otwórz konsolę Amazon Cognito i utwórz grupy użytkowników w puli użytkowników BrChat
2. Dodaj użytkowników do tych grup zgodnie z potrzebami
3. W BrChat wybierz grupy użytkowników, którym chcesz zezwolić na dostęp podczas konfigurowania ustawień udostępniania bota

Uwaga: Zmiany członkostwa w grupach wymagają ponownego zalogowania. Zmiany są odzwierciedlane przy odświeżeniu tokenu, ale nie w trakcie ważności tokenu ID (domyślnie 30 minut w V3, konfigurowalne przez `tokenValidMinutes` w `cdk.json` lub `parameter.ts`).

**P: Czy system sprawdza Cognito za każdym razem, gdy uzyskuje się dostęp do bota?**
O: Nie, autoryzacja jest sprawdzana przy użyciu tokenu JWT, aby uniknąć zbędnych operacji we/wy.

### Funkcjonalność wyszukiwania

**P: Czy wyszukiwanie botów obsługuje wyszukiwanie semantyczne?**
O: Nie, obsługiwane jest tylko częściowe dopasowanie tekstu. Wyszukiwanie semantyczne (np. "samochód" → "auto", "EV", "pojazd") nie jest dostępne ze względu na obecne ograniczenia OpenSearch Serverless (marzec 2025).