# Publicación de API

## Descripción general

Esta muestra incluye una función para publicar APIs. Si bien una interfaz de chat puede ser conveniente para la validación preliminar, la implementación real depende del caso de uso específico y de la experiencia de usuario (UX) deseada para el usuario final. En algunos escenarios, una interfaz de chat puede ser la opción preferida, mientras que en otros, una API independiente podría ser más adecuada. Después de la validación inicial, esta muestra proporciona la capacidad de publicar bots personalizados según las necesidades del proyecto. Al introducir ajustes para cuotas, limitación de velocidad, orígenes, etc., se puede publicar un punto de conexión junto con una clave API, ofreciendo flexibilidad para diversas opciones de integración.

## Seguridad

El uso exclusivo de una clave API no es recomendable según se describe en: [AWS API Gateway Developer Guide](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-api-usage-plans.html). Por consiguiente, este ejemplo implementa una restricción simple de direcciones IP a través de AWS WAF. La regla WAF se aplica de manera común en toda la aplicación debido a consideraciones de costos, bajo la suposición de que las fuentes que se desearían restringir probablemente sean las mismas en todas las APIs emitidas. **Por favor, adhiérase a la política de seguridad de su organización para la implementación real.** Consulte también la sección [Architecture](#architecture).

## Cómo publicar una API de bot personalizada

### Requisitos previos

Por razones de gobernanza, solo usuarios limitados pueden publicar bots. Antes de publicar, el usuario debe ser miembro del grupo llamado `PublishAllowed`, que se puede configurar a través de la consola de administración > Amazon Cognito User pools o mediante aws cli. Ten en cuenta que el id del grupo de usuarios se puede consultar accediendo a CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`.

![](./imgs/group_membership_publish_allowed.png)

### Configuración de publicación de API

Después de iniciar sesión como usuario `PublishedAllowed` y crear un bot, selecciona `API PublishSettings`. Ten en cuenta que solo se puede publicar un bot compartido.
![](./imgs/bot_api_publish_screenshot.png)

En la siguiente pantalla, podemos configurar varios parámetros relacionados con la limitación de tráfico. Para más detalles, consulta también: [Throttle API requests for better throughput](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html).
![](./imgs/bot_api_publish_screenshot2.png)

Después del despliegue, aparecerá la siguiente pantalla donde podrás obtener la URL del endpoint y una clave de API. También podemos añadir y eliminar claves de API.

![](./imgs/bot_api_publish_screenshot3.png)

## Arquitectura

La API se publica según el siguiente diagrama:

![](./imgs/published_arch.png)

El WAF se utiliza para la restricción de direcciones IP. La dirección se puede configurar estableciendo los parámetros `publishedApiAllowedIpV4AddressRanges` y `publishedApiAllowedIpV6AddressRanges` en `cdk.json`.

Cuando un usuario hace clic en publicar el bot, [AWS CodeBuild](https://aws.amazon.com/codebuild/) inicia una tarea de despliegue CDK para aprovisionar el stack de la API (Ver también: [Definición CDK](../cdk/lib/api-publishment-stack.ts)) que contiene API Gateway, Lambda y SQS. SQS se utiliza para desacoplar la solicitud del usuario y la operación del LLM ya que la generación de salida puede exceder los 30 segundos, que es el límite de la cuota de API Gateway. Para obtener la salida, es necesario acceder a la API de forma asíncrona. Para más detalles, consulte [Especificación de la API](#api-specification).

El cliente necesita establecer `x-api-key` en el encabezado de la solicitud.

## Especificación de la API

Ver [aquí](https://aws-samples.github.io/bedrock-chat).