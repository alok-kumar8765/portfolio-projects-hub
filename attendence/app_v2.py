from flask import Flask, render_template, request, jsonify
import cv2
import sqlite3
import numpy as np
import base64
from datetime import datetime, date

app = Flask(__name__)
DB = 'attendance.db'

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    
    # Create base tables
    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_code TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            timestamp TEXT,
            status TEXT,
            FOREIGN KEY(student_id) REFERENCES students(id)
        )
    ''')
    
    # Safe migration: add parent columns if they don't exist in legacy DB
    c.execute("PRAGMA table_info(students)")
    columns = [col[1] for col in c.fetchall()]
    if 'father_name' not in columns:
        c.execute("ALTER TABLE students ADD COLUMN father_name TEXT")
    if 'mother_name' not in columns:
        c.execute("ALTER TABLE students ADD COLUMN mother_name TEXT")
        
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/students/add', methods=['POST'])
def add_student():
    data = request.json
    try:
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute('''
            INSERT INTO students (student_code, name, father_name, mother_name) 
            VALUES (?, ?, ?, ?)
        ''', (data['student_code'], data['name'], data.get('father_name', ''), data.get('mother_name', '')))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Student registered successfully!'})
    except sqlite3.IntegrityError:
        return jsonify({'success': False, 'message': 'Roll Number / Student Code already exists!'}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/students', methods=['GET'])
def get_students():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM students")
    students = [dict(row) for row in c.fetchall()]
    conn.close()
    return jsonify(students)

@app.route('/api/mark', methods=['POST'])
def mark_attendance():
    data = request.get_json()
    student_id = data.get('student_id')
    image_data = data.get('image')

    try:
        header, encoded = image_data.split(',', 1)
        image_bytes = base64.b64decode(encoded)
        np_arr = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        if len(faces) == 0:
            return jsonify({'success': False, 'message': 'No face detected in frame'}), 400

        conn = sqlite3.connect(DB)
        c = conn.cursor()
        
        today_str = date.today().isoformat()
        c.execute("SELECT id FROM attendance WHERE student_id = ? AND timestamp LIKE ?", (student_id, f"{today_str}%"))
        if c.fetchone():
            conn.close()
            return jsonify({'success': True, 'message': 'Attendance already marked for today'})

        c.execute("INSERT INTO attendance (student_id, timestamp, status) VALUES (?, ?, ?)",
                  (student_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'Present'))
        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': 'Attendance recorded successfully!'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    filter_type = request.args.get('filter', 'all')
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("SELECT COUNT(DISTINCT DATE(timestamp)) as total_days FROM attendance")
    row = c.fetchone()
    total_days = row['total_days'] if row and row['total_days'] > 0 else 1

    query = '''
        SELECT s.id, s.student_code, s.name, s.father_name, s.mother_name,
        COUNT(a.id) as present_days
        FROM students s
        LEFT JOIN attendance a ON s.id = a.student_id
    '''
    
    if filter_type == 'monthly':
        current_month = datetime.now().strftime('%Y-%m')
        query += f" WHERE a.timestamp LIKE '{current_month}%'"
    elif filter_type == 'yearly':
        current_year = datetime.now().strftime('%Y')
        query += f" WHERE a.timestamp LIKE '{current_year}%'"

    query += " GROUP BY s.id"
    c.execute(query)
    results = []
    
    for row in c.fetchall():
        data = dict(row)
        percentage = round((data['present_days'] / total_days) * 100, 2) if total_days > 0 else 0.0
        data['attendance_percentage'] = percentage
        
        if filter_type == 'low_attendance' and percentage >= 75.0:
            continue
        results.append(data)

    conn.close()
    return jsonify(results)

@app.route('/api/report', methods=['GET'])
def generate_report():
    student_id = request.args.get('student_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    query = '''
        SELECT a.id, s.student_code, s.name, s.father_name, a.timestamp, a.status
        FROM attendance a
        JOIN students s ON s.id = a.student_id
        WHERE 1=1
    '''
    params = []

    if student_id and student_id != "":
        query += " AND s.id = ?"
        params.append(student_id)
    if start_date and end_date:
        query += " AND DATE(a.timestamp) BETWEEN ? AND ?"
        params.extend([start_date, end_date])

    query += " ORDER BY a.timestamp DESC"
    c.execute(query, params)
    records = [dict(row) for row in c.fetchall()]
    conn.close()
    return jsonify(records)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)