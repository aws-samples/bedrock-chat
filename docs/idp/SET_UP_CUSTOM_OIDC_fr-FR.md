# Configurer un fournisseur d'identité externe

## Étape 1 : Créer un client OIDC

Suivez les procédures du fournisseur OIDC cible, et notez les valeurs de l'ID client OIDC et du secret. L'URL de l'émetteur est également requise pour les étapes suivantes. Si une URI de redirection est nécessaire pour le processus de configuration, saisissez une valeur temporaire, qui sera remplacée une fois le déploiement terminé.

## Étape 2 : Stocker les identifiants dans AWS Secrets Manager

1. Accédez à la Console de gestion AWS.
2. Naviguez vers Secrets Manager et choisissez "Stocker un nouveau secret".
3. Sélectionnez "Autre type de secrets".
4. Saisissez l'ID client et le secret client sous forme de paires clé-valeur.

   - Clé : `clientId`, Valeur : <YOUR_GOOGLE_CLIENT_ID>
   - Clé : `clientSecret`, Valeur : <YOUR_GOOGLE_CLIENT_SECRET>
   - Clé : `issuerUrl`, Valeur : <ISSUER_URL_OF_THE_PROVIDER>

5. Suivez les instructions pour nommer et décrire le secret. Notez le nom du secret car vous en aurez besoin dans votre code CDK (Utilisé dans l'étape 3 variable <YOUR_SECRET_NAME>).
6. Vérifiez et stockez le secret.

### Attention

Les noms des clés doivent correspondre exactement aux chaînes `clientId`, `clientSecret` et `issuerUrl`.

## Étape 3 : Mettre à jour cdk.json

Dans votre fichier cdk.json, ajoutez l'ID du fournisseur et le SecretName au fichier cdk.json.

comme ceci :

```json
{
  "context": {
    // ...
    "identityProviders": [
      {
        "service": "oidc", // Ne pas modifier
        "serviceName": "<YOUR_SERVICE_NAME>", // Définissez la valeur que vous souhaitez
        "secretName": "<YOUR_SECRET_NAME>"
      }
    ],
    "userPoolDomainPrefix": "<UNIQUE_DOMAIN_PREFIX_FOR_YOUR_USER_POOL>"
  }
}
```

### Attention

#### Unicité

Le `userPoolDomainPrefix` doit être globalement unique parmi tous les utilisateurs d'Amazon Cognito. Si vous choisissez un préfixe qui est déjà utilisé par un autre compte AWS, la création du domaine du groupe d'utilisateurs échouera. Il est recommandé d'inclure des identifiants, des noms de projet ou des noms d'environnement dans le préfixe pour garantir son unicité.

## Étape 4 : Déployer votre pile CDK

Déployez votre pile CDK sur AWS :

```sh
npx cdk deploy --require-approval never --all
```

## Étape 5 : Mettre à jour le client OIDC avec les URI de redirection Cognito

Après le déploiement de la pile, `AuthApprovedRedirectURI` s'affiche dans les sorties CloudFormation. Retournez dans votre configuration OIDC et mettez à jour avec les URI de redirection corrects.