# Przewodnik po Migracji Bazy Danych

> [!Warning]
> Ten przewodnik dotyczy migracji z wersji 0 do wersji 1.

Ten przewodnik opisuje kroki migracji danych podczas aktualizacji Bedrock Chat, która obejmuje wymianę klastra Aurora. Poniższa procedura zapewnia płynne przejście przy minimalnym czasie przestoju i ryzyku utraty danych.

## Przegląd

Proces migracji polega na skanowaniu wszystkich botów i uruchamianiu zadań ECS z osadzaniem dla każdego z nich. To podejście wymaga przeliczenia osadzeń, co może być czasochłonne i wiązać się z dodatkowymi kosztami z powodu wykonywania zadań ECS oraz opłat za korzystanie z usługi Bedrock Cohere. Jeśli wolisz uniknąć tych kosztów i wymagań czasowych, zapoznaj się z [alternatywnymi opcjami migracji](#alternative-migration-options), które zostały przedstawione w dalszej części tego przewodnika.

## Kroki migracji

- Po wykonaniu polecenia [npx cdk deploy](../README.md#deploy-using-cdk) z wymianą Aurora, otwórz skrypt [migrate_v0_v1.py](./migrate_v0_v1.py) i zaktualizuj następujące zmienne odpowiednimi wartościami. Wartości można znaleźć w zakładce `CloudFormation` > `BedrockChatStack` > `Outputs`.

```py
# Otwórz stos CloudFormation w konsoli AWS Management Console i skopiuj wartości z zakładki Outputs.
# Klucz: DatabaseConversationTableNameXXXX
TABLE_NAME = "BedrockChatStack-DatabaseConversationTableXXXXX"
# Klucz: EmbeddingClusterNameXXX
CLUSTER_NAME = "BedrockChatStack-EmbeddingClusterXXXXX"
# Klucz: EmbeddingTaskDefinitionNameXXX
TASK_DEFINITION_NAME = "BedrockChatStackEmbeddingTaskDefinitionXXXXX"
CONTAINER_NAME = "Container"  # Nie trzeba zmieniać
# Klucz: PrivateSubnetId0
SUBNET_ID = "subnet-xxxxx"
# Klucz: EmbeddingTaskSecurityGroupIdXXX
SECURITY_GROUP_ID = "sg-xxxx"  # BedrockChatStack-EmbeddingTaskSecurityGroupXXXXX
```

- Uruchom skrypt `migrate_v0_v1.py`, aby rozpocząć proces migracji. Ten skrypt przeskanuje wszystkie boty, uruchomi zadania osadzania ECS i utworzy dane w nowym klastrze Aurora. Należy pamiętać, że:
  - Skrypt wymaga `boto3`.
  - Środowisko wymaga uprawnień IAM do dostępu do tabeli DynamoDB i wywoływania zadań ECS.

## Alternatywne opcje migracji

Jeśli wolisz nie korzystać z powyższej metody ze względu na związane z nią implikacje czasowe i kosztowe, rozważ następujące alternatywne podejścia:

### Przywracanie migawki i migracja DMS

Najpierw zanotuj hasło dostępu do bieżącego klastra Aurora. Następnie uruchom `npx cdk deploy`, co spowoduje wymianę klastra. Potem utwórz tymczasową bazę danych, przywracając ją z migawki oryginalnej bazy danych.
Użyj [AWS Database Migration Service (DMS)](https://aws.amazon.com/dms/), aby przeprowadzić migrację danych z tymczasowej bazy danych do nowego klastra Aurora.

Uwaga: Według stanu na 29 maja 2024 r., DMS nie obsługuje natywnie rozszerzenia pgvector. Można jednak rozważyć następujące opcje obejścia tego ograniczenia:

Użyj [migracji jednorodnej DMS](https://docs.aws.amazon.com/dms/latest/userguide/dm-migrating-data.html), która wykorzystuje natywną replikację logiczną. W tym przypadku zarówno źródłowa, jak i docelowa baza danych muszą być PostgreSQL. DMS może wykorzystać natywną replikację logiczną do tego celu.

Rozważ specyficzne wymagania i ograniczenia Twojego projektu przy wyborze najbardziej odpowiedniego podejścia migracyjnego.