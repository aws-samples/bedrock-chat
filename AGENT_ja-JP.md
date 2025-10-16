# LLM駆動型エージェント (ReAct)

## エージェント (ReAct) とは?

エージェントは、大規模言語モデル (LLM) を中核の計算エンジンとして活用する高度なAIシステムです。LLMの推論能力と、プランニングやツール使用などの追加機能を組み合わせることで、複雑なタスクを自律的に実行することができます。エージェントは複雑なクエリを分解し、ステップバイステップの解決策を生成し、外部ツールやAPIと連携して情報収集やサブタスクの実行を行うことができます。

このサンプルでは、[ReAct (Reasoning + Acting)](https://www.promptingguide.ai/techniques/react)アプローチを用いてエージェントを実装しています。ReActにより、エージェントは推論とアクションを反復的なフィードバックループで組み合わせることで、複雑なタスクを解決することができます。エージェントは、思考(Thought)、行動(Action)、観察(Observation)という3つの重要なステップを繰り返し実行します。LLMを使用して現状を分析し、次に取るべきアクションを決定し、利用可能なツールやAPIを使用してアクションを実行し、観察された結果から学習します。この継続的なプロセスにより、エージェントは動的な環境に適応し、タスク解決の精度を向上させ、状況に応じたソリューションを提供することができます。

この実装は、[Strands Agents](https://strandsagents.com/)によって動作します。これはAIエージェントの構築にモデル駆動型アプローチを採用したオープンソースSDKです。StrandsはPythonデコレータを使用したカスタムツールの作成のための軽量で柔軟なフレームワークを提供し、Amazon Bedrockを含む複数のモデルプロバイダーをサポートしています。

## ユースケースの例

ReActを使用するエージェントは、さまざまなシナリオで適用でき、正確で効率的なソリューションを提供します。

### Text-to-SQL

ユーザーが「前四半期の総売上高」を尋ねた場合、エージェントはこのリクエストを解釈し、SQLクエリに変換し、データベースに対して実行して結果を表示します。

### 財務予測

財務アナリストが次四半期の収益を予測する必要がある場合、エージェントは関連データを収集し、財務モデルを使用して必要な計算を実行し、予測の正確性を確保しながら詳細な予測レポートを生成します。

## エージェント機能を使用するには

カスタマイズしたチャットボットのエージェント機能を有効にするには、以下の手順に従ってください：

エージェント機能を使用するには2つの方法があります：

### ツール使用機能の利用

カスタマイズしたチャットボットでツール使用によるエージェント機能を有効にするには、以下の手順に従ってください：

1. カスタムボット画面のエージェントセクションに移動します。

2. エージェントセクションには、エージェントが使用できるツールのリストが表示されます。デフォルトでは、すべてのツールが無効になっています。

3. ツールを有効にするには、目的のツールの横にあるスイッチを切り替えるだけです。ツールが有効になると、エージェントはそのツールにアクセスし、ユーザーのクエリを処理する際に使用できるようになります。

![](./imgs/agent_tools.png)

4. 例えば、「インターネット検索」ツールを使用すると、エージェントはユーザーの質問に答えるためにインターネットから情報を取得することができます。

![](./imgs/agent1.png)
![](./imgs/agent2.png)

5. エージェントの機能を拡張するために、独自のカスタムツールを開発して追加することができます。カスタムツールの作成と統合については、[独自のツールを開発する方法](#how-to-develop-your-own-tools)のセクションを参照してください。

### Bedrock Agentの使用

Amazon Bedrockで作成した[Bedrock Agent](https://aws.amazon.com/bedrock/agents/)を利用することができます。

まず、Bedrockでエージェントを作成し（例：マネジメントコンソール経由）、カスタムボット設定画面でエージェントIDを指定します。設定が完了すると、チャットボットはユーザーのクエリを処理するためにBedrock Agentを活用します。

![](./imgs/bedrock_agent_tool.png)

## 独自のツールを開発する方法

Strands SDKを使用してAgent用の独自カスタムツールを開発するには、以下のガイドラインに従ってください：

### Strands ツールについて

Strandsは、通常のPython関数をAIエージェントツールに変換する簡単な `@tool` デコレータを提供します。このデコレータは、関数のdocstringと型ヒントから情報を自動的に抽出し、LLMが理解して使用できるツール仕様を作成します。このアプローチは、クリーンで機能的なツール開発体験のためにPythonのネイティブ機能を活用します。

Strandsツールの詳細については、[Python Tools documentation](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/tools/python-tools/)を参照してください。

### 基本的なツールの作成

Strandsの `@tool` デコレータを使用して新しい関数を作成します：

```python
from strands import tool

@tool
def calculator(expression: str) -> dict:
    """
    安全に数学的計算を実行します。

    Args:
        expression: 評価する数式（例："2+2"、"10*5"、"sqrt(16)"）

    Returns:
        dict: toolUseId、status、contentを含むStrands形式の結果
    """
    try:
        # 計算ロジックをここに記述
        result = eval(expression)  # 注：本番環境では安全な評価を使用してください
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

### ボットコンテキストを持つツール（クロージャパターン）

ボット情報（BotModel）にアクセスするには、ボットコンテキストをキャプチャするクロージャパターンを使用します：

```python
from strands import tool
from app.repositories.models.custom_bot import BotModel

def create_calculator_tool(bot: BotModel | None = None):
    """ボットコンテキストクロージャを持つ計算機ツールを作成します。"""

    @tool
    def calculator(expression: str) -> dict:
        """
        安全に数学的計算を実行します。

        Args:
            expression: 評価する数式（例："2+2"、"10*5"、"sqrt(16)"）

        Returns:
            dict: toolUseId、status、contentを含むStrands形式の結果
        """
        # ツール内でボットコンテキストにアクセス
        if bot:
            print(f"Tool used by bot: {bot.id}")

        try:
            result = eval(expression)  # 本番環境では安全な評価を使用してください
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

### 戻り値フォーマットの要件

すべてのStrandsツールは、以下の構造を持つ辞書を返す必要があります：

```python
{
    "toolUseId": "placeholder",  # Strandsによって置き換えられます
    "status": "success" | "error",
    "content": [
        {"text": "シンプルなテキスト応答"} |
        {"json": {"key": "複雑なデータオブジェクト"}}
    ]
}
```

- シンプルなテキスト応答には `{"text": "メッセージ"}` を使用
- 構造化情報として保持すべき複雑なデータには `{"json": データ}` を使用
- `status` は常に `"success"` または `"error"` に設定

### 実装ガイドライン

- 関数名とdocstringは、LLMがどのツールを使用するか検討する際に使用されます。docstringはプロンプトに埋め込まれるため、ツールの目的とパラメータを正確に記述してください。

- [BMI計算ツール](../examples/agents/tools/bmi/bmi_strands.py)のサンプル実装を参照してください。この例は、Strands `@tool` デコレータとクロージャパターンを使用してBMI（Body Mass Index）を計算するツールを作成する方法を示しています。

- 開発完了後、実装ファイルを[backend/app/strands_integration/tools/](../backend/app/strands_integration/tools/)ディレクトリに配置してください。次に[backend/app/strands_integration/utils.py](../backend/app/strands_integration/utils.py)を開き、`get_strands_registered_tools`を編集して新しいツールを追加してください。

- [任意] フロントエンド用の分かりやすい名前と説明を追加します。このステップはオプションですが、実行しない場合は関数のツール名と説明が使用されます。これらはLLMが使用するものであるため、より良いUXのためにユーザーフレンドリーな説明を追加することをお勧めします。

  - i18nファイルを編集します。[en/index.ts](../frontend/src/i18n/en/index.ts)を開き、`agent.tools`に独自の`name`と`description`を追加します。
  - `xx/index.ts`も同様に編集します。`xx`は希望する国コードを表します。

- `npx cdk deploy`を実行して変更をデプロイします。これにより、カスタムボット画面で独自のカスタムツールが利用可能になります。