from flask import Flask, jsonify, request
from celery import Celery
from classes.swype_citizens import SwypeCitizens
from classes.swype import Swype
import os

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = os.environ.get("REDIS_URL")
app.config['CELERY_RESULT_BACKEND'] = os.environ.get("REDIS_URL")
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@celery.task(bind=True)
def long_running_task(self, bank, username, password, task_type):
    if (bank == 'citizens'):
        swype = SwypeCitizens("https://www.accessmycardonline.com/", 25.0, username, password)
    else:
        swype = Swype()

    if (task_type == 'check_balance'):
        balance = swype.get_rewards_balance()
        swype.close_browser()
        return balance
    else:
        swype.redeem_rewards()
        swype.close_browser()
        return 'Redeem Success.'
    

@app.route('/start_task', methods=['POST'])
def start_task():
    # Access JSON POST data
    data = request.get_json()
    # Access specific POST parameters by key
    bank = data.get('bank')
    username = data.get('username')
    password = data.get('password')
    task_type = data.get('task_type')
    task = long_running_task.apply_async(args=[bank, username, password, task_type])
    return jsonify({'task_id': task.id, 'status': 'Task started'}), 202

@app.route('/check_task_status/<task_id>', methods=['GET'])
def check_task_status(task_id):
    task = long_running_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {'status': 'Task is still pending'}
    elif task.state == 'SUCCESS':
        response = {'status': 'Task completed', 'result': task.result}
    else:
        response = {'status': 'Task failed', 'error': str(task.info)}
    return jsonify(response)