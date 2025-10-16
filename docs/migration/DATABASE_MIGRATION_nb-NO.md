# Database-migreringsveiledning

> [!Warning]
> Denne veiledningen er for v0 til v1.

Denne veiledningen beskriver trinnene for å migrere data når du utfører en oppdatering av Bedrock Chat som inneholder en Aurora-klusterutskiftning. Følgende prosedyre sikrer en smidig overgang samtidig som nedetid og datatap minimeres.

## Oversikt

Migrasjonsprosessen innebærer skanning av alle boter og oppstart av innleggings-ECS-oppgaver for hver av dem. Denne tilnærmingen krever ny beregning av innlegginger, noe som kan være tidkrevende og medføre ekstra kostnader på grunn av ECS-oppgaveutførelse og Bedrock Cohere-bruksavgifter. Hvis du foretrekker å unngå disse kostnadene og tidsbruken, vennligst se [alternative migrasjonsalternativer](#alternative-migration-options) som er beskrevet senere i denne veiledningen.

## Migreringstrinn

- Etter [npx cdk deploy](../README.md#deploy-using-cdk) med Aurora-erstatning, åpne [migrate_v0_v1.py](./migrate_v0_v1.py) skriptet og oppdater følgende variabler med passende verdier. Verdiene kan finnes under `CloudFormation` > `BedrockChatStack` > `Outputs`-fanen.

```py
# Åpne CloudFormation-stacken i AWS Management Console og kopier verdiene fra Outputs-fanen.
# Nøkkel: DatabaseConversationTableNameXXXX
TABLE_NAME = "BedrockChatStack-DatabaseConversationTableXXXXX"
# Nøkkel: EmbeddingClusterNameXXX
CLUSTER_NAME = "BedrockChatStack-EmbeddingClusterXXXXX"
# Nøkkel: EmbeddingTaskDefinitionNameXXX
TASK_DEFINITION_NAME = "BedrockChatStackEmbeddingTaskDefinitionXXXXX"
CONTAINER_NAME = "Container"  # Trenger ikke å endres
# Nøkkel: PrivateSubnetId0
SUBNET_ID = "subnet-xxxxx"
# Nøkkel: EmbeddingTaskSecurityGroupIdXXX
SECURITY_GROUP_ID = "sg-xxxx"  # BedrockChatStack-EmbeddingTaskSecurityGroupXXXXX
```

- Kjør `migrate_v0_v1.py` skriptet for å starte migreringsprosessen. Dette skriptet vil skanne alle boter, starte embedding ECS-oppgaver, og opprette dataene i den nye Aurora-clusteren. Merk at:
  - Skriptet krever `boto3`.
  - Miljøet krever IAM-tillatelser for å få tilgang til dynamodb-tabellen og for å starte ECS-oppgaver.

## Alternative migrasjonsalternativer

Hvis du foretrekker å ikke bruke metoden ovenfor på grunn av tids- og kostnadsimplikasjonene, vurder følgende alternative tilnærminger:

### Snapshot-gjenoppretting og DMS-migrasjon

Først, noter passordet for å få tilgang til gjeldende Aurora-cluster. Kjør deretter `npx cdk deploy`, som utløser utskifting av clusteret. Etter det, opprett en midlertidig database ved å gjenopprette fra et snapshot av den originale databasen.
Bruk [AWS Database Migration Service (DMS)](https://aws.amazon.com/dms/) for å migrere data fra den midlertidige databasen til det nye Aurora-clusteret.

Merk: Per 29. mai 2024 støtter ikke DMS pgvector-utvidelsen direkte. Du kan imidlertid utforske følgende alternativer for å omgå denne begrensningen:

Bruk [DMS homogen migrasjon](https://docs.aws.amazon.com/dms/latest/userguide/dm-migrating-data.html), som utnytter innebygd logisk replikering. I dette tilfellet må både kilde- og måldatabasene være PostgreSQL. DMS kan utnytte innebygd logisk replikering for dette formålet.

Vurder de spesifikke kravene og begrensningene i prosjektet ditt når du velger den mest egnede migrasjonstilnærmingen.