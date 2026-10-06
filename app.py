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

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from starlette.middleware.sessions import SessionMiddleware

from api.account import router as account_router
from api.login import router as login_router
from config import Config

DIST_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "web", "dist"))

app = FastAPI()
app.include_router(account_router)
app.include_router(login_router)


# Serves the built frontend (web/dist), so the whole example can also run on port 5000 only.
@app.get("/{path:path}", include_in_schema=False)
async def serve_static(path: str):
    if path.startswith("api"):
        raise HTTPException(status_code=404, detail="Not found")

    file_path = os.path.join(DIST_DIR, path)
    if path and os.path.isfile(file_path):
        return FileResponse(file_path)

    index_path = os.path.join(DIST_DIR, "index.html")
    if not os.path.isfile(index_path):
        raise HTTPException(status_code=404, detail="The frontend is not built, run `yarn build` in web/")
    return FileResponse(index_path)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key=Config.SECRET_KEY,
    session_cookie="fastapi-session",
)

app.state.CASDOOR_SDK = Config.CASDOOR_SDK
app.state.REDIRECT_URI = Config.REDIRECT_URI

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=5000)
