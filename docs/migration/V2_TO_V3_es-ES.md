# Guía de Migración (v2 a v3)

## TL;DR

- V3 introduce control de permisos granular y funcionalidad de Bot Store, requiriendo cambios en el esquema de DynamoDB
- **Haga una copia de seguridad de su tabla ConversationTable de DynamoDB antes de la migración**
- Actualice la URL de su repositorio de `bedrock-claude-chat` a `bedrock-chat`
- Ejecute el script de migración para convertir sus datos al nuevo esquema
- Todos sus bots y conversaciones se conservarán con el nuevo modelo de permisos
- **IMPORTANTE: Durante el proceso de migración, la aplicación no estará disponible para ningún usuario hasta que la migración se complete. Este proceso típicamente toma alrededor de 60 minutos, dependiendo de la cantidad de datos y el rendimiento de su entorno de desarrollo.**
- **IMPORTANTE: Todas las APIs Publicadas deben ser eliminadas durante el proceso de migración.**
- **ADVERTENCIA: El proceso de migración no puede garantizar un éxito del 100% para todos los bots. Por favor, documente sus configuraciones importantes de bots antes de la migración en caso de que necesite recrearlas manualmente**

## Introducción

### Novedades en V3

V3 introduce mejoras significativas en Bedrock Chat:

1. **Control de permisos detallado**: Controla el acceso a tus bots con permisos basados en grupos de usuarios
2. **Tienda de Bots**: Comparte y descubre bots a través de un marketplace centralizado
3. **Características administrativas**: Gestiona APIs, marca bots como esenciales y analiza el uso de los bots

Estas nuevas funciones requirieron cambios en el esquema de DynamoDB, lo que hace necesario un proceso de migración para los usuarios existentes.

### Por qué es necesaria esta migración

El nuevo modelo de permisos y la funcionalidad de la Tienda de Bots requirieron reestructurar cómo se almacenan y acceden los datos de los bots. El proceso de migración convierte tus bots y conversaciones existentes al nuevo esquema mientras preserva todos tus datos.

> [!WARNING]
> Aviso de Interrupción del Servicio: **Durante el proceso de migración, la aplicación no estará disponible para ningún usuario.** Planifica realizar esta migración durante una ventana de mantenimiento cuando los usuarios no necesiten acceder al sistema. La aplicación solo volverá a estar disponible después de que el script de migración haya finalizado correctamente y todos los datos se hayan convertido adecuadamente al nuevo esquema. Este proceso típicamente tarda alrededor de 60 minutos, dependiendo de la cantidad de datos y el rendimiento de tu entorno de desarrollo.

> [!IMPORTANT]
> Antes de proceder con la migración: **El proceso de migración no puede garantizar un éxito del 100% para todos los bots**, especialmente aquellos creados con versiones anteriores o con configuraciones personalizadas. Por favor, documenta las configuraciones importantes de tus bots (instrucciones, fuentes de conocimiento, ajustes) antes de iniciar el proceso de migración en caso de que necesites recrearlas manualmente.

## Proceso de Migración

### Aviso Importante Sobre la Visibilidad de los Bots en V3

En V3, **todos los bots v2 con compartición pública habilitada serán encontrables en la Tienda de Bots.** Si tienes bots que contienen información sensible que no quieres que sea descubrible, considera hacerlos privados antes de migrar a V3.

### Paso 1: Identificar el nombre de tu entorno

En este procedimiento, `{YOUR_ENV_PREFIX}` se especifica para identificar el nombre de tus Stacks de CloudFormation. Si estás usando la función [Deploying Multiple Environments](../../README.md#deploying-multiple-environments), reemplázalo con el nombre del entorno a migrar. Si no, reemplázalo con una cadena vacía.

### Paso 2: Actualizar la URL del Repositorio (Recomendado)

El repositorio ha sido renombrado de `bedrock-claude-chat` a `bedrock-chat`. Actualiza tu repositorio local:

```bash
# Comprueba tu URL remota actual
git remote -v

# Actualiza la URL remota
git remote set-url origin https://github.com/aws-samples/bedrock-chat.git

# Verifica el cambio
git remote -v
```

### Paso 3: Asegúrate de Estar en la Última Versión V2

> [!WARNING]
> DEBES actualizar a v2.10.0 antes de migrar a V3. **Saltarse este paso puede resultar en pérdida de datos durante la migración.**

Antes de comenzar la migración, asegúrate de estar ejecutando la última versión de V2 (**v2.10.0**). Esto garantiza que tienes todas las correcciones de errores y mejoras necesarias antes de actualizar a V3:

```bash
# Obtén las últimas etiquetas
git fetch --tags

# Cambia a la última versión V2
git checkout v2.10.0

# Despliega la última versión V2
cd cdk
npm ci
npx cdk deploy --all
```

### Paso 4: Registra el Nombre de tu Tabla DynamoDB V2

Obtén el nombre de la ConversationTable V2 de las salidas de CloudFormation:

```bash
# Obtén el nombre de la ConversationTable V2
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='ConversationTableName'].OutputValue" \
  --stack-name {YOUR_ENV_PREFIX}BedrockChatStack
```

Asegúrate de guardar este nombre de tabla en un lugar seguro, ya que lo necesitarás para el script de migración más adelante.

### Paso 5: Respaldar tu Tabla DynamoDB

Antes de proceder, crea una copia de seguridad de tu ConversationTable de DynamoDB usando el nombre que acabas de registrar:

```bash
# Crea una copia de seguridad de tu tabla V2
aws dynamodb create-backup \
  --no-cli-pager \
  --backup-name "BedrockChatV2Backup-$(date +%Y%m%d)" \
  --table-name YOUR_V2_CONVERSATION_TABLE_NAME

# Verifica que el estado de la copia de seguridad está disponible
aws dynamodb describe-backup \
  --no-cli-pager \
  --query BackupDescription.BackupDetails \
  --backup-arn YOUR_BACKUP_ARN
```

### Paso 6: Eliminar Todas las APIs Publicadas

> [!IMPORTANT]
> Antes de desplegar V3, debes eliminar todas las APIs publicadas para evitar conflictos de valores de salida de CloudFormation durante el proceso de actualización.

1. Inicia sesión en tu aplicación como administrador
2. Navega a la sección de Administración y selecciona "Gestión de API"
3. Revisa la lista de todas las APIs publicadas
4. Elimina cada API publicada haciendo clic en el botón de eliminar junto a ella

Puedes encontrar más información sobre la publicación y gestión de APIs en la documentación [PUBLISH_API.md](../PUBLISH_API_es-ES.md), [ADMINISTRATOR.md](../ADMINISTRATOR_es-ES.md) respectivamente.

### Paso 7: Obtener V3 y Desplegar

Obtén el último código V3 y despliégalo:

```bash
git fetch
git checkout v3
cd cdk
npm ci
npx cdk deploy --all
```

> [!IMPORTANT]
> Una vez que despliegues V3, la aplicación no estará disponible para ningún usuario hasta que el proceso de migración esté completo. El nuevo esquema es incompatible con el formato de datos antiguo, por lo que los usuarios no podrán acceder a sus bots o conversaciones hasta que completes el script de migración en los siguientes pasos.

### Paso 8: Registrar los Nombres de tus Tablas DynamoDB V3

Después de desplegar V3, necesitas obtener los nombres de la nueva ConversationTable y BotTable:

```bash
# Obtén el nombre de la ConversationTable V3
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='ConversationTableNameV3'].OutputValue" \
  --stack-name {YOUR_ENV_PREFIX}BedrockChatStack

# Obtén el nombre de la BotTable V3
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='BotTableNameV3'].OutputValue" \
  --stack-name {YOUR_ENV_PREFIX}BedrockChatStack
```

> [!Important]
> Asegúrate de guardar estos nombres de tablas V3 junto con tu nombre de tabla V2 previamente guardado, ya que necesitarás todos ellos para el script de migración.

### Paso 9: Ejecutar el Script de Migración

El script de migración convertirá tus datos V2 al esquema V3. Primero, edita el script de migración `docs/migration/migrate_v2_v3.py` para establecer tus nombres de tabla y región:

```python
# Región donde se encuentra dynamodb
REGION = "ap-northeast-1" # Reemplaza con tu región

V2_CONVERSATION_TABLE = "BedrockChatStack-DatabaseConversationTableXXXX" # Reemplaza con tu valor registrado en el Paso 4
V3_CONVERSATION_TABLE = "BedrockChatStack-DatabaseConversationTableV3XXXX" # Reemplaza con tu valor registrado en el Paso 8
V3_BOT_TABLE = "BedrockChatStack-DatabaseBotTableV3XXXXX" # Reemplaza con tu valor registrado en el Paso 8
```

Luego ejecuta el script usando Poetry desde el directorio backend:

> [!NOTE]
> La versión de requisitos de Python se cambió a 3.13.0 o posterior (Posiblemente cambiará en desarrollos futuros. Ver pyproject.toml). Si tienes venv instalado con una versión diferente de Python, necesitarás eliminarlo una vez.

```bash
# Navega al directorio backend
cd backend

# Instala las dependencias si aún no lo has hecho
poetry install

# Ejecuta primero una prueba en seco para ver qué se migraría
poetry run python ../docs/migration/migrate_v2_v3.py --dry-run

# Si todo parece correcto, ejecuta la migración real
poetry run python ../docs/migration/migrate_v2_v3.py

# Verifica que la migración fue exitosa
poetry run python ../docs/migration/migrate_v2_v3.py --verify-only
```

El script de migración generará un archivo de informe en tu directorio actual con detalles sobre el proceso de migración. Revisa este archivo para asegurarte de que todos tus datos se migraron correctamente.

#### Manejo de Grandes Volúmenes de Datos

Para entornos con usuarios intensivos o grandes cantidades de datos, considera estos enfoques:

1. **Migrar usuarios individualmente**: Para usuarios con grandes volúmenes de datos, migrarlos uno a la vez:

   ```bash
   poetry run python ../docs/migration/migrate_v2_v3.py --users user-id-1 user-id-2
   ```

2. **Consideraciones de memoria**: El proceso de migración carga datos en memoria. Si encuentras errores de Falta de Memoria (OOM), intenta:

   - Migrar un usuario a la vez
   - Ejecutar la migración en una máquina con más memoria
   - Dividir la migración en lotes más pequeños de usuarios

3. **Monitorear la migración**: Revisa los archivos de informe generados para asegurar que todos los datos se migren correctamente, especialmente para conjuntos de datos grandes.

### Paso 10: Verificar la Aplicación

Después de la migración, abre tu aplicación y verifica:

- Todos tus bots están disponibles
- Las conversaciones están preservadas
- Los nuevos controles de permisos funcionan

### Limpieza (Opcional)

Después de confirmar que la migración fue exitosa y todos tus datos son accesibles correctamente en V3, puedes opcionalmente eliminar la tabla de conversaciones V2 para ahorrar costos:

```bash
# Eliminar la tabla de conversaciones V2 (SOLO después de confirmar una migración exitosa)
aws dynamodb delete-table --table-name YOUR_V2_CONVERSATION_TABLE_NAME
```

> [!IMPORTANT]
> Solo elimina la tabla V2 después de verificar minuciosamente que todos tus datos importantes se han migrado exitosamente a V3. Recomendamos mantener la copia de seguridad creada en el Paso 2 durante al menos algunas semanas después de la migración, incluso si eliminas la tabla original.

## FAQ de V3

### Acceso y Permisos de Bots

**P: ¿Qué sucede si se elimina un bot que estoy usando o se elimina mi permiso de acceso?**
R: La autorización se verifica en el momento del chat, por lo que perderás el acceso inmediatamente.

**P: ¿Qué sucede si se elimina un usuario (por ejemplo, un empleado que se va)?**
R: Sus datos pueden eliminarse completamente borrando todos los elementos de DynamoDB que tengan su ID de usuario como clave de partición (PK).

**P: ¿Puedo desactivar el compartir para un bot público esencial?**
R: No, el administrador debe marcar primero el bot como no esencial antes de desactivar el compartir.

**P: ¿Puedo eliminar un bot público esencial?**
R: No, el administrador debe marcar primero el bot como no esencial antes de eliminarlo.

### Seguridad e Implementación

**P: ¿Está implementada la seguridad a nivel de fila (RLS) para la tabla de bots?**
R: No, considerando la diversidad de patrones de acceso. La autorización se realiza al acceder a los bots, y el riesgo de filtración de metadatos se considera mínimo en comparación con el historial de conversaciones.

**P: ¿Cuáles son los requisitos para publicar una API?**
R: El bot debe ser público.

**P: ¿Habrá una pantalla de gestión para todos los bots privados?**
R: No en la versión inicial V3. Sin embargo, los elementos aún pueden eliminarse consultando con el ID de usuario según sea necesario.

**P: ¿Habrá funcionalidad de etiquetado de bots para mejorar la experiencia de búsqueda?**
R: No en la versión inicial V3, pero se puede agregar etiquetado automático basado en LLM en futuras actualizaciones.

### Administración

**P: ¿Qué pueden hacer los administradores?**
R: Los administradores pueden:

- Gestionar bots públicos (incluyendo la verificación de bots de alto costo)
- Gestionar APIs
- Marcar bots públicos como esenciales

**P: ¿Puedo hacer que los bots parcialmente compartidos sean esenciales?**
R: No, solo se admiten bots públicos.

**P: ¿Puedo establecer prioridad para los bots fijados?**
R: No en la versión inicial.

### Configuración de Autorización

**P: ¿Cómo configuro la autorización?**
R:

1. Abre la consola de Amazon Cognito y crea grupos de usuarios en el grupo de usuarios de BrChat
2. Agrega usuarios a estos grupos según sea necesario
3. En BrChat, selecciona los grupos de usuarios a los que deseas permitir acceso al configurar los ajustes de compartir del bot

Nota: Los cambios en la membresía de grupo requieren volver a iniciar sesión para que surtan efecto. Los cambios se reflejan en la actualización del token, pero no durante el período de validez del token ID (30 minutos por defecto en V3, configurable mediante `tokenValidMinutes` en `cdk.json` o `parameter.ts`).

**P: ¿El sistema verifica con Cognito cada vez que se accede a un bot?**
R: No, la autorización se verifica usando el token JWT para evitar operaciones I/O innecesarias.

### Funcionalidad de Búsqueda

**P: ¿La búsqueda de bots admite búsqueda semántica?**
R: No, solo se admite coincidencia parcial de texto. La búsqueda semántica (por ejemplo, "automóvil" → "coche", "VE", "vehículo") no está disponible debido a las restricciones actuales de OpenSearch Serverless (marzo 2025).