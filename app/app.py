from flask import Flask, render_template, request, send_file, abort
import mysql.connector
import io
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Database connection details
DB_CONFIG = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_NAME')
}

def get_top_users():
    query = """
    SELECT b.borrowernumber, b.cardnumber,
           CONCAT(b.title, ' ', b.surname) AS name,
           COALESCE(COUNT(i.issue_id), 0) AS borrow_count,
           br.branchname
    FROM borrowers b
    LEFT JOIN issues i ON b.borrowernumber = i.borrowernumber
    LEFT JOIN branches br ON b.branchcode = br.branchcode
    WHERE i.issuedate > DATE_SUB(CURDATE(), INTERVAL 30 DAY)
    GROUP BY b.borrowernumber, b.cardnumber, b.surname, br.branchname
    ORDER BY borrow_count DESC
    LIMIT 5;
    """

    with mysql.connector.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()

@app.route('/')
def index():
    top_users = get_top_users()
    return render_template('index.html', users=top_users)

@app.route('/images/<int:borrowernumber>')
def image(borrowernumber):
    query = "SELECT imagefile FROM patronimage WHERE borrowernumber = %s"
    with mysql.connector.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (borrowernumber,))
            result = cursor.fetchone()

    if result and result[0]:
        return send_file(io.BytesIO(result[0]), mimetype='image/jpeg')
    else:
        return send_file("static/default.jpg", mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
