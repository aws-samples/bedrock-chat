# Przewodnik migracji (v0 do v1)

Jeśli już używasz Bedrock Chat w poprzedniej wersji (~`0.4.x`), musisz wykonać poniższe kroki, aby przeprowadzić migrację.

## Dlaczego muszę to zrobić?

Ta ważna aktualizacja zawiera istotne poprawki bezpieczeństwa.

- Baza danych wektorowa (tj. pgvector na Aurora PostgreSQL) jest teraz szyfrowana, co powoduje wymianę podczas wdrażania. Oznacza to, że istniejące elementy wektorowe zostaną usunięte.
- Wprowadziliśmy grupę użytkowników Cognito `CreatingBotAllowed`, aby ograniczyć użytkowników, którzy mogą tworzyć boty. Obecni użytkownicy nie są w tej grupie, więc musisz ręcznie nadać uprawnienia, jeśli chcesz, aby mieli możliwość tworzenia botów. Zobacz: [Personalizacja Bota](../../README.md#bot-personalization)

## Wymagania wstępne

Przeczytaj [Database Migration Guide](./DATABASE_MIGRATION_pl-PL.md) i określ metodę przywracania elementów.

## Kroki

### Migracja magazynu wektorowego

- Otwórz terminal i przejdź do katalogu projektu
- Pobierz gałąź, którą chcesz wdrożyć. Poniżej przedstawiono sposób przejścia na żądaną gałąź (w tym przypadku `v1`) i pobrania najnowszych zmian:

```sh
git fetch
git checkout v1
git pull origin v1
```

- Jeśli chcesz przywrócić elementy za pomocą DMS, NIE ZAPOMNIJ wyłączyć rotacji haseł i zanotować hasło dostępu do bazy danych. Jeśli przywracasz przy użyciu skryptu migracji ([migrate_v0_v1.py](./migrate_v0_v1.py)), nie musisz notować hasła.
- Usuń wszystkie [opublikowane API](../PUBLISH_API_pl-PL.md), aby CloudFormation mógł usunąć istniejący klaster Aurora.
- Uruchomienie [npx cdk deploy](../README.md#deploy-using-cdk) spowoduje wymianę klastra Aurora i USUNIE WSZYSTKIE ELEMENTY WEKTOROWE.
- Postępuj zgodnie z [Przewodnikiem Migracji Bazy Danych](./DATABASE_MIGRATION_pl-PL.md), aby przywrócić elementy wektorowe.
- Sprawdź, czy użytkownik może korzystać z istniejących botów posiadających wiedzę, np. botów RAG.

### Dodawanie uprawnienia CreatingBotAllowed

- Po wdrożeniu wszyscy użytkownicy nie będą mogli tworzyć nowych botów.
- Jeśli chcesz, aby określeni użytkownicy mogli tworzyć boty, dodaj tych użytkowników do grupy `CreatingBotAllowed` za pomocą konsoli zarządzania lub CLI.
- Sprawdź, czy użytkownik może utworzyć bota. Pamiętaj, że użytkownicy muszą się ponownie zalogować.