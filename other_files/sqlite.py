from flask import Flask, render_template, request
import sqlite3 as sql
from flask_bootstrap import Bootstrap




app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def home():
    print('home_db iniciando ....')
    return render_template('home_db.html')


@app.route('/enternew')
def new_student():
    return render_template('student_db.html')


@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        try:
            nm = request.form['nm']
            addr = request.form['add']
            city = request.form['city']
            pin = request.form['pin']

            with sql.connect("database.db") as con:
                cur = con.cursor()

                cur.execute("INSERT INTO students (name,addr,city,pin) "
                            "VALUES('{0}', '{1}', '{2}', '{3}')".format(nm,addr,city,pin))

                con.commit()
                msg = "Record successfully added"
        except Exception as e1:
            print("Expección :", e1)
            con.rollback()
            msg = "error in insert operation"

        finally:
            return render_template("result_db.html", msg=msg)
            con.close()


@app.route('/list')
def list():
    con = sql.connect("database.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from students")

    rows = cur.fetchall();
    return render_template("list_db.html", rows=rows)


@app.route('/crearbase')
def crearbase():
    # !/usr/bin/python

    print("Creando base de datos")

    conn = sql.connect('database.db')
    print("Opened database successfully")

    print(' >> Borrando la tabla students')

    vsql = 'Drop table students'

    conn.execute(vsql)

    conn.execute('''CREATE TABLE students
             (ID Integer PRIMARY KEY AUTOINCREMENT,
             name           TEXT    NOT NULL,
             addr           TEXT     NOT NULL,
             city        CHAR(50),
             pin         CHAR(50));''')

    print("Table created successfully")

    # _______________________________________________________________________________

    """
    conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
          VALUES (1, 'Paul', 32, 'California', 20000.00 )");

    conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
          VALUES (2, 'Allen', 25, 'Texas', 15000.00 )");

    conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
          VALUES (3, 'Teddy', 23, 'Norway', 20000.00 )");

    conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
          VALUES (4, 'Mark', 25, 'Rich-Mond ', 65000.00 )");

    conn.commit()
    print("Records created successfully")
    
    """
    conn.close()

    return "Listo"



if __name__ == '__main__':
    app.run(debug=True)