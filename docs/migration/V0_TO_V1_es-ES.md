# Guía de Migración (v0 a v1)

Si ya está utilizando Bedrock Chat con una versión anterior (~`0.4.x`), debe seguir los siguientes pasos para migrar.

## ¿Por qué necesito hacerlo?

Esta actualización importante incluye actualizaciones de seguridad importantes.

- El almacenamiento de la base de datos vectorial (es decir, pgvector en Aurora PostgreSQL) ahora está cifrado, lo que provoca un reemplazo al implementarse. Esto significa que los elementos vectoriales existentes se eliminarán.
- Hemos introducido el grupo de usuarios de Cognito `CreatingBotAllowed` para limitar a los usuarios que pueden crear bots. Los usuarios existentes actuales no están en este grupo, por lo que necesitará adjuntar el permiso manualmente si desea que tengan capacidades de creación de bots. Consulte: [Personalización de Bot](../../README.md#bot-personalization)

## Requisitos previos

Lea la [Guía de migración de base de datos](./DATABASE_MIGRATION_es-ES.md) y determine el método para restaurar elementos.

## Pasos

### Migración de almacén de vectores

- Abre tu terminal y navega al directorio del proyecto
- Extrae la rama que deseas desplegar. A continuación, cambia a la rama deseada (en este caso, `v1`) y extrae los últimos cambios:

```sh
git fetch
git checkout v1
git pull origin v1
```

- Si deseas restaurar elementos con DMS, NO OLVIDES deshabilitar la rotación de contraseñas y anotar la contraseña para acceder a la base de datos. Si restauras con el script de migración([migrate_v0_v1.py](./migrate_v0_v1.py)), no necesitas anotar la contraseña.
- Elimina todas las [API publicadas](../PUBLISH_API_es-ES.md) para que CloudFormation pueda eliminar el clúster de Aurora existente.
- Ejecuta [npx cdk deploy](../README.md#deploy-using-cdk) que activa el reemplazo del clúster de Aurora y ELIMINA TODOS LOS ELEMENTOS VECTORIALES.
- Sigue la [Guía de Migración de Base de Datos](./DATABASE_MIGRATION_es-ES.md) para restaurar elementos vectoriales.
- Verifica que el usuario pueda utilizar los bots existentes que tienen conocimiento, es decir, bots RAG.

### Adjuntar permiso CreatingBotAllowed

- Después del despliegue, todos los usuarios no podrán crear nuevos bots.
- Si deseas que usuarios específicos puedan crear bots, agrega esos usuarios al grupo `CreatingBotAllowed` utilizando la consola de administración o CLI.
- Verifica si el usuario puede crear un bot. Ten en cuenta que los usuarios necesitan volver a iniciar sesión.