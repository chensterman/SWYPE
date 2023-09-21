from flask import Flask, jsonify, request
from celery import Celery
from citizens_swype import redeem_rewards
import os

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = os.environ.get('REDIS_URL')
app.config['CELERY_RESULT_BACKEND'] = os.environ.get('REDIS_URL')
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@celery.task(bind=True)
def long_running_task(self, username, password):
    try:
        redeem_rewards(username, password)
    except Exception as e:
        self.update_state(status='FAILED', meta={'error': str(e)})
        raise e
    return f'Task completed'

@app.route('/start_long_task', methods=['POST'])
def start_long_task():
    # Access JSON POST data
    data = request.get_json()
    # Access specific POST parameters by key
    username = data.get('username')
    password = data.get('password')
    task = long_running_task.apply_async(args=[username, password])
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