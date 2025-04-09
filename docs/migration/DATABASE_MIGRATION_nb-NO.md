# Veiledning for databasemigrering

> [!Advarsel]
> Denne veiledningen gjelder for v0 til v1.

Denne veiledningen beskriver trinnene for å migrere data ved oppdatering av Bedrock Chat som inneholder erstatning av en Aurora-klynge. Følgende prosedyre sikrer en smidig overgang med minimal nedetid og datatap.

## Oversikt

Migrasjonsprosessen innebærer å skanne alle bots og starte ECS-oppgaver for innbygging for hver av dem. Denne tilnærmingen krever omberegning av innbygging, noe som kan være tidkrevende og medføre ekstra kostnader på grunn av ECS-oppgavekjøring og Bedrock Cohere-bruksgebyrer. Hvis du ønsker å unngå disse kostnadene og tidsbehovene, kan du se nærmere på de [alternative migrasjonsalternativene](#alternative-migrasjonsmuligheter) som er beskrevet senere i denne veiledningen.

## Migrasjonstrinn

- Etter [npx cdk deploy](../README.md#deploy-using-cdk) med Aurora-erstatning, åpne [migrate_v0_v1.py](./migrate_v0_v1.py)-skriptet og oppdater følgende variabler med egnede verdier. Verdiene kan refereres fra `CloudFormation` > `BedrockChatStack` > fanen `Outputs`.

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

- Kjør `migrate_v0_v1.py`-skriptet for å starte migrasjonsprosessen. Dette skriptet vil søke gjennom alle bots, starte embedding ECS-oppgaver og opprette data i den nye Aurora-clusteren. Merk at:
  - Skriptet krever `boto3`.
  - Miljøet krever IAM-tillatelser for å få tilgang til DynamoDB-tabellen og for å starte ECS-oppgaver.

## Alternative migreringsalternativer

Hvis du foretrekker å ikke bruke metoden over på grunn av tilhørende tids- og kostnadsimplikasjoner, kan du vurdere følgende alternative tilnærminger:

### Snapshot-gjenoppretting og DMS-migrering

Merk først passordet for å få tilgang til gjeldende Aurora-klynge. Kjør deretter `npx cdk deploy`, som utløser erstatning av klyngen. Etterpå oppretter du en midlertidig database ved å gjenopprette fra en øyeblikksbilde av den opprinnelige databasen.
Bruk [AWS Database Migration Service (DMS)](https://aws.amazon.com/dms/) til å migrere data fra den midlertidige databasen til den nye Aurora-klyngen.

Merk: Per 29. mai 2024 støtter ikke DMS pgvector-utvidelsen nativt. Du kan imidlertid utforske følgende alternativer for å omgå denne begrensningen:

Bruk [DMS homogen migrering](https://docs.aws.amazon.com/dms/latest/userguide/dm-migrating-data.html), som benytter innebygd logisk replikering. I dette tilfellet må både kilde- og måldatabasene være PostgreSQL. DMS kan utnytte innebygd logisk replikering for dette formålet.

Vurder de spesifikke kravene og begrensningene i prosjektet ditt når du velger den mest egnede migreringstilnærmingen.