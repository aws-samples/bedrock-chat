# Configurer un fournisseur d'identité externe pour Google

## Étape 1 : Créer un Client OAuth 2.0 Google

1. Accédez à la Console Développeur Google.
2. Créez un nouveau projet ou sélectionnez un projet existant.
3. Naviguez vers "Identifiants", puis cliquez sur "Créer des identifiants" et choisissez "ID client OAuth".
4. Configurez l'écran de consentement si demandé.
5. Pour le type d'application, sélectionnez "Application Web".
6. Laissez l'URI de redirection vide pour l'instant pour le définir plus tard, et enregistrez temporairement.[Voir Étape 5](#step-5-update-google-oauth-client-with-cognito-redirect-uris)
7. Une fois créé, notez l'ID Client et le Secret Client.

Pour plus de détails, consultez [le document officiel de Google](https://support.google.com/cloud/answer/6158849?hl=en)

## Étape 2 : Stocker les identifiants OAuth Google dans AWS Secrets Manager

1. Accédez à la console de gestion AWS.
2. Naviguez vers Secrets Manager et choisissez "Stocker un nouveau secret".
3. Sélectionnez "Autre type de secrets".
4. Saisissez le clientId et le clientSecret OAuth Google sous forme de paires clé-valeur.

   1. Clé : clientId, Valeur : <YOUR_GOOGLE_CLIENT_ID>
   2. Clé : clientSecret, Valeur : <YOUR_GOOGLE_CLIENT_SECRET>

5. Suivez les invites pour nommer et décrire le secret. Notez le nom du secret car vous en aurez besoin dans votre code CDK. Par exemple, googleOAuthCredentials. (À utiliser dans l'étape 3 avec le nom de variable <YOUR_SECRET_NAME>)
6. Vérifiez et stockez le secret.

### Attention

Les noms des clés doivent correspondre exactement aux chaînes 'clientId' et 'clientSecret'.

## Étape 3 : Mettre à jour cdk.json

Dans votre fichier cdk.json, ajoutez l'ID du fournisseur et le SecretName au fichier cdk.json.

comme ceci :

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

### Attention

#### Unicité

Le userPoolDomainPrefix doit être globalement unique pour tous les utilisateurs d'Amazon Cognito. Si vous choisissez un préfixe qui est déjà utilisé par un autre compte AWS, la création du domaine du groupe d'utilisateurs échouera. Il est recommandé d'inclure des identifiants, des noms de projet ou des noms d'environnement dans le préfixe pour garantir l'unicité.

## Étape 4 : Déployer Votre Stack CDK

Déployez votre stack CDK sur AWS :

```sh
npx cdk deploy --require-approval never --all
```

## Étape 5 : Mettre à jour le client OAuth Google avec les URI de redirection Cognito

Après le déploiement de la pile, l'AuthApprovedRedirectURI s'affiche dans les sorties CloudFormation. Retournez dans la Console Google Developer et mettez à jour le client OAuth avec les URI de redirection corrects.