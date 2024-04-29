from pydantic import BaseModel
from fastapi import FastAPI
from celery import Celery
from es import ES


INDEX = 'files'
es = ES(INDEX)
app = FastAPI()
simple_worker = Celery('simple_worker',
                    broker='amqp://admin:mypass@rabbit:5672',
                    backend='rpc://')

# simple_worker = Celery('simple_worker',
#                     broker='amqp://admin:mypass@localhost:5672',
#                     backend='rpc://')



class Item(BaseModel):
    name: str
    text: str


@app.get("/")
async def root():
    return {"message": "Hello World!"}


@app.post("/download/")
async def download(item: Item):
    file_json = {
        'name': item.name,
        'text': item.text, 
    }
    download_file = simple_worker.send_task('tasks.download_file', kwargs=file_json)
    es.add_document(file_json)
    return download_file.id


@app.get("/search")
async def search(text: str, field: str):
    result = es.search_document(text, field)
    print(result)
    return result