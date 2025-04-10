# Publicación de API

## Descripción general

Este ejemplo incluye una característica para publicar APIs. Aunque una interfaz de chat puede ser conveniente para una validación preliminar, la implementación real depende del caso de uso específico y la experiencia de usuario (UX) deseada para el usuario final. En algunos escenarios, una interfaz de chat puede ser la opción preferida, mientras que en otros, una API independiente puede ser más adecuada. Después de la validación inicial, este ejemplo proporciona la capacidad de publicar bots personalizados según las necesidades del proyecto. Al introducir configuraciones para cuotas, limitación de tráfico, orígenes, etc., se puede publicar un punto de enlace junto con una clave de API, ofreciendo flexibilidad para diversas opciones de integración.

## Seguridad

No se recomienda utilizar solo una clave API, como se describe en: [Guía de desarrollador de AWS API Gateway](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-api-usage-plans.html). En consecuencia, este ejemplo implementa una restricción simple de dirección IP a través de AWS WAF. La regla de WAF se aplica comúnmente en toda la aplicación debido a consideraciones de costos, bajo el supuesto de que las fuentes que se desearían restringir probablemente sean las mismas en todas las API emitidas. **Por favor, adhiérase a la política de seguridad de su organización para la implementación real.** Consulte también la sección [Arquitectura](#arquitectura).

## Cómo publicar la API de un bot personalizado

### Requisitos previos

Por razones de gobernanza, solo algunos usuarios limitados pueden publicar bots. Antes de publicar, el usuario debe ser miembro del grupo llamado `PublishAllowed`, que se puede configurar a través de la consola de administración > Amazon Cognito User pools o aws cli. Tenga en cuenta que el ID del grupo de usuarios se puede consultar accediendo a CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`.

![](./imgs/group_membership_publish_allowed.png)

### Configuración de publicación de API

Después de iniciar sesión como usuario `PublishedAllowed` y crear un bot, elija `API PublishSettings`. Tenga en cuenta que solo se puede publicar un bot compartido.
![](./imgs/bot_api_publish_screenshot.png)

En la siguiente pantalla, podemos configurar varios parámetros relacionados con la limitación de solicitudes. Para más detalles, consulte también: [Limitar las solicitudes de API para mejorar el rendimiento](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html).
![](./imgs/bot_api_publish_screenshot2.png)

Después del despliegue, aparecerá la siguiente pantalla donde podrá obtener la URL del punto de enlace y una clave de API. También podemos agregar y eliminar claves de API.

![](./imgs/bot_api_publish_screenshot3.png)

## Arquitectura

La API se publica según el siguiente diagrama:

![](./imgs/published_arch.png)

El WAF se utiliza para la restricción de direcciones IP. La dirección puede configurarse estableciendo los parámetros `publishedApiAllowedIpV4AddressRanges` y `publishedApiAllowedIpV6AddressRanges` en `cdk.json`.

Cuando un usuario hace clic para publicar el bot, [AWS CodeBuild](https://aws.amazon.com/codebuild/) lanza una tarea de despliegue de CDK para aprovisionar la pila de API (Véase también: [Definición de CDK](../cdk/lib/api-publishment-stack.ts)) que contiene API Gateway, Lambda y SQS. SQS se utiliza para desacoplar la solicitud del usuario y la operación de LLM porque generar la salida puede exceder los 30 segundos, que es el límite de la cuota de API Gateway. Para recuperar la salida, es necesario acceder a la API de forma asíncrona. Para más detalles, consulte [Especificación de API](#api-specification).

El cliente necesita establecer `x-api-key` en el encabezado de la solicitud.

## Especificación de la API

Consulte [aquí](https://aws-samples.github.io/bedrock-chat).