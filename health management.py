# app.py
from flask import Flask, render_template, request, g
import sqlite3
from model import predict_health_risk

app = Flask(__name__)
DATABASE = 'health_history.db'

# --- Database Functions ---

def get_db():
    # Gets the database connection object
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    # Closes the database connection when the app context tears down
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    # Creates the history table if it doesn't exist
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age REAL,
                bmi REAL,
                glucose REAL,
                bp REAL,
                insulin REAL,
                risk_level TEXT,
                risk_message TEXT
            );
        ''')
        db.commit()

# Initialize the database on startup
init_db()

# --- Application Routes ---

@app.route('/', methods=['GET', 'POST'])
def index():
    db = get_db()
    
    if request.method == 'POST':
        try:
            # 1. Collect form data (including the new name field)
            name = request.form['name']
            age = float(request.form['age'])
            bmi = float(request.form['bmi'])
            glucose = float(request.form['glucose'])
            bp = float(request.form['bp'])
            insulin = float(request.form['insulin'])
            
            # 2. Prepare data and get prediction
            user_data = [age, bmi, glucose, bp, insulin]
            prediction_int, message = predict_health_risk(user_data)
            risk_level = "HIGH RISK" if prediction_int == 1 else "LOW RISK"
            
            # 3. Save to History
            cursor = db.cursor()
            cursor.execute('''
                INSERT INTO history (name, age, bmi, glucose, bp, insulin, risk_level, risk_message)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (name, age, bmi, glucose, bp, insulin, risk_level, message))
            db.commit()
            
            # 4. Render results page
            return render_template('result.html', 
                                   prediction=prediction_int, 
                                   message=message,
                                   name=name)
            
        except Exception as e:
            error_message = f"Invalid input. Please check all fields. Error: {e}"
            return render_template('index.html', error=error_message)
            
    return render_template('index.html')

@app.route('/history')
def view_history():
    # Route to display all saved history
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM history ORDER BY id DESC")
    history_data = cursor.fetchall()
    
    # Get column names for the table header
    column_names = [description[0] for description in cursor.description]
    
    return render_template('history.html', history_data=history_data, column_names=column_names)

if __name__ == '__main__':
    app.run(debug=True)