from fastapi import FastAPI
from fastapi import FastAPI,  Query
from pydantic import BaseModel
import uvicorn
import os
from typing import List
from fastapi.middleware.cors import CORSMiddleware

class Item(BaseModel):
    logs: List[str]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/items")
async def create_item(item: Item):
    f = open("naxsi.log","w+")
    for i in item.logs:
        f.write(f"{i}\n")
    res = os.system("python nx_util.py -l naxsi.log -o -p 1")
    print(res)
    return res

if __name__ == '__main__':
    try:
        uvicorn.run("main:app", host="0.0.0.0", port=3009, reload=False, log_level="info",
                workers=1, limit_concurrency=1000, limit_max_requests=1000)
    except Exception as e:
       print("Oops!", e.__class__, " error when start serve a connection")
       print(str(e))
       print("Next entry.")