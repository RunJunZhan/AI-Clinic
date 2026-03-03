import os
from google import genai
from google.genai import types
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
def generate_medical_report(image, user_question):
    # 從環境變數讀取 API Key
    key = os.getenv("GEMINI_API_KEY") 
    
    try:
        client = genai.Client(api_key=key)
        
        prompt = f"""
        角色設定：你現在是世界頂尖的放射科與皮膚科專科醫師。
        使用者問題：{user_question}
        
        請依照以下結構分析（繁體中文）：
        1. **【影像特徵】**：詳細描述外觀、顏色、結構。
        2. **【異常發現】**：有無骨折、紅腫、病變？
        3. **【診斷推測】**：最可能的 3 種原因。
        4. **【處置建議】**：護理方式與就醫警訊。
        若整體並無問題則不須特別指出，請直接說明正常的部分即可。
        
        警告：本分析僅供參考，非正式醫療診斷!
        """
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[prompt, image],
            config=types.GenerateContentConfig(temperature=0.3)
        )
        return response.text
        
    except Exception as e:
        return f"分析失敗：{e}"