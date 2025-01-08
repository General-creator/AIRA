import streamlit as st
import matplotlib.pyplot as plt

# Define the questions
questions = [
    "How well-defined are your data governance policies and procedures?",
    "How would you rate the overall quality and accuracy of your data?",
    "To what extent is data integrated across various departments and systems?",
    "How robust are your data security measures to protect sensitive information?",
    "How compliant are you with data privacy regulations (e.g., GDPR, HIPAA)?",
    "How advanced are your data analytics capabilities (e.g., descriptive, predictive, prescriptive)?",
    "How easily can employees access the data they need for their roles?",
    "To what extent is a data-driven culture fostered within your organization?",
    "How well-trained are your employees in data-related skills and tools?",
    "How aligned is your data strategy with your overall business strategy?"
]

# Initialize session state variables
if "page" not in st.session_state:
    st.session_state.page = "survey"
if "scores" not in st.session_state:
    st.session_state.scores = []

# Function to calculate the final score
def calculate_score(scores):
    weighted_scores = [score * 2 for score in scores]  # Convert 1-5 to 2-10
    final_score = sum(weighted_scores)
    percentage = (final_score / 100) * 100  # Convert to percentage
    return percentage, weighted_scores

# Survey Page
if st.session_state.page == "survey":
    st.title("AI Maturity Assessment Tool")
    st.write("Rate your organization on the following dimensions of data maturity. Each question is rated on a scale of 1 to 5.")

    scores = []
    for i, question in enumerate(questions):
        score = st.slider(question, min_value=1, max_value=5, step=1, key=f"q{i}")
        scores.append(score)

    if st.button("Submit"):
        st.session_state.scores = scores
        st.session_state.page = "results"
        st.rerun()  # Updated from st.experimental_rerun

# Results Page
elif st.session_state.page == "results":
    st.title("Your AI Maturity Score")

    # Calculate and display the score
    scores = st.session_state.scores
    percentage, weighted_scores = calculate_score(scores)

    st.write(f"**Your AI Maturity Score: {percentage:.2f}%**")

    # Display feedback
    if percentage < 25:
        st.error("We've noticed some crucial gaps in your data maturity, including undefined governance, poor quality and integration, and weak security measures. These could significantly impact your operations.")
    elif 25 <= percentage <= 50:
        st.warning("Your data maturity shows promise but has room for enhancement in governance, quality, and security measures. Valkyrie specializes in optimizing these aspects.")
    elif 50 < percentage <= 75:
        st.success("Your data maturity stands at a commendable level with defined governance, good quality, and strong security.")
    else:
        st.success("Your high data maturity score is commendable, showcasing excellent governance, top-notch quality, and robust security.")

    # Radar Chart Visualization
    st.subheader("Data Maturity Radar Chart")
    labels = [
        "Governance", "Quality", "Integration", "Security", "Privacy",
        "Analytics", "Accessibility", "Culture", "Training", "Strategy"
    ]

    angles = [n / float(len(labels)) * 2 * 3.14159 for n in range(len(labels))]
    angles += angles[:1]  # Close the circle

    values = weighted_scores + weighted_scores[:1]  # Close the circle

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.fill(angles, values, color='blue', alpha=0.25)
    ax.plot(angles, values, color='blue', linewidth=2)
    ax.set_yticks([2, 4, 6, 8, 10])
    ax.set_yticklabels(["2", "4", "6", "8", "10"], color="grey", size=7)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, size=9)
    st.pyplot(fig)

    # Next Steps Call-to-Action
    st.subheader("Next Steps")
    st.write("Based on your score, we recommend scheduling a consultation with Valkyrie to discuss how we can enhance your AI maturity.")
    if st.button("Contact Us"):
        st.write("Thank you! We'll reach out to you shortly.")

    # Option to retake the survey
    if st.button("Retake Survey"):
        st.session_state.page = "survey"
        st.experimental_rerun()
