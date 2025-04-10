# Características administrativas

## Requisitos previos

El usuario administrador debe ser miembro de un grupo llamado `Admin`, que se puede configurar a través de la consola de administración > Amazon Cognito User pools o la aws cli. Ten en cuenta que el ID del grupo de usuarios se puede consultar accediendo a CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`.

![](./imgs/group_membership_admin.png)

## Marcar bots públicos como Esenciales

Los bots públicos ahora pueden ser marcados como "Esenciales" por los administradores. Los bots marcados como Esenciales se mostrarán en la sección "Esenciales" de la tienda de bots, lo que los hace fácilmente accesibles para los usuarios. Esto permite a los administradores destacar bots importantes que desean que todos los usuarios utilicen.

### Ejemplos

- Bot de Asistente de RRHH: Ayuda a los empleados con preguntas y tareas relacionadas con recursos humanos.
- Bot de Soporte de TI: Proporciona asistencia para problemas técnicos internos y gestión de cuentas.
- Bot de Guía de Políticas Internas: Responde preguntas frecuentes sobre reglas de asistencia, políticas de seguridad y otros reglamentos internos.
- Bot de Incorporación de Nuevos Empleados: Guía a los nuevos empleados a través de procedimientos y uso de sistemas en su primer día.
- Bot de Información de Beneficios: Explica los programas de beneficios de la empresa y servicios de bienestar.

![](./imgs/admin_bot_menue.png)
![](./imgs/bot_store.png)

## Ciclo de retroalimentación

La salida de LLM puede no cumplir siempre con las expectativas del usuario. A veces no logra satisfacer sus necesidades. Para "integrar" eficazmente los LLM en operaciones comerciales y la vida cotidiana, implementar un ciclo de retroalimentación es esencial. Bedrock Chat está equipado con una función de retroalimentación diseñada para permitir a los usuarios analizar por qué surgió la insatisfacción. Basándose en los resultados del análisis, los usuarios pueden ajustar los prompts, las fuentes de datos RAG y los parámetros en consecuencia.

![](./imgs/feedback_loop.png)

![](./imgs/feedback-using-claude-chat.png)

Los analistas de datos pueden acceder a los registros de conversación mediante [Amazon Athena](https://aws.amazon.com/jp/athena/). Si desean analizar los datos en [Jupyter Notebook](https://jupyter.org/), [este ejemplo de cuaderno](../examples/notebooks/feedback_analysis_example.ipynb) puede servir como referencia.

## Panel de Control

Actualmente proporciona una descripción general básica del uso de chatbots y usuarios, centrándose en agregar datos para cada bot y usuario en períodos de tiempo específicos y ordenando los resultados por tarifas de uso.

![](./imgs/admin_bot_analytics.png)

## Notas

- Como se indica en la [arquitectura](../README.md#architecture), las funciones de administración harán referencia al bucket de S3 exportado desde DynamoDB. Tenga en cuenta que, dado que la exportación se realiza cada hora, es posible que las conversaciones más recientes no se reflejen inmediatamente.

- En usos públicos de bots, los bots que no se hayan utilizado durante el período especificado no se mostrarán.

- En usos de usuarios, los usuarios que no hayan utilizado el sistema durante el período especificado no se mostrarán.

> [!Importante]
> Si está utilizando varios entornos (desarrollo, producción, etc.), el nombre de la base de datos de Athena incluirá el prefijo del entorno. En lugar de `bedrockchatstack_usage_analysis`, el nombre de la base de datos será:
>
> - Para el entorno predeterminado: `bedrockchatstack_usage_analysis`
> - Para entornos con nombre: `<prefijo-entorno>_bedrockchatstack_usage_analysis` (por ejemplo, `dev_bedrockchatstack_usage_analysis`)
>
> Además, el nombre de la tabla incluirá el prefijo del entorno:
>
> - Para el entorno predeterminado: `ddb_export`
> - Para entornos con nombre: `<prefijo-entorno>_ddb_export` (por ejemplo, `dev_ddb_export`)
>
> Asegúrese de ajustar sus consultas en consecuencia al trabajar con varios entornos.

## Descargar datos de conversación

Puede consultar los registros de conversaciones mediante Athena, utilizando SQL. Para descargar los registros, abra el Editor de Consultas de Athena desde la consola de administración y ejecute SQL. A continuación, se muestran algunos ejemplos de consultas útiles para analizar casos de uso. La retroalimentación se puede consultar en el atributo `MessageMap`.

### Consulta por ID de Bot

Edite `bot-id` y `datehour`. El `bot-id` se puede consultar en la pantalla de Administración de Bots, a la que se puede acceder desde las API de Publicación de Bots, que se muestra en la barra lateral izquierda. Tenga en cuenta la parte final de la URL, como `https://xxxx.cloudfront.net/admin/bot/<bot-id>`.

```sql
SELECT
    d.newimage.PK.S AS UserId,
    d.newimage.SK.S AS ConversationId,
    d.newimage.MessageMap.S AS MessageMap,
    d.newimage.TotalPrice.N AS TotalPrice,
    d.newimage.CreateTime.N AS CreateTime,
    d.newimage.LastMessageId.S AS LastMessageId,
    d.newimage.BotId.S AS BotId,
    d.datehour AS DateHour
FROM
    bedrockchatstack_usage_analysis.ddb_export d
WHERE
    d.newimage.BotId.S = '<bot-id>'
    AND d.datehour BETWEEN '<yyyy/mm/dd/hh>' AND '<yyyy/mm/dd/hh>'
    AND d.Keys.SK.S LIKE CONCAT(d.Keys.PK.S, '#CONV#%')
ORDER BY
    d.datehour DESC;
```

> [!Nota]
> Si está utilizando un entorno con nombre (por ejemplo, "dev"), reemplace `bedrockchatstack_usage_analysis.ddb_export` con `dev_bedrockchatstack_usage_analysis.dev_ddb_export` en la consulta anterior.

### Consulta por ID de Usuario

Edite `user-id` y `datehour`. El `user-id` se puede consultar en la pantalla de Administración de Bots.

> [!Nota]
> Los análisis de uso de usuarios próximamente.

```sql
SELECT
    d.newimage.PK.S AS UserId,
    d.newimage.SK.S AS ConversationId,
    d.newimage.MessageMap.S AS MessageMap,
    d.newimage.TotalPrice.N AS TotalPrice,
    d.newimage.CreateTime.N AS CreateTime,
    d.newimage.LastMessageId.S AS LastMessageId,
    d.newimage.BotId.S AS BotId,
    d.datehour AS DateHour
FROM
    bedrockchatstack_usage_analysis.ddb_export d
WHERE
    d.newimage.PK.S = '<user-id>'
    AND d.datehour BETWEEN '<yyyy/mm/dd/hh>' AND '<yyyy/mm/dd/hh>'
    AND d.Keys.SK.S LIKE CONCAT(d.Keys.PK.S, '#CONV#%')
ORDER BY
    d.datehour DESC;
```

> [!Nota]
> Si está utilizando un entorno con nombre (por ejemplo, "dev"), reemplace `bedrockchatstack_usage_analysis.ddb_export` con `dev_bedrockchatstack_usage_analysis.dev_ddb_export` en la consulta anterior.