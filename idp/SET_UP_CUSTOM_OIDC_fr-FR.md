# Configurer un fournisseur d'identité externe

## Étape 1 : Créer un Client OIDC

Suivez les procédures du fournisseur OIDC cible, et notez les valeurs de l'identifiant client OIDC et du secret. L'URL de l'émetteur est également requise dans les étapes suivantes. Si une URI de redirection est nécessaire lors du processus de configuration, entrez une valeur factice qui sera remplacée une fois le déploiement terminé.

## Étape 2 : Stocker les identifiants dans AWS Secrets Manager

1. Accédez à la Console de gestion AWS.
2. Accédez à Secrets Manager et choisissez "Stocker un nouveau secret".
3. Sélectionnez "Autre type de secrets".
4. Saisissez l'ID client et le secret client sous forme de paires clé-valeur.

   - Clé : `clientId`, Valeur : <YOUR_GOOGLE_CLIENT_ID>
   - Clé : `clientSecret`, Valeur : <YOUR_GOOGLE_CLIENT_SECRET>
   - Clé : `issuerUrl`, Valeur : <ISSUER_URL_OF_THE_PROVIDER>

5. Suivez les invites pour nommer et décrire le secret. Notez le nom du secret car vous en aurez besoin dans votre code CDK (Utilisé à l'étape 3 dans le nom de variable <YOUR_SECRET_NAME>).
6. Vérifiez et stockez le secret.

### Attention

Les noms de clés doivent correspondre exactement aux chaînes `clientId`, `clientSecret` et `issuerUrl`.

## Étape 3 : Mettre à jour cdk.json

Dans votre fichier cdk.json, ajoutez le fournisseur d'identité et le nom du secret au fichier cdk.json.

comme suit :

```json
{
  "context": {
    // ...
    "identityProviders": [
      {
        "service": "oidc", // Ne pas modifier
        "serviceName": "<VOTRE_NOM_DE_SERVICE>", // Définissez la valeur que vous souhaitez
        "secretName": "<VOTRE_NOM_DE_SECRET>"
      }
    ],
    "userPoolDomainPrefix": "<PRÉFIXE_DE_DOMAINE_UNIQUE_POUR_VOTRE_USER_POOL>"
  }
}
```

### Attention

#### Unicité

Le `userPoolDomainPrefix` doit être globalement unique pour tous les utilisateurs Amazon Cognito. Si vous choisissez un préfixe déjà utilisé par un autre compte AWS, la création du domaine du user pool échouera. Il est recommandé d'inclure des identificateurs, des noms de projet ou des noms d'environnement dans le préfixe pour garantir son unicité.

## Étape 4 : Déployer Votre Stack CDK

Déployez votre stack CDK sur AWS :

```sh
npx cdk deploy --require-approval never --all
```

## Étape 5 : Mettre à jour le client OIDC avec les URI de redirection de Cognito

Après avoir déployé la pile, `AuthApprovedRedirectURI` apparaît dans les sorties de CloudFormation. Retournez à votre configuration OIDC et mettez à jour avec les URI de redirection corrects.