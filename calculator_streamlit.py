import streamlit as st
import math

# Set page configuration
st.set_page_config(
    page_title="Modern Calculator",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS styling
st.markdown("""
<style>
    .calculator-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 20px;
        background: linear-gradient(145deg, #f0f0f0, #ffffff);
        border-radius: 15px;
        box-shadow: 20px 20px 60px #bebebe, -20px -20px 60px #ffffff;
    }
    .stButton > button {
        width: 100%;
        height: 60px;
        background: linear-gradient(145deg, #f0f0f0, #ffffff);
        border: none;
        border-radius: 10px;
        color: #333;
        font-size: 20px;
        font-weight: bold;
        margin: 5px 0;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    .calculator-display {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        text-align: right;
        font-size: 36px;
        font-family: 'Arial', sans-serif;
        box-shadow: inset 0 2px 5px rgba(0,0,0,0.1);
    }
    .title {
        text-align: center;
        color: #333;
        font-family: 'Arial', sans-serif;
        margin-bottom: 30px;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.title("Modern Calculator")
    
    # Initialize session state for calculator display
    if "display" not in st.session_state:
        st.session_state.display = "0"
    
    # Display the current value
    display = st.text_input("", value=st.session_state.display, key="display_input")
    
    # Create button columns
    col1, col2, col3, col4 = st.columns(4)
    
    # Row 1
    if col1.button("7"):
        update_display("7")
    if col2.button("8"):
        update_display("8")
    if col3.button("9"):
        update_display("9")
    if col4.button("/"):
        update_display("/")
    
    # Row 2
    if col1.button("4"):
        update_display("4")
    if col2.button("5"):
        update_display("5")
    if col3.button("6"):
        update_display("6")
    if col4.button("*"):
        update_display("*")
    
    # Row 3
    if col1.button("1"):
        update_display("1")
    if col2.button("2"):
        update_display("2")
    if col3.button("3"):
        update_display("3")
    if col4.button("-"):
        update_display("-")
    
    # Row 4
    if col1.button("0"):
        update_display("0")
    if col2.button("."):
        update_display(".")
    if col3.button("="):
        calculate()
    if col4.button("+"):
        update_display("+")
    
    # Row 5
    if col1.button("C"):
        clear_display()
    if col2.button("←"):
        backspace()

def update_display(value):
    if st.session_state.display == "0":
        st.session_state.display = value
    else:
        st.session_state.display += value

def clear_display():
    st.session_state.display = "0"

def backspace():
    st.session_state.display = st.session_state.display[:-1] if len(st.session_state.display) > 1 else "0"

def calculate():
    try:
        st.session_state.display = str(eval(st.session_state.display))
    except:
        st.session_state.display = "Error"

if __name__ == "__main__":
    main() 