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

from fastapi import Depends, HTTPException
from starlette.requests import Request

async def get_user_from_session(request: Request):
    user = request.session.get("casdoorUser")
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user

def authz_required(request: Request):
    if "casdoorUser" in request.session.keys():
        return request.session["casdoorUser"]
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
