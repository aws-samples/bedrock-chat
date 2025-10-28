<h1 align="center">Bedrock Chat (BrChat)</h1>

<p align="center">
  <img src="https://img.shields.io/github/v/release/aws-samples/bedrock-chat?style=flat-square" />
  <img src="https://img.shields.io/github/license/aws-samples/bedrock-chat?style=flat-square" />
  <img src="https://img.shields.io/github/actions/workflow/status/aws-samples/bedrock-chat/cdk.yml?style=flat-square" />
  <a href="https://github.com/aws-samples/bedrock-chat/issues?q=is%3Aissue%20state%3Aopen%20label%3Aroadmap">
    <img src="https://img.shields.io/badge/roadmap-view-blue?style=flat-square" />
  </a>
</p>

[English](https://github.com/aws-samples/bedrock-chat/blob/v3/README.md) | [日本語](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_ja-JP.md) | [한국어](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_ko-KR.md) | [中文](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_zh-CN.md) | [Français](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_fr-FR.md) | [Deutsch](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_de-DE.md) | [Español](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_es-ES.md) | [Italian](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_it-IT.md) | [Norsk](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_nb-NO.md) | [ไทย](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_th-TH.md) | [Bahasa Indonesia](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_id-ID.md) | [Bahasa Melayu](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_ms-MY.md) | [Tiếng Việt](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_vi-VN.md) | [Polski](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_pl-PL.md) | [Português Brasil](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_pt-BR.md)


Una plataforma de IA generativa multilingüe impulsada por [Amazon Bedrock](https://aws.amazon.com/bedrock/).
Admite chat, bots personalizados con conocimiento (RAG), compartición de bots a través de una tienda de bots y automatización de tareas mediante agentes.

![](./imgs/demo.gif)

> [!Warning]
>
> **V3 lanzada. Para actualizar, por favor revise cuidadosamente la [guía de migración](./migration/V2_TO_V3_es-ES.md).** Sin el debido cuidado, **LOS BOTS DE V2 QUEDARÁN INUTILIZABLES.**

### Personalización de Bots / Tienda de bots

Añade tus propias instrucciones y conocimiento (también conocido como [RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)). El bot puede compartirse entre los usuarios de la aplicación a través del mercado de la tienda de bots. El bot personalizado también puede publicarse como una API independiente (Ver los [detalles](./PUBLISH_API_es-ES.md)).

<details>
<summary>Capturas de pantalla</summary>

![](./imgs/customized_bot_creation.png)
![](./imgs/fine_grained_permission.png)
![](./imgs/bot_store.png)
![](./imgs/bot_api_publish_screenshot3.png)

También puedes importar [KnowledgeBase de Amazon Bedrock](https://aws.amazon.com/bedrock/knowledge-bases/) existentes.

![](./imgs/import_existing_kb.png)

</details>

> [!Important]
> Por razones de gobernanza, solo los usuarios autorizados pueden crear bots personalizados. Para permitir la creación de bots personalizados, el usuario debe ser miembro del grupo llamado `CreatingBotAllowed`, que se puede configurar a través de la consola de administración > Amazon Cognito User pools o aws cli. Ten en cuenta que el ID del grupo de usuarios se puede consultar accediendo a CloudFormation > BedrockChatStack > Outputs > `AuthUserPoolIdxxxx`.

### Características administrativas

Gestión de API, Marcar bots como esenciales, Analizar el uso de bots. [detalles](./ADMINISTRATOR_es-ES.md)

<details>
<summary>Capturas de pantalla</summary>

![](./imgs/admin_bot_menue.png)
![](./imgs/bot_store.png)
![](./imgs/admn_api_management.png)
![](./imgs/admin_bot_analytics.png))

</details>

### Agente

Mediante el uso de la [funcionalidad de Agente](./AGENT_es-ES.md), tu chatbot puede manejar automáticamente tareas más complejas. Por ejemplo, para responder a la pregunta de un usuario, el Agente puede recuperar información necesaria de herramientas externas o desglosar la tarea en múltiples pasos para su procesamiento.

<details>
<summary>Capturas de pantalla</summary>

![](./imgs/agent1.png)
![](./imgs/agent2.png)

</details>

## 🚀 Implementación súper fácil

- En la región us-east-1, abre [Acceso a modelos de Bedrock](https://us-east-1.console.aws.amazon.com/bedrock/home?region=us-east-1#/modelaccess) > `Manage model access` > Marca todos los modelos que desees usar y luego `Save changes`.

<details>
<summary>Captura de pantalla</summary>

![](./imgs/model_screenshot.png)

</details>

### Regiones soportadas

Asegúrate de implementar Bedrock Chat en una región [donde OpenSearch Serverless y las APIs de Ingestion estén disponibles](https://docs.aws.amazon.com/general/latest/gr/opensearch-service.html), si deseas usar bots y crear bases de conocimiento (OpenSearch Serverless es la opción predeterminada). A partir de agosto de 2025, las siguientes regiones están soportadas: us-east-1, us-east-2, us-west-1, us-west-2, ap-south-1, ap-northeast-1, ap-northeast-2, ap-southeast-1, ap-southeast-2, ca-central-1, eu-central-1, eu-west-1, eu-west-2, eu-south-2, eu-north-1, sa-east-1

Para el parámetro **bedrock-region** necesitas elegir una región [donde Bedrock esté disponible](https://docs.aws.amazon.com/general/latest/gr/bedrock.html).

- Abre [CloudShell](https://console.aws.amazon.com/cloudshell/home) en la región donde deseas implementar
- Ejecuta la implementación con los siguientes comandos. Si deseas especificar la versión a implementar o necesitas aplicar políticas de seguridad, especifica los parámetros apropiados de [Parámetros Opcionales](#optional-parameters).

```sh
git clone https://github.com/aws-samples/bedrock-chat.git
cd bedrock-chat
chmod +x bin.sh
./bin.sh
```

- Se te preguntará si eres un usuario nuevo o si estás usando v3. Si no eres un usuario que continúa desde v0, ingresa `y`.

### Parámetros Opcionales

Puedes especificar los siguientes parámetros durante la implementación para mejorar la seguridad y personalización:

- **--disable-self-register**: Deshabilita el auto-registro (habilitado por defecto). Si se establece esta bandera, necesitarás crear todos los usuarios en cognito y no permitirá que los usuarios auto-registren sus cuentas.
- **--enable-lambda-snapstart**: Habilita [Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html) (deshabilitado por defecto). Si se establece esta bandera, mejora los tiempos de inicio en frío para las funciones Lambda, proporcionando tiempos de respuesta más rápidos para una mejor experiencia de usuario.
- **--ipv4-ranges**: Lista separada por comas de rangos IPv4 permitidos. (por defecto: permite todas las direcciones ipv4)
- **--ipv6-ranges**: Lista separada por comas de rangos IPv6 permitidos. (por defecto: permite todas las direcciones ipv6)
- **--disable-ipv6**: Deshabilita las conexiones a través de IPv6. (habilitado por defecto)
- **--allowed-signup-email-domains**: Lista separada por comas de dominios de correo electrónico permitidos para registro. (por defecto: sin restricción de dominio)
- **--bedrock-region**: Define la región donde Bedrock está disponible. (por defecto: us-east-1)
- **--repo-url**: El repositorio personalizado de Bedrock Chat a implementar, si está bifurcado o tiene control de fuente personalizado. (por defecto: https://github.com/aws-samples/bedrock-chat.git)
- **--version**: La versión de Bedrock Chat a implementar. (por defecto: última versión en desarrollo)
- **--cdk-json-override**: Puedes sobrescribir cualquier valor de contexto CDK durante la implementación usando el bloque JSON de anulación. Esto te permite modificar la configuración sin editar directamente el archivo cdk.json.

Ejemplo de uso:

```bash
./bin.sh --cdk-json-override '{
  "context": {
    "selfSignUpEnabled": false,
    "enableLambdaSnapStart": true,
    "allowedIpV4AddressRanges": ["192.168.1.0/24"],
    "allowedCountries": ["US", "CA"],
    "allowedSignUpEmailDomains": ["example.com"],
    "globalAvailableModels": [
      "claude-v3.7-sonnet",
      "claude-v3.5-sonnet",
      "amazon-nova-pro",
      "amazon-nova-lite",
      "llama3-3-70b-instruct"
    ]
  }
}'
```

La anulación JSON debe seguir la misma estructura que cdk.json. Puedes sobrescribir cualquier valor de contexto incluyendo:

- `selfSignUpEnabled`
- `enableLambdaSnapStart`
- `allowedIpV4AddressRanges`
- `allowedIpV6AddressRanges`
- `allowedCountries`
- `allowedSignUpEmailDomains`
- `bedrockRegion`
- `enableRagReplicas`
- `enableBedrockCrossRegionInference`
- `globalAvailableModels`: acepta una lista de IDs de modelos para habilitar. El valor predeterminado es una lista vacía, que habilita todos los modelos.
- `logoPath`: ruta relativa al activo del logo dentro del directorio frontend `public/` que aparece en la parte superior del cajón de navegación.
- Y otros valores de contexto definidos en cdk.json

> [!Note]
> Los valores de anulación se combinarán con la configuración existente de cdk.json durante el tiempo de implementación en AWS code build. Los valores especificados en la anulación tendrán prioridad sobre los valores en cdk.json.

#### Ejemplo de comando con parámetros:

```sh
./bin.sh --disable-self-register --ipv4-ranges "192.0.2.0/25,192.0.2.128/25" --ipv6-ranges "2001:db8:1:2::/64,2001:db8:1:3::/64" --allowed-signup-email-domains "example.com,anotherexample.com" --bedrock-region "us-west-2" --version "v1.2.6"
```

- Después de aproximadamente 35 minutos, obtendrás la siguiente salida, a la que podrás acceder desde tu navegador

```
Frontend URL: https://xxxxxxxxx.cloudfront.net
```

![](./imgs/signin.png)

Aparecerá la pantalla de registro como se muestra arriba, donde podrás registrar tu correo electrónico e iniciar sesión.

> [!Important]
> Sin establecer el parámetro opcional, este método de implementación permite que cualquiera que conozca la URL se registre. Para uso en producción, se recomienda encarecidamente agregar restricciones de dirección IP y deshabilitar el auto-registro para mitigar riesgos de seguridad (puedes definir allowed-signup-email-domains para restringir usuarios de modo que solo las direcciones de correo electrónico de tu dominio empresarial puedan registrarse). Usa tanto ipv4-ranges como ipv6-ranges para restricciones de dirección IP, y deshabilita el auto-registro usando disable-self-register al ejecutar ./bin.

> [!TIP]
> Si la `Frontend URL` no aparece o Bedrock Chat no funciona correctamente, puede ser un problema con la última versión. En este caso, agrega `--version "v3.0.0"` a los parámetros e intenta la implementación nuevamente.

## Arquitectura

Es una arquitectura construida sobre servicios gestionados de AWS, eliminando la necesidad de gestionar infraestructura. Al utilizar Amazon Bedrock, no hay necesidad de comunicarse con APIs fuera de AWS. Esto permite implementar aplicaciones escalables, fiables y seguras.

- [Amazon DynamoDB](https://aws.amazon.com/dynamodb/): Base de datos NoSQL para almacenamiento del historial de conversaciones
- [Amazon API Gateway](https://aws.amazon.com/api-gateway/) + [AWS Lambda](https://aws.amazon.com/lambda/): Punto de conexión de API backend ([AWS Lambda Web Adapter](https://github.com/awslabs/aws-lambda-web-adapter), [FastAPI](https://fastapi.tiangolo.com/))
- [Amazon CloudFront](https://aws.amazon.com/cloudfront/) + [S3](https://aws.amazon.com/s3/): Entrega de aplicación frontend ([React](https://react.dev/), [Tailwind CSS](https://tailwindcss.com/))
- [AWS WAF](https://aws.amazon.com/waf/): Restricción de direcciones IP
- [Amazon Cognito](https://aws.amazon.com/cognito/): Autenticación de usuarios
- [Amazon Bedrock](https://aws.amazon.com/bedrock/): Servicio gestionado para utilizar modelos fundamentales a través de APIs
- [Amazon Bedrock Knowledge Bases](https://aws.amazon.com/bedrock/knowledge-bases/): Proporciona una interfaz gestionada para la Generación Aumentada por Recuperación ([RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)), ofreciendo servicios para incrustar y analizar documentos
- [Amazon EventBridge Pipes](https://aws.amazon.com/eventbridge/pipes/): Recepción de eventos desde el flujo de DynamoDB y lanzamiento de Step Functions para incorporar conocimiento externo
- [AWS Step Functions](https://aws.amazon.com/step-functions/): Orquestación del pipeline de ingesta para incorporar conocimiento externo en Bedrock Knowledge Bases
- [Amazon OpenSearch Serverless](https://aws.amazon.com/opensearch-service/features/serverless/): Sirve como base de datos backend para Bedrock Knowledge Bases, proporcionando búsqueda de texto completo y búsqueda vectorial, permitiendo una recuperación precisa de información relevante
- [Amazon Athena](https://aws.amazon.com/athena/): Servicio de consultas para analizar buckets S3

![](./imgs/arch.png)

## Despliegue usando CDK

El despliegue super fácil utiliza [AWS CodeBuild](https://aws.amazon.com/codebuild/) para realizar el despliegue mediante CDK internamente. Esta sección describe el procedimiento para desplegar directamente con CDK.

- Por favor, tenga UNIX, Docker y un entorno de ejecución Node.js.

> [!Important]
> Si no hay suficiente espacio de almacenamiento en el entorno local durante el despliegue, el arranque de CDK puede resultar en un error. Recomendamos ampliar el tamaño del volumen de la instancia antes de desplegar.

- Clone este repositorio

```
git clone https://github.com/aws-samples/bedrock-chat
```

- Instale los paquetes npm

```
cd bedrock-chat
cd cdk
npm ci
```

- Si es necesario, edite las siguientes entradas en [cdk.json](./cdk/cdk.json).

  - `bedrockRegion`: Región donde Bedrock está disponible. **NOTA: Bedrock NO soporta todas las regiones por ahora.**
  - `allowedIpV4AddressRanges`, `allowedIpV6AddressRanges`: Rango de direcciones IP permitidas.
  - `enableLambdaSnapStart`: Por defecto es true. Establecer en false si se despliega en una [región que no soporta Lambda SnapStart para funciones Python](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions).
  - `globalAvailableModels`: Por defecto son todos. Si se establece (lista de IDs de modelos), permite controlar globalmente qué modelos aparecen en los menús desplegables en todos los chats para todos los usuarios y durante la creación de bots en la aplicación Bedrock Chat.
  - `logoPath`: Ruta relativa bajo `frontend/public` que apunta a la imagen mostrada en la parte superior del cajón de la aplicación.
Los siguientes IDs de modelos son soportados (asegúrese de que también estén habilitados en la consola de Bedrock bajo Model access en su región de despliegue):
- **Modelos Claude:** `claude-v4-opus`, `claude-v4.1-opus`, `claude-v4-sonnet`, `claude-v3.5-sonnet`, `claude-v3.5-sonnet-v2`, `claude-v3.7-sonnet`, `claude-v3.5-haiku`, `claude-v3-haiku`, `claude-v3-opus`
- **Modelos Amazon Nova:** `amazon-nova-pro`, `amazon-nova-lite`, `amazon-nova-micro`
- **Modelos Mistral:** `mistral-7b-instruct`, `mixtral-8x7b-instruct`, `mistral-large`, `mistral-large-2`
- **Modelos DeepSeek:** `deepseek-r1`
- **Modelos Meta Llama:** `llama3-3-70b-instruct`, `llama3-2-1b-instruct`, `llama3-2-3b-instruct`, `llama3-2-11b-instruct`, `llama3-2-90b-instruct`

La lista completa se puede encontrar en [index.ts](./frontend/src/constants/index.ts).

- Antes de desplegar el CDK, necesitará trabajar con Bootstrap una vez para la región en la que está desplegando.

```
npx cdk bootstrap
```

- Despliegue este proyecto de ejemplo

```
npx cdk deploy --require-approval never --all
```

- Obtendrá una salida similar a la siguiente. La URL de la aplicación web se mostrará en `BedrockChatStack.FrontendURL`, así que acceda a ella desde su navegador.

```sh
 ✅  BedrockChatStack

✨  Deployment time: 78.57s

Outputs:
BedrockChatStack.AuthUserPoolClientIdXXXXX = xxxxxxx
BedrockChatStack.AuthUserPoolIdXXXXXX = ap-northeast-1_XXXX
BedrockChatStack.BackendApiBackendApiUrlXXXXX = https://xxxxx.execute-api.ap-northeast-1.amazonaws.com
BedrockChatStack.FrontendURL = https://xxxxx.cloudfront.net
```

### Definición de Parámetros

Puede definir parámetros para su despliegue de dos formas: usando `cdk.json` o usando el archivo `parameter.ts` con seguridad de tipos.

#### Usando cdk.json (Método Tradicional)

La forma tradicional de configurar parámetros es editando el archivo `cdk.json`. Este enfoque es simple pero carece de verificación de tipos:

```json
{
  "app": "npx ts-node --prefer-ts-exts bin/bedrock-chat.ts",
  "context": {
    "bedrockRegion": "us-east-1",
    "allowedIpV4AddressRanges": ["0.0.0.0/1", "128.0.0.0/1"],
    "selfSignUpEnabled": true,
    "globalAvailableModels": [
      "claude-v3.7-sonnet",
      "claude-v3.5-sonnet",
      "amazon-nova-pro",
      "amazon-nova-lite",
      "llama3-3-70b-instruct"
    ],
  }
}
```

#### Usando parameter.ts (Método Recomendado con Seguridad de Tipos)

Para una mejor seguridad de tipos y experiencia de desarrollo, puede usar el archivo `parameter.ts` para definir sus parámetros:

```typescript
// Define parámetros para el entorno predeterminado
bedrockChatParams.set("default", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["192.168.0.0/16"],
  selfSignUpEnabled: true,
  globalAvailableModels: [
      "claude-v3.7-sonnet",
      "claude-v3.5-sonnet",
      "amazon-nova-pro",
      "amazon-nova-lite",
      "llama3-3-70b-instruct"
    ],
});

// Define parámetros para entornos adicionales
bedrockChatParams.set("dev", {
  bedrockRegion: "us-west-2",
  allowedIpV4AddressRanges: ["10.0.0.0/8"],
  enableRagReplicas: false, // Ahorro de costos para entorno de desarrollo
  enableBotStoreReplicas: false, // Ahorro de costos para entorno de desarrollo
});

bedrockChatParams.set("prod", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["172.16.0.0/12"],
  enableLambdaSnapStart: true,
  enableRagReplicas: true, // Disponibilidad mejorada para producción
  enableBotStoreReplicas: true, // Disponibilidad mejorada para producción
});
```

> [!Note]
> Los usuarios existentes pueden continuar usando `cdk.json` sin cambios. El enfoque de `parameter.ts` se recomienda para nuevos despliegues o cuando necesite gestionar múltiples entornos.

### Desplegando Múltiples Entornos

Puede desplegar múltiples entornos desde el mismo código base usando el archivo `parameter.ts` y la opción `-c envName`.

#### Prerequisitos

1. Defina sus entornos en `parameter.ts` como se mostró anteriormente
2. Cada entorno tendrá su propio conjunto de recursos con prefijos específicos del entorno

#### Comandos de Despliegue

Para desplegar un entorno específico:

```bash
# Desplegar el entorno de desarrollo
npx cdk deploy --all -c envName=dev

# Desplegar el entorno de producción
npx cdk deploy --all -c envName=prod
```

Si no se especifica un entorno, se usa el entorno "default":

```bash
# Desplegar el entorno predeterminado
npx cdk deploy --all
```

#### Notas Importantes

1. **Nomenclatura de Stacks**:

   - Los stacks principales para cada entorno tendrán el prefijo del nombre del entorno (ej., `dev-BedrockChatStack`, `prod-BedrockChatStack`)
   - Sin embargo, los stacks de bots personalizados (`BrChatKbStack*`) y los stacks de publicación de API (`ApiPublishmentStack*`) no reciben prefijos de entorno ya que se crean dinámicamente en tiempo de ejecución

2. **Nomenclatura de Recursos**:

   - Solo algunos recursos reciben prefijos de entorno en sus nombres (ej., `dev_ddb_export` tabla, `dev-FrontendWebAcl`)
   - La mayoría de los recursos mantienen sus nombres originales pero están aislados al estar en diferentes stacks

3. **Identificación del Entorno**:

   - Todos los recursos están etiquetados con una etiqueta `CDKEnvironment` que contiene el nombre del entorno
   - Puede usar esta etiqueta para identificar a qué entorno pertenece un recurso
   - Ejemplo: `CDKEnvironment: dev` o `CDKEnvironment: prod`

4. **Anulación del Entorno Predeterminado**: Si define un entorno "default" en `parameter.ts`, anulará la configuración en `cdk.json`. Para continuar usando `cdk.json`, no defina un entorno "default" en `parameter.ts`.

5. **Requisitos del Entorno**: Para crear entornos diferentes al "default", debe usar `parameter.ts`. La opción `-c envName` por sí sola no es suficiente sin las definiciones de entorno correspondientes.

6. **Aislamiento de Recursos**: Cada entorno crea su propio conjunto de recursos, permitiéndole tener entornos de desarrollo, prueba y producción en la misma cuenta de AWS sin conflictos.

## Otros

Puedes definir parámetros para tu despliegue de dos formas: usando `cdk.json` o usando el archivo `parameter.ts` con seguridad de tipos.

#### Usando cdk.json (Método Tradicional)

La forma tradicional de configurar parámetros es editando el archivo `cdk.json`. Este enfoque es simple pero carece de verificación de tipos:

```json
{
  "app": "npx ts-node --prefer-ts-exts bin/bedrock-chat.ts",
  "context": {
    "bedrockRegion": "us-east-1",
    "allowedIpV4AddressRanges": ["0.0.0.0/1", "128.0.0.0/1"],
    "selfSignUpEnabled": true
  }
}
```

#### Usando parameter.ts (Método Recomendado con Seguridad de Tipos)

Para una mejor seguridad de tipos y experiencia de desarrollo, puedes usar el archivo `parameter.ts` para definir tus parámetros:

```typescript
// Define parameters for the default environment
bedrockChatParams.set("default", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["192.168.0.0/16"],
  selfSignUpEnabled: true,
});

// Define parameters for additional environments
bedrockChatParams.set("dev", {
  bedrockRegion: "us-west-2",
  allowedIpV4AddressRanges: ["10.0.0.0/8"],
  enableRagReplicas: false, // Cost-saving for dev environment
});

bedrockChatParams.set("prod", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["172.16.0.0/12"],
  enableLambdaSnapStart: true,
  enableRagReplicas: true, // Enhanced availability for production
});
```

> [!Note]
> Los usuarios existentes pueden continuar usando `cdk.json` sin cambios. El enfoque de `parameter.ts` se recomienda para nuevos despliegues o cuando necesites gestionar múltiples entornos.

### Desplegando Múltiples Entornos

Puedes desplegar múltiples entornos desde el mismo código base usando el archivo `parameter.ts` y la opción `-c envName`.

#### Requisitos Previos

1. Define tus entornos en `parameter.ts` como se mostró arriba
2. Cada entorno tendrá su propio conjunto de recursos con prefijos específicos del entorno

#### Comandos de Despliegue

Para desplegar un entorno específico:

```bash
# Deploy the dev environment
npx cdk deploy --all -c envName=dev

# Deploy the prod environment
npx cdk deploy --all -c envName=prod
```

Si no se especifica ningún entorno, se usa el entorno "default":

```bash
# Deploy the default environment
npx cdk deploy --all
```

#### Notas Importantes

1. **Nomenclatura de Stacks**:

   - Los stacks principales para cada entorno tendrán el prefijo del nombre del entorno (ej., `dev-BedrockChatStack`, `prod-BedrockChatStack`)
   - Sin embargo, los stacks de bot personalizados (`BrChatKbStack*`) y los stacks de publicación de API (`ApiPublishmentStack*`) no reciben prefijos de entorno ya que se crean dinámicamente en tiempo de ejecución

2. **Nomenclatura de Recursos**:

   - Solo algunos recursos reciben prefijos de entorno en sus nombres (ej., tabla `dev_ddb_export`, `dev-FrontendWebAcl`)
   - La mayoría de los recursos mantienen sus nombres originales pero están aislados al estar en diferentes stacks

3. **Identificación de Entorno**:

   - Todos los recursos están etiquetados con una etiqueta `CDKEnvironment` que contiene el nombre del entorno
   - Puedes usar esta etiqueta para identificar a qué entorno pertenece un recurso
   - Ejemplo: `CDKEnvironment: dev` o `CDKEnvironment: prod`

4. **Anulación del Entorno por Defecto**: Si defines un entorno "default" en `parameter.ts`, anulará la configuración en `cdk.json`. Para seguir usando `cdk.json`, no definas un entorno "default" en `parameter.ts`.

5. **Requisitos de Entorno**: Para crear entornos distintos al "default", debes usar `parameter.ts`. La opción `-c envName` por sí sola no es suficiente sin las definiciones de entorno correspondientes.

6. **Aislamiento de Recursos**: Cada entorno crea su propio conjunto de recursos, permitiéndote tener entornos de desarrollo, pruebas y producción en la misma cuenta de AWS sin conflictos.

## Otros

### Eliminar recursos

Si está utilizando cli y CDK, por favor ejecute `npx cdk destroy`. Si no, acceda a [CloudFormation](https://console.aws.amazon.com/cloudformation/home) y elimine manualmente `BedrockChatStack` y `FrontendWafStack`. Tenga en cuenta que `FrontendWafStack` está en la región `us-east-1`.

### Configuración de idioma

Este recurso detecta automáticamente el idioma usando [i18next-browser-languageDetector](https://github.com/i18next/i18next-browser-languageDetector). Puede cambiar de idioma desde el menú de la aplicación. Alternativamente, puede usar Query String para establecer el idioma como se muestra a continuación.

> `https://example.com?lng=ja`

### Deshabilitar el registro automático

Esta muestra tiene el registro automático habilitado por defecto. Para deshabilitarlo, abra [cdk.json](./cdk/cdk.json) y cambie `selfSignUpEnabled` a `false`. Si configura un [proveedor de identidad externo](#external-identity-provider), este valor será ignorado y deshabilitado automáticamente.

### Restringir dominios para direcciones de correo electrónico de registro

Por defecto, esta muestra no restringe los dominios para las direcciones de correo electrónico de registro. Para permitir registros solo desde dominios específicos, abra `cdk.json` y especifique los dominios como una lista en `allowedSignUpEmailDomains`.

```ts
"allowedSignUpEmailDomains": ["example.com"],
```

### Proveedor de identidad externo

Esta muestra admite proveedores de identidad externos. Actualmente soportamos [Google](./idp/SET_UP_GOOGLE_es-ES.md) y [proveedor OIDC personalizado](./idp/SET_UP_CUSTOM_OIDC_es-ES.md).

### WAF Frontend opcional

Para las distribuciones de CloudFront, los WebACLs de AWS WAF deben crearse en la región us-east-1. En algunas organizaciones, la creación de recursos fuera de la región principal está restringida por políticas. En tales entornos, el despliegue de CDK puede fallar al intentar aprovisionar el WAF Frontend en us-east-1.

Para adaptarse a estas restricciones, el stack del WAF Frontend es opcional. Cuando está deshabilitado, la distribución de CloudFront se despliega sin WebACL. Esto significa que no tendrá controles de permitir/denegar IP en el frontend edge. La autenticación y todos los demás controles de la aplicación siguen funcionando como de costumbre. Tenga en cuenta que esta configuración solo afecta al WAF Frontend (ámbito de CloudFront); el WAF de la API Publicada (regional) no se ve afectado.

Para deshabilitar el WAF Frontend, establezca lo siguiente en `parameter.ts` (Método recomendado con seguridad de tipos):

```ts
bedrockChatParams.set("default", {
  enableFrontendWaf: false
});
```

O si usa el legacy `cdk/cdk.json` establezca lo siguiente:

```json
"enableFrontendWaf": false
```

### Añadir nuevos usuarios a grupos automáticamente

Esta muestra tiene los siguientes grupos para dar permisos a los usuarios:

- [`Admin`](./ADMINISTRATOR_es-ES.md)
- [`CreatingBotAllowed`](#bot-personalization)
- [`PublishAllowed`](./PUBLISH_API_es-ES.md)

Si desea que los usuarios recién creados se unan automáticamente a grupos, puede especificarlos en [cdk.json](./cdk/cdk.json).

```json
"autoJoinUserGroups": ["CreatingBotAllowed"],
```

Por defecto, los usuarios recién creados se unirán al grupo `CreatingBotAllowed`.

### Configurar réplicas RAG

`enableRagReplicas` es una opción en [cdk.json](./cdk/cdk.json) que controla la configuración de réplicas para la base de datos RAG, específicamente las Bases de Conocimiento que utilizan Amazon OpenSearch Serverless.

- **Por defecto**: true
- **true**: Mejora la disponibilidad habilitando réplicas adicionales, haciéndolo adecuado para entornos de producción pero aumentando los costos.
- **false**: Reduce los costos usando menos réplicas, haciéndolo adecuado para desarrollo y pruebas.

Esta es una configuración a nivel de cuenta/región, que afecta a toda la aplicación en lugar de a bots individuales.

> [!Note]
> A partir de junio de 2024, Amazon OpenSearch Serverless admite 0.5 OCU, reduciendo los costos de entrada para cargas de trabajo a pequeña escala. Las implementaciones de producción pueden comenzar con 2 OCUs, mientras que las cargas de trabajo de desarrollo/prueba pueden usar 1 OCU. OpenSearch Serverless escala automáticamente según las demandas de carga de trabajo. Para más detalles, visite el [anuncio](https://aws.amazon.com/jp/about-aws/whats-new/2024/06/amazon-opensearch-serverless-entry-cost-half-collection-types/).

### Configurar Bot Store

La función de bot store permite a los usuarios compartir y descubrir bots personalizados. Puede configurar la bot store a través de las siguientes configuraciones en [cdk.json](./cdk/cdk.json):

```json
{
  "context": {
    "enableBotStore": true,
    "enableBotStoreReplicas": false,
    "botStoreLanguage": "en"
  }
}
```

- **enableBotStore**: Controla si la función de bot store está habilitada (por defecto: `true`)
- **botStoreLanguage**: Establece el idioma principal para la búsqueda y descubrimiento de bots (por defecto: `"en"`). Esto afecta cómo se indexan y buscan los bots en la bot store, optimizando el análisis de texto para el idioma especificado.
- **enableBotStoreReplicas**: Controla si las réplicas en espera están habilitadas para la colección OpenSearch Serverless utilizada por la bot store (por defecto: `false`). Establecerlo en `true` mejora la disponibilidad pero aumenta los costos, mientras que `false` reduce los costos pero puede afectar la disponibilidad.
  > **Importante**: No puede actualizar esta propiedad después de que la colección ya esté creada. Si intenta modificar esta propiedad, la colección continuará usando el valor original.

### Inferencia entre regiones

La [inferencia entre regiones](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html) permite que Amazon Bedrock enrute dinámicamente las solicitudes de inferencia de modelos a través de múltiples regiones de AWS, mejorando el rendimiento y la resistencia durante períodos de alta demanda. Para configurar, edite `cdk.json`.

```json
"enableBedrockCrossRegionInference": true
```

### Lambda SnapStart

[Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html) mejora los tiempos de inicio en frío para las funciones Lambda, proporcionando tiempos de respuesta más rápidos para una mejor experiencia de usuario. Por otro lado, para funciones Python, hay un [cargo dependiendo del tamaño de la caché](https://aws.amazon.com/lambda/pricing/#SnapStart_Pricing) y [no está disponible en algunas regiones](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions) actualmente. Para deshabilitar SnapStart, edite `cdk.json`.

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

- `alternateDomainName`: El nombre de dominio personalizado para su aplicación de chat (ej., chat.example.com)
- `hostedZoneId`: El ID de su zona alojada en Route 53 donde se crearán los registros DNS

Cuando se proporcionan estos parámetros, el despliegue automáticamente:

- Creará un certificado ACM con validación DNS en la región us-east-1
- Creará los registros DNS necesarios en su zona alojada de Route 53
- Configurará CloudFront para usar su dominio personalizado

> [!Note]
> El dominio debe estar gestionado por Route 53 en su cuenta de AWS. El ID de la zona alojada se puede encontrar en la consola de Route 53.

### Configurar países permitidos (restricción geográfica)

Puede restringir el acceso a Bedrock-Chat basándose en el país desde el que el cliente está accediendo.
Use el parámetro `allowedCountries` en [cdk.json](./cdk/cdk.json) que toma una lista de [Códigos de País ISO-3166](https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes).
Por ejemplo, una empresa basada en Nueva Zelanda puede decidir que solo las direcciones IP de Nueva Zelanda (NZ) y Australia (AU) pueden acceder al portal y todos los demás deben ser denegados.
Para configurar este comportamiento use la siguiente configuración en [cdk.json](./cdk/cdk.json):

```json
{
  "allowedCountries": ["NZ", "AU"]
}
```

O, usando `parameter.ts` (Método recomendado con seguridad de tipos):

```ts
// Define parameters for the default environment
bedrockChatParams.set("default", {
  allowedCountries: ["NZ", "AU"],
});
```

### Deshabilitar soporte IPv6

El frontend obtiene direcciones IP e IPv6 por defecto. En algunas circunstancias raras, puede necesitar deshabilitar explícitamente el soporte IPv6. Para hacer esto, establezca el siguiente parámetro en [parameter.ts](./cdk/parameter.ts) o de manera similar en [cdk.json](./cdk/cdk.json):

```ts
"enableFrontendIpv6": false
```

Si se deja sin establecer, el soporte IPv6 estará habilitado por defecto.

### Desarrollo local

Ver [LOCAL DEVELOPMENT](./LOCAL_DEVELOPMENT_es-ES.md).

### Contribución

¡Gracias por considerar contribuir a este repositorio! Damos la bienvenida a correcciones de errores, traducciones de idiomas (i18n), mejoras de funcionalidades, [herramientas de agente](./docs/AGENT.md#how-to-develop-your-own-tools), y otras mejoras.

Para mejoras de funcionalidades y otras mejoras, **antes de crear un Pull Request, agradeceríamos mucho si pudiera crear un Issue de Solicitud de Funcionalidad para discutir el enfoque de implementación y los detalles. Para correcciones de errores y traducciones de idiomas (i18n), proceda a crear un Pull Request directamente.**

Por favor, también revise las siguientes pautas antes de contribuir:

- [Desarrollo Local](./LOCAL_DEVELOPMENT_es-ES.md)
- [CONTRIBUTING](./CONTRIBUTING_es-ES.md)

## Contactos

- [Takehiro Suzuki](https://github.com/statefb)
- [Yusuke Wada](https://github.com/wadabee)
- [Yukinobu Mine](https://github.com/Yukinobu-Mine)

## 🏆 Contribuyentes Destacados

- [fsatsuki](https://github.com/fsatsuki)
- [k70suK3-k06a7ash1](https://github.com/k70suK3-k06a7ash1)

## Colaboradores

[![bedrock chat contributors](https://contrib.rocks/image?repo=aws-samples/bedrock-chat&max=1000)](https://github.com/aws-samples/bedrock-chat/graphs/contributors)

## Licencia

Esta biblioteca está licenciada bajo la Licencia MIT-0. Consulte [el archivo LICENSE](./LICENSE).