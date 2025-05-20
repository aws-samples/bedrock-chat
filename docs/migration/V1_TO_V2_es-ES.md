# Guía de Migración (v1 a v2)

## TL;DR

- **Para usuarios de v1.2 o anterior**: Actualice a v1.4 y recree sus bots utilizando Base de Conocimientos (KB). Después de un período de transición, una vez que confirme que todo funciona como se espera con KB, proceda con la actualización a v2.
- **Para usuarios de v1.3**: Incluso si ya está utilizando KB, se **recomienda encarecidamente** actualizar a v1.4 y recrear sus bots. Si aún está utilizando pgvector, migre recreando sus bots utilizando KB en v1.4.
- **Para usuarios que deseen continuar utilizando pgvector**: No se recomienda actualizar a v2 si planea seguir utilizando pgvector. Actualizar a v2 eliminará todos los recursos relacionados con pgvector, y el soporte futuro ya no estará disponible. En este caso, continúe utilizando v1.
- Tenga en cuenta que **actualizar a v2 resultará en la eliminación de todos los recursos relacionados con Aurora.** Las actualizaciones futuras se centrarán exclusivamente en v2, quedando v1 obsoleta.

## Introducción

### Qué va a suceder

La actualización v2 introduce un cambio importante al reemplazar pgvector en Aurora Serverless y la incrustación basada en ECS con [Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html). Este cambio no es compatible con versiones anteriores.

### Por qué este repositorio ha adoptado Knowledge Bases y ha descontinuado pgvector

Hay varias razones para este cambio:

#### Mejor precisión RAG

- Knowledge Bases utiliza OpenSearch Serverless como backend, permitiendo búsquedas híbridas con búsqueda de texto completo y vectorial. Esto conduce a una mejor precisión al responder preguntas que incluyen nombres propios, algo con lo que pgvector tenía dificultades.
- También ofrece más opciones para mejorar la precisión RAG, como segmentación y análisis avanzados.
- Knowledge Bases ha estado disponible de manera general durante casi un año a partir de octubre de 2024, con funciones como la navegación web ya agregadas. Se esperan futuras actualizaciones, lo que facilitará adoptar funcionalidades avanzadas a largo plazo. Por ejemplo, aunque este repositorio no ha implementado características como importar desde buckets de S3 existentes (una característica muy solicitada) en pgvector, ya está soportado en KB (Knowledge Bases).

#### Mantenimiento

- La configuración actual de ECS + Aurora depende de numerosas bibliotecas, incluyendo aquellas para analizar PDF, navegar por la web y extraer transcripciones de YouTube. En comparación, las soluciones administradas como Knowledge Bases reducen la carga de mantenimiento tanto para los usuarios como para el equipo de desarrollo del repositorio.

## Proceso de Migración (Resumen)

Recomendamos encarecidamente actualizar a la v1.4 antes de migrar a la v2. En v1.4, puede utilizar tanto pgvector como bots de Base de Conocimientos, permitiendo un período de transición para recrear sus bots pgvector existentes en la Base de Conocimientos y verificar que funcionen según lo esperado. Incluso si los documentos RAG permanecen idénticos, tenga en cuenta que los cambios de backend en OpenSearch pueden producir resultados ligeramente diferentes, aunque generalmente similares, debido a diferencias como los algoritmos k-NN.

Al establecer `useBedrockKnowledgeBasesForRag` como true en `cdk.json`, puede crear bots utilizando Bases de Conocimientos. Sin embargo, los bots de pgvector pasarán a ser de solo lectura, impidiendo la creación o edición de nuevos bots pgvector.

![](../imgs/v1_to_v2_readonly_bot.png)

En v1.4, también se introducen [Guardrails para Amazon Bedrock](https://aws.amazon.com/jp/bedrock/guardrails/). Debido a las restricciones regionales de las Bases de Conocimientos, el bucket de S3 para cargar documentos debe estar en la misma región que `bedrockRegion`. Recomendamos hacer una copia de seguridad de los buckets de documentos existentes antes de actualizar para evitar cargar manualmente un gran número de documentos más tarde (ya que la funcionalidad de importación de buckets S3 está disponible).

## Proceso de Migración (Detalle)

Los pasos difieren dependiendo de si está utilizando v1.2 o anterior, o v1.3.

![](../imgs/v1_to_v2_arch.png)

### Pasos para usuarios de v1.2 o anterior

1. **Realice una copia de seguridad de su bucket de documentos existente (opcional pero recomendado).** Si su sistema ya está en funcionamiento, recomendamos encarecidamente este paso. Haga una copia de seguridad del bucket denominado `bedrockchatstack-documentbucketxxxx-yyyy`. Por ejemplo, podemos usar [AWS Backup](https://docs.aws.amazon.com/aws-backup/latest/devguide/s3-backups.html).

2. **Actualizar a v1.4**: Obtenga la última etiqueta v1.4, modifique `cdk.json` e implemente. Siga estos pasos:

   1. Obtenga la última etiqueta:
      ```bash
      git fetch --tags
      git checkout tags/v1.4.0
      ```
   2. Modifique `cdk.json` de la siguiente manera:
      ```json
      {
        ...,
        "useBedrockKnowledgeBasesForRag": true,
        ...
      }
      ```
   3. Implemente los cambios:
      ```bash
      npx cdk deploy
      ```

3. **Recrear sus bots**: Recree sus bots en Knowledge Base con las mismas definiciones (documentos, tamaño de fragmentos, etc.) que los bots de pgvector. Si tiene un gran volumen de documentos, restaurar desde la copia de seguridad del paso 1 facilitará este proceso. Para restaurar, podemos usar copias entre regiones. Para más detalles, visite [aquí](https://docs.aws.amazon.com/aws-backup/latest/devguide/restoring-s3.html). Para especificar el bucket restaurado, configure la sección `Origen de datos de S3` de la siguiente manera. La estructura de la ruta es `s3://<nombre-del-bucket>/<id-de-usuario>/<id-del-bot>/documents/`. Puede verificar el ID de usuario en el grupo de usuarios de Cognito y el ID del bot en la barra de direcciones de la pantalla de creación de bots.

![](../imgs/v1_to_v2_KB_s3_source.png)

**Tenga en cuenta que algunas características no están disponibles en Knowledge Bases, como la navegación web y la compatibilidad con transcripciones de YouTube (Planeando admitir el rastreador web ([issue](https://github.com/aws-samples/bedrock-chat/issues/557))).** Además, tenga en cuenta que el uso de Knowledge Bases generará cargos tanto para Aurora como para Knowledge Bases durante la transición.

4. **Eliminar API publicadas**: Todas las API publicadas previamente deberán ser republicadas antes de implementar v2 debido a la eliminación de VPC. Para hacerlo, primero deberá eliminar las API existentes. Usar la [función de Administración de API del administrador](../ADMINISTRATOR_es-ES.md) puede simplificar este proceso. Una vez completada la eliminación de todas las pilas de CloudFormation `APIPublishmentStackXXXX`, el entorno estará listo.

5. **Implementar v2**: Después del lanzamiento de v2, obtenga el origen etiquetado e impleméntelo de la siguiente manera (esto será posible una vez lanzado):
   ```bash
   git fetch --tags
   git checkout tags/v2.0.0
   npx cdk deploy
   ```

> [!Advertencia]
> Después de implementar v2, **TODOS LOS BOTS CON EL PREFIJO [No compatible, Solo lectura] QUEDARÁN OCULTOS.** Asegúrese de recrear los bots necesarios antes de actualizar para evitar cualquier pérdida de acceso.

> [!Consejo]
> Durante las actualizaciones de pila, es posible que encuentre mensajes repetidos como: "El controlador de recursos devolvió el mensaje: La subred 'subnet-xxx' tiene dependencias y no puede eliminarse". En tales casos, navegue a Consola de administración > EC2 > Interfaces de red y busque BedrockChatStack. Elimine las interfaces asociadas con este nombre para ayudar a garantizar un proceso de implementación más fluido.

### Pasos para usuarios de v1.3

Como se mencionó anteriormente, en v1.4, las Knowledge Bases deben crearse en la región bedrockRegion debido a restricciones regionales. Por lo tanto, deberá recrear la KB. Si ya ha probado KB en v1.3, recree el bot en v1.4 con las mismas definiciones. Siga los pasos descritos para usuarios de v1.2.