# League of Legends アイテムクイズ

League of Legendsのアイテム知識を鍛えるクイズアプリケーションです。

## 機能

- **クイズA**: アイテムツリークイズ - 表示されたアイテムの材料を選択
- **クイズB**: 価格当てクイズ - アイテムの価格を当てる
- **アルゴリズム解説**: クイズの仕組みを分かりやすく説明
- **連続正解カウンター**: モチベーション維持機能
- **最新データ**: Riot APIから最新のアイテム情報を取得

## セットアップ

### 1. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 2. 環境変数の設定（任意）

```bash
# .env.example をコピー
cp .env.example .env

# .env ファイルを編集して環境変数を設定
```

### 3. アプリケーションの起動

```bash
python app.py
```

ブラウザで `http://localhost:5000` にアクセスしてください。

## 環境変数

| 変数名 | 説明 | デフォルト |
|--------|------|-----------|
| `SECRET_PASSWORD` | 秘密の機能用パスワード（任意） | なし |
| `PORT` | サーバーポート | 5000 |

## 技術スタック

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **API**: Riot Games Data Dragon API
- **Session**: Flask-Session

## ライセンス

© 2024 LoLAnki. All rights reserved.
