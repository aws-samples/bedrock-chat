# Przewodnik migracji (v1 do v2)

## TL;DR

- **Dla użytkowników v1.2 lub wcześniejszych**: Zaktualizuj do v1.4 i odtwórz swoje boty używając Knowledge Base (KB). Po okresie przejściowym, gdy potwierdzisz, że wszystko działa prawidłowo z KB, przejdź do aktualizacji do v2.
- **Dla użytkowników v1.3**: Nawet jeśli już używasz KB, **zdecydowanie zaleca się** aktualizację do v1.4 i ponowne utworzenie botów. Jeśli nadal używasz pgvector, przeprowadź migrację poprzez ponowne utworzenie botów za pomocą KB w v1.4.
- **Dla użytkowników, którzy chcą nadal korzystać z pgvector**: Aktualizacja do v2 nie jest zalecana, jeśli planujesz dalej korzystać z pgvector. Aktualizacja do v2 usunie wszystkie zasoby związane z pgvector, a przyszłe wsparcie nie będzie już dostępne. W tym przypadku kontynuuj używanie v1.
- Pamiętaj, że **aktualizacja do v2 spowoduje usunięcie wszystkich zasobów związanych z Aurora.** Przyszłe aktualizacje będą skupiać się wyłącznie na v2, a v1 zostanie wycofana.

## Wprowadzenie

### Co się wydarzy

Aktualizacja v2 wprowadza istotną zmianę, zastępując pgvector na Aurora Serverless i osadzanie oparte na ECS przez [Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html). Ta zmiana nie jest wstecznie kompatybilna.

### Dlaczego to repozytorium przyjęło Knowledge Bases i zrezygnowało z pgvector

Jest kilka powodów tej zmiany:

#### Ulepszona dokładność RAG

- Knowledge Bases wykorzystuje OpenSearch Serverless jako backend, umożliwiając hybrydowe wyszukiwanie łączące wyszukiwanie pełnotekstowe i wektorowe. Prowadzi to do lepszej dokładności w odpowiadaniu na pytania zawierające nazwy własne, z którymi pgvector miał trudności.
- Wspiera również więcej opcji poprawy dokładności RAG, takich jak zaawansowane dzielenie na fragmenty i parsowanie.
- Knowledge Bases są ogólnie dostępne od prawie roku (stan na październik 2024), z już dodanymi funkcjami jak crawling stron internetowych. Spodziewane są przyszłe aktualizacje, co ułatwi adoptowanie zaawansowanych funkcjonalności w dłuższej perspektywie. Na przykład, podczas gdy to repozytorium nie zaimplementowało funkcji takich jak importowanie z istniejących bucketów S3 (często żądana funkcja) w pgvector, jest to już wspierane w KB (KnowledgeBases).

#### Utrzymanie

- Obecna konfiguracja ECS + Aurora zależy od licznych bibliotek, w tym do parsowania PDF, crawlingu stron internetowych i wyodrębniania transkryptów z YouTube. W porównaniu, zarządzane rozwiązania jak Knowledge Bases zmniejszają obciążenie związane z utrzymaniem zarówno dla użytkowników, jak i zespołu rozwojowego repozytorium.

## Proces migracji (Podsumowanie)

Zdecydowanie zalecamy aktualizację do wersji v1.4 przed przejściem na v2. W v1.4 można korzystać zarówno z pgvector jak i botów Knowledge Base, co pozwala na okres przejściowy do odtworzenia istniejących botów pgvector w Knowledge Base i zweryfikowania, czy działają zgodnie z oczekiwaniami. Nawet jeśli dokumenty RAG pozostają identyczne, należy pamiętać, że zmiany w backendzie na OpenSearch mogą dawać nieco inne wyniki, choć generalnie podobne, ze względu na różnice w algorytmach k-NN.

Ustawiając `useBedrockKnowledgeBasesForRag` na true w `cdk.json`, można tworzyć boty wykorzystujące Knowledge Bases. Jednak boty pgvector staną się tylko do odczytu, uniemożliwiając tworzenie lub edycję nowych botów pgvector.

![](../imgs/v1_to_v2_readonly_bot.png)

W v1.4 wprowadzono również [Guardrails for Amazon Bedrock](https://aws.amazon.com/jp/bedrock/guardrails/). Ze względu na regionalne ograniczenia Knowledge Bases, bucket S3 do przesyłania dokumentów musi znajdować się w tym samym regionie co `bedrockRegion`. Zalecamy wykonanie kopii zapasowej istniejących bucketów z dokumentami przed aktualizacją, aby uniknąć konieczności ręcznego przesyłania dużej liczby dokumentów później (dostępna jest funkcja importu bucketa S3).

## Proces Migracji (Szczegóły)

Kroki różnią się w zależności od tego, czy używasz wersji v1.2 lub wcześniejszej, czy v1.3.

![](../imgs/v1_to_v2_arch.png)

### Kroki dla użytkowników v1.2 lub wcześniejszej

1. **Wykonaj kopię zapasową istniejącego bucketu dokumentów (opcjonalne, ale zalecane).** Jeśli Twój system jest już w użyciu, zdecydowanie zalecamy ten krok. Wykonaj kopię zapasową bucketu o nazwie `bedrockchatstack-documentbucketxxxx-yyyy`. Możemy na przykład użyć [AWS Backup](https://docs.aws.amazon.com/aws-backup/latest/devguide/s3-backups.html).

2. **Aktualizacja do v1.4**: Pobierz najnowszy tag v1.4, zmodyfikuj `cdk.json` i wdróż. Wykonaj następujące kroki:

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

3. **Odtwórz boty**: Odtwórz swoje boty w Knowledge Base z tymi samymi definicjami (dokumenty, rozmiar fragmentów itp.) co boty pgvector. Jeśli masz dużą ilość dokumentów, przywrócenie z kopii zapasowej z kroku 1 ułatwi ten proces. Aby przywrócić, możemy użyć przywracania kopii międzyregionalnych. Więcej szczegółów znajdziesz [tutaj](https://docs.aws.amazon.com/aws-backup/latest/devguide/restoring-s3.html). Aby określić przywrócony bucket, ustaw sekcję `S3 Data Source` jak poniżej. Struktura ścieżki to `s3://<bucket-name>/<user-id>/<bot-id>/documents/`. Możesz sprawdzić identyfikator użytkownika w puli użytkowników Cognito, a identyfikator bota na pasku adresu na ekranie tworzenia bota.

![](../imgs/v1_to_v2_KB_s3_source.png)

**Pamiętaj, że niektóre funkcje nie są dostępne w Knowledge Bases, takie jak crawling stron internetowych i obsługa transkrypcji YouTube (Planowane wsparcie dla crawlera stron ([issue](https://github.com/aws-samples/bedrock-chat/issues/557))).** Pamiętaj również, że korzystanie z Knowledge Bases będzie generować opłaty zarówno za Aurora, jak i Knowledge Bases podczas przejścia.

4. **Usuń opublikowane API**: Wszystkie wcześniej opublikowane API będą musiały zostać ponownie opublikowane przed wdrożeniem v2 ze względu na usunięcie VPC. W tym celu należy najpierw usunąć istniejące API. Użycie [funkcji zarządzania API administratora](../ADMINISTRATOR_pl-PL.md) może uprościć ten proces. Po zakończeniu usuwania wszystkich stosów CloudFormation `APIPublishmentStackXXXX` środowisko będzie gotowe.

5. **Wdróż v2**: Po wydaniu v2, pobierz oznaczone źródło i wdróż w następujący sposób (będzie to możliwe po wydaniu):
   ```bash
   git fetch --tags
   git checkout tags/v2.0.0
   npx cdk deploy
   ```

> [!Warning]
> Po wdrożeniu v2, **WSZYSTKIE BOTY Z PREFIKSEM [Unsupported, Read-only] ZOSTANĄ UKRYTE.** Upewnij się, że odtworzysz niezbędne boty przed aktualizacją, aby uniknąć utraty dostępu.

> [!Tip]
> Podczas aktualizacji stosu możesz napotkać powtarzające się komunikaty typu: Resource handler returned message: "The subnet 'subnet-xxx' has dependencies and cannot be deleted." W takich przypadkach przejdź do Management Console > EC2 > Network Interfaces i wyszukaj BedrockChatStack. Usuń wyświetlone interfejsy powiązane z tą nazwą, aby zapewnić płynniejszy proces wdrażania.

### Kroki dla użytkowników v1.3

Jak wspomniano wcześniej, w v1.4 Knowledge Bases muszą być tworzone w bedrockRegion ze względu na ograniczenia regionalne. Dlatego będziesz musiał odtworzyć KB. Jeśli już testowałeś KB w v1.3, odtwórz bota w v1.4 z tymi samymi definicjami. Postępuj zgodnie z krokami opisanymi dla użytkowników v1.2.