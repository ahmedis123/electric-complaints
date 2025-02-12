from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)  # تمكين الاتصال بين الواجهة الأمامية والخلفية

# إنشاء قاعدة بيانات SQLite إذا لم تكن موجودة
def init_db():
    with sqlite3.connect("reports.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS reports (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT,
                            phone TEXT,
                            email TEXT,
                            address TEXT,
                            meter_number TEXT,
                            issue_type TEXT,
                            description TEXT,
                            image TEXT,
                            status TEXT DEFAULT "قيد المراجعة"
                        )''')
        conn.commit()

init_db()

# API لإضافة بلاغ جديد
@app.route("/add_report", methods=["POST"])
def add_report():
    data = request.json
    with sqlite3.connect("reports.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO reports (name, phone, email, address, meter_number, issue_type, description, image)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                       (data["name"], data["phone"], data["email"], data["address"],
                        data["meter_number"], data["issue_type"], data["description"], data["image"]))
        conn.commit()
    return jsonify({"message": "تم إرسال البلاغ بنجاح"}), 201

# API لاسترجاع جميع البلاغات
@app.route("/get_reports", methods=["GET"])
def get_reports():
    with sqlite3.connect("reports.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM reports")
        reports = cursor.fetchall()
        report_list = []
        for report in reports:
            report_list.append({
                "id": report[0], "name": report[1], "phone": report[2],
                "email": report[3], "address": report[4], "meter_number": report[5],
                "issue_type": report[6], "description": report[7], "image": report[8],
                "status": report[9]
            })
    return jsonify(report_list)

# API لتحديث حالة البلاغ
@app.route("/update_status/<int:report_id>", methods=["PUT"])
def update_status(report_id):
    data = request.json
    new_status = data.get("status")
    with sqlite3.connect("reports.db") as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE reports SET status = ? WHERE id = ?", (new_status, report_id))
        conn.commit()
    return jsonify({"message": "تم تحديث حالة البلاغ"}), 200

# تشغيل السيرفر
if __name__ == "__main__":
    app.run(debug=True)
