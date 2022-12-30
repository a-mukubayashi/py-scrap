# py-scrap

- Python 3.10.9
- beautifulsoup4==4.11.1
- selenium selenium==4.6.0

## venv

### venv 環境の作成

```
python3 -m venv venv
```

### venv 環境の有効化

```
source venv/bin/activate
```

有効にするとプロンプトの前に環境名（venv）が表示される

初回は使われている plugin を install する

```
pip install -r requirements.txt
```

新しく plugin を install する

```
pip install selenium==4.6.0
```

### 仮想環境に install 済みの plugin を確認

```
pip freeze
```

requirements に書き込み

```
pip freeze > requirements.txt
```

### venv 環境の無効化

```
deactivate
```
