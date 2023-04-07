from fastapi import FastAPI
from fastapi import FastAPI,  Query
import uvicorn
import os


app = FastAPI()


@app.post("/items")
async def create_item(items: str = Query([])):
    f = open("naxsi.log","w+")
    for i in items:
        f.write(f"{i}\n")
    os.system("python nx_util.py -l naxsi.log -o -p 1")
    return items

if __name__ == '__main__':
    try:
        uvicorn.run("main:app", host="0.0.0.0", port=3009, reload=False, log_level="info", debug=False,
                workers=1, limit_concurrency=1000, limit_max_requests=1000)
    except Exception as e:
       print("Oops!", e.__class__, " error when start serve a connection")
       print("Next entry.")