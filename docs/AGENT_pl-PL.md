# Agent napędzany LLM (ReAct)

## Czym jest Agent (ReAct)?

Agent to zaawansowany system sztucznej inteligencji, który wykorzystuje duże modele językowe (LLM) jako centralny silnik obliczeniowy. Łączy on możliwości rozumowania LLM z dodatkowymi funkcjonalnościami, takimi jak planowanie i używanie narzędzi, aby autonomicznie wykonywać złożone zadania. Agenci mogą rozbijać skomplikowane zapytania, generować rozwiązania krok po kroku oraz współdziałać z zewnętrznymi narzędziami lub interfejsami API, aby zbierać informacje lub wykonywać podzadania.

Ten przykład implementuje Agenta przy użyciu podejścia [ReAct (Reasoning + Acting)](https://www.promptingguide.ai/techniques/react). ReAct umożliwia agentowi rozwiązywanie złożonych zadań poprzez łączenie rozumowania i działań w iteracyjnej pętli sprzężenia zwrotnego. Agent wielokrotnie przechodzi przez trzy kluczowe etapy: Myśl, Działanie i Obserwacja. Analizuje bieżącą sytuację za pomocą LLM, podejmuje decyzję o następnym działaniu, wykonuje działanie przy użyciu dostępnych narzędzi lub interfejsów API, a następnie uczy się z zaobserwowanych wyników. Ten ciągły proces pozwala agentowi adaptować się do dynamicznych środowisk, poprawiać dokładność rozwiązywania zadań i dostarczać rozwiązań uwzględniających kontekst.

## Przykładowy Przypadek Użycia

Agent korzystający z ReAct może być stosowany w różnych scenariuszach, dostarczając dokładnych i wydajnych rozwiązań.

### Tekst na SQL

Użytkownik pyta o „całkowite sprzedaży za ostatni kwartał". Agent interpretuje to żądanie, przekształca je w zapytanie SQL, wykonuje je w bazie danych i prezentuje wyniki.

### Prognozowanie Finansowe

Analityk finansowy potrzebuje prognozy przychodów na następny kwartał. Agent gromadzi odpowiednie dane, przeprowadza niezbędne obliczenia przy użyciu modeli finansowych i generuje szczegółowy raport prognostyczny, zapewniając dokładność projekcji.

## Jak korzystać z funkcji Agenta

Aby włączyć funkcjonalność Agenta dla Twojego dostosowanego chatbota, wykonaj następujące kroki:

Istnieją dwa sposoby użycia funkcji Agenta:

### Korzystanie z Użycia Narzędzi

Aby włączyć funkcjonalność Agenta z Użyciem Narzędzi dla Twojego dostosowanego chatbota, wykonaj następujące kroki:

1. Przejdź do sekcji Agenta na ekranie niestandardowego bota.

2. W sekcji Agenta znajdziesz listę dostępnych narzędzi, które mogą być używane przez Agenta. Domyślnie wszystkie narzędzia są wyłączone.

3. Aby aktywować narzędzie, po prostu przesuń przełącznik obok wybranego narzędzia. Po włączeniu narzędzia Agent będzie miał do niego dostęp i będzie mógł go wykorzystać podczas przetwarzania zapytań użytkownika.

![](./imgs/agent_tools.png)

4. Na przykład narzędzie "Wyszukiwanie w Internecie" pozwala Agentowi pobierać informacje z internetu, aby odpowiadać na pytania użytkowników.

![](./imgs/agent1.png)
![](./imgs/agent2.png)

5. Możesz tworzyć i dodawać własne niestandardowe narzędzia, aby rozszerzyć możliwości Agenta. Zapoznaj się z sekcją [Jak tworzyć własne narzędzia](#how-to-develop-your-own-tools), aby uzyskać więcej informacji na temat tworzenia i integracji niestandardowych narzędzi.

### Korzystanie z Agenta Bedrock

Możesz wykorzystać [Agenta Bedrock](https://aws.amazon.com/bedrock/agents/) utworzonego w Amazon Bedrock.

Najpierw utwórz Agenta w Bedrock (np. za pośrednictwem Konsoli Zarządzania). Następnie określ identyfikator Agenta na ekranie ustawień niestandardowego bota. Po ustawieniu Twój chatbot będzie korzystał z Agenta Bedrock do przetwarzania zapytań użytkowników.

![](./imgs/bedrock_agent_tool.png)

## Jak tworzyć własne narzędzia

Aby utworzyć własne niestandardowe narzędzia dla Agenta, postępuj zgodnie z poniższymi wytycznymi:

- Utwórz nową klasę, która dziedziczy po klasie `AgentTool`. Mimo że interfejs jest kompatybilny z LangChain, ta przykładowa implementacja udostępnia własną klasę `AgentTool`, którą należy odziedziczyć ([źródło](../backend/app/agents/tools/agent_tool.py)).

- Zapoznaj się z przykładową implementacją [narzędzia do obliczania BMI](../examples/agents/tools/bmi/bmi.py). Ten przykład pokazuje, jak utworzyć narzędzie obliczające wskaźnik masy ciała (BMI) na podstawie danych wprowadzonych przez użytkownika.

  - Nazwa i opis zadeklarowane w narzędziu są używane, gdy LLM rozważa, które narzędzie powinno zostać użyte do odpowiedzi na pytanie użytkownika. Innymi słowy, są osadzone w monicie podczas wywoływania LLM. Dlatego zaleca się opisanie ich jak najdokładniej.

- [Opcjonalnie] Po wdrożeniu niestandardowego narzędzia zaleca się sprawdzenie jego funkcjonalności za pomocą skryptu testowego ([przykład](../examples/agents/tools/bmi/test_bmi.py)). Ten skrypt pomoże upewnić się, że narzędzie działa zgodnie z oczekiwaniami.

- Po zakończeniu tworzenia i testowania niestandardowego narzędzia przenieś plik implementacji do katalogu [backend/app/agents/tools/](../backend/app/agents/tools/). Następnie otwórz [backend/app/agents/utils.py](../backend/app/agents/utils.py) i edytuj `get_available_tools`, aby użytkownik mógł wybrać utworzone narzędzie.

- [Opcjonalnie] Dodaj czytelne nazwy i opisy dla interfejsu użytkownika. Ten krok jest opcjonalny, ale jeśli go nie wykonasz, użyte zostaną nazwa i opis narzędzia zadeklarowane w narzędziu. Są one przeznaczone dla LLM, a nie dla użytkownika, więc zaleca się dodanie dedykowanego wyjaśnienia w celu poprawy UX.

  - Edytuj pliki i18n. Otwórz [en/index.ts](../frontend/src/i18n/en/index.ts) i dodaj własną `name` i `description` w `agent.tools`.
  - Edytuj również `xx/index.ts`. Gdzie `xx` reprezentuje kod kraju, który chcesz.

- Uruchom `npx cdk deploy`, aby wdrożyć zmiany. Spowoduje to udostępnienie niestandardowego narzędzia na ekranie niestandardowego bota.

## Wkład

**Zapraszamy do współtworzenia repozytorium narzędzi!** Jeśli opracujesz przydatne i dobrze zaimplementowane narzędzie, rozważ jego wkład do projektu, zgłaszając issue lub wysyłając pull request.