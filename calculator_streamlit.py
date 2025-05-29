import streamlit as st
import math

def calculate(expression):
    try:
        # Replace ^ with ** for power operation
        expression = expression.replace('^', '**')
        result = eval(expression)
        # Format number to remove trailing zeros after decimal
        if isinstance(result, float):
            str_num = f"{result:.10f}".rstrip('0')
            if str_num.endswith('.'):
                str_num = str_num[:-1]
            return str_num
        return str(result)
    except ZeroDivisionError:
        return "Cannot divide by zero"
    except Exception as e:
        return "Error"

def main():
    st.set_page_config(
        page_title="Modern Calculator",
        layout="centered",
        initial_sidebar_state="collapsed",
    )

    # Custom CSS for styling
    st.markdown("""
        <style>
        .stButton > button {
            width: 100%;
            height: 50px;
            font-size: 20px;
            font-weight: bold;
            margin: 2px;
        }
        .calculator-display {
            background-color: #2D2D2D;
            color: white;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 10px;
            text-align: right;
            font-family: monospace;
            font-size: 24px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Initialize session state if not exists
    if 'expression' not in st.session_state:
        st.session_state.expression = ""
    if 'result' not in st.session_state:
        st.session_state.result = "0"

    # Calculator title
    st.title("Modern Calculator")

    # Display expression and result
    st.markdown(f'<div class="calculator-display">{st.session_state.expression}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="calculator-display">{st.session_state.result}</div>', unsafe_allow_html=True)

    # Calculator buttons layout
    col1, col2, col3, col4 = st.columns(4)

    # Row 1
    if col1.button("C"):
        st.session_state.expression = ""
        st.session_state.result = "0"
        st.rerun()
    if col2.button("←"):
        st.session_state.expression = st.session_state.expression[:-1]
        if st.session_state.expression:
            st.session_state.result = calculate(st.session_state.expression)
        else:
            st.session_state.result = "0"
        st.rerun()
    if col3.button("^"):
        st.session_state.expression += "^"
        st.rerun()
    if col4.button("/"):
        st.session_state.expression += "/"
        st.rerun()

    # Row 2
    if col1.button("7"):
        st.session_state.expression += "7"
        st.session_state.result = calculate(st.session_state.expression)
        st.rerun()
    if col2.button("8"):
        st.session_state.expression += "8"
        st.session_state.result = calculate(st.session_state.expression)
        st.rerun()
    if col3.button("9"):
        st.session_state.expression += "9"
        st.session_state.result = calculate(st.session_state.expression)
        st.rerun()
    if col4.button("*"):
        st.session_state.expression += "*"
        st.rerun()

    # Row 3
    if col1.button("4"):
        st.session_state.expression += "4"
        st.session_state.result = calculate(st.session_state.expression)
        st.rerun()
    if col2.button("5"):
        st.session_state.expression += "5"
        st.session_state.result = calculate(st.session_state.expression)
        st.rerun()
    if col3.button("6"):
        st.session_state.expression += "6"
        st.session_state.result = calculate(st.session_state.expression)
        st.rerun()
    if col4.button("-"):
        st.session_state.expression += "-"
        st.rerun()

    # Row 4
    if col1.button("1"):
        st.session_state.expression += "1"
        st.session_state.result = calculate(st.session_state.expression)
        st.rerun()
    if col2.button("2"):
        st.session_state.expression += "2"
        st.session_state.result = calculate(st.session_state.expression)
        st.rerun()
    if col3.button("3"):
        st.session_state.expression += "3"
        st.session_state.result = calculate(st.session_state.expression)
        st.rerun()
    if col4.button("+"):
        st.session_state.expression += "+"
        st.rerun()

    # Row 5
    if col1.button("0"):
        st.session_state.expression += "0"
        st.session_state.result = calculate(st.session_state.expression)
        st.rerun()
    if col2.button("."):
        st.session_state.expression += "."
        st.rerun()
    # Combine columns 3 and 4 for the equals button
    col3_4 = st.columns([1, 1])[0]
    if col3_4.button("=", use_container_width=True):
        if st.session_state.expression:
            st.session_state.result = calculate(st.session_state.expression)
            st.session_state.expression = ""
            st.rerun()

if __name__ == "__main__":
    main() 