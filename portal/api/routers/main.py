import os
from typing import List

from azure.identity import VisualStudioCodeCredential
from azure.keyvault.secrets import SecretClient
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from .cosmosdb import DbConnection
from .models.timer_manager import TimerManager

# Azure Static Web App 制約でパスは /api 始まりとすること
app = FastAPI(
    docs_url="/api/docs/swagger",
    redoc_url="/api/docs/redoc",
    openapi_url="/api/docs/openapi.json",
)

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


# Azure Static Web App 制約でパスは /api 始まりとすること
@app.get("/api/timer-manager/{user_id}", response_model=List[TimerManager])
async def select(user_id: str):
    items = dbConn.timer_manager().find_by_userid(user_id)
    return items


@app.post("/api/timer-manager")
async def create(item: TimerManager):
    dbConn.timer_manager().create(item)
    return JSONResponse(status_code=status.HTTP_201_CREATED)


@app.put("/api/timer-manager")
async def update(item: TimerManager):
    dbConn.timer_manager().update(item)
    return JSONResponse(status_code=status.HTTP_200_OK)


@app.delete("/api/timer-manager")
async def delete(item: TimerManager):
    dbConn.timer_manager().delete(item)
    return JSONResponse(status_code=status.HTTP_200_OK)
