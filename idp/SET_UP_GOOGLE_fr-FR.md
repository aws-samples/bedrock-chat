# Configurer un fournisseur d'identité externe pour Google

## Étape 1 : Créer un client OAuth 2.0 Google

1. Accédez à la Console des développeurs Google.
2. Créez un nouveau projet ou sélectionnez un projet existant.
3. Accédez à "Identifiants", puis cliquez sur "Créer des identifiants" et choisissez "ID client OAuth".
4. Configurez l'écran de consentement si demandé.
5. Pour le type d'application, sélectionnez "Application web".
6. Laissez l'URI de redirection vide pour le moment afin de le définir ultérieurement.[Voir l'étape 5](#step-5-update-google-oauth-client-with-cognito-redirect-uris)
7. Une fois créé, notez l'ID client et le secret client.

Pour plus de détails, consultez [le document officiel de Google](https://support.google.com/cloud/answer/6158849?hl=en)

## Étape 2 : Stocker les identifiants OAuth de Google dans AWS Secrets Manager

1. Accédez à la Console de gestion AWS.
2. Accédez à Secrets Manager et choisissez "Stocker un nouveau secret".
3. Sélectionnez "Autre type de secrets".
4. Saisissez les clientId et clientSecret OAuth de Google sous forme de paires clé-valeur.

   1. Clé : clientId, Valeur : <YOUR_GOOGLE_CLIENT_ID>
   2. Clé : clientSecret, Valeur : <YOUR_GOOGLE_CLIENT_SECRET>

5. Suivez les invites pour nommer et décrire le secret. Notez le nom du secret car vous en aurez besoin dans votre code CDK. Par exemple, googleOAuthCredentials. (Utilisez dans le nom de variable de l'étape 3 <YOUR_SECRET_NAME>)
6. Vérifiez et stockez le secret.

### Attention

Les noms de clés doivent correspondre exactement aux chaînes 'clientId' et 'clientSecret'.

## Étape 3 : Mettre à jour cdk.json

Dans votre fichier cdk.json, ajoutez le fournisseur d'identité et le nom du secret au fichier cdk.json.

comme ceci :

```json
{
  "context": {
    // ...
    "identityProviders": [
      {
        "service": "google",
        "secretName": "<VOTRE_NOM_DE_SECRET>"
      }
    ],
    "userPoolDomainPrefix": "<PREFIXE_DE_DOMAINE_UNIQUE_POUR_VOTRE_USER_POOL>"
  }
}
```

### Attention

#### Unicité

Le userPoolDomainPrefix doit être globalement unique parmi tous les utilisateurs Amazon Cognito. Si vous choisissez un préfixe déjà utilisé par un autre compte AWS, la création du domaine de user pool échouera. Il est recommandé d'inclure des identificateurs, des noms de projet ou des noms d'environnement dans le préfixe pour garantir son unicité.

## Étape 4 : Déployer Votre Stack CDK

Déployez votre stack CDK sur AWS :

```sh
npx cdk deploy --require-approval never --all
```

## Étape 5 : Mettre à jour le client OAuth Google avec les URI de redirection Cognito

Après avoir déployé la pile, AuthApprovedRedirectURI apparaît dans les sorties CloudFormation. Retournez dans la Console des développeurs Google et mettez à jour le client OAuth avec les URI de redirection corrects.