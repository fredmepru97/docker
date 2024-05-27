import time
import redis
from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)
cache = redis.Redis(host='srv-captain--redis', password='MyBIPMPassword', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    count = get_hit_count()
    return render_template('hello.html', name= "BIPM", count = count)

titanic_data = pd.read_csv("titanic.csv")

@app.route('/titanic')
def titanic():
    html_table = titanic_data.head().to_html()
    titanic = titanic_data.head()

    return render_template('titanic.html', titanic_preview=titanic, table=html_table)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
