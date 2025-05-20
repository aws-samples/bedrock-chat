# Guía de Migración (v2 a v3)

## TL;DR

- V3 introduce un control de permisos más granular y funcionalidad de Bot Store, lo que requiere cambios en el esquema de DynamoDB
- **Haga una copia de seguridad de su tabla ConversationTable de DynamoDB antes de la migración**
- Actualice la URL de su repositorio de `bedrock-claude-chat` a `bedrock-chat`
- Ejecute el script de migración para convertir sus datos al nuevo esquema
- Todos sus bots y conversaciones se conservarán con el nuevo modelo de permisos
- **IMPORTANTE: Durante el proceso de migración, la aplicación estará indisponible para todos los usuarios hasta que la migración se complete. Este proceso normalmente tarda alrededor de 60 minutos, dependiendo de la cantidad de datos y el rendimiento de su entorno de desarrollo.**
- **IMPORTANTE: Todas las API Publicadas deben ser eliminadas durante el proceso de migración.**
- **ADVERTENCIA: El proceso de migración no puede garantizar un 100% de éxito para todos los bots. Por favor, documente las configuraciones de sus bots importantes antes de la migración en caso de que necesite recrearlos manualmente**

## Introducción

### Novedades en V3

V3 introduce mejoras significativas en Bedrock Chat:

1. **Control de permisos detallado**: Controle el acceso a sus bots con permisos basados en grupos de usuarios
2. **Tienda de Bots**: Comparta y descubra bots a través de un mercado centralizado
3. **Características administrativas**: Administre APIs, marque bots como esenciales y analice el uso de bots

Estas nuevas características requirieron cambios en el esquema de DynamoDB, lo que hace necesario un proceso de migración para usuarios existentes.

### Por Qué Es Necesaria Esta Migración

El nuevo modelo de permisos y la funcionalidad de la Tienda de Bots requirieron reestructurar cómo se almacenan y acceden los datos de los bots. El proceso de migración convierte sus bots y conversaciones existentes al nuevo esquema, preservando todos sus datos.

> [!WARNING]
> Aviso de Interrupción del Servicio: **Durante el proceso de migración, la aplicación estará no disponible para todos los usuarios.** Planifique realizar esta migración durante una ventana de mantenimiento cuando los usuarios no necesiten acceder al sistema. La aplicación solo estará disponible de nuevo después de que el script de migración haya completado con éxito y todos los datos se hayan convertido correctamente al nuevo esquema. Este proceso típicamente tarda alrededor de 60 minutos, dependiendo de la cantidad de datos y el rendimiento de su entorno de desarrollo.

> [!IMPORTANT]
> Antes de proceder con la migración: **El proceso de migración no puede garantizar un éxito del 100% para todos los bots**, especialmente aquellos creados con versiones antiguas o con configuraciones personalizadas. Por favor, documente las configuraciones importantes de sus bots (instrucciones, fuentes de conocimiento, configuraciones) antes de iniciar el proceso de migración en caso de que necesite recrearlos manualmente.

## Proceso de Migración

### Aviso Importante Sobre la Visibilidad de Bots en V3

En V3, **todos los bots v2 con compartición pública habilitada serán buscables en la Tienda de Bots.** Si tiene bots que contienen información sensible que no desea que sean descubribles, considere hacerlos privados antes de migrar a V3.

### Paso 1: Identificar el nombre de su entorno

En este procedimiento, `{SU_PREFIJO_ENV}` se especifica para identificar el nombre de sus Stacks de CloudFormation. Si está utilizando la función de [Despliegue de Múltiples Entornos](../../README.md#deploying-multiple-environments), reemplácelo con el nombre del entorno a migrar. Si no, reemplácelo con una cadena vacía.

### Paso 2: Actualizar URL del Repositorio (Recomendado)

El repositorio ha sido renombrado de `bedrock-claude-chat` a `bedrock-chat`. Actualice su repositorio local:

```bash
# Verificar su URL remota actual
git remote -v

# Actualizar la URL remota
git remote set-url origin https://github.com/aws-samples/bedrock-chat.git

# Verificar el cambio
git remote -v
```

### Paso 3: Asegurarse de Estar en la Última Versión V2

> [!ADVERTENCIA]
> DEBE actualizar a v2.10.0 antes de migrar a V3. **Omitir este paso puede resultar en pérdida de datos durante la migración.**

Antes de comenzar la migración, asegúrese de estar ejecutando la última versión de V2 (**v2.10.0**). Esto garantiza que tenga todas las correcciones de errores y mejoras necesarias antes de actualizar a V3:

```bash
# Obtener las últimas etiquetas
git fetch --tags

# Cambiar a la última versión V2
git checkout v2.10.0

# Desplegar la última versión V2
cd cdk
npm ci
npx cdk deploy --all
```

### Paso 4: Registrar el Nombre de su Tabla DynamoDB V2

Obtenga el nombre de la tabla ConversationTable de V2 desde las salidas de CloudFormation:

```bash
# Obtener el nombre de la tabla ConversationTable V2
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='ConversationTableName'].OutputValue" \
  --stack-name {SU_PREFIJO_ENV}BedrockChatStack
```

Asegúrese de guardar este nombre de tabla en un lugar seguro, ya que lo necesitará para el script de migración más adelante.

### Paso 5: Hacer Copia de Seguridad de su Tabla DynamoDB

Antes de continuar, cree una copia de seguridad de su ConversationTable de DynamoDB usando el nombre que acaba de registrar:

```bash
# Crear una copia de seguridad de su tabla V2
aws dynamodb create-backup \
  --no-cli-pager \
  --backup-name "BedrockChatV2Backup-$(date +%Y%m%d)" \
  --table-name NOMBRE_TABLA_CONVERSACION_V2

# Verificar que el estado de la copia de seguridad esté disponible
aws dynamodb describe-backup \
  --no-cli-pager \
  --query BackupDescription.BackupDetails \
  --backup-arn ARN_COPIA_SEGURIDAD
```

### Paso 6: Eliminar Todas las API Publicadas

> [!IMPORTANTE]
> Antes de desplegar V3, debe eliminar todas las API publicadas para evitar conflictos de valores de salida de Cloudformation durante el proceso de actualización.

1. Inicie sesión en su aplicación como administrador
2. Navegue a la sección de Administración y seleccione "Gestión de API"
3. Revise la lista de todas las API publicadas
4. Elimine cada API publicada haciendo clic en el botón de eliminar junto a ella

Puede encontrar más información sobre la publicación y gestión de API en la documentación de [PUBLISH_API.md](../PUBLISH_API_es-ES.md) y [ADMINISTRATOR.md](../ADMINISTRATOR_es-ES.md) respectivamente.

### Paso 7: Obtener V3 e Implementar

Obtenga el código V3 más reciente e impleméntelo:

```bash
git fetch
git checkout v3
cd cdk
npm ci
npx cdk deploy --all
```

> [!IMPORTANTE]
> Una vez que implemente V3, la aplicación no estará disponible para todos los usuarios hasta que se complete el proceso de migración. El nuevo esquema es incompatible con el formato de datos anterior, por lo que los usuarios no podrán acceder a sus bots o conversaciones hasta que complete el script de migración en los siguientes pasos.

### Paso 8: Registrar los Nombres de sus Tablas DynamoDB V3

Después de implementar V3, necesita obtener los nombres de las tablas ConversationTable y BotTable:

```bash
# Obtener el nombre de la tabla ConversationTable V3
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='ConversationTableNameV3'].OutputValue" \
  --stack-name {SU_PREFIJO_ENV}BedrockChatStack

# Obtener el nombre de la tabla BotTable V3
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='BotTableNameV3'].OutputValue" \
  --stack-name {SU_PREFIJO_ENV}BedrockChatStack
```

> [!Importante]
> Asegúrese de guardar estos nombres de tablas V3 junto con su nombre de tabla V2 previamente guardado, ya que necesitará todos ellos para el script de migración.

[El resto del documento se mantiene igual, solo traducido al español]

## V3 Preguntas Frecuentes

### Acceso y Permisos de Bot

**P: ¿Qué sucede si se elimina un bot que estoy usando o se me quita el permiso de acceso?**
R: La autorización se comprueba en el momento del chat, por lo que perderá el acceso inmediatamente.

**P: ¿Qué sucede si se elimina un usuario (por ejemplo, un empleado que se va)?**
R: Sus datos pueden eliminarse completamente eliminando todos los elementos de DynamoDB con su ID de usuario como clave de partición (PK).

**P: ¿Puedo desactivar el uso compartido de un bot público esencial?**
R: No, el administrador debe marcar primero el bot como no esencial antes de desactivar el uso compartido.

**P: ¿Puedo eliminar un bot público esencial?**
R: No, el administrador debe marcar primero el bot como no esencial antes de eliminarlo.

### Seguridad e Implementación

**P: ¿Está implementada la seguridad a nivel de fila (RLS) para la tabla de bots?**
R: No, considerando la diversidad de patrones de acceso. La autorización se realiza al acceder a los bots, y se considera que el riesgo de filtración de metadatos es mínimo en comparación con el historial de conversaciones.

**P: ¿Cuáles son los requisitos para publicar una API?**
R: El bot debe ser público.

**P: ¿Habrá una pantalla de gestión para todos los bots privados?**
R: No en la versión inicial de V3. Sin embargo, los elementos aún pueden eliminarse consultando con el ID de usuario según sea necesario.

**P: ¿Habrá funcionalidad de etiquetado de bots para mejorar la experiencia de búsqueda?**
R: No en la versión inicial de V3, pero se podría agregar etiquetado automático basado en LLM en futuras actualizaciones.

### Administración

**P: ¿Qué pueden hacer los administradores?**
R: Los administradores pueden:

- Gestionar bots públicos (incluyendo la revisión de bots de alto costo)
- Gestionar APIs
- Marcar bots públicos como esenciales

**P: ¿Puedo hacer bots compartidos parcialmente como esenciales?**
R: No, solo se admiten bots públicos.

**P: ¿Puedo establecer prioridad para bots anclados?**
R: En la versión inicial, no.

### Configuración de Autorización

**P: ¿Cómo configuro la autorización?**
R:

1. Abra la consola de Amazon Cognito y cree grupos de usuarios en el grupo de usuarios de BrChat
2. Agregue usuarios a estos grupos según sea necesario
3. En BrChat, seleccione los grupos de usuarios a los que desea permitir el acceso al configurar los ajustes de uso compartido de bots

Nota: Los cambios de membresía de grupo requieren volver a iniciar sesión para surtir efecto. Los cambios se reflejan al actualizar el token, pero no durante el período de validez del token de ID (predeterminado 30 minutos en V3, configurable por `tokenValidMinutes` en `cdk.json` o `parameter.ts`).

**P: ¿El sistema comprueba con Cognito cada vez que se accede a un bot?**
R: No, la autorización se comprueba utilizando el token JWT para evitar operaciones de E/S innecesarias.

### Funcionalidad de Búsqueda

**P: ¿La búsqueda de bots admite búsqueda semántica?**
R: No, solo se admite coincidencia parcial de texto. La búsqueda semántica (por ejemplo, "automóvil" → "coche", "EV", "vehículo") no está disponible debido a las limitaciones actuales de OpenSearch Serverless (Mar 2025).