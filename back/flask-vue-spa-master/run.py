from flask import Flask, render_template, jsonify
from random import *
from flask_cors import CORS
import requests
import psycopg2
import json
from flask import request




def connect_db(name):
    try:
        con = psycopg2.connect(database=name, user="postgres", password="4869221B", host="127.0.0.1", port="5432")
        con.autocommit = True

        # sqliteConnection = sqlite3.connect(name)
        print("Successfully Connected to SQLite")
        # print("Successfully Connected to SQLite")

        return con
    except Exception as error:
        print("Failed to insert data into sqlite table "+str(error))
        # print("Failed to insert data into sqlite table", error)




def SQL_advanced(conn, sql):
    try:
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        result = cur.fetchall()
        cur.close()
        # result = json.dumps( [dict(ix) for ix in result] ) #CREATE JSON
        # result = json.dumps(dict(result))
        return result
    except Exception as error:
        print("Failed to advanced sql data into sqlite table "+str(error)+"\t\t\t"+sql)
        # print("Failed to advanced sql data into sqlite table", error)
        # print(sql)
        # print()
        # print()
        # print()


with open("a.json") as file:
    ZH_2_EN = json.load(file)

def get_short(data):
    for cou in ZH_2_EN:
        if cou["name"] == data[0]:
            return cou["short"]
    return "None"


app = Flask(__name__,
            static_folder = "./dist/static",
            template_folder = "./dist")
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

db = connect_db("yiqing")

@app.route('/api/random')
def random_number():
    response = {
        'randomNumber': randint(1, 100)
    }
    return jsonify(response)

@app.route('/api/countries<string:type>')
def countries(type):
    print(type)
    sql = "select  国家地区, max(累计确诊) as 累计确诊, sum(新增确诊) as 新增确诊, max(累计死亡) as 累计死亡, sum(新增死亡) as 新增死亡, max(累计治愈) as 累计治愈, sum(仍在治疗) as 仍在治疗, sum(重症病例) as 重症病例 from  yiqing group by 国家地区;"
    # if 
    countries = SQL_advanced(db, sql)
    new_cous = []
    for cou in countries:
        new_cous.append({"id": get_short(cou), "name": cou[0], "累计确诊": cou[1], 
                         "新增确诊": cou[2], "累计死亡": cou[3], "新增死亡": cou[4], "累计治愈": cou[5], "仍在治疗": cou[6], "重症病例": cou[7]})
    countries = new_cous
    response = {
        'countries': countries
    }
    return jsonify(response)



@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if app.debug:
        return requests.get('http://localhost:8080/{}'.format(path)).text
    return render_template("index.html")
