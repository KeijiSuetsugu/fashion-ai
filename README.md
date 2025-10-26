# Fashion AI Outfit Planner

このリポジトリは、ユーザーの希望に基づいてAIがファッションコーディネートを提案する簡易ツールです。顔画像を指定してフェイススワップをシミュレーションしつつ、上半身・下半身・小物・靴・靴下などを自動で選定します。

## 使い方

1. 依存関係は標準ライブラリのみです。Python 3.11 以上を用意してください。
2. 好みのスタイルやカラーを含むJSONファイルを作成します（例: `prefs.json`）。

```json
{
  "style": ["formal", "modern"],
  "color": ["black", "white"],
  "season": ["fall"],
  "weather": ["cool"],
  "favorites": ["Tailored Black Blazer"]
}
```

3. CLIを実行してコーディネートを生成します。

```bash
python main.py --preferences prefs.json --face my_face.png
```

4. 出力例:

```
提案されたAIコーディネート:
- Face: my_face.png
- Top: Tailored Black Blazer
- Bottom: Wide-Leg Trousers
- Footwear: Pointed Toe Heels
- Socks: Sheer Tights
- Accessory: Statement Leather Belt
- Bag: Minimalist Tote Bag

選定理由:
* topはformal, modernスタイルのキーワードにマッチしています。
* カラーパレット(black, white)に調和する色味です。
* 指定されたシーズン(fall)で着用しやすいアイテムです。
```

## テスト

```bash
pytest
```
