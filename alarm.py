import sqlite3
from datetime import datetime

print(datetime.now())

con = sqlite3.connect("lampy.sqlite3")
cur = con.cursor()
cur.execute("select toggle from alarm where id=1")
res = cur.fetchall()
toggleValue = res[0][0]
if toggleValue == 1:
    print("toggle is 1")
else:
    print("toggle is 0")
