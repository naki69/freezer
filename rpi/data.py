import datetime
# import json
import sqlite3

from flask import Flask, request


class Data(object):
    def __init__(self):
        self.data = list()
        self.N = 0
        self.T = ""

    def push(self, jsonData):
        for i in jsonData:
            self.data.append(
                [
                    datetime.datetime.fromtimestamp(i["time"] + 946702800),
                    i["temp1"],
                    i["temp2"],
                ]
            )

    def pop(self):
        return self.data

    def clear(self):
        self.data.clear()


temps = Data()


def inject():
    # Connect and read the db

    con = sqlite3.connect("/home/stef/freezer/freezer.db")
    cur = con.cursor()

    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS temp 
    (
        id integer PRIMARY KEY AUTOINCREMENT,
        date text,
        temp1 integer,
        temp2 integer
        );
        """
    )

    sqlite_insert_query = """INSERT INTO temp
                            (date, temp1, temp2 )
                            VALUES (?, ?, ?)"""

    cur.executemany(sqlite_insert_query, temps.pop())
    print("Total", cur.rowcount, "Records inserted successfully into table")
    temps.clear()
    con.commit()
    res = cur.execute("""Select count(date), max(date) from temp""")
    n = res.fetchone()
    temps.N = n[0]
    temps.T = n[1]
    con.close()
    return n


# create the Flask app
app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def user():
    if request.method == "GET":
        return "So far we have " + str(temps.N) + " last update @ " + temps.T

    if request.method == "POST":
        data = request.get_json()
        data = data[0]
        temps.push(data)
        inject()
        return "Success"

    else:
        # POST Error 405 Method Not Allowed
        pass

if __name__ == "__main__":
    # run app in debug mode on port 5000
    app.run(host="0.0.0.0", debug=True, port=8080)
