# LLM-drevet Agent (ReAct)

## Hva er Agent (ReAct)?

En Agent er et avansert AI-system som bruker store språkmodeller (LLMs) som sin sentrale prosesseringsenhet. Den kombinerer resonnerings-evnene til LLMs med ytterligere funksjoner som planlegging og bruk av verktøy for å selvstendig utføre komplekse oppgaver. Agenter kan bryte ned kompliserte spørsmål, generere trinnvise løsninger, og samhandle med eksterne verktøy eller API-er for å samle informasjon eller utføre deloppgaver.

Dette eksempelet implementerer en Agent ved å bruke [ReAct (Reasoning + Acting)](https://www.promptingguide.ai/techniques/react)-tilnærmingen. ReAct gjør det mulig for agenten å løse komplekse oppgaver ved å kombinere resonnering og handlinger i en iterativ tilbakemeldingssløyfe. Agenten går gjentatte ganger gjennom tre nøkkeltrinn: Tanke, Handling og Observasjon. Den analyserer den nåværende situasjonen ved hjelp av LLM, bestemmer neste handling som skal tas, utfører handlingen ved hjelp av tilgjengelige verktøy eller API-er, og lærer av de observerte resultatene. Denne kontinuerlige prosessen gjør at agenten kan tilpasse seg dynamiske miljøer, forbedre nøyaktigheten i oppgaveløsning, og gi kontekstbevisste løsninger.

Implementeringen drives av [Strands Agents](https://strandsagents.com/), et åpen kildekode-SDK som tar en modelldrevet tilnærming til å bygge AI-agenter. Strands tilbyr et lettvindt, fleksibelt rammeverk for å lage tilpassede verktøy ved hjelp av Python-dekoratører og støtter flere modellleverandører, inkludert Amazon Bedrock.

## Eksempel på bruksområde

En Agent som bruker ReAct kan anvendes i ulike scenarioer, og gir nøyaktige og effektive løsninger.

### Tekst-til-SQL

En bruker spør om "totalt salg for siste kvartal." Agenten tolker denne forespørselen, konverterer den til en SQL-spørring, kjører den mot databasen, og presenterer resultatene.

### Økonomisk prognose

En finansanalytiker trenger å lage en prognose for neste kvartals inntekter. Agenten samler relevant data, utfører nødvendige beregninger ved hjelp av finansielle modeller, og genererer en detaljert prognoserapport, samtidig som den sikrer nøyaktigheten i fremskrivningene.

## For å bruke Agent-funksjonen

For å aktivere Agent-funksjonaliteten for din tilpassede chatbot, følg disse trinnene:

Det er to måter å bruke Agent-funksjonen på:

### Bruke verktøy

For å aktivere Agent-funksjonaliteten med verktøybruk for din tilpassede chatbot, følg disse trinnene:

1. Naviger til Agent-seksjonen i skjermbildet for tilpasset bot.

2. I Agent-seksjonen vil du finne en liste over tilgjengelige verktøy som kan brukes av Agenten. Som standard er alle verktøy deaktivert.

3. For å aktivere et verktøy, slå på bryteren ved siden av det ønskede verktøyet. Når et verktøy er aktivert, vil Agenten ha tilgang til det og kan bruke det ved behandling av brukerforespørsler.

![](./imgs/agent_tools.png)

4. For eksempel lar "Internettsøk"-verktøyet Agenten hente informasjon fra internett for å svare på brukerspørsmål.

![](./imgs/agent1.png)
![](./imgs/agent2.png)

5. Du kan utvikle og legge til dine egne tilpassede verktøy for å utvide Agentens kapasitet. Se seksjonen [Hvordan utvikle dine egne verktøy](#how-to-develop-your-own-tools) for mer informasjon om å lage og integrere tilpassede verktøy.

### Bruke Bedrock Agent

Du kan benytte en [Bedrock Agent](https://aws.amazon.com/bedrock/agents/) opprettet i Amazon Bedrock.

Først må du opprette en Agent i Bedrock (f.eks. via Management Console). Deretter spesifiserer du Agent-ID-en i innstillingsskjermbildet for tilpasset bot. Når dette er satt, vil chatboten din bruke Bedrock Agent til å behandle brukerforespørsler.

![](./imgs/bedrock_agent_tool.png)

## Hvordan utvikle dine egne verktøy

For å utvikle dine egne tilpassede verktøy for Agenten ved hjelp av Strands SDK, følg disse retningslinjene:

### Om Strands-verktøy

Strands tilbyr en enkel `@tool`-dekoratør som transformerer vanlige Python-funksjoner til AI-agent-verktøy. Dekoratøren henter automatisk ut informasjon fra funksjonens docstring og type hints for å lage verktøyspesifikasjoner som LLM kan forstå og bruke. Denne tilnærmingen utnytter Pythons innebygde funksjoner for en ryddig, funksjonell verktøyutviklingsopplevelse.

For detaljert informasjon om Strands-verktøy, se [Python Tools-dokumentasjonen](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/tools/python-tools/).

### Grunnleggende verktøyoppretting

Opprett en ny funksjon dekorert med `@tool`-dekoratøren fra Strands:

```python
from strands import tool

@tool
def calculator(expression: str) -> dict:
    """
    Perform mathematical calculations safely.

    Args:
        expression: Mathematical expression to evaluate (e.g., "2+2", "10*5", "sqrt(16)")

    Returns:
        dict: Result in Strands format with toolUseId, status, and content
    """
    try:
        # Your calculation logic here
        result = eval(expression)  # Note: Use safe evaluation in production
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

### Verktøy med bot-kontekst (Closure-mønster)

For å få tilgang til bot-informasjon (BotModel), bruk et closure-mønster som fanger bot-konteksten:

```python
from strands import tool
from app.repositories.models.custom_bot import BotModel

def create_calculator_tool(bot: BotModel | None = None):
    """Create calculator tool with bot context closure."""

    @tool
    def calculator(expression: str) -> dict:
        """
        Perform mathematical calculations safely.

        Args:
            expression: Mathematical expression to evaluate (e.g., "2+2", "10*5", "sqrt(16)")

        Returns:
            dict: Result in Strands format with toolUseId, status, and content
        """
        # Access bot context within the tool
        if bot:
            print(f"Tool used by bot: {bot.id}")

        try:
            result = eval(expression)  # Use safe evaluation in production
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

### Krav til returformat

Alle Strands-verktøy må returnere en ordbok med følgende struktur:

```python
{
    "toolUseId": "placeholder",  # Will be replaced by Strands
    "status": "success" | "error",
    "content": [
        {"text": "Simple text response"} |
        {"json": {"key": "Complex data object"}}
    ]
}
```

- Bruk `{"text": "message"}` for enkle tekstsvar
- Bruk `{"json": data}` for komplekse data som skal bevares som strukturert informasjon
- Sett alltid `status` til enten `"success"` eller `"error"`

### Implementeringsretningslinjer

- Funksjonsnavnet og docstringen brukes når LLM vurderer hvilket verktøy som skal brukes. Docstringen er innebygd i prompten, så beskriv verktøyets formål og parametere presist.

- Se på eksempelimplementasjonen av et [BMI-beregningsverktøy](../examples/agents/tools/bmi/bmi_strands.py). Dette eksempelet viser hvordan du lager et verktøy som beregner kroppsmasseindeks (BMI) ved hjelp av Strands `@tool`-dekoratøren og closure-mønsteret.

- Etter at utviklingen er fullført, plasser implementasjonsfilen din i [backend/app/strands_integration/tools/](../backend/app/strands_integration/tools/) katalogen. Åpne deretter [backend/app/strands_integration/utils.py](../backend/app/strands_integration/utils.py) og rediger `get_strands_registered_tools` for å inkludere ditt nye verktøy.

- [Valgfritt] Legg til tydelige navn og beskrivelser for frontend. Dette trinnet er valgfritt, men hvis du ikke gjør dette trinnet, vil verktøynavnet og beskrivelsen fra funksjonen din bli brukt. Siden disse er for LLM-forbruk, anbefales det å legge til brukervennlige forklaringer for bedre brukeropplevelse.

  - Rediger i18n-filer. Åpne [en/index.ts](../frontend/src/i18n/en/index.ts) og legg til ditt eget `name` og `description` under `agent.tools`.
  - Rediger også `xx/index.ts`. Der `xx` representerer landkoden du ønsker.

- Kjør `npx cdk deploy` for å distribuere endringene dine. Dette vil gjøre ditt tilpassede verktøy tilgjengelig i skjermbildet for tilpassede boter.