import cv2
import numpy as np
import time
import streamlit as st
import mediapipe as mp
from mediapipe.python.solutions import pose as mp_pose
from mediapipe.python.solutions import drawing_utils as mp_drawing

def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/ np.pi)
    if angle > 180.0: angle = 360 - angle
    return angle 

def run_pose_estimation(mode, count_metric, angle_metric, status_metric, frame_placeholder):
    cap = cv2.VideoCapture(0)
    prev_time = time.time()
    
    with mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7) as pose:
        # 用 st.session_state.run_cam 控制開關
        while cap.isOpened() and st.session_state.get('run_cam', False):
            ret, frame = cap.read()
            if not ret: break
            
            curr_time = time.time()
            dt = curr_time - prev_time
            prev_time = curr_time
            
            h, w, c = frame.shape
            frame = cv2.flip(frame, 1)
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = pose.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            try:
                landmarks = results.pose_landmarks.landmark
                
                # 取得關節座標
                shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

                angle = 0
                display_pos = (0, 0)
                
                # 狀態機邏輯判斷
                if "深蹲" in mode:
                    angle = calculate_angle(hip, knee, ankle)
                    display_pos = tuple(np.multiply(knee, [w, h]).astype(int))
                    
                    if angle > 160: st.session_state.stage = "UP"
                    if angle < 90 and st.session_state.stage == 'UP':
                        st.session_state.stage = "DOWN"
                        st.session_state.counter += 1
                    
                    count_metric.metric("累積次數", st.session_state.counter)

                elif "二頭肌" in mode:
                    angle = calculate_angle(shoulder, elbow, wrist)
                    display_pos = tuple(np.multiply(elbow, [w, h]).astype(int))
                    
                    if angle > 160: st.session_state.stage = "DOWN"
                    if angle < 45 and st.session_state.stage == 'DOWN':
                        st.session_state.stage = "UP"
                        st.session_state.counter += 1
                        
                    count_metric.metric("累積次數", st.session_state.counter)

                elif "側平舉" in mode:
                    angle = calculate_angle(hip, shoulder, elbow)
                    display_pos = tuple(np.multiply(shoulder, [w, h]).astype(int))
                    
                    if angle > 120: 
                        st.session_state.stage = "Holding!"
                        st.session_state.hold_time += dt 
                    else: 
                        st.session_state.stage = "Rest"
                        
                    count_metric.metric("支撐時間", f"{st.session_state.hold_time:.1f} 秒")

                # 繪製IMAGE
                cv2.putText(image, str(int(angle)), display_pos, 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.rectangle(image, (0,0), (225,73), (245,117,16), -1)
                
                if "側平舉" in mode:
                    cv2.putText(image, 'TIME (SEC)', (15,12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
                    cv2.putText(image, f"{st.session_state.hold_time:.1f}", (10,60), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
                else:
                    cv2.putText(image, 'REPS', (15,12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
                    cv2.putText(image, str(st.session_state.counter), (10,60), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
                
                cv2.putText(image, 'STAGE', (130,12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
                cv2.putText(image, str(st.session_state.stage), (120,60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
                
                # 更新儀表板
                angle_metric.metric("目前角度", f"{int(angle)}°")
                status_metric.info(f"狀態: {st.session_state.stage}")

            except:
                pass
            
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            
            # 將影像放到UI裡
            frame_placeholder.image(image, channels="BGR", width="stretch")
            
        cap.release()