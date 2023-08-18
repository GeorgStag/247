from flask import Flask, render_template, request, redirect
import json
import datetime
import os



app = Flask(__name__)

data_file = 'data.json'
memory_file = 'memory.json'


def load_data():
    if os.path.exists(data_file):
        with open(data_file, 'r') as f:
            return json.load(f)
    return []

def load_memory():
    if os.path.exists(memory_file):
        with open(memory_file, 'r') as f:
            return json.load(f)
    return []

def save_data(data):
    with open(data_file, 'w') as f:
        json.dump(data, f, indent=4)

def update_memory(data):
    with open(memory_file, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form.get('text')
        color = request.form.get('color')
        timestamp = datetime.datetime.now().strftime('%d/%m %H:%M')
        new_item = {
            'text': text,
            'color': color,
            'timestamp': timestamp
        }
        data = load_data()
        data.append(new_item)
        save_data(data)
        new_item = {
            'text': text,
            'color': color,
            'timestamp': timestamp,
            'status': 'input'
        }
        memory = load_memory()
        memory.append(new_item)
        update_memory(memory)
    data = load_data()
    return render_template('index.html', data=data)

@app.route('/history', methods=['GET', 'POST'])
def history():
    history = load_memory()
    data = []
    check = False
    check_print = "not_print"
    if request.method == 'POST':
        color = request.form.get('color')
        check_print = request.form.get('full_history')
        for element in history:
            if element['color'] == color:
                data.append(element)
        check = True
    action = request.form.get('clear')
    if action == "confirm":
        data = []
        update_memory([])
    if (not check) or (check_print=="print"):
        check_print = "not_print"
        data = history
    return render_template('history.html', history=data)

@app.route('/remove/<int:index>', methods=['GET'])
def remove(index):
    data = load_data()
    memory = load_memory()
    new_item = data[index]
    new_item['timestamp'] = datetime.datetime.now().strftime('%d/%m %H:%M')
    new_item['status'] = 'delete'
    if 0 <= index < len(data):
        data.pop(index)
        save_data(data)
        memory.append(new_item)
        update_memory(memory)
    return redirect('/')

@app.route('/complete/<int:index>', methods=['GET'])
def complete(index):
    data = load_data()
    memory = load_memory()
    new_item = data[index]
    new_item['timestamp'] = datetime.datetime.now().strftime('%d/%m %H:%M')
    new_item['status'] = 'complete'
    if 0 <= index < len(data):
        data.pop(index)
        save_data(data)
        memory.append(new_item)
        update_memory(memory)
    return redirect('/')

@app.route('/error/<int:index>', methods=['GET'])
def error(index):
    data = load_data()
    memory = load_memory()
    new_item = data[index]
    new_item['timestamp'] = datetime.datetime.now().strftime('%d/%m %H:%M')
    new_item['status'] = 'error'
    if 0 <= index < len(data):
        data.pop(index)
        save_data(data)
        memory.append(new_item)
        update_memory(memory)
    return redirect('/')

@app.route('/top/<int:index>', methods=['GET'])
def top(index):
    data = load_data()
    memory = load_memory()
    new_item = data[index]
    if 0 <= index < len(data):
        temp = data[index]
        data.pop(index)
        data.insert(0,temp)
        save_data(data)
        new_item['timestamp'] = datetime.datetime.now().strftime('%d/%m %H:%M')
        new_item['status'] = 'top'
        memory.append(new_item)
        update_memory(memory)
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=247, debug=True)