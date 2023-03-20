<!--Copyright 2022 The Casdoor Authors. All Rights Reserved.-->

<!--Licensed under the Apache License, Version 2.0 (the "License");-->
<!--you may not use this file except in compliance with the License.-->
<!--You may obtain a copy of the License at-->

<!--     http://www.apache.org/licenses/LICENSE-2.0-->

<!--Unless required by applicable law or agreed to in writing, software-->
<!--distributed under the License is distributed on an "AS IS" BASIS,-->
<!--WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.-->
<!--See the License for the specific language governing permissions and-->
<!--limitations under the License.-->

<template>
  <h1>Callback</h1>
</template>

<script setup>
import { onMounted } from 'vue'
import * as config from '@/config'

function login() {
  window.sdk.signin(config.serverUrl).then((res) => {
    if (res.status === 'ok') {
      alert('Login success')
      if (inIframe()) {
        const message = {tag: "Casdoor", type: "SilentSignin", data: "success"};
        window.parent.postMessage(message, "*");
      }
      window.location.href = '/home'
    } else {
      alert('Login failed')
      window.location.href = '/'
    }
  })
}

function inIframe() {
  try {
    return window !== window.parent;
  } catch (e) {
    return true;
  }
}

onMounted(() => {
  login()
})
</script>


<style scoped></style>
