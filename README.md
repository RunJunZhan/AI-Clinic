# AI-Powered Smart Home Medical Integration Platform

An intelligent, real-time computer vision and LLM-integrated application designed for home rehabilitation tracking and medical image analysis. 

## Key Features

* **Real-time Pose Tracking & State Machine:** Engineered a robust counting system using OpenCV and MediaPipe. Implemented a **State Machine** algorithm to classify complex movements (e.g., Squats, Bicep Curls) based on joint angles, providing zero-latency visual feedback and preventing false triggers.
* **LLM Medical Image Analysis:** Integrated the **Gemini 2.5 Flash API** to process static medical images (e.g., X-rays, skin conditions). The system automatically generates preliminary medical records, structural analysis, and health education advice.

## Project Structure

* app.py: Main Streamlit application and UI routing.
* pose_estimation.py: Core computer vision algorithms, MediaPipe processing, and State Machine logic.
* gemini_api.py: Encapsulated module for interacting with the Google Gemini API.

## Demo
| Rehabilitation Tracking (State Machine) | AI Medical Image Analysis |
| :---: | :---: |
| <img src="link_to_your_squat_gif_or_image" width="400"> | <img src="link_to_your_llm_analysis_image" width="400"> |

## Quick Start

Follow these steps to run the application on your local machine:

**1. Clone the repository**
```bash
git clone [https://github.com/RunJunZhan/your-repo-name.git](https://github.com/RunJunZhan/AI-Clinic.git)
cd AI-Clinic
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Set up Environment Variables**
Create a .env file in the root directory and add your Gemini API Key (refer to .env.example):
```Plaintext
GEMINI_API_KEY=your_actual_api_key_here
```

**4. Run the application**
```bash
streamlit run app.py
```


