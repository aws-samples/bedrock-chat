# Agent wspierany przez LLM (ReAct)

## Czym jest Agent (ReAct)?

Agent to zaawansowany system sztucznej inteligencji, który wykorzystuje duże modele języka (LLM) jako centralny silnik obliczeniowy. Łączy on możliwości rozumowania LLM z dodatkowymi funkcjonalnościami, takimi jak planowanie i używanie narzędzi, aby autonomicznie wykonywać złożone zadania. Agenci mogą rozbijać skomplikowane zapytania, generować rozwiązania krok po kroku oraz wchodzić w interakcje z zewnętrznymi narzędziami lub API, aby zbierać informacje lub wykonywać podzadania.

Ten przykład implementuje Agenta przy użyciu podejścia [ReAct (Reasoning + Acting)](https://www.promptingguide.ai/techniques/react). ReAct umożliwia agentowi rozwiązywanie złożonych zadań poprzez łączenie rozumowania i działań w iteracyjnej pętli sprzężenia zwrotnego. Agent wielokrotnie przechodzi przez trzy kluczowe etapy: Myśl, Działanie i Obserwacja. Analizuje on bieżącą sytuację przy użyciu LLM, podejmuje decyzję o następnym działaniu, wykonuje to działanie za pomocą dostępnych narzędzi lub API i uczy się z zaobserwowanych wyników. Ten ciągły proces pozwala agentowi adaptować się do dynamicznych środowisk, poprawiać dokładność rozwiązywania zadań i dostarczać rozwiązań uwzględniających kontekst.

## Przykładowy Przypadek Użycia

Agent korzystający z ReAct może być stosowany w różnych scenariuszach, dostarczając dokładnych i wydajnych rozwiązań.

### Tekst-do-SQL

Użytkownik pyta o "całkowite sprzedaży za ostatni kwartał". Agent interpretuje to żądanie, przekształca je w zapytanie SQL, wykonuje je na bazie danych i prezentuje wyniki.

### Prognozowanie Finansowe

Analityk finansowy potrzebuje prognozy przychodów na następny kwartał. Agent zbiera odpowiednie dane, przeprowadza niezbędne obliczenia przy użyciu modeli finansowych i generuje szczegółowy raport prognostyczny, zapewniając dokładność projekcji.

## Jak korzystać z funkcji Agenta

Aby włączyć funkcjonalność Agenta dla Twojego dostosowanego chatbota, wykonaj następujące kroki:

1. Przejdź do sekcji Agent na ekranie niestandardowego bota.

2. W sekcji Agent znajdziesz listę dostępnych narzędzi, które mogą być używane przez Agenta. Domyślnie wszystkie narzędzia są wyłączone.

3. Aby aktywować narzędzie, po prostu przestaw przełącznik obok wybranego narzędzia. Po włączeniu narzędzia Agent będzie miał do niego dostęp i będzie mógł go wykorzystać podczas przetwarzania zapytań użytkownika.

![](./imgs/agent_tools.png)

> [!Ważne]
> Należy pamiętać, że włączenie dowolnego narzędzia w sekcji Agent automatycznie spowoduje potraktowanie funkcjonalności ["Wiedza"](https://aws.amazon.com/what-is/retrieval-augmented-generation/) również jako narzędzia. Oznacza to, że LLM autonomicznie zdecyduje, czy użyć "Wiedzy" do odpowiedzi na zapytania użytkownika, traktując ją jako jedno z dostępnych narzędzi.

4. Domyślnie dostępne jest narzędzie "Wyszukiwanie w Internecie". To narzędzie pozwala Agentowi pobierać informacje z internetu, aby odpowiadać na pytania użytkowników.

![](./imgs/agent1.png)
![](./imgs/agent2.png)

To narzędzie korzysta z [DuckDuckGo](https://duckduckgo.com/), które posiada ograniczenia liczby zapytań. Jest odpowiednie do celów proof of concept lub demonstracji, ale jeśli chcesz używać go w środowisku produkcyjnym, zalecamy użycie innego interfejsu API wyszukiwania.

5. Możesz opracować i dodać własne niestandardowe narzędzia, aby rozszerzyć możliwości Agenta. Więcej informacji na temat tworzenia i integracji niestandardowych narzędzi znajdziesz w sekcji [Jak opracować własne narzędzia](#how-to-develop-your-own-tools).

## Jak tworzyć własne narzędzia

Aby stworzyć własne niestandardowe narzędzia dla Agenta, postępuj zgodnie z poniższymi wytycznymi:

- Utwórz nową klasę, która dziedziczy z klasy `AgentTool`. Mimo że interfejs jest kompatybilny z LangChain, ta przykładowa implementacja udostępnia własną klasę `AgentTool`, z której należy dziedziczyć ([źródło](../backend/app/agents/tools/agent_tool.py)).

- Zapoznaj się z przykładową implementacją [narzędzia do obliczania BMI](../examples/agents/tools/bmi/bmi.py). Ten przykład pokazuje, jak utworzyć narzędzie obliczające wskaźnik masy ciała (BMI) na podstawie danych wprowadzonych przez użytkownika.

  - Nazwa i opis zadeklarowane w narzędziu są używane, gdy LLM rozważa, które narzędzie powinno zostać użyte do odpowiedzi na pytanie użytkownika. Innymi słowy, są osadzone w monicie podczas wywoływania LLM. Dlatego zaleca się opisanie ich możliwie jak najdokładniej.

- [Opcjonalnie] Po wdrożeniu niestandardowego narzędzia zaleca się sprawdzenie jego funkcjonalności za pomocą skryptu testowego ([przykład](../examples/agents/tools/bmi/test_bmi.py)). Ten skrypt pomoże upewnić się, że narzędzie działa zgodnie z oczekiwaniami.

- Po zakończeniu tworzenia i testowania niestandardowego narzędzia przenieś plik implementacji do katalogu [backend/app/agents/tools/](../backend/app/agents/tools/). Następnie otwórz plik [backend/app/agents/utils.py](../backend/app/agents/utils.py) i edytuj `get_available_tools`, aby użytkownik mógł wybrać utworzone narzędzie.

- [Opcjonalnie] Dodaj przejrzyste nazwy i opisy dla interfejsu frontendowego. Ten krok jest opcjonalny, ale jeśli go nie wykonasz, będą używane nazwa i opis narzędzia zadeklarowane w narzędziu. Są one przeznaczone dla LLM, a nie dla użytkownika, więc zaleca się dodanie dedykowanego wyjaśnienia dla lepszego UX.

  - Edytuj pliki i18n. Otwórz [en/index.ts](../frontend/src/i18n/en/index.ts) i dodaj własną `name` i `description` w `agent.tools`.
  - Edytuj również `xx/index.ts`. Gdzie `xx` reprezentuje kod kraju, który chcesz.

- Uruchom `npx cdk deploy`, aby wdrożyć zmiany. Spowoduje to udostępnienie Twojego niestandardowego narzędzia na ekranie niestandardowego bota.

## Wkład

**Zapraszamy do współtworzenia repozytorium narzędzi!** Jeśli opracujesz użyteczne i dobrze zaimplementowane narzędzie, rozważ jego wkład do projektu poprzez zgłoszenie problemu lub utworzenie pull request.