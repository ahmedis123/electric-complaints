from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)  # تمكين CORS للتواصل بين الواجهة الأمامية والخلفية

# إنشاء قاعدة البيانات إذا لم تكن موجودة
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

# الصفحة الرئيسية (رفع البلاغ)
@app.route("/")
def index():
    return render_template_string('''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>رفع بلاغات كهرباء</title>
    <style>
        body {
            font-family: 'Tajawal', Arial, sans-serif;
            background: linear-gradient(to right, #dbeafe, #eff6ff);
            color: #333;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        header {
            background-color: #007BFF;
            color: white;
            padding: 20px;
            text-align: center;
            font-size: 1.5rem;
            border-radius: 10px 10px 0 0;
        }
        .container {
            width: 90%;
            max-width: 500px;
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            text-align: center;
        }
        h2 {
            color: #007BFF;
            margin-bottom: 15px;
            font-size: 1.4rem;
        }
        .form-group {
            text-align: right;
            margin-bottom: 15px;
        }
        label {
            font-weight: bold;
            color: #444;
            display: block;
            margin-bottom: 5px;
        }
        input, textarea, select {
            width: 100%;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 8px;
            font-size: 1rem;
            transition: 0.3s;
            background: #f8fafc;
        }
        input:focus, textarea:focus, select:focus {
            border-color: #007BFF;
            outline: none;
            background: #fff;
        }
        textarea {
            resize: vertical;
            min-height: 100px;
        }
        button {
            background-color: #007BFF;
            color: white;
            padding: 12px;
            border: none;
            border-radius: 8px;
            font-size: 1.1rem;
            cursor: pointer;
            width: 100%;
            transition: background-color 0.3s;
        }
        button:hover {
            background-color: #0056b3;
        }
        select {
            appearance: none;
            background-color: #fff;
            cursor: pointer;
        }
        @media (max-width: 768px) {
            .container {
                width: 95%;
                padding: 20px;
            }
            h2 {
                font-size: 1.2rem;
            }
        }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap" rel="stylesheet">
</head>
<body>
    <div class="container">
        <header>
            <h1>رفع بلاغات كهرباء</h1>
        </header>
        <h2>رفع بلاغ جديد</h2>
        <form id="report-form">
            <div class="form-group">
                <label for="name">الاسم الكامل:</label>
                <input type="text" id="name" placeholder="أدخل اسمك" required>
            </div>
            <div class="form-group">
                <label for="phone">رقم الهاتف:</label>
                <input type="tel" id="phone" placeholder="أدخل رقم الهاتف" required>
            </div>
            <div class="form-group">
                <label for="email">البريد الإلكتروني:</label>
                <input type="email" id="email" placeholder="أدخل بريدك الإلكتروني" required>
            </div>
            <div class="form-group">
                <label for="address">العنوان:</label>
                <input type="text" id="address" placeholder="أدخل العنوان" required>
            </div>
            <div class="form-group">
                <label for="meter-number">رقم العداد:</label>
                <input type="text" id="meter-number" placeholder="أدخل رقم العداد" required>
            </div>
            <div class="form-group">
                <label for="issue-type">نوع البلاغ:</label>
                <select id="issue-type" required>
                    <option value="">اختر نوع البلاغ</option>
                    <option value="outage">انقطاع التيار</option>
                    <option value="meter">مشكلة في العدادات</option>
                    <option value="danger">خطر كهربائي</option>
                    <option value="other">أخرى</option>
                </select>
            </div>
            <div class="form-group">
                <label for="description">وصف المشكلة:</label>
                <textarea id="description" placeholder="صف المشكلة بالتفصيل" required></textarea>
            </div>
            <div class="form-group">
                <label for="image">إرفاق صورة (اختياري):</label>
                <input type="file" id="image" accept="image/*">
            </div>
            <button type="submit">إرسال البلاغ</button>
        </form>
    </div>
    <script>
        document.getElementById("report-form").addEventListener("submit", function (e) {
            e.preventDefault();
            const formData = {
                name: document.getElementById("name").value,
                phone: document.getElementById("phone").value,
                email: document.getElementById("email").value,
                address: document.getElementById("address").value,
                meter_number: document.getElementById("meter-number").value,
                issue_type: document.getElementById("issue-type").value,
                description: document.getElementById("description").value,
                image: document.getElementById("image").files[0] ? document.getElementById("image").files[0].name : ""
            };
            fetch("/add_report", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(formData)
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                document.getElementById("report-form").reset();
            })
            .catch(error => console.error("Error:", error));
        });
    </script>
</body>
</html>
    ''')

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

# لوحة التحكم (Admin Panel)
@app.route("/admin")
def admin():
    return render_template_string('''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>لوحة تحكم الإدارة</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Tajawal', Arial, sans-serif;
        }
        body {
            background: #f4f6f9;
        }
        .hidden {
            display: none;
        }
        .login-container {
            width: 100%;
            max-width: 400px;
            background: white;
            padding: 20px;
            margin: 100px auto;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            text-align: center;
        }
        .login-container h2 {
            margin-bottom: 20px;
            color: #007BFF;
        }
        .input-field {
            width: 100%;
            padding: 12px;
            margin-bottom: 15px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 1rem;
        }
        .login-btn {
            width: 100%;
            padding: 12px;
            background: #007BFF;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 1.1rem;
        }
        .login-btn:hover {
            background: #0056b3;
        }
        .error-message {
            color: red;
            margin-top: 10px;
        }
        .dashboard {
            display: flex;
            min-height: 100vh;
        }
        .sidebar {
            width: 250px;
            background: #007BFF;
            color: white;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .sidebar h2 {
            margin-bottom: 20px;
        }
        .sidebar button {
            width: 100%;
            padding: 10px;
            margin-top: 20px;
            background: #0056b3;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .sidebar button:hover {
            background: #004699;
        }
        .main-content {
            flex-grow: 1;
            padding: 20px;
        }
        .main-content h2 {
            margin-bottom: 20px;
            color: #333;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            background: white;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }
        th, td {
            padding: 12px;
            border-bottom: 1px solid #ddd;
            text-align: center;
        }
        th {
            background: #007BFF;
            color: white;
        }
    </style>
</head>
<body>
    <div id="login" class="login-container">
        <h2>تسجيل الدخول</h2>
        <input type="text" id="username" class="input-field" placeholder="اسم المستخدم">
        <input type="password" id="password" class="input-field" placeholder="كلمة المرور">
        <button class="login-btn" onclick="login()">تسجيل الدخول</button>
        <p id="login-message" class="error-message"></p>
    </div>
    <div id="dashboard" class="dashboard hidden">
        <aside class="sidebar">
            <h2>لوحة التحكم</h2>
            <button onclick="logout()">تسجيل الخروج</button>
        </aside>
        <main class="main-content">
            <h2>إدارة البلاغات</h2>
            <table>
                <thead>
                    <tr>
                        <th>رقم البلاغ</th>
                        <th>الاسم</th>
                        <th>نوع البلاغ</th>
                        <th>الحالة</th>
                    </tr>
                </thead>
                <tbody id="reports-table"></tbody>
            </table>
        </main>
    </div>
    <script>
        function login() {
            const username = document.getElementById("username").value;
            const password = document.getElementById("password").value;
            if (username === "admin" && password === "1234") {
                localStorage.setItem("loggedIn", "true");
                showDashboard();
            } else {
                document.getElementById("login-message").innerText = "بيانات غير صحيحة!";
            }
        }

        function logout() {
            localStorage.removeItem("loggedIn");
            document.getElementById("dashboard").classList.add("hidden");
            document.getElementById("login").classList.remove("hidden");
        }

        function showDashboard() {
            document.getElementById("login").classList.add("hidden");
            document.getElementById("dashboard").classList.remove("hidden");
            loadReports();
        }

        function loadReports() {
            fetch("/get_reports")
                .then(response => response.json())
                .then(data => {
                    let tableContent = "";
                    data.forEach(report => {
                        tableContent += `<tr>
                            <td>${report.id}</td>
                            <td>${report.name}</td>
                            <td>${report.issue_type}</td>
                            <td>${report.status}</td>
                        </tr>`;
                    });
                    document.getElementById("reports-table").innerHTML = tableContent;
                })
                .catch(error => console.error("Error:", error));
        }

        if (localStorage.getItem("loggedIn")) {
            showDashboard();
        }
    </script>
</body>
</html>
    ''')

# تشغيل السيرفر
if __name__ == "__main__":
    app.run(debug=True)
