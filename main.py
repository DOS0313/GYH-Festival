from flask import Flask, render_template, request, make_response
import json
import hashlib
import os
from config import *
from collections import OrderedDict

app = Flask(__name__)


def allname() -> str:
    name_all = str()
    for person in 사람들:
        name_all.join(person)

    return name_all


@app.route('/', methods=["GET", "POST"])
def vote():
    name_hash = hashlib.md5(allname().encode()).hexdigest()

    if request.cookies.get(name_hash) == '1':
        return render_template('message.html', icon='error', message='이미 투표하셨습니다.')

    if request.method == "GET":
        return render_template('index.html', people=사람들)

    elif request.method == "POST":
        voted = request.form['vote']

        with open('result.json', 'r', encoding='utf-8') as f:
            read_data = json.load(f)
            read_data[voted] += 1

        with open('result.json', 'w', encoding='utf-8') as f:
            json.dump(read_data, f, ensure_ascii=False, indent='\t')

        resp = make_response(render_template('message.html', icon='success', message='투표 완료'))

        name_hash = hashlib.md5(allname().encode()).hexdigest()
        resp.set_cookie(name_hash, '1')

        return resp


@app.route('/result')
def result_check():
    with open('result.json', 'r', encoding='utf-8') as f:
        json_data = json.load(f)
        dict_data = dict(json_data)

    participants_count = int()

    for key, items in dict_data.items():
        participants_count += items

    # 맥스값 찾아서 우승 띄우게
    max_member = max(사람들)  # 사람 이름으로 나옴
    winner = f"{max_member} 우승"

    return render_template('result.html', result=json_data, count=participants_count, winner=winner,
                           len=len, people=사람들)


if __name__ == '__main__':
    if not os.path.isfile('result.json'):
        with open('result.json', 'w', encoding='utf-8') as f:
            dump_data = OrderedDict()
            for person in 사람들:
                dump_data[person] = 0

            json.dump(dump_data, f, ensure_ascii=False, indent='\t')

    app.run(host='0.0.0.0', port=80)
