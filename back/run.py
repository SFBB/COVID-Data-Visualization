from flask import Flask, render_template, jsonify
from random import *
from flask_cors import CORS
import requests
import psycopg2
import json
from flask import request
import datetime, time




def connect_db(name):
    try:
        con = psycopg2.connect(database=name, user="postgres", password="4869221B", host="127.0.0.1", port="5432")
        con.autocommit = True

        # sqliteConnection = sqlite3.connect(name)
        print("Successfully Connected to PostgressDB")
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
        # print(cur.description)
        # desc = cur.description
        # column_names = [col[0] for col in desc]
        # data = [dict(itertools.izip(column_names, row))  
        #             for row in cur.fetchall()]
        # print(data)
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

def get_name(short):
    for cou in ZH_2_EN:
        if cou["short"] == short:
            return cou["name"]
    return None

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
    print(request.args.get("from"))
    print(request.args.get("to"))
    if request.args.get("from") == None:
        sql = "select  国家地区, sum(新增确诊) as 新增确诊, sum(新增死亡) as 新增死亡, sum(重症病例) as 重症病例, max(累计确诊) as 累计确诊, max(累计治愈) as 累计治愈,  sum(仍在治疗) as 仍在治疗, max(累计死亡) as 累计死亡 from  yiqing group by 国家地区 order by 国家地区"
    else:
        sql = "select  国家地区, sum(新增确诊) as 新增确诊, sum(新增死亡) as 新增死亡, sum(重症病例) as 重症病例, max(累计确诊) as 累计确诊, max(累计治愈) as 累计治愈,  sum(仍在治疗) as 仍在治疗, max(累计死亡) as 累计死亡 from  yiqing where 日期>='"+request.args.get("from")+"' and 日期<='"+request.args.get("to")+"' group by 国家地区 order by 国家地区"
        print(sql)
    # print("asdasdasd")
    # sql = "select  国家地区, max(累计确诊) as 累计确诊, sum(新增确诊) as 新增确诊, max(累计死亡) as 累计死亡, sum(新增死亡) as 新增死亡, max(累计治愈) as 累计治愈, sum(仍在治疗) as 仍在治疗, sum(重症病例) as 重症病例 from  yiqing group by 国家地区;"
    # if 
    countries = SQL_advanced(db, sql)
    sql = '''select t.国家地区, t.日期, t.仍在治疗
            from yiqing t
            inner join (
                select 国家地区, max(日期) as MaxDate
                from yiqing
                group by 国家地区
            ) tm on t.国家地区 = tm.国家地区 and t.日期 = tm.MaxDate order by t.国家地区 '''
    rengzai = SQL_advanced(db, sql)
    new_cous = []
    for cou in countries:
        # print(rengzai[countries.index(cou)][2])
        if rengzai[countries.index(cou)][2] == None:
            reng = 0
        else:
            reng = rengzai[countries.index(cou)][2]
        # new_cous.append({"id": get_short(cou), "name": cou[0], "累计确诊": cou[1], 
        #                  "新增确诊": cou[2], "累计死亡": cou[3], "新增死亡": cou[4], "累计治愈": cou[5], "仍在治疗": cou[6], "重症病例": cou[7]})
        new_cous.append({"id": get_short(cou), "name": cou[0], "新增确诊": cou[1],
                        "新增死亡": cou[2], "重症病例": cou[3], "累计确诊": cou[4], "累计治愈": cou[5], "仍在治疗": reng, "累计死亡": cou[7]})
    countries = new_cous
    response = {
        'countries': countries
        # "daadad": "asdsad"
    }
    # print(response)
    # print(response)
    return jsonify(response)

# 新增确诊 新增死亡 重症病例 累计确诊 累计治愈 仍在治疗 累计死亡 

@app.route('/api/countriesL')
def countriesL():
    fromD = request.args.get("from")
    toD = request.args.get("to")
    couL = request.args.get("countries").split(",")
    type = request.args.get("type")
    # for cou in request.args:
    #     counts.append(cou[0])
    print(type)
    result = {}
    for cou in couL:
        if get_name(cou) == None:
            continue
        sql = "select floor(avg(新增确诊)) as 新增确诊, floor(avg(新增死亡)) as 新增死亡, floor(avg(重症病例)) as 重症病例, floor(avg(累计确诊)) as 累计确诊, floor(avg(累计治愈)) as 累计治愈,   floor(avg(仍在治疗)) as 仍在治疗, floor(avg(累计死亡))as 累计死亡, 日期 from yiqing where 日期>='"+request.args.get("from")+"' and 日期<='"+request.args.get("to")+"' and "+type+"!=0 and 国家地区='"+get_name(cou)+"' group by 日期 order  by 日期;"
        print(sql)
        dates = SQL_advanced(db, sql)
        new_dates = []
        for date in dates:
            # print(int(time.mktime(date[7].timetuple())) * 1000)
            new_dates.append({"date": int(time.mktime(date[7].timetuple()))*1000, "新增确诊": date[0], 
                            "新增死亡": date[1], "重症病例": date[2], "累计确诊": date[3], "累计治愈": date[4], "仍在治疗": date[5], "累计死亡": date[6]})
        dates = new_dates
        result[cou] = dates


    response = {
        "countries": result
    }

    return jsonify(response)



@app.route('/api/overview<string:type>')
def overview(type):
    # print(type)
    sql = "select floor(avg(新增确诊)) as 新增确诊, floor(avg(新增死亡)) as 新增死亡, floor(avg(重症病例)) as 重症病例, floor(avg(累计确诊)) as 累计确诊, floor(avg(累计治愈)) as 累计治愈,   floor(avg(仍在治疗)) as 仍在治疗, floor(avg(累计死亡))as 累计死亡, 日期 from yiqing where 国家地区!='全球' and "+type+"!=0 group by 日期 order  by 日期;"
    # if 
    dates = SQL_advanced(db, sql)
    new_dates = []
    for date in dates:
        # print(int(time.mktime(date[7].timetuple())) * 1000)
        new_dates.append({"date": int(time.mktime(date[7].timetuple()))*1000, "新增确诊": date[0], 
                         "新增死亡": date[1], "重症病例": date[2], "累计确诊": date[3], "累计治愈": date[4], "仍在治疗": date[5], "累计死亡": date[6]})
    dates = new_dates
    response = {
        'dates': dates
    }
    # print(countries[0])
    return jsonify(response)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if app.debug:
        return requests.get('http://localhost:8080/{}'.format(path)).text
    return render_template("index.html")
