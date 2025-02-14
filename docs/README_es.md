# Chat de Bedrock Claude (Nova)

![](https://img.shields.io/github/v/release/aws-samples/bedrock-claude-chat?style=flat-square)
![](https://img.shields.io/github/license/aws-samples/bedrock-claude-chat?style=flat-square)
![](https://img.shields.io/github/actions/workflow/status/aws-samples/bedrock-claude-chat/cdk.yml?style=flat-square)
[![](https://img.shields.io/badge/roadmap-view-blue)](https://github.com/aws-samples/bedrock-claude-chat/issues?q=is%3Aissue%20state%3Aopen%20label%3Aroadmap)

[English](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/README.md) | [日本語](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_ja.md) | [한국어](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_ko.md) | [中文](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_zh.md) | [Français](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_fr.md) | [Deutsch](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_de.md) | [Español](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_es.md) | [Italian](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_it.md) | [Norsk](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_no.md) | [ไทย](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_th.md) | [Bahasa Indonesia](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_id.md) | [Bahasa Melayu](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_ms.md) | [Tiếng Việt](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_vi.md)

> [!Warning]  
> **Se ha lanzado la versión 2. Para actualizar, revise cuidadosamente la [guía de migración](./migration/V1_TO_V2_es.md).** Sin ningún cuidado, **LOS BOTS DE LA VERSIÓN 1 SE VOLVERÁN INUTILIZABLES.**

Un chatbot multilingüe que utiliza modelos LLM proporcionados por [Amazon Bedrock](https://aws.amazon.com/bedrock/) para inteligencia generativa.

### Mira la Descripción General e Instalación en YouTube

[![Descripción general](https://img.youtube.com/vi/PDTGrHlaLCQ/hq1.jpg)](https://www.youtube.com/watch?v=PDTGrHlaLCQ)

### Conversación Básica

![](./imgs/demo.gif)

### Personalización de Bot

Agregue su propia instrucción y proporcione conocimiento externo como URL o archivos (también conocido como [RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)). El bot puede compartirse entre usuarios de la aplicación. El bot personalizado también puede publicarse como API independiente (Consulte los [detalles](./PUBLISH_API_es.md)).

![](./imgs/bot_creation.png)
![](./imgs/bot_chat.png)
![](./imgs/bot_api_publish_screenshot3.png)

> [!Important]
> Por razones de gobernanza, solo los usuarios permitidos pueden crear bots personalizados. Para permitir la creación de bots personalizados, el usuario debe ser miembro del grupo llamado `CreatingBotAllowed`, que se puede configurar a través de la consola de administración > Grupos de usuarios de Amazon Cognito o la CLI de AWS. Tenga en cuenta que el ID del grupo de usuarios se puede consultar accediendo a CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`.

### Panel de administración

<details>
<summary>Panel de administración</summary>

Analice el uso de cada usuario / bot en el panel de administración. [detalles](./ADMINISTRATOR_es.md)

![](./imgs/admin_bot_analytics.png)

</details>

### Agente con tecnología LLM

<details>
<summary>Agente con tecnología LLM</summary>

Utilizando la [funcionalidad de Agente](./AGENT_es.md), su chatbot puede manejar automáticamente tareas más complejas. Por ejemplo, para responder a la pregunta de un usuario, el Agente puede recuperar información necesaria de herramientas externas o dividir la tarea en varios pasos para su procesamiento.

![](./imgs/agent1.png)
![](./imgs/agent2.png)

</details>

## 🚀 Despliegue Super-fácil

- En la región us-east-1, abra [Acceso al modelo Bedrock](https://us-east-1.console.aws.amazon.com/bedrock/home?region=us-east-1#/modelaccess) > `Administrar acceso a modelos` > Marque todos los de `Anthropic / Claude 3`, todos los de `Amazon / Nova`, `Amazon / Titan Text Embeddings V2` y `Cohere / Embed Multilingual`, luego `Guardar cambios`.

<details>
<summary>Captura de pantalla</summary>

![](./imgs/model_screenshot.png)

</details>

- Abra [CloudShell](https://console.aws.amazon.com/cloudshell/home) en la región donde desee implementar
- Ejecute la implementación mediante los siguientes comandos. Si desea especificar la versión a implementar o necesita aplicar políticas de seguridad, especifique los parámetros apropiados de [Parámetros opcionales](#parámetros-opcionales).

```sh
git clone https://github.com/aws-samples/bedrock-claude-chat.git
cd bedrock-claude-chat
chmod +x bin.sh
./bin.sh
```

- Se le preguntará si es un usuario nuevo o si está usando v2. Si no es un usuario continuo desde v0, ingrese `y`.

### Parámetros opcionales

Puede especificar los siguientes parámetros durante la implementación para mejorar la seguridad y personalización:

- **--disable-self-register**: Deshabilitar el registro automático (predeterminado: habilitado). Si esta bandera está configurada, deberá crear todos los usuarios en Cognito y no permitirá a los usuarios registrarse por sí mismos.
- **--enable-lambda-snapstart**: Habilitar [Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html) (predeterminado: deshabilitado). Si esta bandera está configurada, mejora los tiempos de inicio en frío para las funciones Lambda, proporcionando tiempos de respuesta más rápidos para una mejor experiencia de usuario.
- **--ipv4-ranges**: Lista separada por comas de rangos IPv4 permitidos. (predeterminado: permitir todas las direcciones IPv4)
- **--ipv6-ranges**: Lista separada por comas de rangos IPv6 permitidos. (predeterminado: permitir todas las direcciones IPv6)
- **--disable-ipv6**: Deshabilitar conexiones sobre IPv6. (predeterminado: habilitado)
- **--allowed-signup-email-domains**: Lista separada por comas de dominios de correo electrónico permitidos para el registro. (predeterminado: sin restricción de dominio)
- **--bedrock-region**: Definir la región donde Bedrock está disponible. (predeterminado: us-east-1)
- **--repo-url**: El repositorio personalizado de Bedrock Claude Chat para implementar, si está bifurcado o se utiliza un control de código fuente personalizado. (predeterminado: https://github.com/aws-samples/bedrock-claude-chat.git)
- **--version**: La versión de Bedrock Claude Chat para implementar. (predeterminado: última versión en desarrollo)
- **--cdk-json-override**: Puede anular cualquier valor de contexto de CDK durante la implementación utilizando el bloque JSON de anulación. Esto le permite modificar la configuración sin editar directamente el archivo cdk.json.

Ejemplo de uso:

```bash
./bin.sh --cdk-json-override '{
  "context": {
    "selfSignUpEnabled": false,
    "enableLambdaSnapStart": true,
    "allowedIpV4AddressRanges": ["192.168.1.0/24"],
    "allowedSignUpEmailDomains": ["example.com"]
  }
}'
```

El JSON de anulación debe seguir la misma estructura que cdk.json. Puede anular cualquier valor de contexto, incluyendo:

- `selfSignUpEnabled`
- `enableLambdaSnapStart`
- `allowedIpV4AddressRanges`
- `allowedIpV6AddressRanges`
- `allowedSignUpEmailDomains`
- `bedrockRegion`
- `enableRagReplicas`
- `enableBedrockCrossRegionInference`
- Y otros valores de contexto definidos en cdk.json

> [!Nota]
> Los valores de anulación se fusionarán con la configuración de cdk.json existente durante el tiempo de implementación en la compilación de código de AWS. Los valores especificados en la anulación tendrán prioridad sobre los valores en cdk.json.

#### Ejemplo de comando con parámetros:

```sh
./bin.sh --disable-self-register --ipv4-ranges "192.0.2.0/25,192.0.2.128/25" --ipv6-ranges "2001:db8:1:2::/64,2001:db8:1:3::/64" --allowed-signup-email-domains "example.com,anotherexample.com" --bedrock-region "us-west-2" --version "v1.2.6"
```

- Después de aproximadamente 35 minutos, obtendrá la siguiente salida, a la que puede acceder desde su navegador

```
URL de Frontend: https://xxxxxxxxx.cloudfront.net
```

![](./imgs/signin.png)

Aparecerá la pantalla de registro como se muestra arriba, donde puede registrar su correo electrónico e iniciar sesión.

> [!Importante]
> Sin establecer el parámetro opcional, este método de implementación permite que cualquiera que conozca la URL se registre. Para uso en producción, se recomienda encarecidamente agregar restricciones de dirección IP y deshabilitar el registro automático para mitigar riesgos de seguridad (puede definir allowed-signup-email-domains para restringir usuarios para que solo las direcciones de correo electrónico del dominio de su empresa puedan registrarse). Use tanto ipv4-ranges como ipv6-ranges para restricciones de direcciones IP y deshabilite el registro automático mediante el uso de disable-self-register al ejecutar ./bin.

> [!CONSEJO]
> Si la `URL de Frontend` no aparece o Bedrock Claude Chat no funciona correctamente, puede ser un problema con la última versión. En este caso, agregue `--version "v1.2.6"` a los parámetros e intente la implementación nuevamente.

## Arquitectura

Es una arquitectura construida sobre servicios administrados de AWS, eliminando la necesidad de gestionar infraestructura. Utilizando Amazon Bedrock, no es necesario comunicarse con API externas a AWS. Esto permite implementar aplicaciones escalables, confiables y seguras.

- [Amazon DynamoDB](https://aws.amazon.com/dynamodb/): Base de datos NoSQL para almacenamiento del historial de conversaciones
- [Amazon API Gateway](https://aws.amazon.com/api-gateway/) + [AWS Lambda](https://aws.amazon.com/lambda/): Punto de enlace de API backend ([AWS Lambda Web Adapter](https://github.com/awslabs/aws-lambda-web-adapter), [FastAPI](https://fastapi.tiangolo.com/))
- [Amazon CloudFront](https://aws.amazon.com/cloudfront/) + [S3](https://aws.amazon.com/s3/): Entrega de aplicación frontend ([React](https://react.dev/), [Tailwind CSS](https://tailwindcss.com/))
- [AWS WAF](https://aws.amazon.com/waf/): Restricción de direcciones IP
- [Amazon Cognito](https://aws.amazon.com/cognito/): Autenticación de usuarios
- [Amazon Bedrock](https://aws.amazon.com/bedrock/): Servicio administrado para utilizar modelos fundamentales a través de API
- [Amazon Bedrock Knowledge Bases](https://aws.amazon.com/bedrock/knowledge-bases/): Proporciona una interfaz administrada para Generación Aumentada por Recuperación ([RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)), ofreciendo servicios para incrustar y analizar documentos
- [Amazon EventBridge Pipes](https://aws.amazon.com/eventbridge/pipes/): Recepción de eventos desde la transmisión de DynamoDB e inicio de Step Functions para incrustar conocimiento externo
- [AWS Step Functions](https://aws.amazon.com/step-functions/): Orquestación de la canalización de ingesta para incrustar conocimiento externo en Bedrock Knowledge Bases
- [Amazon OpenSearch Serverless](https://aws.amazon.com/opensearch-service/features/serverless/): Sirve como base de datos backend para Bedrock Knowledge Bases, proporcionando capacidades de búsqueda de texto completo y búsqueda vectorial, permitiendo la recuperación precisa de información relevante
- [Amazon Athena](https://aws.amazon.com/athena/): Servicio de consulta para analizar bucket de S3

![](./imgs/arch.png)

## Implementación mediante CDK

La implementación súper fácil utiliza [AWS CodeBuild](https://aws.amazon.com/codebuild/) para realizar la implementación con CDK internamente. Esta sección describe el procedimiento para implementar directamente con CDK.

- Por favor, tenga UNIX, Docker y un entorno de ejecución de Node.js. Si no, también puede usar [Cloud9](https://github.com/aws-samples/cloud9-setup-for-prototyping)

> [!Importante]
> Si hay un espacio de almacenamiento insuficiente en el entorno local durante la implementación, el arranque de CDK puede resultar en un error. Si está ejecutando en Cloud9, etc., recomendamos expandir el tamaño del volumen de la instancia antes de implementar.

- Clone este repositorio

```
git clone https://github.com/aws-samples/bedrock-claude-chat
```

- Instalar paquetes npm

```
cd bedrock-claude-chat
cd cdk
npm ci
```

- Si es necesario, edite las siguientes entradas en [cdk.json](./cdk/cdk.json) si es necesario.

  - `bedrockRegion`: Región donde Bedrock está disponible. **NOTA: Bedrock NO es compatible con todas las regiones por ahora.**
  - `allowedIpV4AddressRanges`, `allowedIpV6AddressRanges`: Rango de direcciones IP permitidas.
  - `enableLambdaSnapStart`: Por defecto es true. Establézcalo en false si implementa en una [región que no es compatible con Lambda SnapStart para funciones de Python](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions).

- Antes de implementar CDK, deberá trabajar con Bootstrap una vez para la región en la que va a implementar.

```
npx cdk bootstrap
```

- Implementar este proyecto de ejemplo

```
npx cdk deploy --require-approval never --all
```

- Obtendrá una salida similar a la siguiente. La URL de la aplicación web se mostrará en `BedrockChatStack.FrontendURL`, así que acceda a ella desde su navegador.

```sh
 ✅  BedrockChatStack

✨  Tiempo de implementación: 78.57s

Salidas:
BedrockChatStack.AuthUserPoolClientIdXXXXX = xxxxxxx
BedrockChatStack.AuthUserPoolIdXXXXXX = ap-northeast-1_XXXX
BedrockChatStack.BackendApiBackendApiUrlXXXXX = https://xxxxx.execute-api.ap-northeast-1.amazonaws.com
BedrockChatStack.FrontendURL = https://xxxxx.cloudfront.net
```

## Otros

### Configurar soporte de modelos Mistral

Actualice `enableMistral` a `true` en [cdk.json](./cdk/cdk.json) y ejecute `npx cdk deploy`.

```json
...
  "enableMistral": true,
```

> [!Importante]
> Este proyecto se enfoca en modelos Anthropic Claude, los modelos Mistral tienen soporte limitado. Por ejemplo, los ejemplos de indicaciones se basan en modelos Claude. Esta es una opción solo para Mistral, una vez que habilite los modelos Mistral, solo podrá usar modelos Mistral para todas las funciones de chat, NO tanto Claude como Mistral.

### Configurar generación de texto predeterminada

Los usuarios pueden ajustar los [parámetros de generación de texto](https://docs.anthropic.com/claude/reference/complete_post) desde la pantalla de creación de bot personalizado. Si el bot no se utiliza, se utilizarán los parámetros predeterminados establecidos en [config.py](./backend/app/config.py).

```py
DEFAULT_GENERATION_CONFIG = {
    "max_tokens": 2000,
    "top_k": 250,
    "top_p": 0.999,
    "temperature": 0.6,
    "stop_sequences": ["Human: ", "Assistant: "],
}
```

### Eliminar recursos

Si está utilizando cli y CDK, ejecute `npx cdk destroy`. Si no, acceda a [CloudFormation](https://console.aws.amazon.com/cloudformation/home) y luego elimine manualmente `BedrockChatStack` y `FrontendWafStack`. Tenga en cuenta que `FrontendWafStack` está en la región `us-east-1`.

### Configuración de idioma

Este recurso detecta automáticamente el idioma usando [i18next-browser-languageDetector](https://github.com/i18next/i18next-browser-languageDetector). Puede cambiar de idioma desde el menú de la aplicación. Alternativamente, puede usar Query String para establecer el idioma como se muestra a continuación.

> `https://example.com?lng=ja`

### Deshabilitar registro automático

Esta muestra tiene el registro automático habilitado de forma predeterminada. Para deshabilitarlo, abra [cdk.json](./cdk/cdk.json) y cambie `selfSignUpEnabled` a `false`. Si configura un [proveedor de identidad externo](#external-identity-provider), el valor se ignorará y se deshabilitará automáticamente.

### Restringir dominios para direcciones de correo electrónico de registro

De forma predeterminada, esta muestra no restringe los dominios para las direcciones de correo electrónico de registro. Para permitir registros solo desde dominios específicos, abra `cdk.json` y especifique los dominios como una lista en `allowedSignUpEmailDomains`.

```ts
"allowedSignUpEmailDomains": ["example.com"],
```

### Proveedor de identidad externo

Esta muestra admite un proveedor de identidad externo. Actualmente, admitimos [Google](./idp/SET_UP_GOOGLE_es.md) y [proveedor OIDC personalizado](./idp/SET_UP_CUSTOM_OIDC_es.md).

### Agregar nuevos usuarios a grupos automáticamente

Esta muestra tiene los siguientes grupos para dar permisos a los usuarios:

- [`Admin`](./ADMINISTRATOR_es.md)
- [`CreatingBotAllowed`](#bot-personalization)
- [`PublishAllowed`](./PUBLISH_API_es.md)

Si desea que los usuarios recién creados se unan automáticamente a grupos, puede especificarlos en [cdk.json](./cdk/cdk.json).

```json
"autoJoinUserGroups": ["CreatingBotAllowed"],
```

De forma predeterminada, los usuarios recién creados se unirán al grupo `CreatingBotAllowed`.

### Configurar réplicas RAG

`enableRagReplicas` es una opción en [cdk.json](./cdk/cdk.json) que controla la configuración de réplicas para la base de datos RAG, específicamente las Bases de Conocimiento que utilizan Amazon OpenSearch Serverless.

- **Predeterminado**: true
- **true**: Mejora la disponibilidad al habilitar réplicas adicionales, lo que lo hace adecuado para entornos de producción, pero aumenta los costos.
- **false**: Reduce los costos usando menos réplicas, lo que lo hace adecuado para desarrollo y pruebas.

Esta es una configuración a nivel de cuenta/región que afecta a toda la aplicación, no a bots individuales.

> [!Nota]
> A partir de junio de 2024, Amazon OpenSearch Serverless admite 0.5 OCU, reduciendo los costos de entrada para cargas de trabajo a pequeña escala. Las implementaciones de producción pueden comenzar con 2 OCU, mientras que las cargas de trabajo de desarrollo/pruebas pueden usar 1 OCU. OpenSearch Serverless se escala automáticamente según las demandas de la carga de trabajo. Para más detalles, visite [anuncio](https://aws.amazon.com/jp/about-aws/whats-new/2024/06/amazon-opensearch-serverless-entry-cost-half-collection-types/).

### Inferencia entre regiones

La [inferencia entre regiones](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html) permite que Amazon Bedrock enrute dinámicamente las solicitudes de inferencia de modelos entre varias regiones de AWS, mejorando el rendimiento y la resistencia durante los períodos de alta demanda. Para configurarlo, edite `cdk.json`.

```json
"enableBedrockCrossRegionInference": true
```

### Lambda SnapStart

[Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html) mejora los tiempos de inicio en frío para las funciones Lambda, proporcionando tiempos de respuesta más rápidos para una mejor experiencia de usuario. Por otro lado, para funciones Python, hay un [cargo dependiendo del tamaño de caché](https://aws.amazon.com/lambda/pricing/#SnapStart_Pricing) y [no está disponible en algunas regiones](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions) actualmente. Para deshabilitar SnapStart, edite `cdk.json`.

```json
"enableLambdaSnapStart": false
```

### Configurar dominio personalizado

Puede configurar un dominio personalizado para la distribución de CloudFront estableciendo los siguientes parámetros en [cdk.json](./cdk/cdk.json):

```json
{
  "alternateDomainName": "chat.example.com",
  "hostedZoneId": "Z0123456789ABCDEF"
}
```

- `alternateDomainName`: El nombre de dominio personalizado para su aplicación de chat (por ejemplo, chat.example.com)
- `hostedZoneId`: El ID de su zona alojada de Route 53 donde se crearán los registros DNS

Cuando se proporcionan estos parámetros, la implementación automáticamente:

- Creará un certificado ACM con validación DNS en la región us-east-1
- Creará los registros DNS necesarios en su zona alojada de Route 53
- Configurará CloudFront para usar su dominio personalizado

> [!Nota]
> El dominio debe ser administrado por Route 53 en su cuenta de AWS. El ID de zona alojada se puede encontrar en la consola de Route 53.

### Desarrollo local

Consulte [DESARROLLO LOCAL](./LOCAL_DEVELOPMENT_es.md).

### Contribución

¡Gracias por considerar contribuir a este repositorio! Damos la bienvenida a correcciones de errores, traducciones de idiomas (i18n), mejoras de características, [herramientas de agente](./docs/AGENT.md#how-to-develop-your-own-tools) y otras mejoras.

Para mejoras de características y otras mejoras, **antes de crear una Pull Request, agradeceríamos mucho que creara un Issue de Solicitud de Característica para discutir el enfoque de implementación y los detalles. Para correcciones de errores y traducciones de idiomas (i18n), proceda directamente a crear una Pull Request.**

Por favor, eche un vistazo a las siguientes pautas antes de contribuir:

- [Desarrollo local](./LOCAL_DEVELOPMENT_es.md)
- [CONTRIBUYENDO](./CONTRIBUTING_es.md)

## Contactos

- [Takehiro Suzuki](https://github.com/statefb)
- [Yusuke Wada](https://github.com/wadabee)
- [Yukinobu Mine](https://github.com/Yukinobu-Mine)

## 🏆 Contribuidores Significativos

- [k70suK3-k06a7ash1](https://github.com/k70suK3-k06a7ash1)
- [fsatsuki](https://github.com/fsatsuki)

## Colaboradores

[![colaboradores de bedrock claude chat](https://contrib.rocks/image?repo=aws-samples/bedrock-claude-chat&max=1000)](https://github.com/aws-samples/bedrock-claude-chat/graphs/contributors)

## Licencia

Esta biblioteca está licenciada bajo la Licencia MIT-0. Consulte [el archivo de LICENCIA](./LICENSE).