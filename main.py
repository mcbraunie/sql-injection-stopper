"""
SQLi Step-by-Step
-------------------------------------------------------------

"INSERT INTO messages VALUES('{}', '{}')"  

step 1:
user IP is entered into first curly braces
"INSERT INTO messages VALUES('127.0.0.1', '{}')"
       
step 2:
second set of curly braces are filled with the remaining data
"INSERT INTO messages VALUES('127.0.0.1', 'uh oh'), \
('256.256.256.256', 'its a trap!')"
        
step 3: 
the SQL statement looks appears to be a valid statement to add
2 rows to the database (which is not its intended use) 

"""
import os
import base64
import sqlite3
import re

from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():

    conn = sqlite3.connect('my_database.db')
    c = conn.cursor()

    if request.method == 'POST':
        
        # Escape character check
        for i in request.form['content']:
            if i == "'":
                raise Exception('You cannot do that!')
                break

        transaction = "INSERT INTO messages VALUES ('{}', '{}')".format(
        request.remote_addr,
        request.form['content'])
        c.execute(transaction)
        conn.commit()


    body = """
<html>
<body>
<h1>Messages</h1>
<h2>Enter a Message</h2>
<form method="POST">
    <label for="content">Message</label>
    <input type="text" name="content"><br>
    <input type="submit" value="Submit">
</form>
<h2>Messages</h2>
"""
    
    for m in c.execute("SELECT * FROM messages"):
        body += """
<div class="message">
{}: {}
</div>
""".format(m[0], m[1]).replace("'", "")

    c.close()

    return body 


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6779))
    app.run(host='0.0.0.0', port=port)

