import json
from typing import Optional, List

from fastapi import FastAPI
from sqlalchemy import create_engine, MetaData, select

app = FastAPI()
db = create_engine("sqlite:///db/init.db")
metadata = MetaData(bind=db, reflect=True)


def rowproxy_to_dict(resultproxy):
    """sqlalchemyのrowproxy型データをdict型へ変換
    input  << resultproxy: resultproxy型のデータ(binary)
    output >> result_dict: 辞書型に変換されたデータ(dict)
    """
    result_dict = dict()
    for rowproxy_ in resultproxy:
        rowproxy = rowproxy_.decode(encoding='utf-8')
        rowproxy = json.loads(rowproxy)
        for column, value in rowproxy.items():
            result_dict = {**result_dict, **{column: value}}
    return result_dict


@app.get("/users/")
async def get_users(limit: Optional[int] = 10):
    table = metadata.tables["users"]
    result = select([table]).limit(limit).execute()
    users = list()
    for r in result:
        user = rowproxy_to_dict(r)
        users.append(user)

    return users
