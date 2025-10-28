# Guía de Migración de Base de Datos

> [!Warning]
> Esta guía es para la migración de v0 a v1.

Esta guía describe los pasos para migrar datos cuando se realiza una actualización de Bedrock Chat que contiene un reemplazo del clúster Aurora. El siguiente procedimiento garantiza una transición fluida mientras minimiza el tiempo de inactividad y la pérdida de datos.

## Descripción general

El proceso de migración implica escanear todos los bots y lanzar tareas ECS de incrustación para cada uno de ellos. Este enfoque requiere el recálculo de las incrustaciones, lo que puede llevar tiempo y generar costos adicionales debido a las tarifas de ejecución de tareas ECS y el uso de Bedrock Cohere. Si prefiere evitar estos costos y requisitos de tiempo, consulte las [opciones alternativas de migración](#alternative-migration-options) que se proporcionan más adelante en esta guía.

## Pasos de Migración

- Después de [npx cdk deploy](../README.md#deploy-using-cdk) con el reemplazo de Aurora, abra el script [migrate_v0_v1.py](./migrate_v0_v1.py) y actualice las siguientes variables con los valores apropiados. Los valores se pueden consultar en la pestaña `CloudFormation` > `BedrockChatStack` > `Outputs`.

```py
# Abra la pila de CloudFormation en la Consola de Administración de AWS y copie los valores de la pestaña Outputs.
# Clave: DatabaseConversationTableNameXXXX
TABLE_NAME = "BedrockChatStack-DatabaseConversationTableXXXXX"
# Clave: EmbeddingClusterNameXXX
CLUSTER_NAME = "BedrockChatStack-EmbeddingClusterXXXXX"
# Clave: EmbeddingTaskDefinitionNameXXX
TASK_DEFINITION_NAME = "BedrockChatStackEmbeddingTaskDefinitionXXXXX"
CONTAINER_NAME = "Container"  # No necesita cambios
# Clave: PrivateSubnetId0
SUBNET_ID = "subnet-xxxxx"
# Clave: EmbeddingTaskSecurityGroupIdXXX
SECURITY_GROUP_ID = "sg-xxxx"  # BedrockChatStack-EmbeddingTaskSecurityGroupXXXXX
```

- Ejecute el script `migrate_v0_v1.py` para iniciar el proceso de migración. Este script escaneará todos los bots, lanzará tareas de embedding en ECS y creará los datos en el nuevo clúster de Aurora. Tenga en cuenta que:
  - El script requiere `boto3`.
  - El entorno requiere permisos IAM para acceder a la tabla de dynamodb y para invocar tareas de ECS.

## Opciones Alternativas de Migración

Si prefieres no utilizar el método anterior debido a las implicaciones de tiempo y coste asociadas, considera los siguientes enfoques alternativos:

### Restauración de Instantánea y Migración DMS

Primero, anota la contraseña para acceder al clúster Aurora actual. Luego ejecuta `npx cdk deploy`, lo que desencadena el reemplazo del clúster. Después, crea una base de datos temporal restaurando desde una instantánea de la base de datos original.
Utiliza [AWS Database Migration Service (DMS)](https://aws.amazon.com/dms/) para migrar datos desde la base de datos temporal al nuevo clúster Aurora.

Nota: A partir del 29 de mayo de 2024, DMS no admite de forma nativa la extensión pgvector. Sin embargo, puedes explorar las siguientes opciones para solucionar esta limitación:

Utiliza [migración homogénea DMS](https://docs.aws.amazon.com/dms/latest/userguide/dm-migrating-data.html), que aprovecha la replicación lógica nativa. En este caso, tanto la base de datos de origen como la de destino deben ser PostgreSQL. DMS puede aprovechar la replicación lógica nativa para este propósito.

Considera los requisitos específicos y las restricciones de tu proyecto al elegir el enfoque de migración más adecuado.