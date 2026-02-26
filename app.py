import streamlit as st
from medicine_engine import MedicineEngine
from risk_engine import RiskEngine
from llm_engine import LLMEngine

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="MedSafe AI 2.0", layout="wide")

# ---------------- SIMPLE DARK THEME ----------------
st.markdown("""
<style>
.stApp {
    background-color: #0f172a;
    color: white;
}

section[data-testid="stSidebar"] {
    background-color: #111827;
}

.stButton>button {
    border-radius: 10px;
    font-weight: 600;
}

[data-testid="stChatMessage"] {
    border-radius: 12px;
    padding: 10px;
}

h1, h2, h3 {
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

# ---------------- INITIALIZE ENGINES ----------------
medicine_engine = MedicineEngine()
risk_engine = RiskEngine()
llm_engine = LLMEngine()

# ---------------- TITLE ----------------
st.title("🏥 MedSafe AI 2.0")
st.markdown("AI-Powered Medicine Safety & Symptom Awareness Assistant")

# ---------------- SIDEBAR ----------------
st.sidebar.header("User Health Profile")
age = st.sidebar.number_input("Age", min_value=0, max_value=120, value=25)
gender = st.sidebar.selectbox("Gender", ["Male", "Female", "Other"])

# ---------------- TABS ----------------
tabs = st.tabs(["💊 Medicine Checker", "💬 AI Health Assistant"])

# =====================================================
# ================= MEDICINE CHECKER ==================
# =====================================================
with tabs[0]:

    st.subheader("Medicine Interaction Checker")

    meds_input = st.text_input("Enter medicines separated by comma")

    if st.button("Check Interactions"):

        med_list_raw = meds_input.split(",")
        matched_meds = []

        for med in med_list_raw:
            match = medicine_engine.match_medicine(med.strip())
            if match:
                matched_meds.append(match)

        st.write("Matched Medicines:", matched_meds)

        interactions = medicine_engine.check_interactions(matched_meds)

        if interactions:

            for interaction in interactions:

                risk_level = interaction["risk"].lower()

                if risk_level == "high":
                    st.error(
                        f"🚨 HIGH RISK: {interaction['medicine_1']} + "
                        f"{interaction['medicine_2']}"
                    )
                elif risk_level == "medium":
                    st.warning(
                        f"⚠ MEDIUM RISK: {interaction['medicine_1']} + "
                        f"{interaction['medicine_2']}"
                    )
                else:
                    st.info(
                        f"ℹ LOW RISK: {interaction['medicine_1']} + "
                        f"{interaction['medicine_2']}"
                    )

                # AI explanation for interaction
                with st.spinner("Generating AI explanation..."):
                    explanation = llm_engine.generate_response(
                        f"""
Explain the interaction between {interaction['medicine_1']}
and {interaction['medicine_2']}.
Include:
- Why the interaction occurs
- What the risk level means
- Precautions a patient should take
Keep it educational and non-diagnostic.
"""
                    )

                st.markdown(explanation)

        else:
            st.success("✅ No known interactions found.")

# =====================================================
# ================= CHAT ASSISTANT ====================
# =====================================================
with tabs[1]:

    st.subheader("💬 MedSafe AI Assistant")

    # Clear chat button
    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User chat input
    if prompt := st.chat_input("Describe your symptoms or ask a health question..."):

        # Store user message
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        # Risk assessment
        risk_result = risk_engine.assess_risk(prompt)

        with st.chat_message("assistant"):

            # Risk alert
            if risk_result["level"] == "HIGH":
                st.error("🚨 HIGH RISK DETECTED")
            elif risk_result["level"] == "MEDIUM":
                st.warning("⚠ MEDIUM RISK")
            else:
                st.success("✅ LOW RISK")

            st.progress(risk_result["score"])

            # AI response
            with st.spinner("Analyzing with AI..."):
                ai_response = llm_engine.generate_response(
                    f"Age: {age}, Gender: {gender}, User Input: {prompt}"
                )

            st.markdown(ai_response)

        # Save assistant response
        st.session_state.messages.append(
            {"role": "assistant", "content": ai_response}
        )

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("⚠ MedSafe AI is for educational purposes only and does not replace professional medical advice.")