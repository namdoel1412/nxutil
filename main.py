from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import uvicorn
import os

class Item(BaseModel):
    logs: List[str]


app = FastAPI()


@app.post("/items")
async def create_item(item: Item):
    f = open("guru99.log","w+")
    for i in item.logs:
        f.write(f"{i}\n")
    os.system("python nx_util.py -l naxsi.log -o -p 1")
    return item

if __name__ == '__main__':
    try:
        uvicorn.run("main:app", host="0.0.0.0", port=3009, reload=False, log_level="info", debug=False,
                workers=1, limit_concurrency=1000, limit_max_requests=1000)
    except Exception as e:
       print("Oops!", e.__class__, " error when start serve a connection")
       print("Next entry.")