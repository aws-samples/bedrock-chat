# Agente basado en LLM (ReAct)

## ¿Qué es el Agente (ReAct)?

Un Agente es un sistema de IA avanzado que utiliza modelos de lenguaje de gran escala (LLM) como su motor computacional central. Combina las capacidades de razonamiento de los LLM con funcionalidades adicionales como planificación y uso de herramientas para realizar tareas complejas de forma autónoma. Los Agentes pueden descomponer consultas complicadas, generar soluciones paso a paso e interactuar con herramientas externas o API para recopilar información o ejecutar subtareas.

Esta muestra implementa un Agente utilizando el enfoque [ReAct (Razonamiento + Acción)](https://www.promptingguide.ai/techniques/react). ReAct permite al agente resolver tareas complejas combinando razonamiento y acciones en un bucle de retroalimentación iterativo. El agente pasa repetidamente por tres pasos clave: Pensamiento, Acción y Observación. Analiza la situación actual utilizando el LLM, decide la siguiente acción a tomar, ejecuta la acción utilizando herramientas o API disponibles, y aprende de los resultados observados. Este proceso continuo permite al agente adaptarse a entornos dinámicos, mejorar la precisión de resolución de tareas y proporcionar soluciones conscientes del contexto.

## Caso de Uso de Ejemplo

Un Agente que utiliza ReAct puede aplicarse en diversos escenarios, proporcionando soluciones precisas y eficientes.

### Texto a SQL

Un usuario solicita "el total de ventas del último trimestre". El Agente interpreta esta solicitud, la convierte en una consulta SQL, la ejecuta contra la base de datos y presenta los resultados.

### Previsión Financiera

Un analista financiero necesita hacer una previsión de los ingresos del próximo trimestre. El Agente recopila los datos relevantes, realiza los cálculos necesarios utilizando modelos financieros y genera un informe de previsión detallado, garantizando la precisión de las proyecciones.

## Cómo utilizar la función de Agente

Para habilitar la funcionalidad de Agente en su chatbot personalizado, siga estos pasos:

1. Navegue hasta la sección de Agente en la pantalla del bot personalizado.

2. En la sección de Agente, encontrará una lista de herramientas disponibles que puede utilizar el Agente. De forma predeterminada, todas las herramientas están desactivadas.

3. Para activar una herramienta, simplemente active el interruptor junto a la herramienta deseada. Una vez que se habilita una herramienta, el Agente tendrá acceso a ella y podrá utilizarla al procesar consultas de usuario.

![](./imgs/agent_tools.png)

> [!Importante]
> Es importante tener en cuenta que habilitar cualquier herramienta en la sección de Agente tratará automáticamente la funcionalidad de ["Conocimiento"](https://aws.amazon.com/what-is/retrieval-augmented-generation/) como una herramienta también. Esto significa que el LLM determinará de forma autónoma si utilizar el "Conocimiento" para responder a las consultas del usuario, considerándolo como una de las herramientas disponibles.

4. De forma predeterminada, se proporciona la herramienta "Búsqueda de Internet". Esta herramienta permite al Agente buscar información en internet para responder preguntas de los usuarios.

![](./imgs/agent1.png)
![](./imgs/agent2.png)

Esta herramienta depende de [DuckDuckGo](https://duckduckgo.com/), que tiene un límite de tasa. Es adecuada para pruebas de concepto o demostración, pero si desea utilizarla en un entorno de producción, recomendamos usar otra API de búsqueda.

5. Puede desarrollar y agregar sus propias herramientas personalizadas para ampliar las capacidades del Agente. Consulte la sección [Cómo desarrollar sus propias herramientas](#how-to-develop-your-own-tools) para obtener más información sobre la creación e integración de herramientas personalizadas.

## Cómo desarrollar sus propias herramientas

Para desarrollar herramientas personalizadas para el Agente, siga estas directrices:

- Cree una nueva clase que herede de la clase `AgentTool`. Aunque la interfaz es compatible con LangChain, esta implementación de ejemplo proporciona su propia clase `AgentTool`, de la cual debe heredar ([source](../backend/app/agents/tools/agent_tool.py)).

- Consulte la implementación de ejemplo de una [herramienta de cálculo de IMC](../examples/agents/tools/bmi/bmi.py). Este ejemplo demuestra cómo crear una herramienta que calcula el Índice de Masa Corporal (IMC) basado en la entrada del usuario.

  - El nombre y la descripción declarados en la herramienta se utilizan cuando el LLM considera qué herramienta debe usarse para responder a la pregunta del usuario. En otras palabras, se incrustan en el prompt cuando se invoca el LLM. Por lo tanto, se recomienda describirlos con la mayor precisión posible.

- [Opcional] Una vez que haya implementado su herramienta personalizada, se recomienda verificar su funcionalidad mediante un script de prueba ([ejemplo](../examples/agents/tools/bmi/test_bmi.py)). Este script le ayudará a asegurarse de que su herramienta funciona como se espera.

- Después de completar el desarrollo y las pruebas de su herramienta personalizada, mueva el archivo de implementación al directorio [backend/app/agents/tools/](../backend/app/agents/tools/). Luego, abra [backend/app/agents/utils.py](../backend/app/agents/utils.py) y edite `get_available_tools` para que el usuario pueda seleccionar la herramienta desarrollada.

- [Opcional] Agregue nombres y descripciones claras para el frontend. Este paso es opcional, pero si no lo hace, se utilizarán el nombre y la descripción de la herramienta declarados en su herramienta. Estos son para el LLM pero no para el usuario, por lo que se recomienda agregar una explicación dedicada para mejorar la experiencia de usuario.

  - Edite los archivos i18n. Abra [en/index.ts](../frontend/src/i18n/en/index.ts) y agregue su propio `name` y `description` en `agent.tools`.
  - Edite también `xx/index.ts`. Donde `xx` representa el código de país que desee.

- Ejecute `npx cdk deploy` para implementar sus cambios. Esto hará que su herramienta personalizada esté disponible en la pantalla de bot personalizado.

## Contribución

**¡Las contribuciones al repositorio de herramientas son bienvenidas!** Si desarrollas una herramienta útil y bien implementada, considera contribuirla al proyecto enviando un issue o una pull request.