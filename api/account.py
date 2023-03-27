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
from starlette.requests import Request
from starlette.responses import JSONResponse
from .utils import authz_required, get_user_from_session

router = APIRouter()


@router.get("/api/get-account", response_class=JSONResponse)
async def get_account(request: Request, user=Depends(get_user_from_session)):
    sdk = request.app.state.CASDOOR_SDK
    print(user)
    return {"status": "ok", "data": sdk.get_user(user["name"])}
