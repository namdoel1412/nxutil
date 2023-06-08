import subprocess
from fastapi import FastAPI
from fastapi import FastAPI,  Query,APIRouter
from pydantic import BaseModel
import uvicorn
import os
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from ast import literal_eval
from fastapi import FastAPI, Body, APIRouter, Request, Response
from typing import Callable
from fastapi.routing import APIRoute
from pydantic import BaseModel
import json

class Item(BaseModel):
    logs: List[str]
    path: str

# class CustomRoute(APIRoute):
#     def __init__(self, *args, **kwargs) -> None:
#         super().__init__(*args, **kwargs)

#     def get_route_handler(self) -> Callable:
#         original_route_handler = super().get_route_handler()

#         async def custom_route_handler(request: Request) -> Response:
#             request_body = await request.body()

#             request_body = literal_eval(request_body.decode("utf-8"))

#             request_body = json.dumps(request_body).encode("utf-8")

#             request._body = request_body  # Note that we are overriding the incoming request's body

#             response = await original_route_handler(request)
#             return response

#         return custom_route_handler

app = FastAPI(title='NAXSI')
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/whitelist")
async def create_whitelist(item: Item=Body(...)):
    f = open("naxsi.log","w+")
    for i in item.logs:
        f.write(f"{i}\n")
    f.close()
    res1 = os.popen('python nx_util.py -l $(pwd)/naxsi.log -o -p 1').read()
    res = os.popen(f'python nx_util.py -l $(pwd)/naxsi.log -o -p 1 >> {item.path}').read()
    os.popen('systemctl restart nginx')
    print(res1)
    print(res)
    return res1

@app.post("/undo")
async def undo_whitelist(item: Item=Body(...)):
    f = open("naxsi.log","w+")
    for i in item.logs:
        f.write(f"{i}\n")
    f.close()
    res1 = os.popen('python nx_util.py -l $(pwd)/naxsi.log -o -p 1').read() # | grep BasicRule
    print('rule: ')
    print(res1)
    lstRules = res1.splitlines()
    for item in lstRules:
        print(item)
        subres = os.popen(f"sed -i 's!{item}!!g' {item.path}").read()
        print(subres)
    os.popen(f"sed -i '/^[[:space:]]*$/d' {item.path}")
    os.popen('systemctl restart nginx')
    return res1

if __name__ == '__main__':
    try:
        uvicorn.run("main:app", host="0.0.0.0", port=3009, reload=False, log_level="info",
                workers=1, limit_concurrency=1000, limit_max_requests=1000)
    except Exception as e:
       print("Oops!", e.__class__, " error when start serve a connection")
       print(str(e))
       print("Next entry.")