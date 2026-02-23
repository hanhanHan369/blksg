import streamlit as st
import streamlit.components.v1 as components
import os
import mysql.connector
import streamlit as st

# Function to establish a database connection
def init_connection():
    return mysql.connector.connect(
        host=st.secrets["mysql"]["host"],
        user=st.secrets["mysql"]["user"],
        password=st.secrets["mysql"]["password"],
        database=st.secrets["mysql"]["database"]
    )

conn = init_connection()

# Function to save a new entry
def save_entry(title, description, category, image_path):
    cursor = conn.cursor()
    query = """
    INSERT INTO portfolio_entries (user_id, title, description, category, image_path) 
    VALUES (%s, %s, %s, %s, %s)
    """
    # Using a placeholder 'user123' until you implement a login system
    cursor.execute(query, ('user123', title, description, category, image_path))
    conn.commit()
    cursor.close()

# Function to fetch all entries for the dashboard
def get_entries():
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM portfolio_entries ORDER BY created_at DESC")
    result = cursor.fetchall()
    cursor.close()
    return result
# 1. Setup the Page Layout
st.set_page_config(page_title="Barrio Conecta", layout="wide")

# Force the app to use every pixel of the screen width
st.markdown("""
    <style>
        .block-container {
            padding-top: 0rem;
            padding-bottom: 0rem;
            padding-left: 0rem;
            padding-right: 0rem;
        }
        iframe {
            width: 100%;
            border: none;
        }
    </style>
    """, unsafe_allow_html=True)

# 2. CREATE THE BUTTONS (Sidebar Navigation)
# This creates a menu on the left that acts as your buttons
st.sidebar.title("Town Directory Menu")
choice = st.sidebar.radio("Navigate to:", ["🏠 Home Page", "📊 My Portfolio", "📤 Upload Manager"])

# 3. Helper Function to Read and Display your HTML
def show_html_page(file_name):
    if os.path.exists(file_name):
        with open(file_name, 'r', encoding='utf-8') as f:
            html_code = f.read()
        
        # This is the "Portal" that displays your HTML
        # height=1000 ensures you can see the whole page
        components.html(html_code, height=1000, scrolling=True)
    else:
        st.error(f"❌ File Not Found: I couldn't find '{file_name}' in the folder.")
        st.info(f"Current Directory: {os.getcwd()}")
        st.write("Current files in folder:", os.listdir("."))

# 4. ROUTING LOGIC (The "Brain" of your app)
if choice == "🏠 Home Page":
    st.write("### Viewing: Community Home")
    show_html_page("index.html")

elif choice == "📊 My Portfolio":
    st.write("### Viewing: User Portfolio")
    show_html_page("dashboard.html")

elif choice == "📤 Upload Manager":
    st.title("🧡 Portfolio Manager")
    # This is the Streamlit part for uploading photos
    with st.form("upload_form"):
        title = st.text_input("Work Experience Title")
        img = st.file_uploader("Upload Image", type=["jpg", "png"])
        submit = st.form_submit_button("Save to Portfolio")
        if submit:
            st.success("Successfully saved! (Note: It won't show in dashboard.html yet without an API connection)")
