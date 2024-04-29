from celery import Celery
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)


app = Celery('tasks',
             broker='amqp://admin:mypass@rabbit:5672',
             backend='rpc://')

# app = Celery('tasks',
#              broker='amqp://admin:mypass@localhost:5672',
#              backend='rpc://')
# es = ES(INDEX)

@app.task
def download_file(text, name):
    with open(f'downloads/{name}.txt', 'w') as file: 
        file.write(text)
    print(f'TASK PASSED FOR {text} {name}')
