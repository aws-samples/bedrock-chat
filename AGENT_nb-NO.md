# LLM-drevet Agent (ReAct)

## Hva er Agent (ReAct)?

En Agent er et avansert AI-system som bruker store språkmodeller (LLMs) som sin sentrale beregningsmator. Den kombinerer resonnementsfunksjonene til LLMs med ytterligere funksjonaliteter som planlegging og verktøysbruk for å autonomt utføre komplekse oppgaver. Agenter kan dele ned kompliserte forespørsler, generere trinnvise løsninger og samhandle med eksterne verktøy eller APIer for å samle informasjon eller utføre deloppgaver.

Denne eksempelet implementerer en Agent ved bruk av [ReAct (Reasoning + Acting)](https://www.promptingguide.ai/techniques/react) tilnærmingen. ReAct gjør det mulig for agenten å løse komplekse oppgaver ved å kombinere resonnement og handlinger i en iterativ tilbakemeldingssløyfe. Agenten går gjentatte ganger gjennom tre nøkkeltrinn: Tanke, Handling og Observasjon. Den analyserer den nåværende situasjonen ved hjelp av LLM-en, bestemmer neste handling som skal utføres, gjennomfører handlingen ved bruk av tilgjengelige verktøy eller APIer, og lærer av de observerte resultatene. Denne kontinuerlige prosessen gjør at agenten kan tilpasse seg dynamiske omgivelser, forbedre sin oppgaveløsningsnøyaktighet og gi kontekstbevisste løsninger.

## Eksempelbrukstilfelle

En Agent som bruker ReAct kan benyttes i forskjellige scenarioer og gir nøyaktige og effektive løsninger.

### Tekst-til-SQL

En bruker ber om "det totale salget for siste kvartal". Agenten tolker denne forespørselen, konverterer den til en SQL-spørring, kjører den mot databasen og presenterer resultatene.

### Finansiell prognose

En finansanalytiker trenger å lage prognose for neste kvartals inntekter. Agenten samler relevante data, utfører nødvendige beregninger ved bruk av finansielle modeller og genererer en detaljert prognose-rapport som sikrer nøyaktigheten til prosjeksjonene.

## Slik bruker du Agent-funksjonen

For å aktivere Agent-funksjonaliteten for din tilpassede chatbot, følg disse trinnene:

Det er to måter å bruke Agent-funksjonen på:

### Bruk av Verktøy

For å aktivere Agent-funksjonaliteten med Verktøybruk for din tilpassede chatbot, følg disse trinnene:

1. Naviger til Agent-seksjonen i den tilpassede bot-skjermen.

2. I Agent-seksjonen vil du finne en liste over tilgjengelige verktøy som kan brukes av Agenten. Som standard er alle verktøy deaktivert.

3. For å aktivere et verktøy, slår du ganske enkelt på bryteren ved siden av det ønskede verktøyet. Når et verktøy er aktivert, vil Agenten ha tilgang til det og kan bruke det ved behandling av brukerforespørsler.

![](./imgs/agent_tools.png)

4. For eksempel lar "Internett-søk"-verktøyet Agenten hente informasjon fra internett for å svare på brukerens spørsmål.

![](./imgs/agent1.png)
![](./imgs/agent2.png)

5. Du kan utvikle og legge til dine egne tilpassede verktøy for å utvide Agentens kapasiteter. Se [Hvordan utvikle dine egne verktøy](#how-to-develop-your-own-tools)-seksjonen for mer informasjon om å opprette og integrere tilpassede verktøy.

### Bruk av Bedrock Agent

Du kan benytte en [Bedrock Agent](https://aws.amazon.com/bedrock/agents/) opprettet i Amazon Bedrock.

Opprett først en Agent i Bedrock (f.eks. via Management Console). Angi deretter Agent-ID-en i innstillingsskjermen for den tilpassede boten. Når dette er gjort, vil din chatbot utnytte Bedrock-agenten for å behandle brukerforespørsler.

![](./imgs/bedrock_agent_tool.png)

## Hvordan utvikle dine egne verktøy

For å utvikle dine egne tilpassede verktøy for Agenten, følg disse retningslinjene:

- Opprett en ny klasse som arver fra `AgentTool`-klassen. Selv om grensesnittet er kompatibelt med LangChain, gir denne eksempelimplementeringen sin egen `AgentTool`-klasse, som du bør arve fra ([kilde](../backend/app/agents/tools/agent_tool.py)).

- Se på eksempelimplementeringen av et [BMI-beregningsverktøy](../examples/agents/tools/bmi/bmi.py). Dette eksempelet viser hvordan du oppretter et verktøy som beregner Body Mass Index (BMI) basert på brukerinput.

  - Navnet og beskrivelsen som er erklært på verktøyet, brukes når LLM vurderer hvilket verktøy som skal brukes for å svare på brukerens spørsmål. Med andre ord er de innebygd i prompten når LLM påkalles. Så det anbefales å beskrive så presist som mulig.

- [Valgfritt] Når du har implementert ditt tilpassede verktøy, anbefales det å verifisere dets funksjonalitet ved hjelp av testskriptet ([eksempel](../examples/agents/tools/bmi/test_bmi.py)). Dette skriptet vil hjelpe deg å sikre at verktøyet fungerer som forventet.

- Etter at du har fullført utviklingen og testingen av ditt tilpassede verktøy, flytt implementeringsfilen til [backend/app/agents/tools/](../backend/app/agents/tools/)-mappen. Åpern så [backend/app/agents/utils.py](../backend/app/agents/utils.py) og rediger `get_available_tools` slik at brukeren kan velge det utviklede verktøyet.

- [Valgfritt] Legg til tydelige navn og beskrivelser for frontend. Dette trinnet er valgfritt, men hvis du ikke gjør dette trinnet, vil verktøynavnet og beskrivelsen som er erklært i ditt verktøy, bli brukt. De er for LLM, ikke for brukeren, så det anbefales å legge til en dedikert forklaring for bedre brukeropplevelse.

  - Rediger i18n-filer. Åpn [en/index.ts](../frontend/src/i18n/en/index.ts) og legg til ditt eget `name` og `description` under `agent.tools`.
  - Rediger også `xx/index.ts`. Hvor `xx` representerer landkoden du ønsker.

- Kjør `npx cdk deploy` for å distribuere endringene dine. Dette vil gjøre ditt tilpassede verktøy tilgjengelig på skjermen for tilpasset bot.

## Bidrag

**Bidrag til verktøylageret er velkomne!** Hvis du utvikler et nyttig og godt implementert verktøy, kan du vurdere å bidra med det til prosjektet ved å sende inn en issue eller en pull request.