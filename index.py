# Copyright 2022 Gwendal Delisle-Arnold DELG67030105
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import Flask
from flask import render_template
from flask import request
from flask import g
from .database import Database

app = Flask(__name__, static_url_path="", static_folder="static")


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.disconnect()


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        db = Database()
        db.get_connection()
        animalList = db.get_animaux()
        tableList = []
        for i in range(0, len(animalList), 3):
            tableList.append(animalList[i:i+3])
        return render_template('index.html', tableList=tableList)
    return render_template('index.html')
