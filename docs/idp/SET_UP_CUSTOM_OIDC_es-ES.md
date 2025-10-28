# Configurar proveedor de identidad externo

## Paso 1: Crear un Cliente OIDC

Sigue los procedimientos para el proveedor OIDC objetivo, y anota los valores del ID de cliente OIDC y el secreto. La URL del emisor también es necesaria en los siguientes pasos. Si se necesita una URI de redirección durante el proceso de configuración, introduce un valor temporal, que será reemplazado una vez que se complete la implementación.

## Paso 2: Almacenar Credenciales en AWS Secrets Manager

1. Ve a la Consola de Administración de AWS.
2. Navega hasta Secrets Manager y selecciona "Almacenar un nuevo secreto".
3. Selecciona "Otro tipo de secretos".
4. Introduce el ID de cliente y el secreto de cliente como pares clave-valor.

   - Clave: `clientId`, Valor: <YOUR_GOOGLE_CLIENT_ID>
   - Clave: `clientSecret`, Valor: <YOUR_GOOGLE_CLIENT_SECRET>
   - Clave: `issuerUrl`, Valor: <ISSUER_URL_OF_THE_PROVIDER>

5. Sigue las indicaciones para nombrar y describir el secreto. Anota el nombre del secreto ya que lo necesitarás en tu código CDK (Usado en el Paso 3 como nombre de variable <YOUR_SECRET_NAME>).
6. Revisa y almacena el secreto.

### Atención

Los nombres de las claves deben coincidir exactamente con las cadenas `clientId`, `clientSecret` y `issuerUrl`.

## Paso 3: Actualizar cdk.json

En tu archivo cdk.json, añade el ID Provider y SecretName al archivo cdk.json.

de esta manera:

```json
{
  "context": {
    // ...
    "identityProviders": [
      {
        "service": "oidc", // No modificar
        "serviceName": "<YOUR_SERVICE_NAME>", // Establece el valor que desees
        "secretName": "<YOUR_SECRET_NAME>"
      }
    ],
    "userPoolDomainPrefix": "<UNIQUE_DOMAIN_PREFIX_FOR_YOUR_USER_POOL>"
  }
}
```

### Atención

#### Unicidad

El `userPoolDomainPrefix` debe ser globalmente único entre todos los usuarios de Amazon Cognito. Si eliges un prefijo que ya está en uso por otra cuenta de AWS, la creación del dominio del grupo de usuarios fallará. Es una buena práctica incluir identificadores, nombres de proyecto o nombres de entorno en el prefijo para garantizar la unicidad.

## Paso 4: Desplegar tu Stack de CDK

Despliega tu stack de CDK en AWS:

```sh
npx cdk deploy --require-approval never --all
```

## Paso 5: Actualizar el Cliente OIDC con las URIs de Redirección de Cognito

Después de desplegar el stack, `AuthApprovedRedirectURI` se muestra en las salidas de CloudFormation. Vuelve a tu configuración de OIDC y actualiza con las URIs de redirección correctas.