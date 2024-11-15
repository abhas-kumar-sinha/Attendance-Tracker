from flask import Flask, render_template, request, redirect, session, url_for, json, send_from_directory
from flask_mail import Mail, Message
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from random import randint
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import sqlite3
import os
import atexit

load_dotenv()

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def update_day_tracker():
    users = read_User_table()
    for i in users:
        if i[0] != 1001:
            User_db = sqlite3.connect(f"Databases/Users/{i[0]}_data.db")
            User_cursor = User_db.cursor()
            date = datetime.today().date()
            day = give_day_code()

            User_cursor.execute('''INSERT INTO day_tracker (day, date, attendance) VALUES (?, ?, ?)''', (day, date, ""))

            User_cursor.execute(f"""CREATE TABLE IF NOT EXISTS '{date}' (
                                course_id TEXT,
                                class_type TEXT ,
                                day TEXT ,
                                start_time TEXT ,
                                end_time TEXT)""")
            
            User_db.commit()
            User_db.close()

def setup_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=update_day_tracker, trigger="cron", hour=0, minute=1)
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown(wait=False))
    return scheduler

scheduler = setup_scheduler()

def create_connect_db(): 
    User_login_db = sqlite3.connect("Databases/System/User_data.db")
    User_db_cursor = User_login_db.cursor()
    User_db_cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            U_id INTEGER NOT NULL,
                            email TEXT PRIMARY KEY,
                            password INTEGER NOT NULL,
                            date DATE NOT NULL
                            )
                            ''')
    User_db_cursor.execute('''INSERT OR IGNORE INTO users 
                           (U_id, email, password, date) 
                           VALUES (1001, "abc@example.com", 987654321, "2024-10-15")''')

    User_login_db.commit()
    User_login_db.close()

create_connect_db()

def create_User(U_id):
    User_db = sqlite3.connect(f"Databases/Users/{U_id}_data.db")
    User_cursor = User_db.cursor()

    User_cursor.execute('''CREATE TABLE IF NOT EXISTS courses (
                        Course_id TEXT PRIMARY KEY,
                        Name TEXT NOT NULL,
                        Credits TEXT NOT NULL,
                        Details TEXT,
                        Website TEXT,
                        Instructor_Name TEXT,
                        Instructor_Email TEXT )''')
    User_db.commit()

    User_cursor.execute('''CREATE TABLE IF NOT EXISTS attendance (
                        Course_id TEXT PRIMARY KEY,
                        Present INT NOT NULL,
                        Absent INT NOT NULL,
                        medical_leave INT NOT NULL)''')
    User_db.commit()

    User_cursor.execute('''CREATE TABLE IF NOT EXISTS timetable (
                    monday TEXT ,
                    tuesday TEXT ,
                    wednesday TEXT ,
                    thursday TEXT ,
                    friday TEXT)''')
    User_db.commit()

    User_cursor.execute('''INSERT INTO timetable 
                        (monday, tuesday, wednesday, thursday, friday) 
                        VALUES("A", "A", "A", "A", "A")''')
    User_db.commit()

    User_cursor.execute('''CREATE TABLE IF NOT EXISTS userDetails (
                    U_id TEXT PRIMARY KEY,
                    user_name TEXT ,
                    user_email TEXT ,
                    joined_date TEXT ,
                    profile_image_url TEXT, 
                    courses_registered INT)''')
    User_db.commit()

    days_list = ['MON', 'TUE', 'WED', 'THUR', 'FRI']

    for i in days_list:
        User_cursor.execute(f"""CREATE TABLE IF NOT EXISTS {i} (
                course_id TEXT,
                class_type TEXT ,
                day TEXT ,
                start_time TEXT ,
                end_time TEXT)""")
        User_db.commit()

    User_cursor.execute('''CREATE TABLE IF NOT EXISTS day_tracker (
                        day TEXT,
                        date TEXT,
                        attendance TEXT)''')
    User_db.commit()
    
    update_day_tracker()

    insert_details = read_User_table()
    for i in insert_details:
        if i[0] == U_id:
            user_email = i[1]
            joined_date = i[3]

    User_cursor.execute('''INSERT INTO userDetails 
                        (U_id, user_name, user_email, joined_date, profile_image_url, courses_registered) 
                        VALUES(?, "", ?, ?, "", 0)''', (U_id, user_email, joined_date))

    User_db.commit()
    User_db.close()

def read_date_table(U_id):
    date = datetime.today().date()
    User_db = sqlite3.connect(f"Databases/Users/{U_id}_data.db")
    User_cursor = User_db.cursor()

    try:
        User_cursor.execute(f"""SELECT * FROM '{date}'""")  
        read_data = User_cursor.fetchall()
    except sqlite3.OperationalError:
        read_data = []

    User_db.close()

    return read_data  

def drop_table(U_id):
    date = datetime.today().date()
    User_db = sqlite3.connect(f"Databases/Users/{U_id}_data.db")
    User_cursor = User_db.cursor()

    User_cursor.execute(f"""DROP TABLE IF EXISTS '{date}'""")

    User_db.commit()
    User_db.close()

def mark_table(U_id):
    date = datetime.today().date()
    User_db = sqlite3.connect(f"Databases/Users/{U_id}_data.db")
    User_cursor = User_db.cursor()

    User_cursor.execute(f"""UPDATE day_tracker
                        SET attendance = 'MARKED'
                        WHERE date = ?""", (date,))
    User_db.commit()
    User_db.close()

def check_today_attendance(U_id):
    date = datetime.today().date()
    User_db = sqlite3.connect(f"Databases/Users/{U_id}_data.db")
    User_cursor = User_db.cursor()

    User_cursor.execute(f"""SELECT * FROM day_tracker""")

    read_data = User_cursor.fetchall()

    User_db.commit()
    User_db.close() 

    for i in read_data:
        if i[1] == str(date):
            ans = i[2]  
     
    return ans

def write_date_table(U_id, data):
    date = datetime.today().date()
    User_db = sqlite3.connect(f"Databases/Users/{U_id}_data.db")
    User_cursor = User_db.cursor()

    User_cursor.execute(f"""INSERT INTO '{date}' (course_id, class_type, day, start_time, end_time) VALUES ('{data[0]}', '{data[1]}', '{data[2]}', '{data[3]}', '{data[4]}')""")

    User_db.commit()
    User_db.close()

def read_userDetails(U_id):
    User_db = sqlite3.connect(f"Databases/Users/{U_id}_data.db")
    User_cursor = User_db.cursor()

    User_cursor.execute('''SELECT * FROM userDetails''')
    read_data = User_cursor.fetchall()

    User_db.close()
    return read_data

def update_userDetails(U_id, user_name, profile_image_url):
    User_db = sqlite3.connect(f"Databases/Users/{U_id}_data.db")
    User_cursor = User_db.cursor()

    if user_name != "":
        User_cursor.execute('''UPDATE userDetails 
            SET user_name = ? 
            WHERE U_id = ?''', 
            (user_name, U_id)) 

    User_cursor.execute('''UPDATE userDetails 
                    SET profile_image_url = ? 
                    WHERE U_id = ?''', 
                    (profile_image_url, U_id)) 
    
    User_db.commit()
    User_db.close() 

def read_day(U_id, day):
    User_db = sqlite3.connect(f"Databases/Users/{U_id}_data.db")
    User_cursor = User_db.cursor()

    User_cursor.execute(f"""SELECT * from {day}""")

    read_data = User_cursor.fetchall()

    return read_data


def update_course_number(U_id):
    User_db = sqlite3.connect(f"Databases/Users/{U_id}_data.db")
    User_cursor = User_db.cursor()
    
    query = f"UPDATE userDetails SET courses_registered = courses_registered + 1 WHERE U_id = ?"
    User_cursor.execute(query, (U_id,))

    User_db.commit()
    User_db.close()

def read_courses(U_id):
    User_db = sqlite3.connect(f"Databases/Users/{U_id}_data.db")
    User_cursor = User_db.cursor()

    User_cursor.execute('''SELECT * FROM courses''') 
    read_data = User_cursor.fetchall()
    ans = 0
    for i in read_data:
        ans+=1
    return ans

def give_day_code():
    today = datetime.today()
    day_name = today.strftime("%A")

    if day_name == "Monday":
        fin_day_name = "MON"
    elif day_name == "Tuesday":
        fin_day_name = "TUE"
    elif day_name == "Wednesday":
        fin_day_name = "WED"
    elif day_name == "Thursday":
        fin_day_name = "THUR"
    elif day_name == "Friday":
        fin_day_name = "FRI"
    elif day_name == "Saturday":
        fin_day_name = "SAT"
    elif day_name == "Sunday":
        fin_day_name = "SUN"

    return fin_day_name

def read_User_table():
    User_login_db = sqlite3.connect("Databases/System/User_data.db")
    User_db_cursor = User_login_db.cursor()

    User_db_cursor.execute("SELECT * from users")
    read_data = User_db_cursor.fetchall()
    User_login_db.close()
    return read_data

def auth_user(input_id, password):
    all_User_data = read_User_table()
    Ans = False
    for i in all_User_data:
        if str(i[0]) == input_id and str(i[2]) == str(password):
            Ans = True
            break
    return Ans

def write_User_table(U_id, email, password, date):
    User_login_db = sqlite3.connect("Databases/System/User_data.db")
    User_db_cursor = User_login_db.cursor()

    try:
        User_db_cursor.execute('''INSERT INTO users (U_id, email, password, date) Values (?, ?, ?, ?)''', (U_id, email, password, date))
        User_login_db.commit()
        User_login_db.close()
        return True
    except:
        return False
    
def write_User(U_id, course_id, course_name, course_credits, course_details, course_website, Instructor_name, Instructor_email):
    User_db = sqlite3.connect(f"Databases/Users/{U_id}_data.db")
    User_cursor = User_db.cursor()

    try:
        User_cursor.execute('''INSERT INTO courses (Course_id, Name, Credits, Details, Website, Instructor_Name, Instructor_Email) Values (?, ?, ?, ?, ?, ?, ?)''', (course_id, course_name, course_credits, course_details, course_website, Instructor_name, Instructor_email))
        User_cursor.execute('''INSERT INTO attendance (Course_id, Present, Absent, medical_leave) Values (?, ?, ?, ?)''', (course_id, 0, 0, 0))
        User_db.commit()
        User_db.close()
        return True
    except:
        return False  

def read_User(U_id):
    User_db = sqlite3.connect(f"Databases/Users/{U_id}_data.db")
    User_cursor = User_db.cursor()

    User_cursor.execute('''SELECT * from courses''')
    read_data = User_cursor.fetchall()
    User_db.close()
    return read_data  

def read_timetable(U_id):
    User_db = sqlite3.connect(f"Databases/Users/{U_id}_data.db")
    User_cursor = User_db.cursor()

    User_cursor.execute('''SELECT * from timetable''')
    read_data = User_cursor.fetchall()
    User_db.close()
    try:
        read_data[0] = tuple(item.replace("'", '"') for item in read_data[0])
        data_list = [json.loads(item) for item in read_data[0]]
    except:
        data_list = [[],[],[],[],[]]
    return data_list

def write_timetable(U_id, timetable_list):
    User_db = sqlite3.connect(f"Databases/Users/{U_id}_data.db")
    User_cursor = User_db.cursor()

    prev_Data = read_timetable(U_id)

    User_cursor.execute('''DELETE FROM timetable''')
    
    mon, tue, wed, thur, fri = [], [], [], [], []
    list_days = [mon, tue, wed, thur, fri]
    list_days_name = ["MON", "TUE", "WED", "THUR", "FRI"]

    for i in list_days_name:
        User_cursor.execute(f"""DELETE FROM {i}""")

    for i in range(0, len(prev_Data)):
        if i == 0:
            mon+=prev_Data[i]
        elif i == 1:
            tue+=prev_Data[i]
        elif i== 2:
            wed+=prev_Data[i]
        elif i==3:
            thur+=prev_Data[i]
        elif i==4:
            fri+=prev_Data[i]

    for i in timetable_list:
        if i['day'] == "MON":
           mon+=[i]
        elif i['day'] == "TUE":
            tue+=[i]
        elif i['day'] == "WED":
            wed+=[i]
        elif i['day'] == "THUR":
            thur+=[i]
        elif i['day'] == "FRI":
            fri+=[i]

    User_cursor.execute('''INSERT INTO timetable 
                        (monday, tuesday, wednesday, thursday, friday) 
                        VALUES(?, ?, ?, ?, ?)''', (f"{mon}", f"{tue}", f"{wed}", f"{thur}", f"{fri}"))
    idx=0
    for i in list_days:
        for j in i:
            User_cursor.execute(f"""INSERT INTO {list_days_name[idx]}
                                (course_id, class_type, day, start_time, end_time) 
                                VALUES(?, ?, ?, ?, ?)""", (j['course_id'], j['class_type'], j['day'], j['start_time'], j['end_time']))
        idx+=1

    User_db.commit()
    User_db.close()
    
def del_User(U_id, C_id):
    User_db = sqlite3.connect(f"Databases/Users/{U_id}_data.db")
    User_cursor = User_db.cursor()

    User_cursor.execute('''DELETE FROM courses 
                        WHERE Course_id = ?''',(C_id,))
    User_cursor.execute('''DELETE FROM attendance 
                        WHERE Course_id = ?''',(C_id,))
    
    User_db.commit()
    User_db.close()

def read_User_attendance(U_id):
    User_db = sqlite3.connect(f"Databases/Users/{U_id}_data.db")
    User_cursor = User_db.cursor()

    User_cursor.execute('''SELECT * from attendance''')
    read_data = User_cursor.fetchall()
    User_db.close()
    return read_data

def write_User_attendance(U_id, attendance, Course_id):
    User_db = sqlite3.connect(f"Databases/Users/{U_id}_data.db")
    User_cursor = User_db.cursor()

    query = f"UPDATE attendance SET {attendance} = {attendance} + 1 WHERE Course_id = ?"
    User_cursor.execute(query, (Course_id,))

    User_db.commit()
    User_db.close()

def create_U_id():
    existing_U_id = []
    for i in read_User_table():
        existing_U_id.append(i[0])
    
    gen_U_id = existing_U_id[0]
    while gen_U_id in existing_U_id:
        gen_U_id = randint(1000, 9999)
    
    return gen_U_id

def generate_otp():
    return str(randint(100000, 999999))

app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

mail = Mail(app)

@app.route('/')
def home():
    return redirect('Sign-In')

@app.route("/Home", methods=['GET', 'POST'])
def main_Web():
    read_data_user = read_userDetails(session['U_id'])
    attendance = read_User_attendance(session['U_id'])
    return render_template('index.html', attendance = attendance, read_data_user=read_data_user)

@app.route("/Sign-In", methods=['GET', 'POST'])
def Sign_In_Web():
    if request.method == 'POST':
        input_id = request.form["signin-i'd"]
        password = request.form['signin-password']
        if auth_user(input_id, password):
            session.clear()
            session['U_id'] = input_id
            return redirect('Home')
        else:
            return "error! Invalid Credentials"

    return render_template('Signin.html')

@app.route("/Sign-Up", methods=['GET', 'POST'])
def Sign_Up_Web():
    if request.method == 'POST':
        email = request.form['signup-email']
        password = request.form['signup-password']
        session.clear()

        session['email'] = email
        session['password'] = password
        session.pop('OTP', None)
        return redirect("/Verify-OTP")
        
    return render_template('Signup.html')

@app.route("/Verify-OTP", methods=['GET', 'POST'])
def Verify_User():
    U_id = create_U_id()
    email = session.get('email')
    password = session.get('password')
    date = datetime.today().date()
    if 'OTP' not in session:
        OTP = generate_otp()
        
        session['OTP'] = OTP

        html_content = render_template("email_template.html", email=email, OTP=OTP)
        msg_sender = os.getenv('MAIL_USERNAME')
        msg = Message("Please verify your email", sender=msg_sender, recipients=[email])
        msg.html = html_content

        try:
            mail.send(msg)
        except Exception as e:
            return f'Failed to send OTP: {e}'

    if request.method == 'POST':
        entered_OTP = request.form['entered_OTP']

        OTP = session.get('OTP')
        
        if entered_OTP == OTP:
            if write_User_table(U_id, email, password, date):
                msg_sender = os.getenv('MAIL_USERNAME')
                new_msg = Message('Account Created', sender=msg_sender, recipients=[email])
                new_msg.body = f"This is a system generated Mail. Please Do not reply. \nYour Login Credentials \nKeep Your Credentials safe and avoid sharing with others. \nUser I'd: {U_id}\nPassword: {password} \nThank you for chosing us ❤️."
                session.pop('OTP', None)
                create_User(U_id)
            
                try:
                    mail.send(new_msg)
                except Exception as e:
                    return f'Failed to send OTP: {e}'
                
                session.pop('email', None)
                session.pop('password', None)

                session['U_id'] = U_id
                
                return redirect('Home')
            else:
                return "Error! Email already used..."
        else:
            return "OTP does not match!!!"
    
    return render_template('Signup-OTP.html', email=email)

@app.route("/Add-Course", methods = ['GET', 'POST'])
def Add_Course():
    read_data_user = read_userDetails(session['U_id'])
    courses = read_User(session['U_id'])
    form_name = request.form.get('form-name')

    if request.method == 'POST' and form_name == "add-course":
        course_id = request.form.get('form-course-id')
        course_name = request.form.get('form-course-name')
        course_credits = request.form.get('form-course-credits')
        course_details = request.form.get('form-course-details')
        course_website = request.form.get('form-course-website')
        Instructor_name = request.form.get('form-instructor')
        Instructor_email = request.form.get('form-instructor-email')

        if write_User(session['U_id'], course_id, course_name, course_credits, course_details, course_website, Instructor_name, Instructor_email):
            update_course_number(session['U_id'])
            return redirect("Add-Course")
        else:
            return "Error. Course already exists."
        
    if request.method == 'POST' and form_name == "delete-course":
        C_id = request.form.get("C_id")
        del_User(session['U_id'], C_id)
        courses = read_User(session['U_id'])

    return render_template('AddCourse.html', courses = courses, read_data_user=read_data_user)

@app.route("/Mark-Attendance", methods = ['GET', 'POST'])
def Mark_Attendance():
    read_data_user = read_userDetails(session['U_id'])
    courses = read_User(session['U_id'])
    fin_day_name=give_day_code()
    date = datetime.today().date()
    today_attendance = read_day(session['U_id'], fin_day_name)
    done_attendance = read_date_table(session['U_id'])

    fin_timetables_list = []
    for i in today_attendance:
        if i not in done_attendance and check_today_attendance(session['U_id']) != "MARKED":
            fin_timetables_list.append(i)

    if done_attendance == today_attendance and today_attendance != []:
        drop_table(session['U_id'])
        mark_table(session['U_id'])
        fin_timetables_list=[]

    if request.method == 'POST':
        course_id = request.form.get("form-course-id")
        class_type = request.form.get("form-class-type")
        attendance = request.form.get("attendance")
        day = request.form.get("form-day")
        start_time = request.form.get("form-start-time")
        end_time = request.form.get("form-end-time")
        
        write_User_attendance(session['U_id'], attendance, course_id)
        write_date_table(session['U_id'], [course_id, class_type, day, start_time, end_time])

        return redirect("Mark-Attendance")
        
    return render_template('MarkAttendance.html', courses=courses, fin_timetables_list=fin_timetables_list, fin_day_name=fin_day_name, read_data_user = read_data_user, date = date)

@app.route("/Today-Schedule", methods = ['GET', 'POST'])
def Schedule():
    read_data_user = read_userDetails(session['U_id'])
    timetables = read_timetable(session['U_id'])
    timetables_list = [item for sublist in timetables for item in sublist]
    courses = read_User(session['U_id'])
    form_name = request.form.get('form-name')

    if request.method == 'POST' and form_name == "add-course":
        form_data = request.form

        all_forms_data = []

        for key, value in form_data.items():
        # Extract the form index (e.g., from form-course-name-123, we extract 123)
            if key.startswith('course-id-'):
                form_index = key.split('-')[-1]
                # Now create a dictionary for this form's data
                form_dict = {
                    'course_id': form_data.get(f'course-id-{form_index}'),
                    'class_type': form_data.get(f'class-type-{form_index}'),
                    'day': form_data.get(f'day-{form_index}'),
                    'start_time': form_data.get(f'class-start-time-{form_index}'),
                    'end_time': form_data.get(f'class-end-time-{form_index}')
                }
                all_forms_data.append(form_dict)

        write_timetable(session['U_id'], all_forms_data)
        timetables = read_timetable(session['U_id'])
        timetables_list = [item for sublist in timetables for item in sublist]
        courses = read_User(session['U_id'])
        
    if request.method == 'POST' and form_name == "delete-course":
        C_id = request.form.get("C_id")
        del_User(session['U_id'], C_id)
        timetables = read_timetable(session['U_id'])
        timetables_list = [item for sublist in timetables for item in sublist]
        courses = read_User(session['U_id'])

    return render_template('Schedule.html', timetables_list=timetables_list, courses=courses, read_data_user=read_data_user)

@app.route("/Analytics", methods = ['GET', 'POST'])
def Course_Analytics():
    read_data_user = read_userDetails(session['U_id'])
    attendance = read_User_attendance(session['U_id'])
    return render_template('Analytics-web.html', attendance=attendance, read_data_user=read_data_user)

@app.route("/Grades", methods = ['GET', 'POST'])
def Grades():
    read_data_user = read_userDetails(session['U_id'])
    return render_template('Grades.html', read_data_user=read_data_user)

@app.route("/User-Profile", methods = ['GET', 'POST'])
def User_Profile():
    read_data_user = read_userDetails(session['U_id'])

    if request.method == 'POST':
        user_name = request.form.get('User-Name')
        user_name =user_name.title()
        file = request.files['imageInput']
        if file:
            # Secure the filename and save the file to the server
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Generate the URL to the uploaded file
            profile_image_url = url_for('static', filename=f'uploads/{filename}', _external=True)
        else:
            profile_image_url = ""

        if profile_image_url != "":
            update_userDetails(session['U_id'], user_name, profile_image_url)
        else:
            update_userDetails(session['U_id'], user_name, read_data_user[0][4])

        return redirect('Home')

    return render_template('UserProfile.html', read_data_user=read_data_user)

@app.route("/Log-Out", methods = ['GET', 'POST'])
def Logout():
    session.clear()
    return redirect("Sign-In")

@app.route("/sitemap.xml", methods = ['GET', 'POST'])
def Sitemap():
    return send_from_directory('static', 'sitemap.xml')

if __name__ == "__main__":
    app.run(debug=True, port=8000)