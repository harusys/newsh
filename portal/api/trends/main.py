import os
import string
from typing import List

from azure.identity import VisualStudioCodeCredential
from azure.keyvault.secrets import SecretClient
from fastapi import FastAPI

from models.timer_manager import TimerManager

from .cosmosdb import DbConnection

app = FastAPI()

# 環境設定
COSMOS_ENDPOINT = os.environ["COSMOS_ENDPOINT"]
COSMOS_PRIMARYKEY = os.environ["COSMOS_PRIMARYKEY"]

# ローカル実行時は Key Vault 参照機能不可
if os.environ["Environment"] == "local":
    credential = VisualStudioCodeCredential()
    client = SecretClient(
        vault_url="https://kv-newsh-test-je-001.vault.azure.net",
        credential=credential,
    )
    # シークレットを直接取得
    COSMOS_ENDPOINT = client.get_secret("COSMOS-ENDPOINT").value
    COSMOS_PRIMARYKEY = client.get_secret("COSMOS-PRIMARYKEY").value

# インスタンス生成
dbConn = DbConnection(COSMOS_ENDPOINT, COSMOS_PRIMARYKEY)


@app.get("/timer_manager/{user_id}")
async def select(user_id: string) -> List[TimerManager]:
    dbConn.timer_manager().find_by_userid(user_id)


@app.post("/timer_manager")
async def create(req: TimerManager):
    dbConn.timer_manager().create(req)


@app.put("/timer_manager")
async def update(req: TimerManager):
    dbConn.timer_manager().update(req)


@app.delete("/timer_manager")
async def delete(user_id: string) -> TimerManager:
    dbConn.timer_manager().find_by_userid(user_id)
