from flask import Flask,render_template,request,redirect,url_for
import sqlite3 as sql
app=Flask(__name__)

@app.route('/')
def home():
    return render_template('slide1.jinja2')
    #with sql.connect("sqldb.db") as con:
    #    cur = con.cursor()
    #    cur.execute("drop table booking")

@app.route('/rooms/')
def rooms():
    return render_template('rooms.jinja2')

@app.route('/rooms/addrooms/' , methods=['GET','POST'])
def addrooms():
    if request.method == 'POST':
        roomno = request.form['roomno']
        type = request.form['type']
        defaultval=10000
        price=defaultval*int(type)
        switcher={
            3:"Presidential Suite",
            2:"Extended Villa",
            1.5:"Executive Suite",
            1:"PentHouse Suite",
            0.5:"Wood Cabin "
        }
        suitename=switcher.get(int(type),0.5)
        if roomno.strip() is "" and type.strip() is "" :
            return render_template('addroom.jinja2', error="Enter all fields properly")
        else:
            try:
                with sql.connect("sqldb.db") as con:
                    cur = con.cursor()
                    cur.execute("create table if not exists rooms (roomno INT primary key, type TEXT , status BOOLEAN , guestno INT DEFAULT NULL,price INT)")
                    cur.execute("INSERT INTO rooms (roomno,type,status,guestno,price) VALUES (?,?,?,?,?)", (roomno,suitename,"Yes","NULL",price))
                    con.commit()
                    msg = "Record saved successfully"
            except:
                con.rollback()
                msg = "Error in inserting record"
            finally:
                con.close()
                return render_template("addroom.jinja2", msg=msg)
    roomulist=request.args.get('roomno',"")
    return render_template('addroom.jinja2',roomulist=roomulist)

@app.route('/rooms/lstroom/')
def lstrooms():
    with sql.connect("sqldb.db") as con:
        cur = con.cursor()
        cur.execute("select * from rooms")
        roomlist = cur.fetchall()
    return render_template('lstroom.jinja2',roomlist=roomlist)

@app.route('/rooms/deleterooms/' , methods=['GET','POST'])
def deleterooms():
    if request.method == 'POST':
        roomno=request.form['delbutton']
        print("this is the roomno",int(roomno))
        try:
            with sql.connect("sqldb.db") as con:
                cur = con.cursor()
                print("connection established\n\n\n\n")
                cur.execute("delete from rooms where roomno=%d"%int(roomno))
                print("sql function worked\n\n\n\n")
                con.commit()
                print("IT IS  commiting\n\n\n")
                con.close()
                print("successfully closed \n\n\n")
                return render_template("deleterooms.jinja2")
        except:
            return render_template("deleterooms.jinja2")
    else :
        return render_template("deleterooms.jinja2")

@app.route('/booking/' , methods = ['GET','POST'])
def booking():
    if request.method == 'POST':
        #bookingno = request.form['bookingno']
        checkin = request.form['checkin']
        checkout = request.form['checkout']
        guestname = request.form['guestname']
        roomno = request.form['roomno']
        phone = request.form['phone']
        address = request.form['address']
        with sql.connect("sqldb.db") as con:
            cur = con.cursor()
            cur.execute("select roomno from rooms")
            rlst= cur.fetchall()

        if  roomno.strip() is "" and phone.strip() is "":
            return render_template('addemp.jinja2', error="Enter all fields properly")
        elif int(roomno.strip()) not in rlst[0] :
            print("ROMM NOI ",roomno.strip(),rlst[0])
            return render_template('addemp.jinja2', error="Room not existing")
        else:
            try:
                with sql.connect("sqldb.db") as con:
                    cur = con.cursor()
                    print("beginning table creation")
                    #cur.execute("drop table booking")
                    cur.execute("create table if not exists booking (bookingno INTEGER primary key autoincrement, checkin DATE , checkout DATE)")
                    print("table1 created")
                    #cur.execute("drop table guest")
                    cur.execute("create table if not exists guest (guestno INTEGER primary key autoincrement,guestname TEXT, bookingno INT default NULL,phone INT,address TEXT,foreign key(bookingno) references booking(bookingno) on delete cascade)")
                    print("tables created")
                    cur.execute("select * from booking")
                    curobject= cur.fetchall()
                    print("select statement")
                    print(str(curobject))
                    print(type(curobject))
                    bookingno = len(curobject)
                    print(bookingno)
                    cur.execute("INSERT INTO booking (checkin,checkout) VALUES (?,?)", (checkin,checkout))
                    print("1st insert finished")
                    cur.execute("INSERT INTO guest (guestname,phone,address) VALUES (?,?,?)", (guestname,phone,address))
                    print("@nd insert finished")
                    cur.execute("UPDATE guest set bookingno = {0} where guestno = {0}".format((bookingno+1)))
                    print("1st update finished")
                    cur.execute("UPDATE rooms set guestno = {0} where roomno = {1}".format(bookingno+1,roomno))
                    print("2nd update finished")
                    con.commit()
                    msg = "Record saved successfully"
            except:
                con.rollback()
                msg = "Error in inserting record"
            finally:
                con.close()
                return render_template("booking.jinja2", msg=msg)
    bookingulist=(request.args.get('checkin',""),request.args.get('checkout',""),request.args.get('guestname',""),request.args.get('roomno',""),request.args.get('phone',""),request.args.get('address',""))
    return render_template('booking.jinja2',bookingulist=bookingulist)

@app.route('/booking/blist/')
def blist():
    with sql.connect("sqldb.db") as con:
        cur = con.cursor()
        cur.execute("select * from booking")
        blist = cur.fetchall()
    return render_template('blist.jinja2',blist=blist)

@app.route('/guests/')
def guests():
    with sql.connect("sqldb.db") as con:
        cur = con.cursor()
        cur.execute("select * from guest")
        guestlist = cur.fetchall()
    return render_template('guests.jinja2',guestlist=guestlist)

@app.route('/guests/deleteguests/' , methods = ['GET','POST'])
def delguests():
    if request.method == 'POST':
        guestno=request.form['delbutton']
        print("this is the guestno",int(guestno))
        try:
            with sql.connect("sqldb.db") as con:
                cur = con.cursor()
                print("connection established\n\n\n\n")
                cur.execute("delete from guest where guestno=%d"%int(guestno))
                print("sql function worked\n\n\n\n")
                cur.execute("delete from booking where bookingno=%d"%int(guestno))
                con.commit()
                print("it is commiting\n\n\n")
                con.close()
                print("successfully closed \n\n\n")
                return render_template("deleteguests.jinja2")
        except:
            return render_template("deleteguests.jinja2")
    else :
        return render_template("deleteguests.jinja2")

@app.route('/employees/')
def employees():
    return render_template('lstemp.jinja2')

@app.route('/employees/addemp/' ,methods =['GET','POST'])
def addemp():
    if request.method == 'POST':
        emp_id = request.form['empid']
        emp_name = request.form['empname']
        emp_age =   request.form['empage']
        emp_des = request.form['empdes']
        emp_phone = request.form['empphone']
        emp_address = request.form['empaddress']
        if emp_id.strip() is "" and emp_name.strip() is "" and emp_phone.strip() is "":
            return render_template('addemp.jinja2', error="Enter all fields properly")
        else:
            try:
                with sql.connect("sqldb.db") as con:
                    cur = con.cursor()
                    cur.execute("create table if not exists employees (emp_id INT primary key, emp_name TEXT , emp_age INT , emp_des TEXT , emp_phone INT ,emp_address TEXT)")
                    cur.execute("INSERT INTO employees (emp_id,emp_name,emp_age,emp_des,emp_phone,emp_address) VALUES (?,?,?,?,?,?)", (emp_id,emp_name, emp_age, emp_des, emp_phone,emp_address))
                    con.commit()
                    msg = "Record saved successfully"
            except:
                con.rollback()
                msg = "Error in inserting record"
            finally:
                con.close()
                return render_template("addemp.jinja2", msg=msg)
    empulist=[request.args.get('empid',""),request.args.get('empname',""),request.args.get('empage',""),request.args.get('empdes',""),request.args.get('empphone',""),request.args.get('empaddress',"")]
    return render_template('addemp.jinja2',empulist=empulist)

@app.route('/employees/lstemp/')
def lstemp():
    with sql.connect("sqldb.db") as con:
        cur = con.cursor()
        cur.execute("select * from employees")
        emplist = cur.fetchall()
    return render_template('mgemp.jinja2',emplist=emplist)

@app.route('/employees/deleteemp/' , methods=['GET','POST'])
def deleteemp():
    if request.method == 'POST':
        empid=request.form['delbutton']
        print("this is the empid",int(empid))
        try:
            with sql.connect("sqldb.db") as con:
                cur = con.cursor()
                print("connection established\n\n\n\n")
                cur.execute("delete from employees where emp_id=%d"%int(empid))
                print("sql function worked\n\n\n\n")
                con.commit()
                print("IT IS  commiting\n\n\n")
                con.close()
                print("successfully closed \n\n\n")
                return render_template("deleteemp.jinja2")
        except:
            return render_template("deleteemp.jinja2")
    else :
        return render_template("deleteemp.jinja2")

@app.route('/<string:post_id>')  #eg - /post/2 returns 2 to post_id
def error1(post_id):
    return render_template('404.jinja2',message=f'{post_id} was not found')

@app.route('/<string:post_id>/')  #eg - /post/2 returns 2 to post_id
def error2(post_id):
    return render_template('404.jinja2',message=f'{post_id} was not found')


app.run(debug=True)
