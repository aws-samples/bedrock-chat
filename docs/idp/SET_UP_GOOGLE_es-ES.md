# Configurar proveedor de identidad externo para Google

## Paso 1: Crear un Cliente OAuth 2.0 de Google

1. Ve a la Consola de Desarrolladores de Google.
2. Crea un nuevo proyecto o selecciona uno existente.
3. Navega a "Credenciales", luego haz clic en "Crear credenciales" y elige "ID de cliente OAuth".
4. Configura la pantalla de consentimiento si se te solicita.
5. Para el tipo de aplicación, selecciona "Aplicación web".
6. Deja el URI de redirección en blanco por ahora para configurarlo más tarde, y guarda temporalmente.[Ver Paso 5](#step-5-update-google-oauth-client-with-cognito-redirect-uris)
7. Una vez creado, anota el ID de Cliente y el Secreto de Cliente.

Para más detalles, visita [el documento oficial de Google](https://support.google.com/cloud/answer/6158849?hl=en)

## Paso 2: Almacenar las Credenciales de Google OAuth en AWS Secrets Manager

1. Ve a la Consola de Administración de AWS.
2. Navega hasta Secrets Manager y selecciona "Almacenar un nuevo secreto".
3. Selecciona "Otro tipo de secretos".
4. Introduce el clientId y clientSecret de Google OAuth como pares clave-valor.

   1. Clave: clientId, Valor: <YOUR_GOOGLE_CLIENT_ID>
   2. Clave: clientSecret, Valor: <YOUR_GOOGLE_CLIENT_SECRET>

5. Sigue las indicaciones para nombrar y describir el secreto. Anota el nombre del secreto ya que lo necesitarás en tu código CDK. Por ejemplo, googleOAuthCredentials. (Usar en el Paso 3 el nombre de variable <YOUR_SECRET_NAME>)
6. Revisa y almacena el secreto.

### Atención

Los nombres de las claves deben coincidir exactamente con las cadenas 'clientId' y 'clientSecret'.

## Paso 3: Actualizar cdk.json

En tu archivo cdk.json, añade el Proveedor de ID y SecretName al archivo cdk.json.

de esta manera:

```json
{
  "context": {
    // ...
    "identityProviders": [
      {
        "service": "google",
        "secretName": "<YOUR_SECRET_NAME>"
      }
    ],
    "userPoolDomainPrefix": "<UNIQUE_DOMAIN_PREFIX_FOR_YOUR_USER_POOL>"
  }
}
```

### Atención

#### Unicidad

El userPoolDomainPrefix debe ser globalmente único entre todos los usuarios de Amazon Cognito. Si eliges un prefijo que ya está en uso por otra cuenta de AWS, la creación del dominio del grupo de usuarios fallará. Es una buena práctica incluir identificadores, nombres de proyecto o nombres de entorno en el prefijo para garantizar la unicidad.

## Paso 4: Desplegar Tu Stack de CDK

Despliega tu stack de CDK en AWS:

```sh
npx cdk deploy --require-approval never --all
```

## Paso 5: Actualizar el Cliente OAuth de Google con las URIs de Redirección de Cognito

Después de desplegar el stack, AuthApprovedRedirectURI se muestra en las salidas de CloudFormation. Vuelve a la Consola de Desarrolladores de Google y actualiza el cliente OAuth con las URIs de redirección correctas.