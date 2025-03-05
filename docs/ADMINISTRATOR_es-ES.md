# Características del administrador

Las características del administrador son una herramienta vital ya que proporciona información esencial sobre el uso de bots personalizados y el comportamiento de los usuarios. Sin esta funcionalidad, sería difícil para los administradores comprender qué bots personalizados son populares, por qué lo son y quiénes los están utilizando. Esta información es crucial para optimizar los mensajes de instrucción, personalizar las fuentes de datos RAG e identificar usuarios frecuentes que podrían convertirse en influenciadores.

## Bucle de retroalimentación

La salida de LLM puede no cumplir siempre con las expectativas del usuario. A veces no logra satisfacer sus necesidades. Para "integrar" efectivamente los LLM en operaciones comerciales y en la vida diaria, implementar un bucle de retroalimentación es esencial. Bedrock Claude Chat está equipado con una función de retroalimentación diseñada para permitir a los usuarios analizar por qué surgió la insatisfacción. Basándose en los resultados del análisis, los usuarios pueden ajustar los prompts, las fuentes de datos RAG y los parámetros en consecuencia.

![](./imgs/feedback_loop.png)

![](./imgs/feedback-using-claude-chat.png)

Los analistas de datos pueden acceder a los registros de conversación mediante [Amazon Athena](https://aws.amazon.com/jp/athena/). Si desean analizar los datos con [Jupyter Notebook](https://jupyter.org/), [este ejemplo de notebook](../examples/notebooks/feedback_analysis_example.ipynb) puede servir como referencia.

## Panel de administración

Actualmente proporciona una visión general básica del uso del chatbot y de los usuarios, centrándose en agregar datos para cada bot y usuario durante períodos de tiempo específicos y ordenando los resultados por tarifas de uso.

![](./imgs/admin_bot_analytics.png)

> [!Note]
> Los análisis de uso de usuarios próximamente estarán disponibles.

### Requisitos previos

El usuario administrador debe ser miembro del grupo llamado `Admin`, que se puede configurar a través de la consola de administración > Grupos de usuarios de Amazon Cognito o aws cli. Ten en cuenta que el ID del grupo de usuarios se puede consultar accediendo a CloudFormation > BedrockChatStack > Salidas > `AuthUserPoolIdxxxx`.

![](./imgs/group_membership_admin.png)

## Notas

- Como se indica en la [arquitectura](../README.md#architecture), las características de administración harán referencia al bucket de S3 exportado desde DynamoDB. Tenga en cuenta que, dado que la exportación se realiza una vez cada hora, las conversaciones más recientes pueden no reflejarse inmediatamente.

- En los usos públicos de bots, los bots que no se hayan utilizado durante el período especificado no se mostrarán.

- En los usos de usuarios, los usuarios que no hayan utilizado el sistema durante el período especificado no se mostrarán.

## Descargar datos de conversación

Puede consultar los registros de conversaciones mediante Athena, utilizando SQL. Para descargar los registros, abra el Editor de Consultas de Athena desde la consola de administración y ejecute SQL. A continuación, se presentan algunas consultas de ejemplo útiles para analizar casos de uso. La retroalimentación se puede consultar en el atributo `MessageMap`.

### Consulta por ID de Bot

Edite `bot-id` y `datehour`. El `bot-id` se puede encontrar en la pantalla de Administración de Bots, a la que se puede acceder desde las API de Publicación de Bots, que se muestra en la barra lateral izquierda. Tenga en cuenta la parte final de la URL como `https://xxxx.cloudfront.net/admin/bot/<bot-id>`.

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

### Consulta por ID de Usuario

Edite `user-id` y `datehour`. El `user-id` se puede encontrar en la pantalla de Administración de Bots.

> [!Nota]
> Los análisis de uso de usuario están próximamente disponibles.

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