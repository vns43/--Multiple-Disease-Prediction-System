import sqlite3
import streamlit as st
from streamlit_option_menu import option_menu

# Set page configuration
st.set_page_config(
    page_title="Health Assistant",
    layout="wide",
    page_icon="🧑‍⚕️"
)

# Initialize SQLite database
conn = sqlite3.connect('health_records.db')
c = conn.cursor()

# Create users table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)''')

# Create diabetes details table if not exists
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

# Create heart disease details table if not exists
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

# Create Parkinson's disease details table if not exists
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

# Commit changes to the database
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

# Function to add Parkinson's disease details
def add_parkinsons_details(username, patient_name, details):
    try:
        c.execute('''INSERT INTO parkinsons_details (username, patient_name, fo, fhi, flo, Jitter_percent, Jitter_Abs, RAP, PPQ, DDP, Shimmer, Shimmer_dB, APQ3, APQ5, APQ, DDA, NHR, HNR, RPDE, DFA, spread1, spread2, D2, PPE, diagnosis)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                  (username, patient_name, *details))
        conn.commit()
    except Exception as e:
        st.error(f"Database insertion error: {e}")

# Function to get user details
def get_user_details(username):
    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    data = c.fetchone()
    return data

# Function to show home page
def show_home_page():
    st.title("Welcome to Health Assistant")
    st.markdown(
        """
        <style>
        body {
            background-image: url('img1.png'); /* Replace with your image path */
            background-size: cover;
            background-repeat: no-repeat;
            height: 100vh;
        }
        </style>
        """, unsafe_allow_html=True)
    st.write("Please use the options in the sidebar to navigate through the app.")



# Function to show login page
def show_login_page():
    st.title("Login")
    st.markdown(
        """
        <style>
        body {
            background-image: url("img2.png");
            background-size: cover;
        }
        </style>
        """, unsafe_allow_html=True)
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = login_user(username, password)
        if user:
            st.session_state["user"] = username
            st.success("Logged in successfully")
        else:
            st.error("Invalid username or password")

# Function to show sign-up page
def show_signup_page():
    st.title("Sign Up")
    st.markdown(
        """
        <style>
        body {
            background-image: url("img3.png");
            background-size: cover;
        }
        </style>
        """, unsafe_allow_html=True)
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Sign Up"):
        add_user(username, password)
        st.success("Account created successfully")

# Function to show contact page
# Function to show contact page
def show_contact_page():
    st.title("Contact Us")
    st.write("""
    ## Contact Information
    If you have any questions, feedback, or inquiries, please don't hesitate to contact us. We're here to help!
    
    ### General Inquiries
    For general inquiries or support related to Health Assistant, you can reach us at:
    
    - **Email:** vallepunarayanaswamy27@gmail.com
    
    ### Technical Support
    Need technical assistance or facing issues with the app? Our technical support team is available to assist you:
    
    - **Email:** techsupport@healthassistant.com
    
    ### Business Partnerships
    Interested in partnering with Health Assistant or exploring business opportunities? Contact our partnerships team:
    
    - **Email:** partnerships@healthassistant.com
    
    ### Customer Support
    For customer support related to your account, billing inquiries, or any other customer-related matters, please contact:
    
    - **Email:** customersupport@healthassistant.com
    
    ### Feedback
    Your feedback is valuable to us! We welcome any suggestions or comments to help us improve Health Assistant:
    
    - **Email:** feedback@healthassistant.com
    
    ### Social Media
    Connect with us on social media to stay updated with the latest news, tips, and features of Health Assistant:
    
    - **Facebook:** [Health Assistant Facebook Page](https://www.facebook.com/healthassistant)
    - **Twitter:** [@HealthAssistant](https://twitter.com/healthassistant)
    - **LinkedIn:** [Health Assistant LinkedIn Page](https://www.linkedin.com/company/healthassistant)
    
    We look forward to hearing from you and providing you with excellent service and support!
    """)


# Function to show about us page
# Function to show about us page
def show_about_page():
    st.title("About Us")
    st.write("""
    ## Welcome to Health Assistant
    Health Assistant is a comprehensive health management application designed to assist individuals and healthcare providers in managing health records and diagnosing various diseases. Our mission is to leverage technology to improve health outcomes and make healthcare more accessible and efficient.

    ### Our Features
    - **User-Friendly Interface:** Easy to navigate and use, ensuring a seamless experience for users of all ages.
    - **Health Records Management:** Securely store and manage health records, making it easier for users to keep track of their medical history.
    - **Disease Prediction:** Utilize advanced algorithms to predict the likelihood of diabetes, heart disease, and Parkinson's disease based on user input.
    - **Data Privacy:** We prioritize your privacy and ensure that all your health data is stored securely and confidentially.

    ### Our Mission
    Our mission is to empower individuals to take control of their health by providing them with the tools and information they need to make informed decisions. We believe in the power of technology to transform healthcare and are committed to continuous improvement and innovation.

    ### Our Team
    Our team consists of experienced healthcare professionals, data scientists, and software developers who are passionate about improving health outcomes. We work together to ensure that Health Assistant is always at the cutting edge of healthcare technology.

    ### Contact Us
    If you have any questions or need support, feel free to reach out to us at vallepunarayanaswamy27@gmail.com. We are here to help!

    Thank you for choosing Health Assistant. We are dedicated to helping you achieve better health and wellness.
    """)


# Function to show diabetes prediction page
def show_diabetes_prediction_page():
    if "user" not in st.session_state:
        st.warning("Please log in to use this feature.")
        return
    st.title("Diabetes Prediction")
    patient_name = st.text_input("Patient Name")
    Pregnancies = st.number_input("Pregnancies")
    Glucose = st.number_input("Glucose")
    BloodPressure = st.number_input("Blood Pressure")
    SkinThickness = st.number_input("Skin Thickness")
    Insulin = st.number_input("Insulin")
    BMI = st.number_input("BMI")
    DiabetesPedigreeFunction = st.number_input("Diabetes Pedigree Function")
    Age = st.number_input("Age")
    if st.button("Predict"):
        details = [Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]
        # Add prediction logic here
        diagnosis = "Positive" if Glucose > 140 else "Negative"  # Example logic
        add_diabetes_details(st.session_state["user"], patient_name, details + [diagnosis])
        st.success(f"Diagnosis: {diagnosis}")

# Function to show heart disease prediction page
def show_heart_disease_prediction_page():
    if "user" not in st.session_state:
        st.warning("Please log in to use this feature.")
        return
    st.title("Heart Disease Prediction")
    patient_name = st.text_input("Patient Name")
    age = st.number_input("Age")
    sex = st.selectbox("Sex", [0, 1])
    cp = st.number_input("CP")
    trestbps = st.number_input("Trestbps")
    chol = st.number_input("Chol")
    fbs = st.number_input("FBS")
    restecg = st.number_input("Restecg")
    thalach = st.number_input("Thalach")
    exang = st.selectbox("Exang", [0, 1])
    oldpeak = st.number_input("Oldpeak")
    slope = st.number_input("Slope")
    ca = st.number_input("CA")
    thal = st.number_input("Thal")
    if st.button("Predict"):
        details = [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]
        # Add prediction logic here
        diagnosis = "Positive" if thalach < 150 else "Negative"  # Example logic
        add_heart_disease_details(st.session_state["user"], patient_name, details + [diagnosis])
        st.success(f"Diagnosis: {diagnosis}")

# Function to show Parkinson's prediction page
def show_parkinsons_prediction_page():
    if "user" not in st.session_state:
        st.warning("Please log in to use this feature.")
        return
    st.title("Parkinson's Prediction")
    patient_name = st.text_input("Patient Name")
    fo = st.number_input("Fo")
    fhi = st.number_input("Fhi")
    flo = st.number_input("Flo")
    Jitter_percent = st.number_input("Jitter_percent")
    Jitter_Abs = st.number_input("Jitter_Abs")
    RAP = st.number_input("RAP")
    PPQ = st.number_input("PPQ")
    DDP = st.number_input("DDP")
    Shimmer = st.number_input("Shimmer")
    Shimmer_dB = st.number_input("Shimmer_dB")
    APQ3 = st.number_input("APQ3")
    APQ5 = st.number_input("APQ5")
    APQ = st.number_input("APQ")
    DDA = st.number_input("DDA")
    NHR = st.number_input("NHR")
    HNR = st.number_input("HNR")
    RPDE = st.number_input("RPDE")
    DFA = st.number_input("DFA")
    spread1 = st.number_input("Spread1")
    spread2 = st.number_input("Spread2")
    D2 = st.number_input("D2")
    PPE = st.number_input("PPE")
    if st.button("Predict"):
        details = [fo, fhi, flo, Jitter_percent, Jitter_Abs, RAP, PPQ, DDP, Shimmer, Shimmer_dB, APQ3, APQ5, APQ, DDA, NHR, HNR, RPDE, DFA, spread1, spread2, D2, PPE]
        
        if len(details) != 22:
            st.error("Error: Mismatch in the number of features. Please check the inputs.")
            return
        
        # Add prediction logic here
        diagnosis = "Positive" if HNR < 20 else "Negative"  # Example logic
        
        try:
            add_parkinsons_details(st.session_state["user"], patient_name, details + [diagnosis])
            st.success(f"Diagnosis: {diagnosis}")
        except Exception as e:
            st.error(f"Error: {e}")

# Sidebar navigation
with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["Home", "Login", "Sign Up", "Diabetes Prediction", "Heart Disease Prediction", "Parkinson's Prediction", "Contact", "About Us"],
        icons=["house", "box-arrow-in-right", "person-plus", "activity", "heart", "soundwave", "envelope", "info-circle"],
        menu_icon="cast",
        default_index=0,
    )

# Navigation options
if selected == "Home":
    show_home_page()
elif selected == "Login":
    show_login_page()
elif selected == "Sign Up":
    show_signup_page()
elif selected == "Diabetes Prediction":
    show_diabetes_prediction_page()
elif selected == "Heart Disease Prediction":
    show_heart_disease_prediction_page()
elif selected == "Parkinson's Prediction":
    show_parkinsons_prediction_page()
elif selected == "Contact":
    show_contact_page()
elif selected == "About Us":
    show_about_page()

