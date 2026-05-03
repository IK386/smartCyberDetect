import streamlit as st

st.set_page_config(page_title="Request Demo", page_icon="📩")

st.title("📩 Request a Product Demo")
st.write("Fill out the form below to schedule a live demo with our team.")

with st.form("demo_form"):
    full_name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    company = st.text_input("Organization / University")
    details = st.text_area("Additional Details (Optional)")
    
    submit_button = st.form_submit_button("Submit Request")

if submit_button:
    if full_name and email:
        st.success(f"Thank you {full_name}! Your request has been sent.")
    else:
        st.error("Please fill in the required fields.")