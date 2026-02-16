import streamlit as st
import os
import json
from datetime import datetime

# Setup
st.set_page_config(page_title="Barrio Conecta Admin", page_icon="🧡")
UPLOAD_DIR = "assets/uploads"
DATA_FILE = "portfolio_data.json"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

st.title("🧡 Barrio Conecta: Portfolio Manager")
st.write("Upload your contributions to the town directory.")

# Form to add a new contribution
with st.form("contribution_form"):
    title = st.text_input("Project Title (e.g., Urban Gardening)")
    description = st.text_area("What did you achieve?")
    category = st.selectbox("Category", ["Hogar", "Tecnología", "Cuidados", "Enseñanza"])
    uploaded_file = st.file_uploader("Upload a photo of your work", type=['png', 'jpg', 'jpeg'])
    
    submit = st.form_submit_button("Add to Portfolio")

if submit and uploaded_file:
    # Save the image
    file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Save the metadata (This acts like your "API Database")
    new_entry = {
        "title": title,
        "description": description,
        "category": category,
        "image": file_path,
        "date": datetime.now().strftime("%Y-%m-%d")
    }
    
    st.success(f"Successfully added '{title}' to your portfolio!")
    st.json(new_entry) # This shows you what the "API" would send back