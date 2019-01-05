#*-* coding:utf-8 *-*
from flask import Flask,render_template,request,redirect
import sqlite3
import sys
import os
import os
reload(sys)
sys.setdefaultencoding('utf-8')
app=Flask(__name__)
@app.route("/login",methods=["POST"])
def login():
    username=request.form["username"]
    passwd=request.form["password"]
    conn=sqlite3.connect("darukhune.dbs")
    cur=conn.cursor()    
    cur.execute("select * from users where username='%s' and passwd='%s'"%(username,passwd))
    user_id=cur.fetchone()
    if user_id!=None:
        cur.execute("select * from drugs")
        drug=cur.fetchall()
        conn.close()                
        return render_template("index.html",flag="login",drugs=drug,id=user_id)
         
    else:
        return "user or pass wrong"    
@app.route("/signup",methods=["POST"])
def signup():
    username=request.form["username"]
    passwd=request.form["password"]
    email=request.form["email"]
    conn=sqlite3.connect("darukhune.dbs")
    cur=conn.cursor()
    cur.execute("select * from users where username='%s'"%username)
    
    if cur.fetchall()==[]:
        cur.execute("insert into users values('%s','%s','%s',NULL)"%(username,passwd,email))
        conn.commit()
        conn.close()        
        return render_template("index.html" ,flag="signup")
         
    else:
        return render_template("index.html",flag="this username is exists")
@app.route("/kharid",methods=["POST"])
def kharid():
    data=request.form["id"]
    conn=sqlite3.connect("darukhune.dbs")
    cur=conn.cursor()  
    
    cur.execute("select * from kharid where user_id='%s'"%data)
    wishlist=cur.fetchall()
    kk=""
    M=0
    for a,b,c,d,e in wishlist:
        cur.execute("select * from drugs where id='%s'"%c)
        go=cur.fetchone()
        M+=go[4]
        kk+="<div id='drug_show'><br><p id='code'>%s</p><br><p id='name'>%s </p><br><p id='tozih'>%s</p><button onclick=\"delete_kharid('%s')\">-</button></div>"%(go[0],go[1],go[3],a)
    conn.close()        
    return kk+"<div>مبلغ قایل پرداخت:%s</div>"%M
@app.route("/valid_drugs",methods=["POST"])
def valid_drugs():
    conn=sqlite3.connect("darukhune.dbs")
    cur=conn.cursor()
    cur.execute("select * from drugs")
    drugs=cur.fetchall()
    kk=""
    req=request.form["post"]
    if req=="home":
        for i in drugs:
            kk+="<div id='drug_show'><p >کد محصول: %s</p> <p > %s :نام محصول </p><p >تعداد: %s</p><p >قیمت: %s تومان</p><button id='header_button' value='ورود' onclick='change_header(value)' >برای خریدن لطفا وارد شوید</button></div>"%(i[0],i[1],i[2],i[4])
        conn.close()
        return kk
    if req=="login":
        for i in drugs:
            kk+="<div id='drug_show'><p >کد محصول: %s</p> <p > %s :نام محصول </p><p >تعداد: %s</p><p >قیمت: %s تومان</p><button id='header_button' onclick='add_kharid(\"%s\")' >اضافه نمودن به سبد خرید</button></div>"%(i[0],i[1],i[2],i[4],i[0])
        conn.close()
        return kk 
@app.route("/add_kharid",methods=["POST"])
def add_kharid():
    drug_id=request.form["drug_id"]
    user_id=request.form["user_id"]
    conn=sqlite3.connect("darukhune.dbs")
    cur=conn.cursor()
    cur.execute("insert into kharid values(NULL,'%s','%s',NULL,NULL)"%(user_id,drug_id))
    conn.commit()
    conn.close()    
    return "با موفقیت به سبد شما اضافه شد"
@app.route("/delete_kharid",methods=["POST"])
def delete_kharid():
    user_id=request.form["user_id"]
    kharid_id=request.form["id"]
    print kharid_id
    conn=sqlite3.connect("darukhune.dbs")
    cur=conn.cursor()
    cur.execute("delete from kharid where id='%s'"%kharid_id)
    conn.commit()
    conn.close()    
    return "با موفقیت حذف کردید"
@app.route("/")
def dd():
    conn=sqlite3.connect("darukhune.dbs")
    cur=conn.cursor()    
    cur.execute("select * from drugs")
    drug=cur.fetchall()
    conn.close()    
    return render_template("index.html",flag="",drugs=drug)
@app.route("/adminpanel")
def admin_panel():
    return render_template("index.html",flag="admin_panel")
@app.route("/adminpanel/admin",methods=["post"])
def admin_admin_panel():
    admin_user=request.form["admin_user"]
    admin_password=request.form["admin_password"]    
    conn=sqlite3.connect("darukhune.dbs")
    cur=conn.cursor()
    cur.execute("select * from admin where admin='%s' and pass='%s'"%(admin_user,admin_password))
    if cur.fetchone()!=None:
        cur.execute("select * from kharid")
        shops=cur.fetchall()
        content=""
        for i in shops:
            
            cur.execute("select * from drugs where id='%s'"%i[2])
            drug_info=cur.fetchone()
            content+=''
        return render_template('admin_page.html',flag='admin_login')
@app.route('/add_drug',methods=["POST"])
def add_drug():
   drug_name=request.form["durg_name"]
   drug_details=request.form["drug_details"]
   drug_money=request.form["money"]
   take_place=request.form["take_place"]
   conn=sqlite3.connect("darukhune.dbs")
   cur=conn.cursor()
   exece="insert into drugs values(null,'%s',%s,'%s',%s)"%(drug_name,take_place,drug_details,drug_money)
   print exece
   cur.execute(exece)
   conn.commit()
   return "added"
@app.route("/adminpanel/admin/get_buyed" ,methods=["post"])
def get_buyed():
    admin=request.form["admin"]
    print admin
    if admin=="admin":
        conn=sqlite3.connect("darukhune.dbs")
        cur=conn.cursor()
        cur.execute("select * from pass_kharid")
        all_buyers=cur.fetchall()
        post_response=""
        for i in all_buyers:
            cur.execute("select name from drugs where id='%s'"%i[2])
            drug_name=cur.fetchone()
            post_response+='<div id="drug_show"> <p >کد محصول: %s</p><p > %s :نام محصول </p><p>نشانی و نام خریدار:%s</p><button id="header_button" >ارسال دارو</button></div>'%(i[2],drug_name[0],i[3])
        return post_response
@app.route("/pardakht",methods=["POST"])
def pardkhat():
    name=request.form["name"]
    adres=request.form["adres"]
    user_id=request.form["user_id"]
    conn=sqlite3.connect("darukhune.dbs")
    cur=conn.cursor()
    cur.execute("select * from kharid where user_id=%s"%(user_id))
    all_passed=cur.fetchall()
    for i in all_passed:
        cur.execute("insert into pass_kharid values(%s,%s,%s,'%s','%s')"%(i[0],i[1],i[2],adres,name))
        cur.execute("delete from kharid where user_id=%s"%user_id)
    conn.commit()
    return "yessssss"
app.run(host="0.0.0.0")
