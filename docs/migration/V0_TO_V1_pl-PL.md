# Przewodnik migracji (z wersji 0 do wersji 1)

Jeśli już używasz Bedrock Chat w poprzedniej wersji (~`0.4.x`), musisz postępować zgodnie z poniższymi krokami, aby przeprowadzić migrację.

## Dlaczego muszę to zrobić?

Ta główna aktualizacja obejmuje ważne aktualizacje bezpieczeństwa.

- Magazyn bazy danych wektorowych (tj. pgvector na Aurora PostgreSQL) jest teraz szyfrowany, co powoduje wymianę podczas wdrożenia. Oznacza to, że istniejące elementy wektorowe zostaną usunięte.
- Wprowadziliśmy grupę użytkowników Cognito `CreatingBotAllowed`, aby ograniczyć użytkowników, którzy mogą tworzyć boty. Obecni istniejący użytkownicy nie należą do tej grupy, więc musisz ręcznie dołączyć uprawnienia, jeśli chcesz, aby mogli tworzyć boty. Zobacz: [Personalizacja Bota](../../README.md#bot-personalization)

## Wymagania wstępne

Przeczytaj [Przewodnik migracji bazy danych](./DATABASE_MIGRATION_pl-PL.md) i ustal metodę przywracania elementów.

## Kroki

### Migracja magazynu wektorowego

- Otwórz terminal i przejdź do katalogu projektu
- Pobierz branch, który chcesz wdrożyć. Przełącz się na żądany branch (w tym przypadku `v1`) i pobierz najnowsze zmiany:

```sh
git fetch
git checkout v1
git pull origin v1
```

- Jeśli chcesz przywrócić elementy za pomocą DMS, PAMIĘTAJ o wyłączeniu rotacji hasła i zanotuj hasło dostępu do bazy danych. Jeśli przywracasz za pomocą skryptu migracyjnego([migrate_v0_v1.py](./migrate_v0_v1.py)), nie musisz notować hasła.
- Usuń wszystkie [opublikowane interfejsy API](../PUBLISH_API_pl-PL.md), aby CloudFormation mógł usunąć istniejący klaster Aurora.
- Uruchom [npx cdk deploy](../README.md#deploy-using-cdk), co spowoduje wymianę klastra Aurora i USUNIE WSZYSTKIE ELEMENTY WEKTOROWE.
- Postępuj zgodnie z [Przewodnikiem migracji bazy danych](./DATABASE_MIGRATION_pl-PL.md), aby przywrócić elementy wektorowe.
- Sprawdź, czy użytkownik może korzystać z istniejących botów z wiedzą, tj. botów RAG.

### Dołączenie uprawnienia CreatingBotAllowed

- Po wdrożeniu wszyscy użytkownicy nie będą mogli tworzyć nowych botów.
- Jeśli chcesz, aby konkretni użytkownicy mogli tworzyć boty, dodaj tych użytkowników do grupy `CreatingBotAllowed` za pomocą konsoli zarządzania lub interfejsu wiersza poleceń.
- Sprawdź, czy użytkownik może utworzyć bota. Pamiętaj, że użytkownicy muszą się ponownie zalogować.