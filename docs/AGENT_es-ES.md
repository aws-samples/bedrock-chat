# Agente potenciado por LLM (ReAct)

## ¿Qué es el Agente (ReAct)?

Un Agente es un sistema avanzado de IA que utiliza modelos de lenguaje grandes (LLMs) como su motor computacional central. Combina las capacidades de razonamiento de los LLMs con funcionalidades adicionales como la planificación y el uso de herramientas para realizar tareas complejas de forma autónoma. Los agentes pueden desglosar consultas complicadas, generar soluciones paso a paso e interactuar con herramientas externas o APIs para recopilar información o ejecutar subtareas.

Este ejemplo implementa un Agente utilizando el enfoque [ReAct (Razonamiento + Actuación)](https://www.promptingguide.ai/techniques/react). ReAct permite al agente resolver tareas complejas combinando razonamiento y acciones en un bucle de retroalimentación iterativo. El agente pasa repetidamente por tres pasos clave: Pensamiento, Acción y Observación. Analiza la situación actual utilizando el LLM, decide la siguiente acción a tomar, ejecuta la acción utilizando herramientas o APIs disponibles, y aprende de los resultados observados. Este proceso continuo permite al agente adaptarse a entornos dinámicos, mejorar su precisión en la resolución de tareas y proporcionar soluciones contextualizadas.

La implementación está impulsada por [Strands Agents](https://strandsagents.com/), un SDK de código abierto que adopta un enfoque basado en modelos para construir agentes de IA. Strands proporciona un marco ligero y flexible para crear herramientas personalizadas utilizando decoradores de Python y es compatible con múltiples proveedores de modelos, incluyendo Amazon Bedrock.

## Caso de Uso de Ejemplo

Un Agente que utiliza ReAct puede aplicarse en varios escenarios, proporcionando soluciones precisas y eficientes.

### Texto a SQL

Un usuario solicita "las ventas totales del último trimestre". El Agente interpreta esta solicitud, la convierte en una consulta SQL, la ejecuta en la base de datos y presenta los resultados.

### Previsión Financiera

Un analista financiero necesita pronosticar los ingresos del próximo trimestre. El Agente recopila los datos relevantes, realiza los cálculos necesarios utilizando modelos financieros y genera un informe detallado de previsión, garantizando la precisión de las proyecciones.

## Para usar la función de Agente

Para habilitar la funcionalidad de Agente en tu chatbot personalizado, sigue estos pasos:

Hay dos formas de usar la función de Agente:

### Usando Herramientas

Para habilitar la funcionalidad de Agente con Herramientas en tu chatbot personalizado, sigue estos pasos:

1. Navega a la sección Agente en la pantalla del bot personalizado.

2. En la sección Agente, encontrarás una lista de herramientas disponibles que puede usar el Agente. Por defecto, todas las herramientas están deshabilitadas.

3. Para activar una herramienta, simplemente activa el interruptor junto a la herramienta deseada. Una vez que una herramienta está habilitada, el Agente tendrá acceso a ella y podrá utilizarla al procesar las consultas del usuario.

![](./imgs/agent_tools.png)

4. Por ejemplo, la herramienta "Búsqueda en Internet" permite al Agente obtener información de internet para responder preguntas de los usuarios.

![](./imgs/agent1.png)
![](./imgs/agent2.png)

5. Puedes desarrollar y añadir tus propias herramientas personalizadas para extender las capacidades del Agente. Consulta la sección [Cómo desarrollar tus propias herramientas](#how-to-develop-your-own-tools) para obtener más información sobre cómo crear e integrar herramientas personalizadas.

### Usando Bedrock Agent

Puedes utilizar un [Bedrock Agent](https://aws.amazon.com/bedrock/agents/) creado en Amazon Bedrock.

Primero, crea un Agente en Bedrock (por ejemplo, a través de la Consola de Administración). Luego, especifica el ID del Agente en la pantalla de configuración del bot personalizado. Una vez configurado, tu chatbot utilizará el Bedrock Agent para procesar las consultas de los usuarios.

![](./imgs/bedrock_agent_tool.png)

## Cómo desarrollar tus propias herramientas

Para desarrollar tus propias herramientas personalizadas para el Agente usando Strands SDK, sigue estas pautas:

### Acerca de las Herramientas Strands

Strands proporciona un decorador `@tool` simple que transforma funciones regulares de Python en herramientas para agentes de IA. El decorador extrae automáticamente información del docstring y las anotaciones de tipo de tu función para crear especificaciones de herramientas que el LLM puede entender y usar. Este enfoque aprovecha las características nativas de Python para una experiencia de desarrollo de herramientas limpia y funcional.

Para información detallada sobre las herramientas Strands, consulta la [documentación de Python Tools](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/tools/python-tools/).

### Creación Básica de Herramientas

Crea una nueva función decorada con el decorador `@tool` de Strands:

```python
from strands import tool

@tool
def calculator(expression: str) -> dict:
    """
    Realizar cálculos matemáticos de forma segura.

    Args:
        expression: Expresión matemática a evaluar (ej., "2+2", "10*5", "sqrt(16)")

    Returns:
        dict: Resultado en formato Strands con toolUseId, status y content
    """
    try:
        # Tu lógica de cálculo aquí
        result = eval(expression)  # Nota: Usar evaluación segura en producción
        return {
            "toolUseId": "placeholder",
            "status": "success",
            "content": [{"text": str(result)}]
        }
    except Exception as e:
        return {
            "toolUseId": "placeholder",
            "status": "error",
            "content": [{"text": f"Error: {str(e)}"}]
        }
```

### Herramientas con Contexto del Bot (Patrón Closure)

Para acceder a la información del bot (BotModel), usa un patrón closure que capture el contexto del bot:

```python
from strands import tool
from app.repositories.models.custom_bot import BotModel

def create_calculator_tool(bot: BotModel | None = None):
    """Crear herramienta calculadora con closure de contexto del bot."""

    @tool
    def calculator(expression: str) -> dict:
        """
        Realizar cálculos matemáticos de forma segura.

        Args:
            expression: Expresión matemática a evaluar (ej., "2+2", "10*5", "sqrt(16)")

        Returns:
            dict: Resultado en formato Strands con toolUseId, status y content
        """
        # Acceder al contexto del bot dentro de la herramienta
        if bot:
            print(f"Herramienta usada por el bot: {bot.id}")

        try:
            result = eval(expression)  # Usar evaluación segura en producción
            return {
                "toolUseId": "placeholder",
                "status": "success",
                "content": [{"text": str(result)}]
            }
        except Exception as e:
            return {
                "toolUseId": "placeholder",
                "status": "error",
                "content": [{"text": f"Error: {str(e)}"}]
            }

    return calculator
```

### Requisitos del Formato de Retorno

Todas las herramientas Strands deben devolver un diccionario con la siguiente estructura:

```python
{
    "toolUseId": "placeholder",  # Será reemplazado por Strands
    "status": "success" | "error",
    "content": [
        {"text": "Respuesta de texto simple"} |
        {"json": {"key": "Objeto de datos complejo"}}
    ]
}
```

- Usa `{"text": "mensaje"}` para respuestas de texto simples
- Usa `{"json": data}` para datos complejos que deben preservarse como información estructurada
- Siempre establece `status` como `"success"` o `"error"`

### Pautas de Implementación

- El nombre de la función y el docstring se utilizan cuando el LLM considera qué herramienta usar. El docstring se incrusta en el prompt, así que describe el propósito y los parámetros de la herramienta con precisión.

- Consulta la implementación de ejemplo de una [herramienta de cálculo de IMC](../examples/agents/tools/bmi/bmi_strands.py). Este ejemplo demuestra cómo crear una herramienta que calcula el Índice de Masa Corporal (IMC) usando el decorador `@tool` de Strands y el patrón closure.

- Después de completar el desarrollo, coloca tu archivo de implementación en el directorio [backend/app/strands_integration/tools/](../backend/app/strands_integration/tools/). Luego abre [backend/app/strands_integration/utils.py](../backend/app/strands_integration/utils.py) y edita `get_strands_registered_tools` para incluir tu nueva herramienta.

- [Opcional] Añade nombres y descripciones claras para el frontend. Este paso es opcional, pero si no lo haces, se usarán el nombre y la descripción de tu función. Como estos son para consumo del LLM, se recomienda añadir explicaciones amigables para el usuario para una mejor experiencia de usuario.

  - Edita los archivos i18n. Abre [en/index.ts](../frontend/src/i18n/en/index.ts) y añade tu propio `name` y `description` en `agent.tools`.
  - Edita también `xx/index.ts`. Donde `xx` representa el código de país que desees.

- Ejecuta `npx cdk deploy` para desplegar tus cambios. Esto hará que tu herramienta personalizada esté disponible en la pantalla de bot personalizado.