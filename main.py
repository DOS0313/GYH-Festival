from flask import Flask, render_template
import csv
from collections import defaultdict
import os

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/result')
def result_check():
    result = defaultdict(int)

    with open('제목 없는 설문지.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            if line[0] == '타임스탬프':
                continue

            result[line[1]] += 1

    participants_count = int()

    for key, value in result.items():
        participants_count += value

    return render_template('result.html', result=dict(result), count=participants_count)


app.run(host='0.0.0.0', port=80)
