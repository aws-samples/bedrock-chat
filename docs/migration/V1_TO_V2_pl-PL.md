# Przewodnik migracji (z wersji 1 do 2)

## TL;DR

- **Dla użytkowników wersji 1.2 lub wcześniejszych**: Zaktualizuj do wersji 1.4 i odtwórz swoje boty przy użyciu Bazy Wiedzy (KB). Po okresie przejściowym, gdy potwierdzisz, że wszystko działa zgodnie z oczekiwaniami z KB, przejdź do aktualizacji do wersji 2.
- **Dla użytkowników wersji 1.3**: Nawet jeśli już korzystasz z KB, **zdecydowanie zaleca się** aktualizację do wersji 1.4 i ponowne utworzenie botów. Jeśli nadal używasz pgvector, dokonaj migracji, tworząc na nowo boty przy użyciu KB w wersji 1.4.
- **Dla użytkowników, którzy chcą nadal korzystać z pgvector**: Aktualizacja do wersji 2 nie jest zalecana, jeśli planujesz kontynuować korzystanie z pgvector. Aktualizacja do wersji 2 spowoduje usunięcie wszystkich zasobów związanych z pgvector, a wsparcie w przyszłości nie będzie już dostępne. W takim przypadku kontynuuj korzystanie z wersji 1.
- Należy pamiętać, że **aktualizacja do wersji 2 spowoduje usunięcie wszystkich zasobów związanych z Aurora.** Przyszłe aktualizacje będą koncentrować się wyłącznie na wersji 2, a wersja 1 zostanie wycofana.

## Wprowadzenie

### Co się stanie

Aktualizacja v2 wprowadza istotną zmianę, zastępując pgvector na Aurora Serverless i osadzanie oparte na ECS [Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html). Ta zmiana nie jest wstecznie kompatybilna.

### Dlaczego to repozytorium przyjęło Knowledge Bases i zaprzestało używania pgvector

Jest kilka powodów tej zmiany:

#### Ulepszona dokładność RAG

- Knowledge Bases używają OpenSearch Serverless jako zaplecza, umożliwiając wyszukiwanie hybrydowe zarówno pełnotekstowe, jak i wektorowe. Prowadzi to do lepszej dokładności w odpowiadaniu na pytania zawierające nazwy własne, z czym pgvector miał trudności.
- Oferuje również więcej opcji poprawy dokładności RAG, takich jak zaawansowane dzielenie i parsowanie.
- Knowledge Bases są ogólnie dostępne już prawie rok (stan na październik 2024), z funkcjami takimi jak indeksowanie stron internetowych. Oczekuje się przyszłych aktualizacji, co ułatwi długoterminowe przyjęcie zaawansowanej funkcjonalności. Na przykład, podczas gdy to repozytorium nie zaimplementowało takich funkcji jak importowanie z istniejących zasobników S3 (często zgłaszana funkcja) w pgvector, jest to już obsługiwane w KB (Knowledge Bases).

#### Utrzymanie

- Obecna konfiguracja ECS + Aurora zależy od licznych bibliotek, w tym do parsowania PDF, indeksowania stron internetowych i wyodrębniania transkrypcji YouTube. W porównaniu, rozwiązania zarządzane, takie jak Knowledge Bases, zmniejszają obciążenie związane z utrzymaniem zarówno dla użytkowników, jak i zespołu programistów repozytorium.

## Proces migracji (Podsumowanie)

Zdecydowanie zalecamy aktualizację do wersji 1.4 przed przejściem do wersji 2. W wersji 1.4 możesz używać zarówno botów pgvector, jak i botów Bazy Wiedzy, co pozwala na okres przejściowy, w którym możesz odtworzyć istniejące boty pgvector w Bazie Wiedzy i sprawdzić, czy działają zgodnie z oczekiwaniami. Nawet jeśli dokumenty RAG pozostaną identyczne, należy pamiętać, że zmiany w backendzie OpenSearch mogą powodować nieznacznie różne wyniki, choć generalnie podobne, ze względu na różnice w algorytmach k-NN.

Ustawiając `useBedrockKnowledgeBasesForRag` na true w pliku `cdk.json`, możesz tworzyć boty przy użyciu Baz Wiedzy. Jednak boty pgvector staną się tylko do odczytu, uniemożliwiając tworzenie lub edycję nowych botów pgvector.

![](../imgs/v1_to_v2_readonly_bot.png)

W wersji 1.4 wprowadzono również [Guardrails for Amazon Bedrock](https://aws.amazon.com/jp/bedrock/guardrails/). Ze względu na regionalne ograniczenia Baz Wiedzy, bucket S3 do przesyłania dokumentów musi znajdować się w tym samym regionie co `bedrockRegion`. Zalecamy utworzenie kopii zapasowej istniejących bucketów dokumentów przed aktualizacją, aby uniknąć ręcznego przesyłania dużej liczby dokumentów później (ponieważ dostępna jest funkcja importu bucketa S3).

## Proces migracji (Szczegóły)

Kroki różnią się w zależności od tego, czy używasz wersji v1.2 lub starszej, czy v1.3.

![](../imgs/v1_to_v2_arch.png)

### Kroki dla użytkowników wersji v1.2 lub starszej

1. **Utwórz kopię zapasową istniejącego zasobnika dokumentów (opcjonalne, ale zalecane).** Jeśli Twój system jest już w eksploatacji, zdecydowanie zalecamy ten krok. Utwórz kopię zapasową zasobnika o nazwie `bedrockchatstack-documentbucketxxxx-yyyy`. Na przykład możemy użyć [AWS Backup](https://docs.aws.amazon.com/aws-backup/latest/devguide/s3-backups.html).

2. **Aktualizacja do v1.4**: Pobierz najnowszy tag v1.4, zmodyfikuj `cdk.json` i wdróż. Postępuj zgodnie z następującymi krokami:

   1. Pobierz najnowszy tag:
      ```bash
      git fetch --tags
      git checkout tags/v1.4.0
      ```
   2. Zmodyfikuj `cdk.json` w następujący sposób:
      ```json
      {
        ...,
        "useBedrockKnowledgeBasesForRag": true,
        ...
      }
      ```
   3. Wdróż zmiany:
      ```bash
      npx cdk deploy
      ```

3. **Odtwórz swoje boty**: Odtwórz swoje boty w Knowledge Base z takimi samymi definicjami (dokumenty, rozmiar fragmentu itp.) jak boty pgvector. Jeśli masz dużą liczbę dokumentów, przywrócenie kopii zapasowej z kroku 1 ułatwi ten proces. Aby przywrócić, możemy użyć przywracania kopii między regionami. Więcej szczegółów znajdziesz [tutaj](https://docs.aws.amazon.com/aws-backup/latest/devguide/restoring-s3.html). Aby określić przywrócony zasobnik, ustaw sekcję `S3 Data Source` w następujący sposób. Struktura ścieżki to `s3://<nazwa-zasobnika>/<identyfikator-użytkownika>/<identyfikator-bota>/documents/`. Identyfikator użytkownika możesz sprawdzić w puli użytkowników Cognito, a identyfikator bota na pasku adresu podczas tworzenia bota.

![](../imgs/v1_to_v2_KB_s3_source.png)

**Należy pamiętać, że niektóre funkcje nie są dostępne w Knowledge Bases, takie jak web crawling i obsługa transkrypcji YouTube (planowane jest wsparcie web crawlera ([issue](https://github.com/aws-samples/bedrock-claude-chat/issues/557))).** Pamiętaj również, że korzystanie z Knowledge Bases będzie wiązało się z opłatami zarówno za Aurora, jak i Knowledge Bases podczas przejścia.

4. **Usuń opublikowane interfejsy API**: Wszystkie wcześniej opublikowane interfejsy API będą musiały zostać ponownie opublikowane przed wdrożeniem v2 z powodu usunięcia VPC. Aby to zrobić, musisz najpierw usunąć istniejące interfejsy API. Użycie [funkcji zarządzania interfejsami API administratora](../ADMINISTRATOR_pl-PL.md) może uprościć ten proces. Po całkowitym usunięciu wszystkich stosów CloudFormation `APIPublishmentStackXXXX` środowisko będzie gotowe.

5. **Wdróż v2**: Po wydaniu v2 pobierz źródło z tagiem i wdróż w następujący sposób (będzie to możliwe po wydaniu):
   ```bash
   git fetch --tags
   git checkout tags/v2.0.0
   npx cdk deploy
   ```

> [!Ostrzeżenie]
> Po wdrożeniu v2 **WSZYSTKIE BOTY Z PREFIKSEM [Nieobsługiwane, tylko do odczytu] ZOSTANĄ UKRYTE.** Upewnij się, że przed aktualizacją odtworzysz niezbędne boty, aby uniknąć utraty dostępu.

> [!Wskazówka]
> Podczas aktualizacji stosu możesz napotkać powtarzające się komunikaty w stylu: Resource handler returned message: "The subnet 'subnet-xxx' has dependencies and cannot be deleted." W takich przypadkach przejdź do Konsoli Zarządzania > EC2 > Interfejsy sieciowe i wyszukaj BedrockChatStack. Usuń wyświetlone interfejsy sieciowe powiązane z tą nazwą, aby zapewnić płynniejszy proces wdrażania.

### Kroki dla użytkowników wersji v1.3

Jak wspomniano wcześniej, w v1.4 Knowledge Bases muszą być tworzone w regionie bedrockRegion z powodu ograniczeń regionalnych. Dlatego będziesz musiał odtworzyć KB. Jeśli już testowałeś KB w v1.3, odtwórz bota w v1.4 z tymi samymi definicjami. Postępuj zgodnie z krokami opisanymi dla użytkowników v1.2.