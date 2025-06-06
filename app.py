import streamlit as st
from PIL import Image
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key="AIzaSyAJxR45NmBK1rs4n8LBi5AEQef1_YZt3Es")
model = genai.GenerativeModel(model_name="gemini-1.5-pro")

# Page Configuration
st.set_page_config(
    page_title="Tomato Leaf Disease Detection",
    page_icon="🍅",
    layout="wide"
)

# Custom Styling
st.markdown(
    """
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f0f4f8;
        }
        .title {
            text-align: center;
            color: #E63946;
            font-size: 3em;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .subheader {
            text-align: center;
            color: #457B9D;
            font-size: 1.4em;
            margin-bottom: 30px;
        }
        .section {
            padding: 20px;
            background: linear-gradient(135deg, #FFFFFF, #F1FAEE);
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
        .section h3 {
            color: #1D3557;
        }
        .analyze-btn {
            background-color: #E63946;
            color: white;
            padding: 12px 24px;
            font-size: 18px;
            font-weight: bold;
            border-radius: 8px;
            border: none;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .analyze-btn:hover {
            background-color: #457B9D;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Page Title
st.markdown("<div class='title'>Tomato Leaf Disease Detection</div>", unsafe_allow_html=True)
st.markdown("<div class='subheader'>Upload an image of a tomato leaf and analyze its condition using AI.</div>", unsafe_allow_html=True)

# Image Upload Section
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.subheader("📤 Upload an Image")
uploaded_image = st.file_uploader(
    "Choose an image file (e.g., .jpg, .jpeg, .png)",
    type=["jpg", "jpeg", "png"],
    help="Upload a clear image of a tomato leaf."
)
st.markdown("</div>", unsafe_allow_html=True)

# Text Input Section for Custom Prompt
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.subheader("💬 Enter Your Question or Prompt")
custom_prompt = st.text_area(
    "Enter a custom prompt related to the uploaded image",
    placeholder="E.g., 'Identify the disease and suggest remedies.'",
    help="Type your specific question or let the app analyze the image automatically."
)
st.markdown("</div>", unsafe_allow_html=True)

# Analyze Button and Logic
if uploaded_image:
    # Open the uploaded image
    image = Image.open(uploaded_image)

    # Display the uploaded image with a fixed width
    st.image(image, caption="Uploaded Image", width=400)

    # Process the image and prompt when the user clicks the button
    if st.button("Analyze Image", key="analyze_btn"):
        try:
            # Default prompt if no custom prompt is provided
            if not custom_prompt.strip():
                custom_prompt = (
                            "Analyze the uploaded image of a tomato leaf to determine the disease it is affected by. "
                        "The possible classes include: Late Blight, Healthy, Early Blight, Septoria Leaf Spot, Tomato Yellow Leaf Curl Virus, "
        "Bacterial Spot, Target Spot, Tomato Mosaic Virus, Leaf Mold, Spider Mites (Two-Spotted Spider Mite), and Powdery Mildew. "
        "For the identified disease, provide a detailed description, the symptoms observed, and cost-effective remedies or treatments. "
        "If the leaf is healthy, confirm that no disease is detected."
                )

            # Generate response using AI
            response = model.generate_content(
                [custom_prompt, image],
                generation_config=genai.GenerationConfig(
                    max_output_tokens=1000,
                    temperature=0.7,
                ),
            )

            # Display the AI response
            st.markdown("<h3 style='color: #4CAF50;'>AI Analysis Result</h3>", unsafe_allow_html=True)
            st.write(response.text)
        except Exception as e:
            st.error(f"An error occurred during analysis: {str(e)}")
else:
    st.info("Please upload an image to start the analysis.")