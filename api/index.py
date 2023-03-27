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

from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from .utils import authz_required

router = APIRouter()
templates = Jinja2Templates(directory="templates")  # 请确保已经创建了“templates”文件夹并包含“index.html”


@router.get("/", response_class=HTMLResponse)
async def index(request: Request, casdoor_user=Depends(authz_required)):
    return templates.TemplateResponse("index.html", {"request": request, "username": casdoor_user.get("name")})
