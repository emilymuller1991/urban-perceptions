import json
import os

import flask
import psycopg2
from flask import jsonify, request
from flask_cors import CORS

app = flask.Flask(__name__)
CORS(app, support_credentials=True, resources={r"/*": {"origins": "*"}})
app.config["DEBUG"] = True


@app.route("/post_data", methods=["POST"])
def post_data():
    print(json.loads(request.data))
    insert_rating(json.loads(request.data))
    return jsonify({"step": "1"})


@app.route("/get_data", methods=["GET"])
def get_data():
    meta = get_image()
    response = jsonify(meta)
    print(response)
    return response


dbconn = {
    "database": os.getenv("db"),
    "user": os.getenv("db_user"),
    "port": os.getenv("port"),
}

pg_conn = psycopg2.connect(**dbconn)
pg_cur = pg_conn.cursor()


def get_image():
    sql = """select * from images.preprocessing where exist=1 ORDER
                        BY random() LIMIT 20
           """
    pg_cur.execute(sql)
    data = pg_cur.fetchall()
    return data


def insert_rating(data):
    sql = """insert into users.perceptions
            select img_1, img_2, perception, choice, user_id, time
            from json_to_recordset(%s) x (img_1 varchar(60),
                                          img_2 varchar(60),
                                          perception varchar(60),
                                          choice varchar(60),
                                          user_id varchar(100),
                                          time varchar(100)
            )
        """
    pg_cur.execute(sql, (json.dumps([data]),))
    pg_conn.commit()


if __name__ == "__main__":
    app.run(host=os.getenv("app_host"), port="5000")
