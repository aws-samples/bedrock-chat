<h1 align="center">Chat de Bedrock (BrChat)</h1>

<p align="center">
  <img src="https://img.shields.io/github/v/release/aws-samples/bedrock-chat?style=flat-square" />
  <img src="https://img.shields.io/github/license/aws-samples/bedrock-chat?style=flat-square" />
  <img src="https://img.shields.io/github/actions/workflow/status/aws-samples/bedrock-chat/cdk.yml?style=flat-square" />
  <a href="https://github.com/aws-samples/bedrock-chat/issues?q=is%3Aissue%20state%3Aopen%20label%3Aroadmap">
    <img src="https://img.shields.io/badge/roadmap-view-blue?style=flat-square" />
  </a>
</p>

[English](https://github.com/aws-samples/bedrock-chat/blob/v3/README.md) | [日本語](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_ja-JP.md) | [한국어](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_ko-KR.md) | [中文](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_zh-CN.md) | [Français](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_fr-FR.md) | [Deutsch](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_de-DE.md) | [Español](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_es-ES.md) | [Italian](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_it-IT.md) | [Norsk](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_nb-NO.md) | [ไทย](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_th-TH.md) | [Bahasa Indonesia](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_id-ID.md) | [Bahasa Melayu](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_ms-MY.md) | [Tiếng Việt](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_vi-VN.md) | [Polski](https://github.com/aws-samples/bedrock-chat/blob/v3/docs/README_pl-PL.md)

Una plataforma de IA generativa multilingüe impulsada por [Amazon Bedrock](https://aws.amazon.com/bedrock/).
Admite chat, bots personalizados con conocimiento (RAG), compartir bots a través de una tienda de bots y automatización de tareas mediante agentes.

![](./imgs/demo.gif)

> [!Advertencia]
>
> **V3 lanzada. Para actualizar, revise cuidadosamente la [guía de migración](./migration/V2_TO_V3_es-ES.md).** Sin ningún cuidado, **LOS BOTS DE V2 SE VOLVERÁN INUTILIZABLES.**

### Personalización de Bots / Tienda de Bots

Agregue su propia instrucción y conocimiento (también conocido como [RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)). El bot puede compartirse entre los usuarios de la aplicación a través del mercado de la tienda de bots. El bot personalizado también puede publicarse como API independiente (Consulte los [detalles](./PUBLISH_API_es-ES.md)).

<details>
<summary>Capturas de pantalla</summary>

![](./imgs/customized_bot_creation.png)
![](./imgs/fine_grained_permission.png)
![](./imgs/bot_store.png)
![](./imgs/bot_api_publish_screenshot3.png)

También puede importar [Bases de Conocimiento existentes de Amazon Bedrock](https://aws.amazon.com/bedrock/knowledge-bases/).

![](./imgs/import_existing_kb.png)

</details>

> [!Importante]
> Por razones de gobernanza, solo los usuarios autorizados pueden crear bots personalizados. Para permitir la creación de bots personalizados, el usuario debe ser miembro del grupo llamado `CreatingBotAllowed`, que se puede configurar a través de la consola de administración > Grupos de usuarios de Amazon Cognito o la CLI de AWS. Tenga en cuenta que el ID del grupo de usuarios se puede consultar accediendo a CloudFormation > BedrockChatStack > Salidas > `AuthUserPoolIdxxxx`.

### Características administrativas

Gestión de API, marcar bots como esenciales, analizar el uso de bots. [detalles](./ADMINISTRATOR_es-ES.md)

<details>
<summary>Capturas de pantalla</summary>

![](./imgs/admin_bot_menue.png)
![](./imgs/bot_store.png)
![](./imgs/admn_api_management.png)
![](./imgs/admin_bot_analytics.png))

</details>

### Agente

Utilizando la [funcionalidad de Agente](./AGENT_es-ES.md), su chatbot puede manejar automáticamente tareas más complejas. Por ejemplo, para responder a la pregunta de un usuario, el Agente puede recuperar información necesaria de herramientas externas o dividir la tarea en varios pasos para su procesamiento.

<details>
<summary>Capturas de pantalla</summary>

![](./imgs/agent1.png)
![](./imgs/agent2.png)

</details>

## 🚀 Despliegue súper fácil

- En la región us-east-1, abra [Acceso al modelo Bedrock](https://us-east-1.console.aws.amazon.com/bedrock/home?region=us-east-1#/modelaccess) > `Administrar acceso a modelos` > Marque todos los modelos que desee usar y luego `Guardar cambios`.

<details>
<summary>Captura de pantalla</summary>

![](./imgs/model_screenshot.png)

</details>

- Abra [CloudShell](https://console.aws.amazon.com/cloudshell/home) en la región donde desee implementar
- Ejecute la implementación mediante los siguientes comandos. Si desea especificar la versión para implementar o necesita aplicar políticas de seguridad, especifique los parámetros apropiados de [Parámetros opcionales](#parámetros-opcionales).

```sh
git clone https://github.com/aws-samples/bedrock-chat.git
cd bedrock-chat
chmod +x bin.sh
./bin.sh
```

- Se le preguntará si es un usuario nuevo o si está usando v3. Si no es un usuario continuado desde v0, introduzca `y`.

### Parámetros opcionales

Puede especificar los siguientes parámetros durante la implementación para mejorar la seguridad y la personalización:

- **--disable-self-register**: Desactivar el registro automático (predeterminado: habilitado). Si se establece esta bandera, deberá crear todos los usuarios en Cognito y no se permitirá a los usuarios registrarse por sí mismos.
- **--enable-lambda-snapstart**: Habilitar [Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html) (predeterminado: desactivado). Si se establece esta bandera, mejora los tiempos de arranque en frío para las funciones Lambda, proporcionando tiempos de respuesta más rápidos para una mejor experiencia de usuario.
- **--ipv4-ranges**: Lista separada por comas de rangos IPv4 permitidos. (predeterminado: permitir todas las direcciones IPv4)
- **--ipv6-ranges**: Lista separada por comas de rangos IPv6 permitidos. (predeterminado: permitir todas las direcciones IPv6)
- **--disable-ipv6**: Desactivar conexiones sobre IPv6. (predeterminado: habilitado)
- **--allowed-signup-email-domains**: Lista separada por comas de dominios de correo electrónico permitidos para el registro. (predeterminado: sin restricción de dominio)
- **--bedrock-region**: Definir la región donde Bedrock está disponible. (predeterminado: us-east-1)
- **--repo-url**: El repositorio personalizado de Bedrock Chat para implementar, si está bifurcado o se utiliza un control de origen personalizado. (predeterminado: https://github.com/aws-samples/bedrock-chat.git)
- **--version**: La versión de Bedrock Chat para implementar. (predeterminado: última versión en desarrollo)
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

El JSON de anulación debe seguir la misma estructura que cdk.json. Puede anular cualquier valor de contexto, incluidos:

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

- Después de unos 35 minutos, obtendrá la siguiente salida, a la que podrá acceder desde su navegador

```
Frontend URL: https://xxxxxxxxx.cloudfront.net
```

![](./imgs/signin.png)

Aparecerá la pantalla de registro como se muestra arriba, donde podrá registrar su correo electrónico e iniciar sesión.

> [!Importante]
> Sin establecer el parámetro opcional, este método de implementación permite que cualquiera que conozca la URL se registre. Para uso en producción, se recomienda encarecidamente agregar restricciones de dirección IP y desactivar el registro automático para mitigar los riesgos de seguridad (puede definir allowed-signup-email-domains para restringir a los usuarios de modo que solo puedan registrarse direcciones de correo electrónico del dominio de su empresa). Use tanto ipv4-ranges como ipv6-ranges para las restricciones de direcciones IP y desactive el registro automático mediante disable-self-register al ejecutar ./bin.

> [!CONSEJO]
> Si la `URL de frontend` no aparece o Bedrock Chat no funciona correctamente, puede ser un problema con la última versión. En este caso, agregue `--version "v3.0.0"` a los parámetros e intente la implementación de nuevo.

## Arquitectura

Es una arquitectura construida sobre servicios administrados de AWS, eliminando la necesidad de gestionar infraestructura. Utilizando Amazon Bedrock, no es necesario comunicarse con APIs fuera de AWS. Esto permite implementar aplicaciones escalables, confiables y seguras.

- [Amazon DynamoDB](https://aws.amazon.com/dynamodb/): Base de datos NoSQL para almacenar el historial de conversaciones
- [Amazon API Gateway](https://aws.amazon.com/api-gateway/) + [AWS Lambda](https://aws.amazon.com/lambda/): Punto de enlace de API de backend ([AWS Lambda Web Adapter](https://github.com/awslabs/aws-lambda-web-adapter), [FastAPI](https://fastapi.tiangolo.com/))
- [Amazon CloudFront](https://aws.amazon.com/cloudfront/) + [S3](https://aws.amazon.com/s3/): Entrega de aplicación frontend ([React](https://react.dev/), [Tailwind CSS](https://tailwindcss.com/))
- [AWS WAF](https://aws.amazon.com/waf/): Restricción de direcciones IP
- [Amazon Cognito](https://aws.amazon.com/cognito/): Autenticación de usuarios
- [Amazon Bedrock](https://aws.amazon.com/bedrock/): Servicio administrado para utilizar modelos fundamentales a través de APIs
- [Amazon Bedrock Knowledge Bases](https://aws.amazon.com/bedrock/knowledge-bases/): Proporciona una interfaz administrada para Generación Aumentada por Recuperación ([RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)), ofreciendo servicios para incrustar y analizar documentos
- [Amazon EventBridge Pipes](https://aws.amazon.com/eventbridge/pipes/): Recepción de eventos del flujo de DynamoDB e inicio de Step Functions para incrustar conocimiento externo
- [AWS Step Functions](https://aws.amazon.com/step-functions/): Orquestación de la canalización de ingesta para incrustar conocimiento externo en Bedrock Knowledge Bases
- [Amazon OpenSearch Serverless](https://aws.amazon.com/opensearch-service/features/serverless/): Sirve como base de datos backend para Bedrock Knowledge Bases, proporcionando capacidades de búsqueda de texto completo y búsqueda vectorial, permitiendo la recuperación precisa de información relevante
- [Amazon Athena](https://aws.amazon.com/athena/): Servicio de consultas para analizar bucket de S3

![](./imgs/arch.png)

## Desplegar usando CDK

El despliegue súper fácil utiliza [AWS CodeBuild](https://aws.amazon.com/codebuild/) para realizar el despliegue internamente con CDK. Esta sección describe el procedimiento para desplegar directamente con CDK.

- Por favor, tenga un entorno con UNIX, Docker y un entorno de ejecución de Node.js. Si no lo tiene, también puede usar [Cloud9](https://github.com/aws-samples/cloud9-setup-for-prototyping)

> [!Importante]
> Si hay espacio de almacenamiento insuficiente en el entorno local durante el despliegue, el arranque de CDK puede resultar en un error. Si está ejecutando en Cloud9, etc., recomendamos expandir el tamaño del volumen de la instancia antes de desplegar.

- Clonar este repositorio

```
git clone https://github.com/aws-samples/bedrock-chat
```

- Instalar paquetes npm

```
cd bedrock-chat
cd cdk
npm ci
```

- Si es necesario, edite las siguientes entradas en [cdk.json](./cdk/cdk.json) si es necesario.

  - `bedrockRegion`: Región donde Bedrock está disponible. **NOTA: Bedrock NO es compatible con todas las regiones por ahora.**
  - `allowedIpV4AddressRanges`, `allowedIpV6AddressRanges`: Rango de direcciones IP permitidas.
  - `enableLambdaSnapStart`: Por defecto es verdadero. Establézcalo en falso si despliega en una [región que no es compatible con Lambda SnapStart para funciones de Python](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions).

- Antes de desplegar CDK, necesitará trabajar con Bootstrap una vez para la región en la que va a desplegar.

```
npx cdk bootstrap
```

- Desplegar este proyecto de ejemplo

```
npx cdk deploy --require-approval never --all
```

- Obtendrá una salida similar a la siguiente. La URL de la aplicación web se mostrará en `BedrockChatStack.FrontendURL`, así que acceda a ella desde su navegador.

```sh
 ✅  BedrockChatStack

✨  Tiempo de despliegue: 78.57s

Salidas:
BedrockChatStack.AuthUserPoolClientIdXXXXX = xxxxxxx
BedrockChatStack.AuthUserPoolIdXXXXXX = ap-northeast-1_XXXX
BedrockChatStack.BackendApiBackendApiUrlXXXXX = https://xxxxx.execute-api.ap-northeast-1.amazonaws.com
BedrockChatStack.FrontendURL = https://xxxxx.cloudfront.net
```

### Definiendo Parámetros

Puede definir parámetros para su despliegue de dos maneras: usando `cdk.json` o usando el archivo `parameter.ts` con tipado seguro.

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

#### Usando parameter.ts (Método Recomendado con Tipado Seguro)

Para una mejor seguridad de tipos y experiencia de desarrollo, puede usar el archivo `parameter.ts` para definir sus parámetros:

```typescript
// Definir parámetros para el entorno predeterminado
bedrockChatParams.set("default", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["192.168.0.0/16"],
  selfSignUpEnabled: true,
});

// Definir parámetros para entornos adicionales
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
  enableRagReplicas: true, // Mayor disponibilidad para producción
  enableBotStoreReplicas: true, // Mayor disponibilidad para producción
});
```

> [!Nota]
> Los usuarios existentes pueden continuar usando `cdk.json` sin ningún cambio. El enfoque de `parameter.ts` se recomienda para nuevos despliegues o cuando necesite administrar múltiples entornos.

### Desplegando Múltiples Entornos

Puede desplegar múltiples entornos desde la misma base de código utilizando el archivo `parameter.ts` y la opción `-c envName`.

#### Requisitos Previos

1. Defina sus entornos en `parameter.ts` como se muestra anteriormente
2. Cada entorno tendrá su propio conjunto de recursos con prefijos específicos del entorno

#### Comandos de Despliegue

Para desplegar un entorno específico:

```bash
# Desplegar el entorno de desarrollo
npx cdk deploy --all -c envName=dev

# Desplegar el entorno de producción
npx cdk deploy --all -c envName=prod
```

Si no se especifica ningún entorno, se utiliza el entorno "default":

```bash
# Desplegar el entorno predeterminado
npx cdk deploy --all
```

#### Notas Importantes

1. **Nomenclatura de Stacks**:

   - Los stacks principales para cada entorno tendrán un prefijo con el nombre del entorno (por ejemplo, `dev-BedrockChatStack`, `prod-BedrockChatStack`)
   - Sin embargo, los stacks de bots personalizados (`BrChatKbStack*`) y los stacks de publicación de API (`ApiPublishmentStack*`) no reciben prefijos de entorno ya que se crean dinámicamente en tiempo de ejecución

2. **Nomenclatura de Recursos**:

   - Solo algunos recursos reciben prefijos de entorno en sus nombres (por ejemplo, tabla `dev_ddb_export`, `dev-FrontendWebAcl`)
   - La mayoría de los recursos mantienen sus nombres originales pero están aislados al estar en diferentes stacks

3. **Identificación de Entornos**:

   - Todos los recursos están etiquetados con una etiqueta `CDKEnvironment` que contiene el nombre del entorno
   - Puede usar esta etiqueta para identificar a qué entorno pertenece un recurso
   - Ejemplo: `CDKEnvironment: dev` o `CDKEnvironment: prod`

4. **Anulación de Entorno Predeterminado**: Si define un entorno "default" en `parameter.ts`, anulará la configuración en `cdk.json`. Para continuar usando `cdk.json`, no defina un entorno "default" en `parameter.ts`.

5. **Requisitos de Entorno**: Para crear entornos distintos de "default", debe usar `parameter.ts`. La opción `-c envName` por sí sola no es suficiente sin definiciones de entorno correspondientes.

6. **Aislamiento de Recursos**: Cada entorno crea su propio conjunto de recursos, lo que le permite tener entornos de desarrollo, pruebas y producción en la misma cuenta de AWS sin conflictos.

## Otros

Puede definir parámetros para su implementación de dos formas: usando `cdk.json` o usando el archivo de tipo seguro `parameter.ts`.

#### Usando cdk.json (Método Tradicional)

La forma tradicional de configurar parámetros es editando el archivo `cdk.json`. Este enfoque es simple pero carece de comprobación de tipos:

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

#### Usando parameter.ts (Método Recomendado de Tipo Seguro)

Para una mayor seguridad de tipos y experiencia de desarrollo, puede usar el archivo `parameter.ts` para definir sus parámetros:

```typescript
// Definir parámetros para el entorno predeterminado
bedrockChatParams.set("default", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["192.168.0.0/16"],
  selfSignUpEnabled: true,
});

// Definir parámetros para entornos adicionales
bedrockChatParams.set("dev", {
  bedrockRegion: "us-west-2",
  allowedIpV4AddressRanges: ["10.0.0.0/8"],
  enableRagReplicas: false, // Ahorro de costes para entorno de desarrollo
});

bedrockChatParams.set("prod", {
  bedrockRegion: "us-east-1",
  allowedIpV4AddressRanges: ["172.16.0.0/12"],
  enableLambdaSnapStart: true,
  enableRagReplicas: true, // Mayor disponibilidad para producción
});
```

> [!Nota]
> Los usuarios existentes pueden continuar usando `cdk.json` sin ningún cambio. Se recomienda el enfoque de `parameter.ts` para nuevas implementaciones o cuando necesite administrar varios entornos.

### Implementación de Múltiples Entornos

Puede implementar varios entornos desde el mismo código base utilizando el archivo `parameter.ts` y la opción `-c envName`.

#### Requisitos Previos

1. Defina sus entornos en `parameter.ts` como se muestra arriba
2. Cada entorno tendrá su propio conjunto de recursos con prefijos específicos del entorno

#### Comandos de Implementación

Para implementar un entorno específico:

```bash
# Implementar el entorno de desarrollo
npx cdk deploy --all -c envName=dev

# Implementar el entorno de producción
npx cdk deploy --all -c envName=prod
```

Si no se especifica ningún entorno, se utiliza el entorno "default":

```bash
# Implementar el entorno predeterminado
npx cdk deploy --all
```

#### Notas Importantes

1. **Nomenclatura de Pilas**:

   - Las pilas principales para cada entorno tendrán un prefijo con el nombre del entorno (por ejemplo, `dev-BedrockChatStack`, `prod-BedrockChatStack`)
   - Sin embargo, las pilas de bots personalizados (`BrChatKbStack*`) y las pilas de publicación de API (`ApiPublishmentStack*`) no reciben prefijos de entorno ya que se crean dinámicamente en tiempo de ejecución

2. **Nomenclatura de Recursos**:

   - Solo algunos recursos reciben prefijos de entorno en sus nombres (por ejemplo, tabla `dev_ddb_export`, `dev-FrontendWebAcl`)
   - La mayoría de los recursos mantienen sus nombres originales pero están aislados al estar en diferentes pilas

3. **Identificación de Entorno**:

   - Todos los recursos están etiquetados con una etiqueta `CDKEnvironment` que contiene el nombre del entorno
   - Puede usar esta etiqueta para identificar a qué entorno pertenece un recurso
   - Ejemplo: `CDKEnvironment: dev` o `CDKEnvironment: prod`

4. **Anulación de Entorno Predeterminado**: Si define un entorno "default" en `parameter.ts`, anulará la configuración en `cdk.json`. Para continuar usando `cdk.json`, no defina un entorno "default" en `parameter.ts`.

5. **Requisitos de Entorno**: Para crear entornos distintos de "default", debe usar `parameter.ts`. La opción `-c envName` por sí sola no es suficiente sin las definiciones de entorno correspondientes.

6. **Aislamiento de Recursos**: Cada entorno crea su propio conjunto de recursos, lo que le permite tener entornos de desarrollo, pruebas y producción en la misma cuenta de AWS sin conflictos.

## Otros

### Eliminar recursos

Si está utilizando CLI y CDK, use `npx cdk destroy`. Si no, acceda a [CloudFormation](https://console.aws.amazon.com/cloudformation/home) y luego elimine manualmente `BedrockChatStack` y `FrontendWafStack`. Tenga en cuenta que `FrontendWafStack` está en la región `us-east-1`.

### Configuración de idioma

Este recurso detecta automáticamente el idioma utilizando [i18next-browser-languageDetector](https://github.com/i18next/i18next-browser-languageDetector). Puede cambiar de idioma desde el menú de la aplicación. Alternativamente, puede usar Query String para establecer el idioma como se muestra a continuación.

> `https://example.com?lng=ja`

### Desactivar registro automático

Este ejemplo tiene el registro automático habilitado de forma predeterminada. Para desactivarlo, abra [cdk.json](./cdk/cdk.json) y cambie `selfSignUpEnabled` a `false`. Si configura un [proveedor de identidad externo](#proveedor-de-identidad-externo), este valor se ignorará y se desactivará automáticamente.

### Restringir dominios para direcciones de correo electrónico de registro

De forma predeterminada, este ejemplo no restringe los dominios para las direcciones de correo electrónico de registro. Para permitir registros solo desde dominios específicos, abra `cdk.json` y especifique los dominios como una lista en `allowedSignUpEmailDomains`.

```ts
"allowedSignUpEmailDomains": ["example.com"],
```

### Proveedor de identidad externo

Este ejemplo admite un proveedor de identidad externo. Actualmente, se admiten [Google](./idp/SET_UP_GOOGLE_es-ES.md) y [proveedor OIDC personalizado](./idp/SET_UP_CUSTOM_OIDC_es-ES.md).

### Agregar nuevos usuarios a grupos automáticamente

Este ejemplo tiene los siguientes grupos para dar permisos a los usuarios:

- [`Admin`](./ADMINISTRATOR_es-ES.md)
- [`CreatingBotAllowed`](#bot-personalization)
- [`PublishAllowed`](./PUBLISH_API_es-ES.md)

Si desea que los usuarios recién creados se unan automáticamente a grupos, puede especificarlos en [cdk.json](./cdk/cdk.json).

```json
"autoJoinUserGroups": ["CreatingBotAllowed"],
```

De forma predeterminada, los usuarios recién creados se unirán al grupo `CreatingBotAllowed`.

### Configurar réplicas de RAG

`enableRagReplicas` es una opción en [cdk.json](./cdk/cdk.json) que controla la configuración de réplicas para la base de datos RAG, específicamente las Bases de Conocimiento que utilizan Amazon OpenSearch Serverless.

- **Predeterminado**: true
- **true**: Mejora la disponibilidad al habilitar réplicas adicionales, lo que lo hace adecuado para entornos de producción, pero aumenta los costos.
- **false**: Reduce los costos utilizando menos réplicas, lo que lo hace adecuado para desarrollo y pruebas.

Esta es una configuración a nivel de cuenta/región que afecta a toda la aplicación, no a bots individuales.

> [!Nota]
> A partir de junio de 2024, Amazon OpenSearch Serverless admite 0.5 OCU, reduciendo los costos de entrada para cargas de trabajo a pequeña escala. Las implementaciones de producción pueden comenzar con 2 OCU, mientras que las cargas de trabajo de desarrollo/pruebas pueden usar 1 OCU. OpenSearch Serverless escala automáticamente según la demanda de carga de trabajo. Para más detalles, visite [anuncio](https://aws.amazon.com/jp/about-aws/whats-new/2024/06/amazon-opensearch-serverless-entry-cost-half-collection-types/).

### Configurar Bot Store

La función de bot store permite a los usuarios compartir y descubrir bots personalizados. Puede configurar el bot store a través de los siguientes ajustes en [cdk.json](./cdk/cdk.json):

```json
{
  "context": {
    "enableBotStore": true,
    "enableBotStoreReplicas": false,
    "botStoreLanguage": "en"
  }
}
```

- **enableBotStore**: Controla si la función de bot store está habilitada (predeterminado: `true`)
- **botStoreLanguage**: Establece el idioma principal para la búsqueda y descubrimiento de bots (predeterminado: `"en"`). Esto afecta cómo se indexan y buscan los bots en el bot store, optimizando el análisis de texto para el idioma especificado.
- **enableBotStoreReplicas**: Controla si se habilitan réplicas en espera para la colección de OpenSearch Serverless utilizada por el bot store (predeterminado: `false`). Establecerlo en `true` mejora la disponibilidad pero aumenta los costos, mientras que `false` reduce los costos pero puede afectar la disponibilidad.
  > **Importante**: No puede actualizar esta propiedad una vez que la colección ya ha sido creada. Si intenta modificar esta propiedad, la colección continuará utilizando el valor original.

### Inferencia entre regiones

La [inferencia entre regiones](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html) permite que Amazon Bedrock enrute dinámicamente las solicitudes de inferencia de modelos entre múltiples regiones de AWS, mejorando el rendimiento y la resistencia durante períodos de alta demanda. Para configurarlo, edite `cdk.json`.

```json
"enableBedrockCrossRegionInference": true
```

### Lambda SnapStart

[Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html) mejora los tiempos de inicio en frío para las funciones Lambda, proporcionando tiempos de respuesta más rápidos para una mejor experiencia de usuario. Por otro lado, para funciones de Python, hay un [cargo dependiendo del tamaño de caché](https://aws.amazon.com/lambda/pricing/#SnapStart_Pricing) y [no está disponible en algunas regiones](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions) actualmente. Para desactivar SnapStart, edite `cdk.json`.

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
> El dominio debe ser administrado por Route 53 en su cuenta de AWS. El ID de la zona alojada se puede encontrar en la consola de Route 53.

### Desarrollo local

Consulte [DESARROLLO LOCAL](./LOCAL_DEVELOPMENT_es-ES.md).

### Contribución

¡Gracias por considerar contribuir a este repositorio! Damos la bienvenida a correcciones de errores, traducciones de idiomas (i18n), mejoras de características, [herramientas de agente](./docs/AGENT.md#how-to-develop-your-own-tools) y otras mejoras.

Para mejoras de características y otras mejoras, **antes de crear una Solicitud de Extracción, le agradeceríamos mucho que creara un Issue de Solicitud de Característica para discutir el enfoque de implementación y los detalles. Para correcciones de errores y traducciones de idiomas (i18n), proceda directamente a crear una Solicitud de Extracción.**

Por favor, eche un vistazo también a las siguientes pautas antes de contribuir:

- [Desarrollo local](./LOCAL_DEVELOPMENT_es-ES.md)
- [CONTRIBUCIÓN](./CONTRIBUTING_es-ES.md)

## Contactos

- [Takehiro Suzuki](https://github.com/statefb)
- [Yusuke Wada](https://github.com/wadabee)
- [Yukinobu Mine](https://github.com/Yukinobu-Mine)

## 🏆 Contribuidores Significativos

- [fsatsuki](https://github.com/fsatsuki)
- [k70suK3-k06a7ash1](https://github.com/k70suK3-k06a7ash1)

## Colaboradores

[![colaboradores de bedrock chat](https://contrib.rocks/image?repo=aws-samples/bedrock-chat&max=1000)](https://github.com/aws-samples/bedrock-chat/graphs/contributors)

## Licencia

Esta biblioteca está licenciada bajo la Licencia MIT-0. Consulte [el archivo de LICENCIA](./LICENSE).