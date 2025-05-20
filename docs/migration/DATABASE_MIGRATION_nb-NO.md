# Veiledning for databasemigrering

> [!Advarsel]
> Denne veiledningen gjelder for v0 til v1.

Denne veiledningen beskriver trinnene for å migrere data ved oppdatering av Bedrock Chat som inneholder utskifting av en Aurora-klynge. Følgende prosedyre sikrer en smidig overgang mens nedetid og datatap minimeres.

## Oversikt

Migrasjonsprosessen innebærer scanning av alle bots og igangsetting av innlemmings-ECS-oppgaver for hver av dem. Denne tilnærmingen krever ny beregning av innlemminger, noe som kan være tidkrevende og medføre ekstra kostnader på grunn av ECS-oppgavekjøring og Bedrock Cohere-bruksgebyrer. Hvis du foretrekker å unngå disse kostnadene og tidsbehovene, kan du se nærmere på de [alternative migreringsalternativene](#alternative-migration-options) som presenteres senere i denne veiledningen.

## Migrasjonstrinn

- Etter [npx cdk deploy](../README.md#deploy-using-cdk) med Aurora-erstatning, åpne [migrate_v0_v1.py](./migrate_v0_v1.py)-skriptet og oppdater følgende variabler med de aktuelle verdiene. Verdiene kan refereres fra `CloudFormation` > `BedrockChatStack` > `Outputs`-fanen.

```py
# Åpne CloudFormation-stacken i AWS Management Console og kopier verdiene fra Outputs-fanen.
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

- Kjør `migrate_v0_v1.py`-skriptet for å starte migrasjonsprosessen. Dette skriptet vil søke gjennom alle bots, starte embedding ECS-oppgaver og opprette data i den nye Aurora-clusteren. Merk at:
  - Skriptet krever `boto3`.
  - Miljøet krever IAM-tillatelser for å få tilgang til dynamodb-tabellen og for å starte ECS-oppgaver.

## Alternative migreringsalternativer

Hvis du foretrekker å ikke bruke metoden nevnt ovenfor på grunn av tilhørende tids- og kostnadsimplikasjoner, kan du vurdere følgende alternative tilnærminger:

### Snapshot-gjenoppretting og DMS-migrering

Først, noter passordet for å få tilgang til gjeldende Aurora-klynge. Deretter kjør `npx cdk deploy`, som utløser erstatning av klyngen. Etterpå oppretter du en midlertidig database ved å gjenopprette fra en øyeblikksbilde av den opprinnelige databasen.
Bruk [AWS Database Migration Service (DMS)](https://aws.amazon.com/dms/) for å migrere data fra den midlertidige databasen til den nye Aurora-klyngen.

Merk: Per 29. mai 2024 støtter ikke DMS pgvector-utvidelsen naturlig. Du kan imidlertid utforske følgende alternativer for å omgå denne begrensningen:

Bruk [DMS homogen migrering](https://docs.aws.amazon.com/dms/latest/userguide/dm-migrating-data.html), som benytter innebygd logisk replikering. I dette tilfellet må både kilde- og måldatabasene være PostgreSQL. DMS kan utnytte innebygd logisk replikering for dette formålet.

Vurder de spesifikke kravene og begrensningene i prosjektet ditt når du velger den mest egnede migreringstilnærmingen.