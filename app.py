import streamlit as st
import hr
import candidate

# ✅ Ensure `set_page_config` is the first command
st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

# ✅ Use session state to track the selected role
if "selected_role" not in st.session_state:
    st.session_state.selected_role = None  # Default: No selection

def main():
    # If no role is selected, show role selection page
    if st.session_state.selected_role is None:
        st.title("AI-Based Resume Analyzer")
        st.write("Select your role to proceed:")

        # ✅ Buttons for role selection
        col1, col2 = st.columns(2)
        with col1:
            if st.button("HR", use_container_width=True):
                st.session_state.selected_role = "HR"
                st.rerun()

        with col2:
            if st.button("Candidate", use_container_width=True):
                st.session_state.selected_role = "Candidate"
                st.rerun()

    # ✅ Load the appropriate UI based on user selection
    elif st.session_state.selected_role == "HR":
        hr.show_hr_ui()
    elif st.session_state.selected_role == "Candidate":
        candidate.show_candidate_ui()

if __name__ == "__main__":
    main()
