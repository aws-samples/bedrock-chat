# Guía de Migración (v0 a v1)

Si ya utilizas Bedrock Chat con una versión anterior (~`0.4.x`), necesitas seguir los pasos a continuación para migrar.

## ¿Por qué necesito hacerlo?

Esta actualización importante incluye actualizaciones de seguridad relevantes.

- El almacenamiento de la base de datos vectorial (es decir, pgvector en Aurora PostgreSQL) ahora está cifrado, lo que activa un reemplazo cuando se despliega. Esto significa que los elementos vectoriales existentes serán eliminados.
- Hemos introducido el grupo de usuarios de Cognito `CreatingBotAllowed` para limitar los usuarios que pueden crear bots. Los usuarios existentes actuales no están en este grupo, por lo que necesitas asignar el permiso manualmente si quieres que tengan capacidades de creación de bots. Ver: [Personalización de Bot](../../README.md#bot-personalization)

## Requisitos previos

Lea la [Guía de migración de base de datos](./DATABASE_MIGRATION_es-ES.md) y determine el método para restaurar elementos.

## Pasos

### Migración del almacén de vectores

- Abre tu terminal y navega al directorio del proyecto
- Extrae la rama que deseas implementar. A continuación se muestra cómo cambiar a la rama deseada (en este caso, `v1`) y extraer los últimos cambios:

```sh
git fetch
git checkout v1
git pull origin v1
```

- Si deseas restaurar elementos con DMS, NO OLVIDES deshabilitar la rotación de contraseñas y anotar la contraseña para acceder a la base de datos. Si restauras con el script de migración ([migrate_v0_v1.py](./migrate_v0_v1.py)), no necesitas anotar la contraseña.
- Elimina todas las [APIs publicadas](../PUBLISH_API_es-ES.md) para que CloudFormation pueda eliminar el clúster Aurora existente.
- Ejecutar [npx cdk deploy](../README.md#deploy-using-cdk) activa el reemplazo del clúster Aurora y ELIMINA TODOS LOS ELEMENTOS VECTORIALES.
- Sigue la [Guía de Migración de Base de Datos](./DATABASE_MIGRATION_es-ES.md) para restaurar los elementos vectoriales.
- Verifica que los usuarios puedan utilizar los bots existentes que tienen conocimiento, es decir, los bots RAG.

### Adjuntar permiso CreatingBotAllowed

- Después de la implementación, todos los usuarios no podrán crear nuevos bots.
- Si deseas que usuarios específicos puedan crear bots, añade esos usuarios al grupo `CreatingBotAllowed` usando la consola de administración o CLI.
- Verifica si el usuario puede crear un bot. Ten en cuenta que los usuarios necesitan volver a iniciar sesión.