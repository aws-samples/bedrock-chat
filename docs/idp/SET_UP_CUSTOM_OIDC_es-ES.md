# Configurar proveedor de identidad externo

## Paso 1: Crear un Cliente OIDC

Siga los procedimientos del proveedor OIDC de destino y anote los valores del ID de cliente OIDC y el secreto. También se requiere la URL del emisor en los siguientes pasos. Si se necesita un URI de redirección para el proceso de configuración, introduzca un valor ficticio, que se reemplazará después de completar la implementación.

## Paso 2: Almacenar Credenciales en AWS Secrets Manager

1. Vaya a la Consola de Administración de AWS.
2. Navegue hasta Secrets Manager y elija "Almacenar un nuevo secreto".
3. Seleccione "Otro tipo de secretos".
4. Introduzca el ID de cliente y el secreto de cliente como pares de clave-valor.

   - Clave: `clientId`, Valor: <YOUR_GOOGLE_CLIENT_ID>
   - Clave: `clientSecret`, Valor: <YOUR_GOOGLE_CLIENT_SECRET>
   - Clave: `issuerUrl`, Valor: <ISSUER_URL_OF_THE_PROVIDER>

5. Siga las indicaciones para nombrar y describir el secreto. Anote el nombre del secreto, ya que lo necesitará en su código CDK (Utilizado en el nombre de variable <YOUR_SECRET_NAME> del Paso 3).
6. Revise y almacene el secreto.

### Atención

Los nombres de las claves deben coincidir exactamente con las cadenas `clientId`, `clientSecret` e `issuerUrl`.

## Paso 3: Actualizar cdk.json

En su archivo cdk.json, agregue el Proveedor de Identidad y el Nombre del Secreto al archivo cdk.json.

de la siguiente manera:

```json
{
  "context": {
    // ...
    "identityProviders": [
      {
        "service": "oidc", // No cambiar
        "serviceName": "<SU_NOMBRE_DE_SERVICIO>", // Establezca cualquier valor que desee
        "secretName": "<SU_NOMBRE_DE_SECRETO>"
      }
    ],
    "userPoolDomainPrefix": "<PREFIJO_DE_DOMINIO_ÚNICO_PARA_SU_USER_POOL>"
  }
}
```

### Atención

#### Unicidad

El `userPoolDomainPrefix` debe ser único globalmente entre todos los usuarios de Amazon Cognito. Si elige un prefijo que ya está en uso por otra cuenta de AWS, la creación del dominio del grupo de usuarios fallará. Es una buena práctica incluir identificadores, nombres de proyectos o nombres de entornos en el prefijo para garantizar la unicidad.

## Paso 4: Desplegar Tu Stack de CDK

Despliega tu stack de CDK en AWS:

```sh
npx cdk deploy --require-approval never --all
```

## Paso 5: Actualizar el Cliente OIDC con las URI de Redireccionamiento de Cognito

Después de desplegar la pila, `AuthApprovedRedirectURI` se mostrará en las salidas de CloudFormation. Vuelva a su configuración de OIDC y actualice con las URI de redireccionamiento correctas.