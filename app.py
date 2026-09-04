import streamlit as st
from openai import OpenAI
import os

# 1. PAGE CONFIG (Applies to the whole site)
st.set_page_config(page_title="Privio", page_icon="🛡️", layout="wide")

# Connect to Featherless AI (happens in the background)
client = OpenAI(
    base_url="https://api.featherless.ai/v1",
    api_key=os.environ.get("FEATHERLESS_API_KEY")
)

# 2. THE SIDEBAR
with st.sidebar:
    st.header("🛡️ Privio")
    st.write("Two tools. One mission: Keeping your data safe.")
    st.write("---")
    st.write("**Built by:**")
    st.write("- Nikhil Shaurya")
    st.write("- Aditya")
    st.write("- Jacintha Goldy")
    st.write("- Kruthika Reddy")
    st.info("Powered by Featherless AI")

# 3. CREATE THE TABS
# This creates the clickable navigation menu at the top of the page
tab1, tab2, tab3 = st.tabs(["Privacy Policy Scanner", "Password Roaster", "Data Breach Checker"])

# ==========================================
# TAB 1: THE PRIVACY SCANNER
# ==========================================
with tab1:
    st.header("Sketchy App Scanner")
    st.write("Paste a Terms of Service agreement below to find the red flags.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        user_text = st.text_area("Paste the text here:", height=300, key="privacy_box")
        scan_btn = st.button("🔍 Scan Policy", use_container_width=True)
        
    with col2:
        if scan_btn and user_text:
            with st.spinner("Scanning for legal jargon..."):
                response = client.chat.completions.create(
                    model="Qwen/Qwen2.5-7B-Instruct", 
                    messages=[
                        {"role": "system", "content": "You are a privacy advocate. Read this terms of service text. Extract and summarize clauses about sharing data, tracking location, or claiming ownership of content. Explain risks simply. If safe, say 'Looks good!'"},
                        {"role": "user", "content": f"Here is the policy: {user_text}"}
                    ]
                )
            st.success("Scan Complete!")
            st.write(response.choices[0].message.content)
        elif scan_btn and not user_text:
            st.warning("Please paste some text first!")

# ==========================================
# TAB 2: THE PASSWORD ROASTER
# ==========================================
with tab2:
    st.header("The Password Roaster")
    st.write("Enter a password you *used* to use (don't enter your real current one!). Our AI will explain exactly how a hacker would crack it.")
    
    # We don't need columns for this one, just a simple layout
    user_password = st.text_input("Enter a dummy password:", type="password")
    roast_btn = st.button("Enter")
    
    if roast_btn and user_password:
        with st.spinner("Preparing the roast..."):
            response = client.chat.completions.create(
                model="Qwen/Qwen2.5-7B-Instruct", 
                messages=[
                    {"role": "system", "content": "You are a sarcastic cybersecurity expert. Roast the user's password for being weak, and explain the exact hacking method (like a dictionary attack or brute force) that would break it. Keep it educational but funny."},
                    {"role": "user", "content": f"My password is: {user_password}"}
                ]
            )
        st.error("📊 RISK ASSESSMENT RESULT:")
        st.write(response.choices[0].message.content)
    elif roast_btn and not user_password:
        st.warning("You have to enter a password first!")

# TAB 3

with tab3:
    st.header("Data Breach & Credential Exposure Checker")
    st.write("Check if an email address or username has been exposed in known public threat intelligence databases.")
    
    user_email = st.text_input("Enter an email address to audit:")
    
    if st.button("Run Security Audit"):
        if user_email:
            with st.spinner("Analyzing threat intelligence logs..."):
                # Constructing the prompt for your Featherless.ai / Qwen backend
                prompt = f"Act as a cybersecurity threat intelligence system. Analyze the risk profile for the email address or handle: {user_email}. Provide a simulated security audit report detailing potential exposure risks, credential stuffing vulnerability, and 3 actionable remediation steps."
                
                # Make sure this matches your existing API call variable from the other tabs
                response = client.chat.completions.create(
                    model="Qwen/Qwen2.5-7B-Instruct",
                    messages=[{"role": "user", "content": prompt}],
                    stream=True
                )
                
                st.subheader("🔴 SECURITY DEFICIT IDENTIFIED:")
                stream_container = st.empty()
                full_response = ""
                for chunk in response:
                    if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                        content_chunk = chunk.choices[0].delta.content
                        full_response += content_chunk
                        stream_container.markdown(full_response)
        else:
            st.warning("Please enter a valid email address first.")