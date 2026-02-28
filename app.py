from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# 🔹 Load API Key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# 🔹 Gemini Response Function
def get_gemini_response(input_text, uploaded_file, prompt):

    model = genai.GenerativeModel("gemini-1.5-flash")

    image_bytes = uploaded_file.getvalue()

    response = model.generate_content([
        input_text,
        {
            "mime_type": uploaded_file.type,
            "data": image_bytes
        },
        prompt
    ])

    return response.text

# 🔹 PROMPT
input_prompt = """
You are a civil engineer. Please describe the structure in the image and provide details such as:

1. Type of structure
2. Materials used
3. Estimated dimensions
4. Construction methods
5. Notable features
6. Engineering challenges
"""

# 🔹 Streamlit UI
st.set_page_config(page_title="Civil Engineering Insight Studio", page_icon="🏗️")
st.header("Civil Engineering Insight Studio")

input_text = st.text_input("Input Prompt:")

uploaded_file = st.file_uploader(
    "Upload an image...",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image")

submit = st.button("Describe Structure")

if submit:
    if uploaded_file is None:
        st.warning("Please upload an image first.")
    else:
        try:
            response = get_gemini_response(input_text, uploaded_file, input_prompt)

            st.subheader("Description:")
            st.write(response)

        except Exception as e:
            st.error(f"Error: {str(e)}")