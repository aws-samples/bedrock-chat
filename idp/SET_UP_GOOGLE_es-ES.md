# Configurar proveedor de identidad externo para Google

## Paso 1: Crear un Cliente OAuth 2.0 de Google

1. Ir a la Consola de Desarrolladores de Google.
2. Crear un nuevo proyecto o seleccionar uno existente.
3. Navegar a "Credenciales", luego hacer clic en "Crear credenciales" y elegir "ID de cliente de OAuth".
4. Configurar la pantalla de consentimiento si se solicita.
5. Para el tipo de aplicación, seleccionar "Aplicación web".
6. Dejar en blanco el URI de redirección por ahora para configurarlo más tarde, y guardar temporalmente.[Ver Paso 5](#step-5-update-google-oauth-client-with-cognito-redirect-uris)
7. Una vez creado, anotar el ID de cliente y el Secreto de cliente.

Para más detalles, visite [documento oficial de Google](https://support.google.com/cloud/answer/6158849?hl=en)

## Paso 2: Almacenar credenciales de Google OAuth en AWS Secrets Manager

1. Vaya a la Consola de Administración de AWS.
2. Navegue hasta Secrets Manager y elija "Almacenar un nuevo secreto".
3. Seleccione "Otro tipo de secretos".
4. Introduzca el clientId y clientSecret de Google OAuth como pares clave-valor.

   1. Clave: clientId, Valor: <YOUR_GOOGLE_CLIENT_ID>
   2. Clave: clientSecret, Valor: <YOUR_GOOGLE_CLIENT_SECRET>

5. Siga las indicaciones para nombrar y describir el secreto. Anote el nombre del secreto, ya que lo necesitará en su código CDK. Por ejemplo, googleOAuthCredentials. (Usar en el nombre de variable de Step 3 <YOUR_SECRET_NAME>)
6. Revise y almacene el secreto.

### Atención

Los nombres de las claves deben coincidir exactamente con las cadenas 'clientId' y 'clientSecret'.

## Paso 3: Actualizar cdk.json

En su archivo cdk.json, agregue el Proveedor de Identidad y el Nombre del Secreto al archivo cdk.json.

de la siguiente manera:

```json
{
  "context": {
    // ...
    "identityProviders": [
      {
        "service": "google",
        "secretName": "<SU_NOMBRE_DE_SECRETO>"
      }
    ],
    "userPoolDomainPrefix": "<PREFIJO_DE_DOMINIO_ÚNICO_PARA_SU_USER_POOL>"
  }
}
```

### Atención

#### Unicidad

El userPoolDomainPrefix debe ser globalmente único en todos los usuarios de Amazon Cognito. Si elige un prefijo que ya está en uso por otra cuenta de AWS, la creación del dominio del grupo de usuarios fallará. Es una buena práctica incluir identificadores, nombres de proyectos o nombres de entornos en el prefijo para garantizar la unicidad.

## Paso 4: Desplegar tu Stack de CDK

Despliega tu stack de CDK en AWS:

```sh
npx cdk deploy --require-approval never --all
```

## Paso 5: Actualizar el Cliente OAuth de Google con los URI de Redirección de Cognito

Después de desplegar la pila, AuthApprovedRedirectURI aparecerá en las salidas de CloudFormation. Vuelva a la Consola de Desarrolladores de Google y actualice el cliente OAuth con los URI de redirección correctos.