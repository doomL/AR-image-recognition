from flask import Flask, render_template, Response
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'admin'
#app.config['MYSQL_PASSWORD'] = 'a3d2wJuPfYks6vdQ'
app.config['MYSQL_DB'] = 'arsistant'

mysql = MySQL(app)
print("qua leggo")

@app.route('/', methods=['GET', 'POST'])
def main():
    print("qua entro")
    cur = mysql.connection.cursor()
    print(cur.execute("INSERT INTO user(Username,Password) VALUES('Giovanni','Grasso');"))
    mysql.connection.commit()
    cur.close()
    


if __name__ == '__main__':
    # main()
    app.run()
