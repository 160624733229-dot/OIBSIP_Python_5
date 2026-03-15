import streamlit as st
import string
import secrets
import pandas as pd
import pyperclip

st.set_page_config(page_title="Ultimate Password Generator", layout="centered")

st.markdown("""
<style>

.big-title{
font-size:55px;
font-weight:800;
text-align:center;
color:#4A90E2;
letter-spacing:2px;
margin-bottom:10px;
}

.sub-text{
text-align:center;
font-size:18px;
color:gray;
margin-bottom:25px;
}

.password-box{
background:#f1f3f6;
padding:15px;
border-radius:10px;
font-size:20px;
text-align:center;
margin-top:10px;
}

.stButton>button{
width:100%;
border-radius:10px;
height:45px;
font-size:16px;
}

</style>
""", unsafe_allow_html=True)

st.markdown('<div class="big-title"> ULTIMATE PASSWORD GENERATOR</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-text">Generate secure passwords instantly with customizable options</div>', unsafe_allow_html=True)

length = st.slider("Password Length", 4, 40, 12)

col1, col2, col3 = st.columns(3)

with col1:
    use_letters = st.checkbox("Letters", value=True)

with col2:
    use_numbers = st.checkbox("Numbers", value=True)

with col3:
    use_symbols = st.checkbox("Symbols", value=True)

exclude_chars = st.text_input("Exclude Characters (optional)")

num_passwords = st.slider("Number of Passwords", 1, 10, 1)

if "history" not in st.session_state:
    st.session_state.history = []

def generate_password():
    
    characters = ""
    
    if use_letters:
        characters += string.ascii_letters
        
    if use_numbers:
        characters += string.digits
        
    if use_symbols:
        characters += string.punctuation

    if exclude_chars:
        characters = ''.join(c for c in characters if c not in exclude_chars)

    if characters == "":
        return None

    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password

def check_strength(password):

    score = 0

    if len(password) >= 12:
        score += 1

    if any(c.islower() for c in password):
        score += 1

    if any(c.isupper() for c in password):
        score += 1

    if any(c.isdigit() for c in password):
        score += 1

    if any(c in string.punctuation for c in password):
        score += 1

    if score <= 2:
        return "Weak "
    elif score <= 4:
        return "Medium "
    else:
        return "Strong "

if st.button("Generate Passwords"):

    passwords = []

    for i in range(num_passwords):
        pwd = generate_password()
        if pwd:
            passwords.append(pwd)
            st.session_state.history.append(pwd)

    if passwords:

        st.success("Passwords Generated Successfully!")

        for pwd in passwords:

            st.markdown(f'<div class="password-box">{pwd}</div>', unsafe_allow_html=True)

            strength = check_strength(pwd)
            st.write("Strength:", strength)

            if st.button(f"Copy {pwd}"):
                pyperclip.copy(pwd)
                st.info("Copied to clipboard")

    else:
        st.error("Select at least one character type")

st.markdown("---")
st.subheader("Generated Password History")

if st.session_state.history:
    df = pd.DataFrame(st.session_state.history, columns=["Passwords"])
    st.dataframe(df)

    csv = df.to_csv(index=False).encode('utf-8')

    st.download_button(
        "Download Password List",
        csv,
        "passwords.csv",
        "text/csv"
    )
else:
    st.info("No passwords generated yet")

st.markdown("---")
st.subheader("Password Safety Tips")

st.write("""
• Use passwords with at least 12 characters  
• Mix letters, numbers, and symbols  
• Avoid using personal information  
• Use different passwords for each account  
• Change passwords regularly  
""")
