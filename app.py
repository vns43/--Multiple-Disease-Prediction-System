import os
import pickle
import sqlite3
import streamlit as st
from streamlit_option_menu import option_menu

# Set page configuration
st.set_page_config(page_title="Health Assistant",
                   layout="wide",
                   page_icon="🧑‍⚕️")

# Initialize SQLite database
conn = sqlite3.connect('users.db')
c = conn.cursor()
# Create users table
c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)''')
# Create tables for storing disease details
c.execute('''CREATE TABLE IF NOT EXISTS diabetes_details (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                patient_name TEXT,
                Pregnancies REAL, 
                Glucose REAL, 
                BloodPressure REAL, 
                SkinThickness REAL, 
                Insulin REAL, 
                BMI REAL, 
                DiabetesPedigreeFunction REAL, 
                Age REAL,
                diagnosis TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS heart_disease_details (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                patient_name TEXT,
                age REAL, 
                sex REAL, 
                cp REAL, 
                trestbps REAL, 
                chol REAL, 
                fbs REAL, 
                restecg REAL, 
                thalach REAL, 
                exang REAL, 
                oldpeak REAL, 
                slope REAL, 
                ca REAL, 
                thal REAL,
                diagnosis TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS parkinsons_details (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                patient_name TEXT,
                fo REAL, 
                fhi REAL, 
                flo REAL, 
                Jitter_percent REAL, 
                Jitter_Abs REAL, 
                RAP REAL, 
                PPQ REAL, 
                DDP REAL, 
                Shimmer REAL, 
                Shimmer_dB REAL, 
                APQ3 REAL, 
                APQ5 REAL, 
                APQ REAL, 
                DDA REAL, 
                NHR REAL, 
                HNR REAL, 
                RPDE REAL, 
                DFA REAL, 
                spread1 REAL, 
                spread2 REAL, 
                D2 REAL, 
                PPE REAL,
                diagnosis TEXT)''')
conn.commit()

# Function to add user to the database
def add_user(username, password):
    c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    conn.commit()

# Function to check user credentials
def login_user(username, password):
    c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    data = c.fetchone()
    return data

# Function to add diabetes details
def add_diabetes_details(username, patient_name, details):
    c.execute('''INSERT INTO diabetes_details (username, patient_name, Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age, diagnosis)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
              (username, patient_name, *details))
    conn.commit()

# Function to add heart disease details
def add_heart_disease_details(username, patient_name, details):
    c.execute('''INSERT INTO heart_disease_details (username, patient_name, age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, diagnosis)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
              (username, patient_name, *details))
    conn.commit()

# Function to add Parkinson's details
def add_parkinsons_details(username, patient_name, details):
    c.execute('''INSERT INTO parkinsons_details (username, patient_name, fo, fhi, flo, Jitter_percent, Jitter_Abs, RAP, PPQ, DDP, Shimmer, Shimmer_dB, APQ3, APQ5, APQ, DDA, NHR, HNR, RPDE, DFA, spread1, spread2, D2, PPE, diagnosis)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
              (username, patient_name, *details))
    conn.commit()

# Create session state for login and signup
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "signed_up" not in st.session_state:
    st.session_state["signed_up"] = False

# Sign-up page
if not st.session_state["signed_up"]:
    st.title("Sign Up")

    signup_username = st.text_input("Enter a username")
    signup_password = st.text_input("Enter a password", type="password")
    signup_button = st.button("Sign Up")

    if signup_button:
        if signup_username and signup_password:
            add_user(signup_username, signup_password)
            st.success("Successfully signed up! Please login now.")
            st.session_state["signed_up"] = True
        else:
            st.error("Please fill in both fields")

# Login page
if st.session_state["signed_up"] and not st.session_state["logged_in"]:
    st.title("Login")

    login_username = st.text_input("Username")
    login_password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        user = login_user(login_username, login_password)
        if user:
            st.session_state["logged_in"] = True
            st.session_state["username"] = login_username
            st.success("Successfully logged in!")
        else:
            st.error("Invalid username or password")

# Main application
if st.session_state["logged_in"]:
    # getting the working directory of the main.py
    working_dir = os.path.dirname(os.path.abspath(__file__))

    # loading the saved models
    diabetes_model = pickle.load(open(f'{working_dir}/saved_models/diabetes_model.sav', 'rb'))
    heart_disease_model = pickle.load(open(f'{working_dir}/saved_models/heart_disease_model.sav', 'rb'))
    parkinsons_model = pickle.load(open(f'{working_dir}/saved_models/parkinsons_model.sav', 'rb'))

    # sidebar for navigation
    with st.sidebar:
        selected = option_menu('Multiple Disease Prediction System',
                               ['Diabetes Prediction',
                                'Heart Disease Prediction',
                                'Parkinsons Prediction',
                                'Patient Details'],
                               menu_icon='hospital-fill',
                               icons=['activity', 'heart', 'person', 'list'],
                               default_index=0)

    # Diabetes Prediction Page
    if selected == 'Diabetes Prediction':
        # page title
        st.title('Diabetes Prediction using ML')

        # getting the input data from the user
        col1, col2, col3 = st.columns(3)

        with col1:
            patient_name = st.text_input('Patient Name')
            Pregnancies = st.text_input('Number of Pregnancies')

        with col2:
            Glucose = st.text_input('Glucose Level')

        with col3:
            BloodPressure = st.text_input('Blood Pressure')
        with col3:
            BloodPressure = st.text_input('Blood Pressure value')

        with col1:
            SkinThickness = st.text_input('Skin Thickness value')

        with col2:
            Insulin = st.text_input('Insulin Level')

        with col3:
            BMI = st.text_input('BMI value')

        with col1:
            DiabetesPedigreeFunction = st.text_input('Diabetes Pedigree Function value')

        with col2:
            Age = st.text_input('Age of the Person')

        # code for Prediction
        diab_diagnosis = ''

        # creating a button for Prediction
        if st.button('Diabetes Test Result'):
            if all([patient_name, Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]):
                user_input = [Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]

                user_input = [float(x) if x else 0.0 for x in user_input]

                diab_prediction = diabetes_model.predict([user_input])

                if diab_prediction[0] == 1:
                    diab_diagnosis = 'The person is diabetic'
                else:
                    diab_diagnosis = 'The person is not diabetic'
                
                add_diabetes_details(st.session_state["username"], patient_name, user_input + [diab_diagnosis])
            else:
                st.error("Please fill in all fields to proceed with the prediction.")

        st.success(diab_diagnosis)

    # Heart Disease Prediction Page
    if selected == 'Heart Disease Prediction':
        # page title
        st.title('Heart Disease Prediction using ML')

        col1, col2, col3 = st.columns(3)

        with col1:
            patient_name = st.text_input('Patient Name')
            age = st.text_input('Age')

        with col2:
            sex = st.text_input('Sex')

        with col3:
            cp = st.text_input('Chest Pain types')

        with col1:
            trestbps = st.text_input('Resting Blood Pressure')

        with col2:
            chol = st.text_input('Serum Cholestoral in mg/dl')

        with col3:
            fbs = st.text_input('Fasting Blood Sugar > 120 mg/dl')

        with col1:
            restecg = st.text_input('Resting Electrocardiographic results')

        with col2:
            thalach = st.text_input('Maximum Heart Rate achieved')

        with col3:
            exang = st.text_input('Exercise Induced Angina')

        with col1:
            oldpeak = st.text_input('ST depression induced by exercise')

        with col2:
            slope = st.text_input('Slope of the peak exercise ST segment')

        with col3:
            ca = st.text_input('Major vessels colored by flourosopy')

        with col1:
            thal = st.text_input('thal: 0 = normal; 1 = fixed defect; 2 = reversable defect')

        # code for Prediction
        heart_diagnosis = ''

        # creating a button for Prediction
        if st.button('Heart Disease Test Result'):
            if all([patient_name, age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]):
                user_input = [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]

                user_input = [float(x) if x else 0.0 for x in user_input]

                heart_prediction = heart_disease_model.predict([user_input])

                if heart_prediction[0] == 1:
                    heart_diagnosis = 'The person is having heart disease'
                else:
                    heart_diagnosis = 'The person does not have any heart disease'
                
                add_heart_disease_details(st.session_state["username"], patient_name, user_input + [heart_diagnosis])
            else:
                st.error("Please fill in all fields to proceed with the prediction.")

        st.success(heart_diagnosis)

    # Parkinson's Prediction Page
    if selected == "Parkinsons Prediction":
        # page title
        st.title("Parkinson's Disease Prediction using ML")

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            patient_name = st.text_input('Patient Name')
            fo = st.text_input('MDVP:Fo(Hz)')

        with col2:
            fhi = st.text_input('MDVP:Fhi(Hz)')

        with col3:
            flo = st.text_input('MDVP:Flo(Hz)')

        with col4:
            Jitter_percent = st.text_input('MDVP:Jitter(%)')

        with col5:
            Jitter_Abs = st.text_input('MDVP:Jitter(Abs)')

        with col1:
            RAP = st.text_input('MDVP:RAP')

        with col2:
            PPQ = st.text_input('MDVP:PPQ')

        with col3:
            DDP = st.text_input('Jitter:DDP')

        with col4:
            Shimmer = st.text_input('MDVP:Shimmer')

        with col5:
            Shimmer_dB = st.text_input('MDVP:Shimmer(dB)')

        with col1:
            APQ3 = st.text_input('Shimmer:APQ3')

        with col2:
            APQ5 = st.text_input('Shimmer:APQ5')

        with col3:
            APQ = st.text_input('MDVP:APQ')

        with col4:
            DDA = st.text_input('Shimmer:DDA')

        with col5:
            NHR = st.text_input('NHR')

        with col1:
            HNR = st.text_input('HNR')

        with col2:
            RPDE = st.text_input('RPDE')

        with col3:
            DFA = st.text_input('DFA')

        with col4:
            spread1 = st.text_input('spread1')

        with col5:
            spread2 = st.text_input('spread2')

        with col1:
            D2 = st.text_input('D2')

        with col2:
            PPE = st.text_input('PPE')

        # code for Prediction
        parkinsons_diagnosis = ''

        # creating a button for Prediction    
        if st.button("Parkinson's Test Result"):
            if all([patient_name, fo, fhi, flo, Jitter_percent, Jitter_Abs, RAP, PPQ, DDP, Shimmer, Shimmer_dB, APQ3, APQ5, APQ, DDA, NHR, HNR, RPDE, DFA, spread1, spread2, D2, PPE]):
                user_input = [fo, fhi, flo, Jitter_percent, Jitter_Abs, RAP, PPQ, DDP, Shimmer, Shimmer_dB, APQ3, APQ5, APQ, DDA, NHR, HNR, RPDE, DFA, spread1, spread2, D2, PPE]

                user_input = [float(x) if x else 0.0 for x in user_input]

                parkinsons_prediction = parkinsons_model.predict([user_input])

                if parkinsons_prediction[0] == 1:
                    parkinsons_diagnosis = "The person has Parkinson's disease"
                else:
                    parkinsons_diagnosis = "The person does not have Parkinson's disease"
                
                add_parkinsons_details(st.session_state["username"], patient_name, user_input + [parkinsons_diagnosis])
            else:
                st.error("Please fill in all fields to proceed with the prediction.")

        st.success(parkinsons_diagnosis)

    # Patient Details Page
    if selected == "Patient Details":
        st.title("Patient Details")

        # Display Diabetes Patients
        st.subheader("Diabetes Patients")
        c.execute("SELECT patient_name, diagnosis FROM diabetes_details WHERE username = ?", (st.session_state["username"],))
        diabetes_patients = c.fetchall()
        for patient in diabetes_patients:
            st.write(f"Patient Name: {patient[0]}, Diagnosis: {patient[1]}")

        # Display Heart Disease Patients
        st.subheader("Heart Disease Patients")
        c.execute("SELECT patient_name, diagnosis FROM heart_disease_details WHERE username = ?", (st.session_state["username"],))
        heart_patients = c.fetchall()
        for patient in heart_patients:
            st.write(f"Patient Name: {patient[0]}, Diagnosis: {patient[1]}")

        # Display Parkinson's Patients
        st.subheader("Parkinson's Patients")
        c.execute("SELECT patient_name, diagnosis FROM parkinsons_details WHERE username = ?", (st.session_state["username"],))
        parkinsons_patients = c.fetchall()
        for patient in parkinsons_patients:
            st.write(f"Patient Name: {patient[0]}, Diagnosis: {patient[1]}")

conn.close()

