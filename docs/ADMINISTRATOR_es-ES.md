# Funcionalidades de administración

Las funcionalidades de administración son una herramienta vital ya que proporciona información esencial sobre el uso de bots personalizados y el comportamiento de los usuarios. Sin esta funcionalidad, sería difícil para los administradores comprender qué bots personalizados son populares, por qué lo son y quiénes los están utilizando. Esta información es crucial para optimizar los mensajes de instrucciones, personalizar las fuentes de datos RAG e identificar usuarios intensivos que podrían convertirse en influenciadores.

## Bucle de retroalimentación

La salida de LLM puede no cumplir siempre con las expectativas del usuario. A veces no logra satisfacer sus necesidades. Para "integrar" efectivamente los LLM en operaciones comerciales y la vida cotidiana, implementar un bucle de retroalimentación es esencial. Bedrock Claude Chat está equipado con una función de retroalimentación diseñada para permitir a los usuarios analizar por qué surgió la insatisfacción. Basándose en los resultados del análisis, los usuarios pueden ajustar los avisos, las fuentes de datos RAG y los parámetros en consecuencia.

![](./imgs/feedback_loop.png)

![](./imgs/feedback-using-claude-chat.png)

Los analistas de datos pueden acceder a los registros de conversación utilizando [Amazon Athena](https://aws.amazon.com/jp/athena/). Si desean analizar los datos en [Jupyter Notebook](https://jupyter.org/), [este ejemplo de notebook](../examples/notebooks/feedback_analysis_example.ipynb) puede ser una referencia.

## Panel de administración

Actualmente proporciona una visión general básica del uso del chatbot y de los usuarios, centrándose en agregar datos para cada bot y usuario durante períodos de tiempo específicos y ordenando los resultados por tarifas de uso.

![](./imgs/admin_bot_analytics.png)

> [!Note]
> Las analíticas de uso de usuarios próximamente estarán disponibles.

### Requisitos previos

El usuario administrador debe ser miembro de un grupo llamado `Admin`, que se puede configurar a través de la consola de administración > Amazon Cognito User pools o aws cli. Tenga en cuenta que el ID del grupo de usuarios se puede consultar accediendo a CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`.

![](./imgs/group_membership_admin.png)

## Notas

- Como se indica en la [arquitectura](../README.md#architecture), las funciones de administración harán referencia al bucket de S3 exportado desde DynamoDB. Tenga en cuenta que, dado que la exportación se realiza cada hora, es posible que las conversaciones más recientes no se reflejen inmediatamente.

- En los usos públicos de bots, los bots que no se hayan utilizado durante el período especificado no se mostrarán.

- En los usos de usuarios, los usuarios que no hayan utilizado el sistema durante el período especificado no se mostrarán.

> [!Importante] > **Nombres de Bases de Datos Multi-Entorno**
>
> Si está utilizando varios entornos (desarrollo, producción, etc.), el nombre de la base de datos de Athena incluirá el prefijo del entorno. En lugar de `bedrockchatstack_usage_analysis`, el nombre de la base de datos será:
>
> - Para entorno predeterminado: `bedrockchatstack_usage_analysis`
> - Para entornos con nombre: `<prefijo-entorno>_bedrockchatstack_usage_analysis` (por ejemplo, `dev_bedrockchatstack_usage_analysis`)
>
> Además, el nombre de la tabla incluirá el prefijo del entorno:
>
> - Para entorno predeterminado: `ddb_export`
> - Para entornos con nombre: `<prefijo-entorno>_ddb_export` (por ejemplo, `dev_ddb_export`)
>
> Asegúrese de ajustar sus consultas en consecuencia al trabajar con múltiples entornos.

## Descargar datos de conversación

Puede consultar los registros de conversaciones mediante Athena, utilizando SQL. Para descargar los registros, abra el Editor de Consultas de Athena desde la consola de administración y ejecute SQL. A continuación, se presentan algunos ejemplos de consultas útiles para analizar casos de uso. Los comentarios pueden consultarse en el atributo `MessageMap`.

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
> Si está utilizando un entorno con nombre (por ejemplo, "dev"), reemplace `bedrockchatstack_usage_analysis.ddb_export` por `dev_bedrockchatstack_usage_analysis.dev_ddb_export` en la consulta anterior.

### Consulta por ID de Usuario

Edite `user-id` y `datehour`. El `user-id` se puede consultar en la pantalla de Administración de Bots.

> [!Nota]
> Los análisis de uso de usuarios están próximamente.

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
> Si está utilizando un entorno con nombre (por ejemplo, "dev"), reemplace `bedrockchatstack_usage_analysis.ddb_export` por `dev_bedrockchatstack_usage_analysis.dev_ddb_export` en la consulta anterior.