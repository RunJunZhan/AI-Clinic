import streamlit as st
from PIL import Image

from rehabilitation import run_pose_estimation
from gemini import generate_medical_report

# UI 設定
st.set_page_config(page_title="AI 智慧居家醫療平台", layout="wide", page_icon="🏥")
st.title("🏥 AI 智慧居家醫療整合平台")

with st.sidebar:
    st.divider()
    st.header("復健設定")
    mode = st.selectbox(
        "選擇復健項目",
        ["🦵 深蹲 (計數)", "💪 二頭肌彎舉 (計數)", "🙆‍♂️ 側平舉 (計時挑戰)"]
    )

    if st.button("🔄 重置數據"):
        st.session_state.counter = 0
        st.session_state.hold_time = 0.0 
        st.session_state.stage = None

tab1, tab2 = st.tabs(["AI 復健教練", "醫療影像諮詢"])

# Page1(復健教練)
with tab1:
    col1, col2 = st.columns([3, 1])
    
    with col2:
        st.markdown(f"### {mode}")
        angle_metric = st.empty()
        count_metric = st.empty() 
        status_metric = st.empty()
        
        # 使用 st.checkbox 並綁定 key，這樣 pose_estimation.py 讀得到狀態
        run_camera = st.checkbox("📸 啟動攝影機", key="run_cam")
        
        st.markdown("---")
        if "側平舉" in mode:
            st.info("⏱規則：請將雙手平舉超過 120°，自動累積支撐時間。")
        elif "深蹲" in mode:
            st.info("規則：當膝蓋彎曲小於 90° 且之前是站立狀態，計數器將增加一次。")
        elif "二頭肌" in mode:
            st.info("規則：當手肘彎曲小於 45° 且之前是放下狀態，計數器將增加一次。")

    with col1:
        frame_placeholder = st.empty()

    # 初始化 Session State
    if 'counter' not in st.session_state: st.session_state.counter = 0
    if 'hold_time' not in st.session_state: st.session_state.hold_time = 0.0
    if 'stage' not in st.session_state: st.session_state.stage = None

    # 若勾選啟動攝影機，呼叫外部模組執行
    if run_camera:
        run_pose_estimation(mode, count_metric, angle_metric, status_metric, frame_placeholder)

# Page2(醫療影像諮詢)
with tab2:
    st.header("醫療影像 AI 分析")
    st.write("請上傳您的患部照片或 X 光片，AI 將進行分析。")
   
    if 'ai_report' not in st.session_state:
        st.session_state['ai_report'] = ""
   
    uploaded_file = st.file_uploader("點擊上傳照片...", type=["jpg", "png", "jpeg"])
   
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="已上傳影像", width=400)
       
        user_question = st.text_input("描述您的症狀或疑問：", "請詳細分析這張影像的異常之處。")
       
        if st.button("執行專業分析"):
            with st.spinner("AI 正在撰寫病歷報告..."):
                # 呼叫外部模組來生成報告
                st.session_state['ai_report'] = generate_medical_report(image, user_question)

    if st.session_state['ai_report']:
        st.divider()
        st.success("分析報告已生成")
        st.markdown(st.session_state['ai_report'])
       
        st.download_button(
            label="下載完整病歷報告 (.txt)",
            data=st.session_state['ai_report'],
            file_name="AI_Medical_Report.txt",
            mime="text/plain"

        )
