import csv
import io
import os
import json
from flask import Flask, render_template, request, jsonify, make_response
import cv2
import sqlite3
import numpy as np
from deepface import DeepFace
from datetime import datetime, date

app = Flask(__name__)
DB = 'attendance.db'

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_code TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            father_name TEXT,
            mother_name TEXT,
            face_encoding TEXT
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
    
    # Safe database column migrations for legacy databases
    c.execute("PRAGMA table_info(students)")
    columns = [col[1] for col in c.fetchall()]
    if 'father_name' not in columns:
        c.execute("ALTER TABLE students ADD COLUMN father_name TEXT")
    if 'mother_name' not in columns:
        c.execute("ALTER TABLE students ADD COLUMN mother_name TEXT")
    if 'face_encoding' not in columns:
        c.execute("ALTER TABLE students ADD COLUMN face_encoding TEXT")
        
    conn.commit()
    conn.close()

def decode_image(image_data_str):
    if "," in image_data_str:
        image_data_str = image_data_str.split(",")[1]
    image_bytes = base64.b64decode(image_data_str)
    np_arr = np.frombuffer(image_bytes, np.uint8)
    return cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

@app.route('/')
def index():
    return render_template('index.html')

# --- 1. REGISTER STUDENT WITH DEEPFACE ENCODING ---
@app.route('/api/students/add', methods=['POST'])
def add_student():
    import base64
    data = request.json
    image_data = data.get('image')

    if not image_data:
        return jsonify({'success': False, 'message': 'Face snapshot required for registration!'}), 400

    temp_path = "temp_reg.jpg"
    try:
        frame = decode_image(image_data)
        cv2.imwrite(temp_path, frame)

        # Extract embedding using DeepFace (Facenet model)
        embedding_objs = DeepFace.represent(img_path=temp_path, model_name="Facenet", enforce_detection=True)
        if os.path.exists(temp_path): 
            os.remove(temp_path)

        if not embedding_objs:
            return jsonify({'success': False, 'message': 'No face detected clearly!'}), 400

        embedding_vector = embedding_objs[0]["embedding"]
        encoding_json = json.dumps(embedding_vector)

        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute('''
            INSERT INTO students (student_code, name, father_name, mother_name, face_encoding) 
            VALUES (?, ?, ?, ?, ?)
        ''', (data['student_code'], data['name'], data.get('father_name', ''), data.get('mother_name', ''), encoding_json))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Student registered successfully with face data!'})
    except sqlite3.IntegrityError:
        if os.path.exists(temp_path): os.remove(temp_path)
        return jsonify({'success': False, 'message': 'Roll Number / Student Code already exists!'}), 400
    except Exception as e:
        if os.path.exists(temp_path): os.remove(temp_path)
        return jsonify({'success': False, 'message': 'Face detection failed. Ensure face is clearly visible.'}), 400

# --- 2. AUTOMATED FACE MATCHING ATTENDANCE ---
@app.route('/api/mark', methods=['POST'])
def mark_attendance():
    import base64
    data = request.get_json()
    image_data = data.get('image')

    if not image_data:
        return jsonify({'success': False, 'message': 'No image data provided'}), 400

    temp_path = "temp_scan.jpg"
    try:
        frame = decode_image(image_data)
        cv2.imwrite(temp_path, frame)

        scan_objs = DeepFace.represent(img_path=temp_path, model_name="Facenet", enforce_detection=True)
        if os.path.exists(temp_path): 
            os.remove(temp_path)

        if not scan_objs:
            return jsonify({'success': False, 'message': 'No face detected in frame'}), 400

        target_vector = np.array(scan_objs[0]["embedding"])

        conn = sqlite3.connect(DB)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT id, name, student_code, face_encoding FROM students WHERE face_encoding IS NOT NULL")
        students = c.fetchall()

        matched_student = None
        min_distance = float('inf')
        
        for student in students:
            known_vector = np.array(json.loads(student['face_encoding']))
            euclidean_dist = np.linalg.norm(target_vector - known_vector)
            
            # Threshold constraint for Facenet similarity matching
            if euclidean_dist < 10.0:  
                if euclidean_dist < min_distance:
                    min_distance = euclidean_dist
                    matched_student = student

        if not matched_student:
            conn.close()
            return jsonify({'success': False, 'message': 'Face not recognized! Please register first.'}), 404

        student_id = matched_student['id']
        today_str = date.today().isoformat()
        
        c.execute("SELECT id FROM attendance WHERE student_id = ? AND timestamp LIKE ?", (student_id, f"{today_str}%"))
        if c.fetchone():
            conn.close()
            return jsonify({'success': True, 'message': f'Attendance already marked today for {matched_student["name"]}'})

        c.execute("INSERT INTO attendance (student_id, timestamp, status) VALUES (?, ?, ?)",
                  (student_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'Present'))
        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': f'Welcome {matched_student["name"]}! Attendance recorded.'})
    except Exception as e:
        if os.path.exists(temp_path): os.remove(temp_path)
        return jsonify({'success': False, 'message': 'Face verification scan failed.'}), 400

@app.route('/api/students', methods=['GET'])
def get_students():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT id, student_code, name, father_name, mother_name FROM students")
    students = [dict(row) for row in c.fetchall()]
    conn.close()
    return jsonify(students)

# --- 3. ANALYTICS & FILTERING ---
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

# --- 4. REPORTS GENERATOR ---
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

# --- 5. CSV EXPORT ROUTE ---
@app.route('/api/export/csv', methods=['GET'])
def export_csv():
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

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Roll Number', 'Student Name', "Father's Name", 'Timestamp', 'Status'])
    for r in records:
        writer.writerow([r['student_code'], r['name'], r['father_name'], r['timestamp'], r['status']])

    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=attendance_report.csv"
    response.headers["Content-type"] = "text/csv"
    return response

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)