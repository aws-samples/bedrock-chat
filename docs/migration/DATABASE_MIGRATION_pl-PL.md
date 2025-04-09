# Przewodnik po Migracji Bazy Danych

> [!Warning]
> Ten przewodnik dotyczy migracji z wersji 0 do wersji 1.

Ten przewodnik opisuje kroki migracji danych podczas aktualizacji Bedrock Chat, która obejmuje wymianę klastra Aurora. Poniższa procedura zapewnia płynne przejście przy minimalnym czasie przestoju i ryzyku utraty danych.

## Przegląd

Proces migracji polega na przeskanowaniu wszystkich botów i uruchomieniu zadań ECS osadzania dla każdego z nich. To podejście wymaga ponownego obliczenia osadzeń, co może być czasochłonne i wiązać się z dodatkowymi kosztami ze względu na wykonanie zadań ECS oraz opłaty za usługę Bedrock Cohere. Jeśli wolisz uniknąć tych kosztów i wymagań czasowych, zapoznaj się z [alternatywnymi opcjami migracji](#alternative-migration-options) przedstawionymi w dalszej części tego przewodnika.

## Kroki migracji

- Po wykonaniu polecenia [npx cdk deploy](../README.md#deploy-using-cdk) z zastąpieniem Aurora, otwórz skrypt [migrate_v0_v1.py](./migrate_v0_v1.py) i zaktualizuj następujące zmienne odpowiednimi wartościami. Wartości można znaleźć w zakładce `CloudFormation` > `BedrockChatStack` > `Outputs`.

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

- Uruchom skrypt `migrate_v0_v1.py`, aby zainicjować proces migracji. Ten skrypt przeskanuje wszystkie boty, uruchomi zadania osadzania ECS i utworzy dane w nowym klastrze Aurora. Należy pamiętać, że:
  - Skrypt wymaga `boto3`.
  - Środowisko wymaga uprawnień IAM do dostępu do tabeli dynamodb i wywoływania zadań ECS.

## Alternatywne opcje migracji

Jeśli wolisz nie korzystać z powyższej metody ze względu na związane z nią implikacje czasowe i kosztowe, rozważ następujące alternatywne podejścia:

### Przywracanie migawki i migracja DMS

Najpierw zanotuj hasło dostępu do bieżącego klastra Aurora. Następnie uruchom `npx cdk deploy`, co spowoduje zastąpienie klastra. Potem utwórz tymczasową bazę danych, przywracając ją z migawki oryginalnej bazy danych.
Użyj [AWS Database Migration Service (DMS)](https://aws.amazon.com/dms/), aby przeprowadzić migrację danych z tymczasowej bazy danych do nowego klastra Aurora.

Uwaga: Według stanu na 29 maja 2024 roku, DMS nie obsługuje natywnie rozszerzenia pgvector. Można jednak rozważyć następujące opcje obejścia tego ograniczenia:

Użyj [migracji jednorodnej DMS](https://docs.aws.amazon.com/dms/latest/userguide/dm-migrating-data.html), która wykorzystuje natywną replikację logiczną. W tym przypadku zarówno źródłowa, jak i docelowa baza danych muszą być bazami PostgreSQL. DMS może wykorzystać natywną replikację logiczną do tego celu.

Rozważ konkretne wymagania i ograniczenia Twojego projektu przy wyborze najbardziej odpowiedniego podejścia migracyjnego.