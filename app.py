from flask import Flask, render_template,request
import datetime,json

#Json
#起動時jsonファイから既存のデータの読み込み
try:
    with open("date.json","r") as f:
        responses=json.load(f)
except:
        responses=[]



app=Flask(__name__)

#てーぶる作成時にしようする日付リスト
date_list=[
    "4/19","4/20","4/21","4/22","4/23","4/24","4/25","4/26","4/27","4/28","4/29","4/30",
    "5/1","5/2","5/3","5/4","5/5","5/6","5/7","5/8","5/9","5/10","5/11","5/12","5/13","5/14","5/15"
    ]

def get_date_with_weekday(date_str):
    month,day=map(int,date_str.split("/"))
    dt=datetime.date(2026,month,day)
    weekday=["月","火","水","木","金","土","日"][dt.weekday()]
    return f"{date_str}({weekday})",weekday

date_info=[]
for d in date_list:
    label,weekday=get_date_with_weekday(d)
    date_info.append({
        "date":d,
        "label":label,
        "weekday":weekday
    })


@app.route("/", methods=["GET", "POST"])

def home():
    #名前と希望日をついかする空リスト
    global responses

    best_dates=[]
    max_count=0

    if request.method=="POST":
        name=request.form.get("username")
        selected_dates=request.form.getlist("dates")

        responses=[r for r in responses if r["name"] != name]

        responses.append({
            "name":name,
            "dates":selected_dates
        })

            #POST後に保存
        with open("date.json","w") as f:
            json.dump(responses,f)

        print(responses)

    #人気の日付の集計
    date_count={d:0 for d in date_list}

    for r in responses:
        for d in r["dates"]:
            if d in date_count:
                date_count[d]+=1
            
    #最大値の取得
    max_count=max(date_count.values()) if date_count else 0
    #一番人気の日付のリスト
    best_dates=[d for d,c in date_count.items() if c == max_count and c > 0]
    

    return render_template(
        "index.html", 
        responses=responses,
        date_list=date_list,
        date_info=date_info,
        best_dates=best_dates,
        max_count=max_count,
        )

app.run(debug=True)
