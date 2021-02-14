# FastAPIサンプル
FastAPIとsqliteを用いた簡易APIサンプル

## WHAT IS THIS
- 疑似ユーザーデータを作成しjsonファイル及びDBに保存
  - ユーザーデータは以下のようなjson形式でblobとして保存
    ```
    {
     "user": str,
     "key": str,
     "gender": str,
     "age": int,
     "hight": int,
     "weight": int,
     "adress": dict, # {country: str, state: str}
     "is_active": bool
    }
    ```
  - ユーザーデータはプログラム実行ごとにランダムで作成される
- FastAPI上でDBからデータを読み込み、GETでレスポンスを返すことができる
  - ex: `$ curl "http://localhost:8080/users/?limit=10"`


## HOW TO USE
### make data & insert DB
以下のコマンドを実行してください。

```
$ python make_dummy_data.py
```

- `./db/`および、`./file_dir/`下にAPI用のデータが作成されます。

### FastAPI
以下のコマンドでAPIサーバが起動します。

```
$ uvicorn server:app --port 8080
```

-  `localhost:8080/docs`にてswagerを確認できます。
