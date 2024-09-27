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

from casdoor import CasdoorSDK
from fastapi import APIRouter, Depends, Form
from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")  # 请确保已经创建了“templates”文件夹并包含“index.html”


@router.post("/api/signin", response_class=JSONResponse)
async def post_signin(request: Request):
    code = request.query_params.get("code")
    state = request.query_params.get("state")

    sdk = request.app.state.CASDOOR_SDK
    token = sdk.get_oauth_token(code)
    user = sdk.parse_jwt_token(token["access_token"])
    request.session["casdoorUser"] = user

    return {"status": "ok"}


@router.post("/api/signout", response_class=JSONResponse)
async def post_signout(request: Request):
    del request.session["casdoorUser"]
    return {"status": "ok"}


@router.get("/toLogin", response_class=HTMLResponse)
async def to_login(request: Request):
    sdk: CasdoorSDK = request.app.state.CASDOOR_SDK
    redirect_url = sdk.get_auth_link(redirect_uri=request.app.state.REDIRECT_URI, state='app-built-in')
    return templates.TemplateResponse("tologin.html", {"request": request, "redirect_url": redirect_url})
