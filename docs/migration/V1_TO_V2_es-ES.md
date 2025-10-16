# Guía de Migración (v1 a v2)

## TL;DR

- **Para usuarios de v1.2 o anteriores**: Actualicen a v1.4 y recreen sus bots usando Knowledge Base (KB). Después de un período de transición, una vez que confirmen que todo funciona según lo esperado con KB, procedan a actualizar a v2.
- **Para usuarios de v1.3**: Incluso si ya están usando KB, se **recomienda encarecidamente** actualizar a v1.4 y recrear sus bots. Si todavía están usando pgvector, migren recreando sus bots usando KB en v1.4.
- **Para usuarios que deseen continuar usando pgvector**: No se recomienda actualizar a v2 si planean seguir usando pgvector. La actualización a v2 eliminará todos los recursos relacionados con pgvector, y el soporte futuro ya no estará disponible. Continúen usando v1 en este caso.
- Tengan en cuenta que **la actualización a v2 resultará en la eliminación de todos los recursos relacionados con Aurora.** Las actualizaciones futuras se centrarán exclusivamente en v2, quedando v1 obsoleta.

## Introducción

### Qué va a ocurrir

La actualización v2 introduce un cambio importante al reemplazar pgvector en Aurora Serverless y la incrustación basada en ECS con [Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html). Este cambio no es compatible con versiones anteriores.

### Por qué este repositorio ha adoptado Knowledge Bases y descontinuado pgvector

Hay varias razones para este cambio:

#### Mejor precisión en RAG

- Knowledge Bases utiliza OpenSearch Serverless como backend, permitiendo búsquedas híbridas tanto de texto completo como de vectores. Esto resulta en una mejor precisión al responder preguntas que incluyen nombres propios, con los que pgvector tenía dificultades.
- También soporta más opciones para mejorar la precisión de RAG, como fragmentación y análisis avanzados.
- Knowledge Bases ha estado disponible de forma general durante casi un año desde octubre de 2024, con características ya añadidas como el rastreo web. Se esperan actualizaciones futuras, facilitando la adopción de funcionalidades avanzadas a largo plazo. Por ejemplo, aunque este repositorio no ha implementado características como la importación desde buckets S3 existentes (una característica frecuentemente solicitada) en pgvector, ya está soportada en KB (KnowledgeBases).

#### Mantenimiento

- La configuración actual de ECS + Aurora depende de numerosas bibliotecas, incluyendo las de análisis de PDF, rastreo web y extracción de transcripciones de YouTube. En comparación, las soluciones gestionadas como Knowledge Bases reducen la carga de mantenimiento tanto para los usuarios como para el equipo de desarrollo del repositorio.

## Proceso de Migración (Resumen)

Recomendamos encarecidamente actualizar a v1.4 antes de pasar a v2. En v1.4, puedes usar tanto pgvector como bots de Knowledge Base, lo que permite un período de transición para recrear tus bots existentes de pgvector en Knowledge Base y verificar que funcionan según lo esperado. Incluso si los documentos RAG permanecen idénticos, ten en cuenta que los cambios en el backend a OpenSearch pueden producir resultados ligeramente diferentes, aunque generalmente similares, debido a diferencias como los algoritmos k-NN.

Al establecer `useBedrockKnowledgeBasesForRag` como true en `cdk.json`, puedes crear bots usando Knowledge Bases. Sin embargo, los bots de pgvector pasarán a ser de solo lectura, impidiendo la creación o edición de nuevos bots pgvector.

![](../imgs/v1_to_v2_readonly_bot.png)

En v1.4, también se introducen los [Guardrails for Amazon Bedrock](https://aws.amazon.com/jp/bedrock/guardrails/). Debido a las restricciones regionales de Knowledge Bases, el bucket S3 para cargar documentos debe estar en la misma región que `bedrockRegion`. Recomendamos hacer una copia de seguridad de los buckets de documentos existentes antes de actualizar, para evitar tener que cargar manualmente grandes cantidades de documentos más tarde (ya que la funcionalidad de importación de buckets S3 está disponible).

## Proceso de Migración (Detalle)

Los pasos difieren dependiendo de si estás usando v1.2 o anterior, o v1.3.

![](../imgs/v1_to_v2_arch.png)

### Pasos para usuarios de v1.2 o anterior

1. **Respalda tu bucket de documentos existente (opcional pero recomendado).** Si tu sistema ya está en operación, recomendamos encarecidamente este paso. Respalda el bucket llamado `bedrockchatstack-documentbucketxxxx-yyyy`. Por ejemplo, podemos usar [AWS Backup](https://docs.aws.amazon.com/aws-backup/latest/devguide/s3-backups.html).

2. **Actualiza a v1.4**: Obtén la última etiqueta v1.4, modifica `cdk.json` y despliega. Sigue estos pasos:

   1. Obtén la última etiqueta:
      ```bash
      git fetch --tags
      git checkout tags/v1.4.0
      ```
   2. Modifica `cdk.json` de la siguiente manera:
      ```json
      {
        ...,
        "useBedrockKnowledgeBasesForRag": true,
        ...
      }
      ```
   3. Despliega los cambios:
      ```bash
      npx cdk deploy
      ```

3. **Recrea tus bots**: Recrea tus bots en Knowledge Base con las mismas definiciones (documentos, tamaño de fragmento, etc.) que los bots de pgvector. Si tienes un gran volumen de documentos, restaurar desde el respaldo del paso 1 hará este proceso más fácil. Para restaurar, podemos usar la restauración de copias entre regiones. Para más detalles, visita [aquí](https://docs.aws.amazon.com/aws-backup/latest/devguide/restoring-s3.html). Para especificar el bucket restaurado, configura la sección `S3 Data Source` como se muestra a continuación. La estructura de la ruta es `s3://<bucket-name>/<user-id>/<bot-id>/documents/`. Puedes verificar el ID de usuario en el grupo de usuarios de Cognito y el ID del bot en la barra de direcciones en la pantalla de creación del bot.

![](../imgs/v1_to_v2_KB_s3_source.png)

**Ten en cuenta que algunas funciones no están disponibles en Knowledge Bases, como el rastreo web y el soporte de transcripción de YouTube (Se planea dar soporte al rastreador web ([issue](https://github.com/aws-samples/bedrock-chat/issues/557))).** Además, ten en cuenta que usar Knowledge Bases generará cargos tanto por Aurora como por Knowledge Bases durante la transición.

4. **Elimina las APIs publicadas**: Todas las APIs previamente publicadas deberán ser republicadas antes de desplegar v2 debido a la eliminación de VPC. Para hacer esto, necesitarás eliminar primero las APIs existentes. Usar la [función de Gestión de API del administrador](../ADMINISTRATOR_es-ES.md) puede simplificar este proceso. Una vez que se complete la eliminación de todas las pilas CloudFormation `APIPublishmentStackXXXX`, el entorno estará listo.

5. **Despliega v2**: Después del lanzamiento de v2, obtén el código fuente etiquetado y despliega de la siguiente manera (esto será posible una vez lanzado):
   ```bash
   git fetch --tags
   git checkout tags/v2.0.0
   npx cdk deploy
   ```

> [!Warning]
> Después de desplegar v2, **TODOS LOS BOTS CON EL PREFIJO [Unsupported, Read-only] SERÁN OCULTADOS.** Asegúrate de recrear los bots necesarios antes de actualizar para evitar cualquier pérdida de acceso.

> [!Tip]
> Durante las actualizaciones de la pila, podrías encontrar mensajes repetidos como: Resource handler returned message: "The subnet 'subnet-xxx' has dependencies and cannot be deleted." En tales casos, navega a la Consola de Administración > EC2 > Interfaces de Red y busca BedrockChatStack. Elimina las interfaces mostradas asociadas con este nombre para ayudar a garantizar un proceso de despliegue más fluido.

### Pasos para usuarios de v1.3

Como se mencionó anteriormente, en v1.4, Knowledge Bases debe crearse en la bedrockRegion debido a restricciones regionales. Por lo tanto, necesitarás recrear el KB. Si ya has probado KB en v1.3, recrea el bot en v1.4 con las mismas definiciones. Sigue los pasos descritos para los usuarios de v1.2.