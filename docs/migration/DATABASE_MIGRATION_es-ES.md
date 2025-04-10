# Guía de Migración de Base de Datos

> [!Warning]
> Esta guía es para la migración de v0 a v1.

Esta guía describe los pasos para migrar datos al realizar una actualización de Bedrock Chat que incluye el reemplazo de un clúster de Aurora. El siguiente procedimiento garantiza una transición fluida minimizando el tiempo de inactividad y la pérdida de datos.

## Descripción general

El proceso de migración implica escanear todos los bots e iniciar tareas de ECS de incrustación para cada uno de ellos. Este enfoque requiere un recálculo de las incrustaciones, lo que puede ser consumidor de tiempo e incurrir en costos adicionales debido a la ejecución de tareas de ECS y las tareas de uso de Bedrock Cohere. Si prefiere evitar estos costos y requisitos de tiempo, consulte las [opciones de migración alternativas](#alternative-migration-options) proporcionadas más adelante en esta guía.

## Pasos de Migración

- Después de [npx cdk deploy](../README.md#deploy-using-cdk) con reemplazo de Aurora, abra el script [migrate_v0_v1.py](./migrate_v0_v1.py) y actualice las siguientes variables con los valores apropiados. Los valores se pueden consultar en la pestaña `CloudFormation` > `BedrockChatStack` > `Outputs`.

```py
# Abra el stack de CloudFormation en la Consola de Administración de AWS y copie los valores de la pestaña Outputs.
# Clave: DatabaseConversationTableNameXXXX
TABLE_NAME = "BedrockChatStack-DatabaseConversationTableXXXXX"
# Clave: EmbeddingClusterNameXXX
CLUSTER_NAME = "BedrockChatStack-EmbeddingClusterXXXXX"
# Clave: EmbeddingTaskDefinitionNameXXX
TASK_DEFINITION_NAME = "BedrockChatStackEmbeddingTaskDefinitionXXXXX"
CONTAINER_NAME = "Container"  # No es necesario cambiar
# Clave: PrivateSubnetId0
SUBNET_ID = "subnet-xxxxx"
# Clave: EmbeddingTaskSecurityGroupIdXXX
SECURITY_GROUP_ID = "sg-xxxx"  # BedrockChatStack-EmbeddingTaskSecurityGroupXXXXX
```

- Ejecute el script `migrate_v0_v1.py` para iniciar el proceso de migración. Este script escaneará todos los bots, iniciará tareas de incrustación de ECS y creará los datos en el nuevo clúster de Aurora. Tenga en cuenta que:
  - El script requiere `boto3`.
  - El entorno requiere permisos de IAM para acceder a la tabla de DynamoDB e invocar tareas de ECS.

## Opciones Alternativas de Migración

Si prefiere no utilizar el método anterior debido a las implicaciones de tiempo y costo, considere los siguientes enfoques alternativos:

### Restauración de Snapshot y Migración con DMS

Primero, anote la contraseña para acceder al clúster de Aurora actual. Luego ejecute `npx cdk deploy`, lo que desencadena el reemplazo del clúster. Después de eso, cree una base de datos temporal restaurándola desde un snapshot de la base de datos original.
Utilice [AWS Database Migration Service (DMS)](https://aws.amazon.com/dms/) para migrar datos desde la base de datos temporal al nuevo clúster de Aurora.

Nota: A partir del 29 de mayo de 2024, DMS no es compatible de forma nativa con la extensión pgvector. Sin embargo, puede explorar las siguientes opciones para solucionar esta limitación:

Utilice [migración homogénea de DMS](https://docs.aws.amazon.com/dms/latest/userguide/dm-migrating-data.html), que aprovecha la replicación lógica nativa. En este caso, tanto la base de datos de origen como la de destino deben ser PostgreSQL. DMS puede aprovechar la replicación lógica nativa para este propósito.

Considere los requisitos y restricciones específicos de su proyecto al elegir el enfoque de migración más adecuado.