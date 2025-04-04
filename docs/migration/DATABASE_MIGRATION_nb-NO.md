# Database Migration Guide

Denne veiledningen beskriver trinnene for å migrere data når du utfører en oppdatering av Bedrock Claude Chat som inneholder en erstatning av Aurora-klyngen. Følgende prosedyre sikrer en smidig overgang med minimalt med nedetid og datatap.

## Oversikt

Migrasjonsprosessen innebærer å skanne alle bots og starte ECS-oppgaver for innbygging for hver av dem. Denne tilnærmingen krever ny beregning av innbygginger, noe som kan være tidkrevende og medføre ekstra kostnader på grunn av ECS-oppgavekjøring og bruksgebyrer for Bedrock Cohere. Hvis du ønsker å unngå disse kostnadene og tidsbehovene, kan du se de [alternative migreringsalternativene](#alternative-migration-options) som er beskrevet senere i denne veiledningen.

## Migrasjonstrinn

- Etter [npx cdk deploy](../README.md#deploy-using-cdk) med Aurora-erstatning, åpne [migrate.py](./migrate.py)-skriptet og oppdater følgende variabler med riktige verdier. Verdiene kan refereres fra `CloudFormation` > `BedrockChatStack` > `Outputs`-fanen.

```py
# Åpne CloudFormation-stakken i AWS Management Console og kopier verdiene fra Outputs-fanen.
# Nøkkel: DatabaseConversationTableNameXXXX
TABLE_NAME = "BedrockChatStack-DatabaseConversationTableXXXXX"
# Nøkkel: EmbeddingClusterNameXXX
CLUSTER_NAME = "BedrockChatStack-EmbeddingClusterXXXXX"
# Nøkkel: EmbeddingTaskDefinitionNameXXX
TASK_DEFINITION_NAME = "BedrockChatStackEmbeddingTaskDefinitionXXXXX"
CONTAINER_NAME = "Container"  # Ikke nødvendig å endre
# Nøkkel: PrivateSubnetId0
SUBNET_ID = "subnet-xxxxx"
# Nøkkel: EmbeddingTaskSecurityGroupIdXXX
SECURITY_GROUP_ID = "sg-xxxx"  # BedrockChatStack-EmbeddingTaskSecurityGroupXXXXX
```

- Kjør `migrate.py`-skriptet for å starte migrasjonsprosessen. Dette skriptet vil søke gjennom alle bots, starte embedding ECS-oppgaver og opprette data i den nye Aurora-clusteren. Merk at:
  - Skriptet krever `boto3`.
  - Miljøet krever IAM-tillatelser for å få tilgang til dynamodb-tabellen og for å starte ECS-oppgaver.

## Alternative migreringsalternativer

Hvis du foretrekker å ikke bruke metoden over på grunn av tilhørende tids- og kostnadsimplikasjoner, kan du vurdere følgende alternative tilnærminger:

### Snapshot-gjenoppretting og DMS-migrering

Først noter passordet for å få tilgang til gjeldende Aurora-klynge. Kjør så `npx cdk deploy`, som utløser erstatning av klyngen. Deretter oppretter du en midlertidig database ved å gjenopprette fra en øyeblikksbilde av originalbasen.
Bruk [AWS Database Migration Service (DMS)](https://aws.amazon.com/dms/) til å migrere data fra den midlertidige databasen til den nye Aurora-klyngen.

Merk: Per 29. mai 2024 støtter ikke DMS pgvector-utvidelsen native. Du kan imidlertid utforske følgende alternativer for å omgå denne begrensningen:

Bruk [DMS homogen migrering](https://docs.aws.amazon.com/dms/latest/userguide/dm-migrating-data.html), som benytter native logisk replikering. I dette tilfellet må både kilde- og måldatabasene være PostgreSQL. DMS kan utnytte native logisk replikering for dette formålet.

Vurder de spesifikke kravene og begrensningene i prosjektet ditt når du velger den mest egnede migreringstilnærmingen.