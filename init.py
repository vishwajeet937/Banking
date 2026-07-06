import os
import boto3
import sys
import pymysql

client = boto3.client("ssm", region_name="us-east-1")

def get_param(name):
    response = client.get_parameters(
        Names=f"/application/banking/{name}",
        WithDecryption=True
    )["parameters"]["value"]

try:
    conn = pymysql.connect(
        host=get_param["DB_HOST"],
        port=int(get_param["DB_PORT"]),
        user=get_param["DB_USER"],
        password=get_param["DB_PASSWORD"],
        connect_timeout=10
    )

    cur = conn.cursor()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sql_file_path = os.path.join(base_dir, "init.sql")

    with open(sql_file_path, "r", encoding="utf-8") as f:
        sql=f.read()

    for statement in sql.split(";"):
        statement = statement.strip()
        if statement:
            cur.execute(statement)

    conn.commit()
    print("Data connected succesfully ✅")
except Exception as e:
    print("error: ", e)
    
finally:
    conn.close()