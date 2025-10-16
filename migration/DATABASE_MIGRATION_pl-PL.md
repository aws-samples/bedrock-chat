# Przewodnik migracji bazy danych

> [!Warning]
> Ten przewodnik dotyczy migracji z v0 do v1.

Ten przewodnik przedstawia kroki niezbędne do migracji danych podczas aktualizacji Bedrock Chat, która zawiera wymianę klastra Aurora. Poniższa procedura zapewnia płynne przejście przy jednoczesnym zminimalizowaniu przestojów i utraty danych.

## Przegląd

Proces migracji obejmuje skanowanie wszystkich botów i uruchamianie zadań osadzania ECS dla każdego z nich. To podejście wymaga ponownego obliczenia osadzeń, co może być czasochłonne i generować dodatkowe koszty związane z wykonywaniem zadań ECS oraz opłatami za korzystanie z Bedrock Cohere. Jeśli wolisz uniknąć tych kosztów i wymagań czasowych, zapoznaj się z [alternatywnymi opcjami migracji](#alternative-migration-options) przedstawionymi w dalszej części tego przewodnika.

## Kroki migracji

- Po wykonaniu [npx cdk deploy](../README.md#deploy-using-cdk) z wymianą Aurora, otwórz skrypt [migrate_v0_v1.py](./migrate_v0_v1.py) i zaktualizuj następujące zmienne odpowiednimi wartościami. Wartości można znaleźć w zakładce `CloudFormation` > `BedrockChatStack` > `Outputs`.

```py
# Otwórz stos CloudFormation w konsoli AWS Management Console i skopiuj wartości z zakładki Outputs.
# Klucz: DatabaseConversationTableNameXXXX
TABLE_NAME = "BedrockChatStack-DatabaseConversationTableXXXXX"
# Klucz: EmbeddingClusterNameXXX
CLUSTER_NAME = "BedrockChatStack-EmbeddingClusterXXXXX"
# Klucz: EmbeddingTaskDefinitionNameXXX
TASK_DEFINITION_NAME = "BedrockChatStackEmbeddingTaskDefinitionXXXXX"
CONTAINER_NAME = "Container"  # Nie wymaga zmiany
# Klucz: PrivateSubnetId0
SUBNET_ID = "subnet-xxxxx"
# Klucz: EmbeddingTaskSecurityGroupIdXXX
SECURITY_GROUP_ID = "sg-xxxx"  # BedrockChatStack-EmbeddingTaskSecurityGroupXXXXX
```

- Uruchom skrypt `migrate_v0_v1.py`, aby rozpocząć proces migracji. Ten skrypt przeskanuje wszystkie boty, uruchomi zadania osadzania ECS i utworzy dane w nowym klastrze Aurora. Należy pamiętać, że:
  - Skrypt wymaga `boto3`.
  - Środowisko wymaga uprawnień IAM do dostępu do tabeli dynamodb i uruchamiania zadań ECS.

## Alternatywne Opcje Migracji

Jeśli wolisz nie korzystać z powyższej metody ze względu na związane z nią implikacje czasowe i kosztowe, rozważ następujące alternatywne podejścia:

### Przywracanie ze Snapshota i Migracja DMS

Najpierw zanotuj hasło dostępu do obecnego klastra Aurora. Następnie uruchom `npx cdk deploy`, co spowoduje wymianę klastra. Po tym utworzysz tymczasową bazę danych poprzez przywrócenie jej ze snapshota oryginalnej bazy danych.
Użyj [AWS Database Migration Service (DMS)](https://aws.amazon.com/dms/) do migracji danych z tymczasowej bazy danych do nowego klastra Aurora.

Uwaga: Na dzień 29 maja 2024 r., DMS nie obsługuje natywnie rozszerzenia pgvector. Możesz jednak rozważyć następujące opcje obejścia tego ograniczenia:

Użyj [migracji homogenicznej DMS](https://docs.aws.amazon.com/dms/latest/userguide/dm-migrating-data.html), która wykorzystuje natywną replikację logiczną. W tym przypadku zarówno źródłowa, jak i docelowa baza danych muszą być PostgreSQL. DMS może wykorzystać natywną replikację logiczną do tego celu.

Przy wyborze najbardziej odpowiedniego podejścia do migracji weź pod uwagę specyficzne wymagania i ograniczenia swojego projektu.