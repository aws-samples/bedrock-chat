# Przewodnik migracji (v2 do v3)

## TL;DR

- Wersja V3 wprowadza szczegółową kontrolę uprawnień i funkcjonalność Bot Store, wymagając zmian w schemacie DynamoDB
- **Wykonaj kopię zapasową tabeli ConversationTable w DynamoDB przed migracją**
- Zaktualizuj URL repozytorium z `bedrock-claude-chat` na `bedrock-chat`
- Uruchom skrypt migracyjny, aby przekonwertować dane do nowego schematu
- Wszystkie twoje boty i konwersacje zostaną zachowane w nowym modelu uprawnień
- **WAŻNE: Podczas procesu migracji aplikacja będzie niedostępna dla wszystkich użytkowników do czasu zakończenia migracji. Ten proces trwa zazwyczaj około 60 minut, w zależności od ilości danych i wydajności środowiska deweloperskiego.**
- **WAŻNE: Wszystkie opublikowane API muszą zostać usunięte podczas procesu migracji.**
- **OSTRZEŻENIE: Proces migracji nie może zagwarantować 100% sukcesu dla wszystkich botów. Przed migracją należy udokumentować ważne konfiguracje botów na wypadek konieczności ich ręcznego odtworzenia**

## Wprowadzenie

### Co nowego w V3

V3 wprowadza znaczące ulepszenia do Bedrock Chat:

1. **Precyzyjna kontrola uprawnień**: Kontroluj dostęp do botów za pomocą uprawnień opartych na grupach użytkowników
2. **Bot Store**: Udostępniaj i odkrywaj boty poprzez scentralizowany marketplace
3. **Funkcje administracyjne**: Zarządzaj API, oznaczaj boty jako kluczowe i analizuj ich wykorzystanie

Te nowe funkcje wymagały zmian w schemacie DynamoDB, co wymusiło proces migracji dla istniejących użytkowników.

### Dlaczego ta migracja jest konieczna

Nowy model uprawnień i funkcjonalność Bot Store wymagały restrukturyzacji sposobu przechowywania i dostępu do danych botów. Proces migracji przekształca istniejące boty i konwersacje do nowego schematu, zachowując wszystkie dane.

> [!WARNING]
> Informacja o przerwach w działaniu usługi: **Podczas procesu migracji aplikacja będzie niedostępna dla wszystkich użytkowników.** Zaplanuj przeprowadzenie tej migracji w oknie serwisowym, gdy użytkownicy nie potrzebują dostępu do systemu. Aplikacja będzie ponownie dostępna dopiero po pomyślnym zakończeniu skryptu migracyjnego i prawidłowej konwersji wszystkich danych do nowego schematu. Ten proces zazwyczaj trwa około 60 minut, w zależności od ilości danych i wydajności środowiska deweloperskiego.

> [!IMPORTANT]
> Przed rozpoczęciem migracji: **Proces migracji nie może zagwarantować 100% sukcesu dla wszystkich botów**, szczególnie tych utworzonych w starszych wersjach lub z niestandardowymi konfiguracjami. Prosimy o udokumentowanie ważnych konfiguracji botów (instrukcje, źródła wiedzy, ustawienia) przed rozpoczęciem procesu migracji, na wypadek gdyby trzeba było je odtworzyć ręcznie.

## Proces migracji

### Ważna informacja o widoczności botów w V3

W V3, **wszystkie boty v2 z włączonym publicznym udostępnianiem będą możliwe do wyszukania w Bot Store.** Jeśli masz boty zawierające poufne informacje, których nie chcesz udostępniać publicznie, rozważ ustawienie ich jako prywatne przed migracją do V3.

### Krok 1: Zidentyfikuj nazwę swojego środowiska

W tej procedurze, `{YOUR_ENV_PREFIX}` służy do identyfikacji nazwy Twoich stosów CloudFormation. Jeśli korzystasz z funkcji [Deploying Multiple Environments](../../README.md#deploying-multiple-environments), zastąp ją nazwą środowiska, które ma zostać zmigrowane. Jeśli nie, zastąp ją pustym ciągiem.

### Krok 2: Aktualizacja adresu URL repozytorium (Zalecane)

Nazwa repozytorium została zmieniona z `bedrock-claude-chat` na `bedrock-chat`. Zaktualizuj swoje lokalne repozytorium:

```bash
# Check your current remote URL
git remote -v

# Update the remote URL
git remote set-url origin https://github.com/aws-samples/bedrock-chat.git

# Verify the change
git remote -v
```

### Krok 3: Upewnij się, że masz najnowszą wersję V2

> [!WARNING]
> MUSISZ zaktualizować do wersji v2.10.0 przed migracją do V3. **Pominięcie tego kroku może skutkować utratą danych podczas migracji.**

Przed rozpoczęciem migracji upewnij się, że używasz najnowszej wersji V2 (**v2.10.0**). Zapewni to dostęp do wszystkich niezbędnych poprawek błędów i ulepszeń przed aktualizacją do V3:

```bash
# Fetch the latest tags
git fetch --tags

# Checkout the latest V2 version
git checkout v2.10.0

# Deploy the latest V2 version
cd cdk
npm ci
npx cdk deploy --all
```

### Krok 4: Zapisz nazwę tabeli DynamoDB V2

Pobierz nazwę tabeli ConversationTable V2 z wyników CloudFormation:

```bash
# Get the V2 ConversationTable name
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='ConversationTableName'].OutputValue" \
  --stack-name {YOUR_ENV_PREFIX}BedrockChatStack
```

Pamiętaj, aby zapisać tę nazwę tabeli w bezpiecznym miejscu, ponieważ będzie potrzebna później do skryptu migracji.

### Krok 5: Utwórz kopię zapasową tabeli DynamoDB

Przed kontynuowaniem utwórz kopię zapasową tabeli ConversationTable DynamoDB używając zapisanej wcześniej nazwy:

```bash
# Create a backup of your V2 table
aws dynamodb create-backup \
  --no-cli-pager \
  --backup-name "BedrockChatV2Backup-$(date +%Y%m%d)" \
  --table-name YOUR_V2_CONVERSATION_TABLE_NAME

# Check the backup status is available
aws dynamodb describe-backup \
  --no-cli-pager \
  --query BackupDescription.BackupDetails \
  --backup-arn YOUR_BACKUP_ARN
```

### Krok 6: Usuń wszystkie opublikowane API

> [!IMPORTANT]
> Przed wdrożeniem V3 musisz usunąć wszystkie opublikowane API, aby uniknąć konfliktów wartości wyjściowych Cloudformation podczas procesu aktualizacji.

1. Zaloguj się do aplikacji jako administrator
2. Przejdź do sekcji Admin i wybierz "API Management"
3. Przejrzyj listę wszystkich opublikowanych API
4. Usuń każde opublikowane API klikając przycisk usuwania obok niego

Więcej informacji o publikowaniu i zarządzaniu API znajdziesz w dokumentacji [PUBLISH_API.md](../PUBLISH_API_pl-PL.md), [ADMINISTRATOR.md](../ADMINISTRATOR_pl-PL.md).

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
> Po wdrożeniu V3 aplikacja będzie niedostępna dla wszystkich użytkowników do czasu zakończenia procesu migracji. Nowy schemat jest niekompatybilny ze starym formatem danych, więc użytkownicy nie będą mogli uzyskać dostępu do swoich botów ani konwersacji do czasu zakończenia skryptu migracji w kolejnych krokach.

### Krok 8: Zapisz nazwy tabel DynamoDB V3

Po wdrożeniu V3 musisz pobrać nazwy zarówno nowej tabeli ConversationTable jak i BotTable:

```bash
# Get the V3 ConversationTable name
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='ConversationTableNameV3'].OutputValue" \
  --stack-name {YOUR_ENV_PREFIX}BedrockChatStack

# Get the V3 BotTable name
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='BotTableNameV3'].OutputValue" \
  --stack-name {YOUR_ENV_PREFIX}BedrockChatStack
```

> [!Important]
> Pamiętaj, aby zapisać te nazwy tabel V3 wraz z wcześniej zapisaną nazwą tabeli V2, ponieważ wszystkie będą potrzebne do skryptu migracji.

### Krok 9: Uruchom skrypt migracji

Skrypt migracji przekonwertuje Twoje dane V2 do schematu V3. Najpierw edytuj skrypt migracji `docs/migration/migrate_v2_v3.py`, aby ustawić nazwy tabel i region:

```python
# Region where dynamodb is located
REGION = "ap-northeast-1" # Replace with your region

V2_CONVERSATION_TABLE = "BedrockChatStack-DatabaseConversationTableXXXX" # Replace with your  value recorded in Step 4
V3_CONVERSATION_TABLE = "BedrockChatStack-DatabaseConversationTableV3XXXX" # Replace with your  value recorded in Step 8
V3_BOT_TABLE = "BedrockChatStack-DatabaseBotTableV3XXXXX" # Replace with your  value recorded in Step 8
```

Następnie uruchom skrypt używając Poetry z katalogu backend:

> [!NOTE]
> Wersja wymagań Pythona została zmieniona na 3.13.0 lub nowszą (Może ulec zmianie w przyszłym rozwoju. Zobacz pyproject.toml). Jeśli masz zainstalowane venv z inną wersją Pythona, będziesz musiał je najpierw usunąć.

```bash
# Navigate to the backend directory
cd backend

# Install dependencies if you haven't already
poetry install

# Run a dry run first to see what would be migrated
poetry run python ../docs/migration/migrate_v2_v3.py --dry-run

# If everything looks good, run the actual migration
poetry run python ../docs/migration/migrate_v2_v3.py

# Verify the migration was successful
poetry run python ../docs/migration/migrate_v2_v3.py --verify-only
```

Skrypt migracji wygeneruje plik raportu w bieżącym katalogu ze szczegółami procesu migracji. Sprawdź ten plik, aby upewnić się, że wszystkie dane zostały poprawnie zmigrowane.

#### Obsługa dużych ilości danych

Dla środowisk z dużą liczbą użytkowników lub dużą ilością danych rozważ następujące podejścia:

1. **Migruj użytkowników pojedynczo**: Dla użytkowników z dużą ilością danych, migruj ich po kolei:

   ```bash
   poetry run python ../docs/migration/migrate_v2_v3.py --users user-id-1 user-id-2
   ```

2. **Uwagi dotyczące pamięci**: Proces migracji ładuje dane do pamięci. Jeśli napotkasz błędy Out-Of-Memory (OOM), spróbuj:

   - Migrować jednego użytkownika na raz
   - Uruchomić migrację na maszynie z większą ilością pamięci
   - Podzielić migrację na mniejsze partie użytkowników

3. **Monitoruj migrację**: Sprawdzaj wygenerowane pliki raportów, aby upewnić się, że wszystkie dane są poprawnie migrowane, szczególnie w przypadku dużych zbiorów danych.

### Krok 10: Zweryfikuj aplikację

Po migracji otwórz swoją aplikację i zweryfikuj:

- Wszystkie boty są dostępne
- Konwersacje zostały zachowane
- Nowe kontrole uprawnień działają

### Czyszczenie (Opcjonalne)

Po potwierdzeniu, że migracja zakończyła się sukcesem i wszystkie dane są poprawnie dostępne w V3, możesz opcjonalnie usunąć tabelę konwersacji V2, aby zaoszczędzić koszty:

```bash
# Delete the V2 conversation table (ONLY after confirming successful migration)
aws dynamodb delete-table --table-name YOUR_V2_CONVERSATION_TABLE_NAME
```

> [!IMPORTANT]
> Usuń tabelę V2 dopiero po dokładnym zweryfikowaniu, że wszystkie ważne dane zostały pomyślnie zmigrowane do V3. Zalecamy zachowanie kopii zapasowej utworzonej w Kroku 2 przez co najmniej kilka tygodni po migracji, nawet jeśli usuniesz oryginalną tabelę.

## V3 FAQ

### Dostęp i uprawnienia botów

**Q: Co się stanie, jeśli bot, którego używam, zostanie usunięty lub moje uprawnienia dostępu zostaną cofnięte?**
A: Autoryzacja jest sprawdzana w momencie czatu, więc stracisz dostęp natychmiast.

**Q: Co się stanie, jeśli użytkownik zostanie usunięty (np. pracownik odchodzi)?**
A: Jego dane mogą zostać całkowicie usunięte poprzez skasowanie wszystkich elementów z DynamoDB z jego ID użytkownika jako kluczem partycji (PK).

**Q: Czy mogę wyłączyć udostępnianie dla bota publicznego oznaczonego jako niezbędny?**
A: Nie, administrator musi najpierw oznaczyć bota jako nieistotnego przed wyłączeniem udostępniania.

**Q: Czy mogę usunąć niezbędnego bota publicznego?**
A: Nie, administrator musi najpierw oznaczyć bota jako nieistotnego przed usunięciem.

### Bezpieczeństwo i implementacja

**Q: Czy zaimplementowano zabezpieczenia na poziomie wierszy (RLS) dla tabeli botów?**
A: Nie, biorąc pod uwagę różnorodność wzorców dostępu. Autoryzacja jest wykonywana podczas dostępu do botów, a ryzyko wycieku metadanych jest uznawane za minimalne w porównaniu z historią konwersacji.

**Q: Jakie są wymagania dotyczące publikowania API?**
A: Bot musi być publiczny.

**Q: Czy będzie ekran zarządzania dla wszystkich prywatnych botów?**
A: Nie w początkowej wersji V3. Jednak elementy nadal mogą być usuwane poprzez zapytania z ID użytkownika w razie potrzeby.

**Q: Czy będzie funkcja tagowania botów dla lepszego UX wyszukiwania?**
A: Nie w początkowej wersji V3, ale automatyczne tagowanie oparte na LLM może zostać dodane w przyszłych aktualizacjach.

### Administracja

**Q: Co mogą robić administratorzy?**
A: Administratorzy mogą:

- Zarządzać botami publicznymi (w tym sprawdzać boty o wysokich kosztach)
- Zarządzać API
- Oznaczać boty publiczne jako niezbędne

**Q: Czy mogę oznaczyć częściowo udostępnione boty jako niezbędne?**
A: Nie, obsługiwane są tylko boty publiczne.

**Q: Czy mogę ustawić priorytet dla przypiętych botów?**
A: Nie w początkowej wersji.

### Konfiguracja autoryzacji

**Q: Jak skonfigurować autoryzację?**
A:

1. Otwórz konsolę Amazon Cognito i utwórz grupy użytkowników w puli użytkowników BrChat
2. Dodaj użytkowników do tych grup według potrzeb
3. W BrChat wybierz grupy użytkowników, którym chcesz zezwolić na dostęp podczas konfigurowania ustawień udostępniania botów

Uwaga: Zmiany członkostwa w grupach wymagają ponownego logowania, aby weszły w życie. Zmiany są odzwierciedlane przy odświeżaniu tokena, ale nie w okresie ważności tokena ID (domyślnie 30 minut w V3, konfigurowalne przez `tokenValidMinutes` w `cdk.json` lub `parameter.ts`).

**Q: Czy system sprawdza Cognito za każdym razem, gdy bot jest używany?**
A: Nie, autoryzacja jest sprawdzana przy użyciu tokena JWT, aby uniknąć niepotrzebnych operacji I/O.

### Funkcjonalność wyszukiwania

**Q: Czy wyszukiwanie botów obsługuje wyszukiwanie semantyczne?**
A: Nie, obsługiwane jest tylko częściowe dopasowanie tekstu. Wyszukiwanie semantyczne (np. "automobil" → "samochód", "EV", "pojazd") nie jest dostępne ze względu na obecne ograniczenia OpenSearch Serverless (marzec 2025).