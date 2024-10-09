import streamlit as st
import requests
import json

# Streamlit App Title
st.title("Keigo Analyzer")

# Description
st.write("""
### Analyze Your Japanese Text for Keigo Usage
Enter your Japanese text below, and the application will analyze your use of keigo (honorific language).
""")

# Input Text Area
user_input = st.text_area(
    "Enter your Japanese text:",
    value="私は、問題解決力とコミュニケーション能力を活かせると考えています。学生時代にチームで課題に取り組む際、問題点を見つけて解決策を提案することで、チーム全体をまとめることができました。",
    height=150
)


# Submit Button
if st.button("Analyze"):
    api_url = st.secrets["KEIGO_ANALYSIS_ENDPOINT"]
    # st.
    if not api_url:
        st.error("Please provide a valid API endpoint URL.")
    elif not user_input.strip():
        st.error("Please enter some text to analyze.")
    else:
        with st.spinner("Analyzing..."):
            try:
                data = {"answer": user_input}
                headers = {"Content-Type": "application/json"}
                response = requests.post(api_url, json=data, headers=headers)

                if response.status_code == 200:
                    # Parse the nested JSON string
                    response_json_str = response.json().get("response", "{}")
                    response_data = json.loads(response_json_str)

                    # Display Analysis Results
                    st.success("Analysis Successful!")

                    # Contextual Validity
                    st.subheader("Contextual Validity of Keigo")
                    st.write(f"**Valid:** {response_data.get('contextual_validity_of_keigo', 'N/A')}")
                    st.write(f"**Analysis:** {response_data.get('contextual_analysis_of_keigo', 'N/A')}")

                    # Keigo Counts
                    st.subheader("Keigo Counts")
                    keigo_counts = response_data.get("keigo_count", {})
                    st.write(f"**Teineigo (Polite):** {keigo_counts.get('teineigo', 0)}")
                    st.write(f"**Sonkeigo (Respectful):** {keigo_counts.get('sonkeigo', 0)}")
                    st.write(f"**Kenjougo (Humble):** {keigo_counts.get('kenjougo', 0)}")

                    # Keigo Analysis
                    st.subheader("Keigo Analysis")
                    st.write(response_data.get("keigo_analysis", "N/A"))

                    # Proficiency Level
                    st.subheader("Proficiency Level")
                    st.write(f"**Level:** {response_data.get('proficiency_level', 'N/A')}")

                    # Improvement Tips
                    st.subheader("Improvement Tips")
                    improvement_tips = response_data.get("improvement_tips", [])
                    if improvement_tips:
                        for idx, tip in enumerate(improvement_tips, 1):
                            st.write(f"{idx}. {tip}")
                    else:
                        st.write("No improvement tips available.")

                else:
                    st.error(f"Failed to analyze text. Status Code: {response.status_code}")
                    st.text(response.text)

            except requests.exceptions.RequestException as e:
                st.error(f"An error occurred: {e}")
            except json.JSONDecodeError:
                st.error("Failed to parse the response from the server.")

# Optional: Display the original response JSON for debugging
with st.expander("View Raw Response"):
    try:
        raw_response = response.json()
        st.json(raw_response)
    except:
        st.write("No response to display.")

