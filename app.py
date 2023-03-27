# Copyright 2022 The Casdoor Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.routing import Route
from starlette.middleware.sessions import SessionMiddleware

from config import Config
from api.account import router as account_router
from api.index import router as index_router
from api.login import router as login_router

app = FastAPI()

app.include_router(account_router)
# app.include_router(index_router)
app.include_router(login_router)

app.mount("/web", StaticFiles(directory="./web/dist", html=True), name="web")

@app.get("/", include_in_schema=False)
async def index(request: Request):
    dist_dir = os.path.abspath(os.path.join(os.getcwd(), "./web/dist"))
    return FileResponse(os.path.join(dist_dir, "index.html"))

@app.get("/{path:path}", include_in_schema=False)
async def serve_static(request: Request, path: str):
    if not path.startswith("api"):
        dist_dir = os.path.abspath(os.path.join(os.getcwd(), "./web/dist"))
        file_path = os.path.join(dist_dir, path)
        if os.path.exists(file_path):
            return FileResponse(file_path)
        else:
            return FileResponse(os.path.join(dist_dir, "index.html"))
    else:
        raise HTTPException(status_code=404, detail="Not found")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key=Config.SECRET_KEY,
    session_cookie="fastapi-session",
)

app.state.CASDOOR_SDK = Config().CASDOOR_SDK
app.state.REDIRECT_URI = Config().REDIRECT_URI
app.state.SECRET_TYPE = Config().SECRET_TYPE
app.state.SECRET_KEY = Config().SECRET_KEY

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)
