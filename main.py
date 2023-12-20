import hashlib

from flask import Flask, render_template, request, make_response
import json
import hashlib
import os
from config import *

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def vote():
    name_hash = hashlib.md5((첫번째사람 + 두번째사람).encode()).hexdigest()
    if request.cookies.get(name_hash) == '1':
        return render_template('message.html', icon='error', message='이미 투표하셨습니다.')

    if request.method == "GET":
        return render_template('index.html', first=첫번째사람, last=두번째사람)

    elif request.method == "POST":
        voted = request.form['vote']

        with open('result.json', 'r', encoding='utf-8') as f:
            read_data = json.load(f)
            read_data[voted] += 1

        with open('result.json', 'w', encoding='utf-8') as f:
            json.dump(read_data, f, ensure_ascii=False, indent='\t')

        resp = make_response(render_template('message.html', icon='success', message='투표 완료'))
        name_hash = hashlib.md5((첫번째사람+두번째사람).encode()).hexdigest()
        resp.set_cookie(name_hash, '1')

        return resp


@app.route('/result')
def result_check():
    with open('result.json', 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    first_count, second_count = json_data.get(첫번째사람), json_data.get(두번째사람)

    participants_count = first_count + second_count

    if first_count > second_count:
        winner = f'"{첫번째사람}" 우승'
    elif first_count == second_count:
        winner = '무승부'
    else:
        winner = f'"{두번째사람}" 우승'

    return render_template('result.html', result=json_data, count=participants_count, winner=winner)


if __name__ == '__main__':
    if not os.path.isfile('result.json'):
        with open('result.json', 'w', encoding='utf-8') as f:
            json.dump({첫번째사람: 0, 두번째사람: 0}, f, ensure_ascii=False, indent='\t')

    app.run(host='0.0.0.0', port=80)
