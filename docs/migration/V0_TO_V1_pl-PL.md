# Przewodnik migracji (z wersji 0 do wersji 1)

Jeśli już używasz Bedrock Claude Chat z poprzednią wersją (~`0.4.x`), musisz wykonać poniższe kroki, aby przeprowadzić migrację.

## Dlaczego muszę to zrobić?

Ta główna aktualizacja zawiera ważne aktualizacje bezpieczeństwa.

- Magazyn bazy danych wektorowych (tj. pgvector na Aurora PostgreSQL) jest teraz szyfrowany, co powoduje jego wymianę podczas wdrożenia. Oznacza to, że istniejące elementy wektorowe zostaną usunięte.
- Wprowadziliśmy grupę użytkowników Cognito `CreatingBotAllowed`, aby ograniczyć użytkowników, którzy mogą tworzyć boty. Obecni istniejący użytkownicy nie należą do tej grupy, więc musisz ręcznie przypisać uprawnienia, jeśli chcesz, aby mogli tworzyć boty. Zobacz: [Personalizacja Bota](../../README.md#bot-personalization)

## Wymagania wstępne

Zapoznaj się z [Przewodnikiem migracji bazy danych](./DATABASE_MIGRATION_pl-PL.md) i ustal metodę przywracania elementów.

## Kroki

### Migracja magazynu wektorowego

- Otwórz terminal i przejdź do katalogu projektu
- Pobierz branch, który chcesz wdrożyć. Przełącz się na żądany branch (w tym przypadku `v1`) i pobierz najnowsze zmiany:

```sh
git fetch
git checkout v1
git pull origin v1
```

- Jeśli chcesz przywrócić elementy za pomocą DMS, PAMIĘTAJ o wyłączeniu rotacji hasła i zanotuj hasło dostępu do bazy danych. Jeśli przywracasz przy użyciu skryptu migracyjnego ([migrate.py](./migrate.py)), nie musisz notować hasła.
- Usuń wszystkie [opublikowane interfejsy API](../PUBLISH_API_pl-PL.md), aby CloudFormation mógł usunąć istniejący klaster Aurora.
- Uruchom [npx cdk deploy](../README.md#deploy-using-cdk), co spowoduje wymianę klastra Aurora i USUNIĘCIE WSZYSTKICH ELEMENTÓW WEKTOROWYCH.
- Postępuj zgodnie z [Przewodnikiem migracji bazy danych](./DATABASE_MIGRATION_pl-PL.md), aby przywrócić elementy wektorowe.
- Sprawdź, czy użytkownik może korzystać z istniejących botów, którzy posiadają wiedzę, tj. botów RAG.

### Dołączenie uprawnienia CreatingBotAllowed

- Po wdrożeniu wszyscy użytkownicy nie będą mogli tworzyć nowych botów.
- Jeśli chcesz, aby konkretni użytkownicy mogli tworzyć boty, dodaj tych użytkowników do grupy `CreatingBotAllowed` za pomocą konsoli zarządzania lub interfejsu wiersza poleceń.
- Sprawdź, czy użytkownik może utworzyć bota. Należy pamiętać, że użytkownicy muszą się ponownie zalogować.