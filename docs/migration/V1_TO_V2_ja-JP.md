# 移行ガイド（v1からv2へ）

## TL;DR

- **v1.2以前のバージョンをご利用の方**: v1.4にアップグレードし、ナレッジベース（KB）を使用してボットを再作成してください。移行期間を経て、KBで全ての機能が正常に動作することを確認した後、v2へのアップグレードを進めてください。
- **v1.3をご利用の方**: すでにKBを使用している場合でも、v1.4へのアップグレードとボットの再作成を**強く推奨**します。まだpgvectorを使用している場合は、v1.4でKBを使用してボットを再作成することで移行してください。
- **pgvectorの使用を継続したい方**: pgvectorの使用を継続する予定の場合、v2へのアップグレードは推奨されません。v2へのアップグレードによりpgvector関連のリソースがすべて削除され、今後のサポートも提供されなくなります。この場合はv1の使用を継続してください。
- **v2へのアップグレードにより、Aurora関連のリソースがすべて削除される**ことにご注意ください。今後のアップデートはv2に専念し、v1は非推奨となります。

## はじめに

### 実施される変更内容

v2アップデートでは、Aurora ServerlessとECSベースの埋め込みを[Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html)に置き換えるという大きな変更が導入されます。この変更には後方互換性がありません。

### このリポジトリがKnowledge Basesを採用しpgvectorを廃止した理由

この変更には以下のような理由があります：

#### RAGの精度向上

- Knowledge BasesはバックエンドとしてOpenSearch Serverlessを使用し、全文検索とベクトル検索の両方によるハイブリッド検索が可能です。これにより、pgvectorが苦手としていた固有名詞を含む質問への応答精度が向上します。
- また、高度なチャンキングやパーシングなど、RAGの精度を向上させるためのオプションがより多く用意されています。
- Knowledge Basesは2024年10月の時点で一般提供開始から約1年が経過しており、ウェブクローリングなどの機能も既に追加されています。今後もアップデートが予定されており、長期的に見て高度な機能の採用がより容易になると期待されます。例えば、このリポジトリではpgvectorで既存のS3バケットからのインポート（よくリクエストされる機能）を実装していませんでしたが、KB（KnowledgeBases）では既にサポートされています。

#### メンテナンス

- 現在のECS + Auroraのセットアップは、PDFパース、ウェブクローリング、YouTubeの字幕抽出など、多数のライブラリに依存しています。一方、Knowledge Basesのようなマネージドソリューションを使用することで、ユーザーとリポジトリの開発チームの両方のメンテナンス負担を軽減できます。

## 移行プロセス（概要）

v2への移行前にv1.4へのアップグレードを強く推奨します。v1.4では、pgvectorとKnowledge Baseの両方のボットを使用できるため、既存のpgvectorボットをKnowledge Baseで再作成し、期待通りに動作することを確認するための移行期間が設けられます。RAGドキュメントが同一であっても、バックエンドがOpenSearchに変更されることで、k-NNアルゴリズムなどの違いにより、結果が若干異なる可能性がありますが、一般的には類似した結果が得られます。

`cdk.json`で`useBedrockKnowledgeBasesForRag`をtrueに設定することで、Knowledge Basesを使用したボットを作成できます。ただし、pgvectorボットは読み取り専用となり、新しいpgvectorボットの作成や編集ができなくなります。

![](../imgs/v1_to_v2_readonly_bot.png)

v1.4では、[Guardrails for Amazon Bedrock](https://aws.amazon.com/jp/bedrock/guardrails/)も導入されています。Knowledge Basesの地域制限により、ドキュメントをアップロードするためのS3バケットは`bedrockRegion`と同じリージョンに存在する必要があります。S3バケットのインポート機能が利用可能なため、後で大量のドキュメントを手動でアップロードする必要がないよう、更新前に既存のドキュメントバケットをバックアップすることをお勧めします。

## 移行プロセス (詳細)

移行手順は、v1.2以前を使用しているか、v1.3を使用しているかによって異なります。

![](../imgs/v1_to_v2_arch.png)

### v1.2以前のユーザー向けの手順

1. **既存のドキュメントバケットのバックアップ（任意ですが推奨）。** システムが既に運用中の場合、このステップを強く推奨します。`bedrockchatstack-documentbucketxxxx-yyyy`という名前のバケットをバックアップします。例えば、[AWS Backup](https://docs.aws.amazon.com/aws-backup/latest/devguide/s3-backups.html)を使用できます。

2. **v1.4へのアップデート**: 最新のv1.4タグを取得し、`cdk.json`を修正してデプロイします。以下の手順に従ってください：

   1. 最新のタグを取得：
      ```bash
      git fetch --tags
      git checkout tags/v1.4.0
      ```
   2. `cdk.json`を以下のように修正：
      ```json
      {
        ...,
        "useBedrockKnowledgeBasesForRag": true,
        ...
      }
      ```
   3. 変更をデプロイ：
      ```bash
      npx cdk deploy
      ```

3. **ボットの再作成**: pgvectorボットと同じ定義（ドキュメント、チャンクサイズなど）でKnowledge Base上にボットを再作成します。ドキュメント量が多い場合、ステップ1のバックアップからの復元でこのプロセスが容易になります。復元には、クロスリージョンコピーの復元を使用できます。詳細は[こちら](https://docs.aws.amazon.com/aws-backup/latest/devguide/restoring-s3.html)をご覧ください。復元したバケットを指定するには、`S3 Data Source`セクションを以下のように設定します。パス構造は`s3://<bucket-name>/<user-id>/<bot-id>/documents/`です。ユーザーIDはCognitoユーザープールで、ボットIDはボット作成画面のアドレスバーで確認できます。

![](../imgs/v1_to_v2_KB_s3_source.png)

**WebクローリングやYouTubeトランスクリプトのサポートなど、Knowledge Basesでは利用できない機能があることにご注意ください（Webクローラーのサポートは計画中です[issue](https://github.com/aws-samples/bedrock-chat/issues/557)）。**また、移行期間中はAuroraとKnowledge Basesの両方に料金が発生することにご留意ください。

4. **公開済みAPIの削除**: VPCの削除により、v2をデプロイする前にすべての既存のAPIを再公開する必要があります。そのためには、まず既存のAPIを削除する必要があります。[管理者のAPI管理機能](../ADMINISTRATOR_ja-JP.md)を使用するとこのプロセスが簡単になります。すべての`APIPublishmentStackXXXX` CloudFormationスタックの削除が完了すると、環境の準備が整います。

5. **v2のデプロイ**: v2がリリースされた後、タグ付けされたソースを取得し、以下のようにデプロイします（リリース後に可能となります）：
   ```bash
   git fetch --tags
   git checkout tags/v2.0.0
   npx cdk deploy
   ```

> [!Warning]
> v2をデプロイした後、**プレフィックス[Unsupported, Read-only]が付いたすべてのボットは非表示になります。**アクセスが失われないよう、必要なボットをアップグレード前に再作成してください。

> [!Tip]
> スタックの更新中に、「Resource handler returned message: "The subnet 'subnet-xxx' has dependencies and cannot be deleted."」のようなメッセージが繰り返し表示される場合があります。その場合、マネジメントコンソール > EC2 > ネットワークインターフェイスに移動し、BedrockChatStackで検索してください。この名前に関連付けられた表示されているインターフェイスを削除すると、デプロイプロセスがスムーズになります。

### v1.3ユーザー向けの手順

前述の通り、v1.4ではリージョンの制限により、Knowledge BasesをbedrockRegionに作成する必要があります。そのため、KBを再作成する必要があります。v1.3でKBをすでにテストしている場合は、同じ定義でv1.4でボットを再作成してください。v1.2ユーザー向けの手順に従ってください。