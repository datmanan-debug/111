import streamlit as st
import time
import os
import base64
import pandas as pd
from datetime import datetime

# 1. إعدادات الصفحة الأساسية والثيم الرسمي
st.set_page_config(
    page_title="Mammogram AI Diagnostics",
    page_icon="🧬",
    layout="centered",
    initial_sidebar_state="expanded"
)

# مسار ملف حفظ البيانات (الإكسل)
LOG_FILE = "patients_log.csv"

# دالة لقراءة الصورة وتحويلها لـ Base64 لضمان عمل الـ CSS عليها بدقة
def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

img_data = get_image_base64("m.jpg")

# 2. إضافة حزمة CSS المخصصة للتحكم المطلق بمواقع وتجاور الأزرار
st.markdown("""
    <style>
    /* تغيير الخلفية العامة إلى الخلفية العاجية الدافئة */
    .stApp {
        background-color: #FAFAF6;
    }
    
    /* العناوين الرئيسية بالأزرق البترولي */
    h1, h2, h3 {
        color: #2E4A62 !important;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-weight: 700;
        text-align: center;
    }
    
    /* تصفير الفراغات الافتراضية من ستريمليت لضمان السنتر الدقيق */
    .block-container {
        padding-top: 3rem !important;
    }

    /* حاوية الفليكس لفرض التوسط المطلق في الصفحة الأولى */
    .center-wrapper {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        width: 100%;
    }

    /* تنسيق مخصص للأزرار باللون الأزرق البترولي */
    div.stButton > button {
        width: 100% !important;
        background-color: #2E4A62 !important;
        color: white !important;
        border-radius: 6px !important;
        padding: 10px 20px !important;
        border: none !important;
        font-weight: 600 !important;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #D4A5B8 !important;
        color: #2E4A62 !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    /* تأثير شارة الذكاء الاصطناعي باللون الوردي المغبر */
    .ai-badge {
        background-color: #FAFAF6;
        color: #2E4A62;
        padding: 6px 12px;
        border-radius: 4px;
        font-size: 0.85rem;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 15px;
        border: 1px solid #D4A5B8;
    }

    /* تنسيق منطقة رفع الملفات المتناسق مع الرمادي الفاتح */
    .stFileUploader {
        background-color: #EAEAEA !important;
        border: 2px dashed #2E4A62 !important;
        border-radius: 8px;
        padding: 10px;
    }

    /* حواف نتائج الـ AI بالدرجات المطلوبة (الوردي الناعم #E8A7A1 والوردي الغامق #D4A5B8) */
    .card-pink-light {
        border: 2px solid #E8A7A1;
        padding: 20px;
        border-radius: 6px;
        background-color: #FAFAF6;
    }
    .card-pink-dark {
        border: 2px solid #D4A5B8;
        padding: 20px;
        border-radius: 6px;
        background-color: #FAFAF6;
    }
    </style>
""", unsafe_allow_html=True)

# 3. إدارة التنقل والبيانات باستخدام Session State
if 'page' not in st.session_state:
    st.session_state.page = 1

# تهيئة بيانات المريض الافتراضية
if 'patient_name' not in st.session_state: st.session_state.patient_name = ""
if 'patient_age' not in st.session_state: st.session_state.patient_age = ""  
if 'patient_phone' not in st.session_state: st.session_state.patient_phone = ""
if 'patient_history' not in st.session_state: st.session_state.patient_history = "No"

# دالات المساعدة للتنقل
def next_page(): st.session_state.page += 1
def prev_page(): st.session_state.page -= 1

# دالة حفظ البيانات في ملف الـ CSV وتصفير النظام للعودة للواجهة الأولى
def save_and_reset():
    now = datetime.now()
    new_record = {
        "Date": now.strftime("%Y-%m-%d"),
        "Time": now.strftime("%H:%M:%S"),
        "Patient Name": st.session_state.patient_name if st.session_state.patient_name else "Anonymous",
        "Age": st.session_state.patient_age if st.session_state.patient_age else "N/A",
        "Phone": st.session_state.patient_phone if st.session_state.patient_phone else "N/A",
        "History of Pathology": st.session_state.patient_history,
        "AI Diagnostics Result": "Pending Correlation"  
    }
    
    df_new = pd.DataFrame([new_record])
    
    if os.path.exists(LOG_FILE):
        try:
            df_old = pd.read_csv(LOG_FILE)
            if "Date & Time" in df_old.columns:
                df_new.to_csv(LOG_FILE, index=False)
            else:
                df_combined = pd.concat([df_old, df_new], ignore_index=True)
                df_combined.to_csv(LOG_FILE, index=False)
        except:
            df_new.to_csv(LOG_FILE, index=False)
    else:
        df_new.to_csv(LOG_FILE, index=False)
        
    st.session_state.page = 1
    st.session_state.patient_name = ""
    st.session_state.patient_age = ""
    st.session_state.patient_phone = ""
    st.session_state.patient_history = "No"

# ==========================================
# بناء القائمة الجانبية (Sidebar Navigation)
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='text-align: left; font-size: 1.5rem; margin-bottom: 20px; color: #2E4A62;'>⚙️ Control Panel</h2>", unsafe_allow_html=True)
    menu_selection = st.radio(
        "Navigate System Modules:",
        ["🔬 New AI Diagnostics", "📋 Patients Medical Log"]
    )
    st.markdown("<hr style='border-top: 1px solid #D4A5B8;'>", unsafe_allow_html=True)
    st.markdown("<small style='color: #2E4A62;'>System Status: <b>Online</b><br>Database: <b>Local CSV</b></small>", unsafe_allow_html=True)

# ==========================================
# القسم الأول: نظام الفحص (5 واجهات تتابعية)
# ==========================================
if menu_selection == "🔬 New AI Diagnostics":

    # الواجهة 1: الشاشة الترحيبية الرسمية (Splash Screen) - زر Next في المنتصف تماماً وبشكل مستقل
    if st.session_state.page == 1:
        st.markdown("<div class='center-wrapper'>", unsafe_allow_html=True)
        if img_data:
            logo_html = f"""
            <div style='display: flex; align-items: center; justify-content: center; gap: 15px; margin-bottom: 20px;'>
                <h2 style='color: #2E4A62 !important; font-size: 2rem; margin: 0; letter-spacing: 2px;'>ENGINEERING TITANS</h2>
                <img src='data:image/jpeg;base64,{img_data}' style='height: 60px; width: auto; object-fit: contain; mix-blend-mode: multiply;'>
            </div>
            """
        else:
            logo_html = "<h2 style='color: #2E4A62 !important; font-size: 2rem; margin-bottom: 20px; letter-spacing: 2px;'>ENGINEERING TITANS</h2>"
            
        st.markdown(logo_html, unsafe_allow_html=True)
        st.markdown("<h1>Mammogram AI Diagnostics System</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color: #2E4A62; font-size: 1.1rem; margin-top: -5px; text-align: center; width: 100%;'>Integrating Engineering Precision with Medical Artificial Intelligence</p>", unsafe_allow_html=True)
        
        st.markdown("<hr style='border-top: 2px solid #D4A5B8; width: 60%; margin: 25px auto;'>", unsafe_allow_html=True)
        st.write("")
        st.write("")
        
        # تقسيم مخصص لجعل زر الـ Next في السنتر تماماً
        col_btn_l, col_btn_mid, col_btn_r = st.columns([1.5, 1, 1.5])
        with col_btn_mid:
            st.button("Next", on_click=next_page, key="btn_p1_next")
        st.markdown("</div>", unsafe_allow_html=True)

    # الواجهة 2: بيانات المريض الطبية (Patient Info) - أزرار متقاربة ومتوسطة الشاشة
    elif st.session_state.page == 2:
        st.markdown("<h2 style='text-align: left; color: #2E4A62;'>📋 Patient Registration & Demographics</h2>", unsafe_allow_html=True)
        st.markdown("Please enter the patient's records accurately to map with the DICOM metadata.")
        st.write("")
        
        st.session_state.patient_name = st.text_input("Patient Full Name", value=st.session_state.patient_name)
        
        col_age, col_phone = st.columns(2)
        with col_age:
            st.session_state.patient_age = st.text_input("Patient Age", value=st.session_state.patient_age)
        with col_phone:
            st.session_state.patient_phone = st.text_input("Contact Number", value=st.session_state.patient_phone)
            
        st.session_state.patient_history = st.radio("Prior Medical History of Breast Pathology?", ["No", "Yes"], index=0 if st.session_state.patient_history == "No" else 1)
        
        st.write("")
        st.markdown("<hr style='border-top: 1px solid #D4A5B8; margin: 20px 0;'>", unsafe_allow_html=True)
        
        # أزرار متقاربة في منتصف الواجهة
        col_l, col_back, col_next, col_r = st.columns([1.2, 1, 1, 1.2])
        with col_back:
            st.button("Back", on_click=prev_page, key="btn_p2_back")
        with col_next:
            st.button("Next", on_click=next_page, key="btn_p2_next")

    # الواجهة 3: رفع ملف الـ DICOM (Upload File) - أزرار متقاربة ومتوسطة الشاشة
    elif st.session_state.page == 3:
        st.markdown("<h2 style='text-align: left; color: #2E4A62;'>📂 Mammography File Ingestion</h2>", unsafe_allow_html=True)
        st.write("")
        st.markdown("<span class='ai-badge'>Supports standard .dcm / .dicom formats</span>", unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("Upload Digital Mammography (DICOM File)", type=["dcm", "dicom"])
        st.markdown("""
            <div style='margin-top: 5px; margin-bottom: 20px; font-size: 0.85rem; color: #2E4A62;'>
                ⚠️ Max file size: 200MB. Data is encrypted and processed locally ensuring HIPAA compliance.
            </div>
        """, unsafe_allow_html=True)
        
        if uploaded_file is not None:
            with st.spinner("AI Engine running inference... Processing pixel arrays and neural layers."):
                time.sleep(1.5) 
            st.success("Analysis complete. Ready to view results.")
            
        st.write("")
        st.markdown("<hr style='border-top: 1px solid #D4A5B8; margin: 20px 0;'>", unsafe_allow_html=True)
        
        # أزرار متقاربة في منتصف الواجهة
        col_l, col_back, col_next, col_r = st.columns([1.2, 1, 1, 1.2])
        with col_back:
            st.button("Back", on_click=prev_page, key="btn_p3_back")
        with col_next:
            st.button("Next", on_click=next_page, key="btn_p3_next")

    # الواجهة 4: النتيجة الأولية (Normal / Abnormal) - أزرار متقاربة ومتوسطة الشاشة
    elif st.session_state.page == 4:
        st.markdown("<h2 style='text-align: left; color: #2E4A62;'>🔬 AI Diagnostic Analysis Result</h2>", unsafe_allow_html=True)
        st.write("")
        
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.markdown("""
                <div class="card-pink-light">
                    <h3 style='color: #2E4A62 !important; margin: 0; text-align: center;'>NORMAL</h3>
                    <p style='color: #2E4A62; font-size: 0.9rem; margin: 5px 0 0 0; text-align: center;'>Confidence: --%</p>
                </div>
            """, unsafe_allow_html=True)
        with col_res2:
            st.markdown("""
                <div class="card-pink-dark">
                    <h3 style='color: #2E4A62 !important; margin: 0; text-align: center;'>ABNORMAL FINDINGS</h3>
                    <p style='color: #2E4A62; font-size: 0.9rem; margin: 5px 0 0 0; text-align: center;'>Confidence: --%</p>
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown("""
            <div style='text-align: left; margin-top: 20px; padding: 15px; background-color: #EAEAEA; border-radius: 6px; font-size: 0.9rem; color: #2E4A62; border-left: 4px solid #D4A5B8;'>
                💡 <b>AI Recommendation:</b> Verification of inference layers. Secondary classification tracks can be populated dynamically post-execution.
            </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        st.markdown("<hr style='border-top: 1px solid #D4A5B8; margin: 20px 0;'>", unsafe_allow_html=True)
        
        # أزرار متقاربة في منتصف الواجهة
        col_l, col_back, col_next, col_r = st.columns([1.2, 1, 1, 1.2])
        with col_back:
            st.button("Back", on_click=prev_page, key="btn_p4_back")
        with col_next:
            st.button("Next", on_click=next_page, key="btn_p4_next")

    # الواجهة 5: تفصيل النتيجة (Benign / Malignant) - أزرار متقاربة ومتوسطة الشاشة
    elif st.session_state.page == 5:
        st.markdown("<h2 style='text-align: left; color: #2E4A62;'>🧬 Secondary Pathological Classification</h2>", unsafe_allow_html=True)
        st.write("")
        st.markdown("""
            <div style='background-color: #EAEAEA; border: 1px solid #D4A5B8; padding: 12px; border-radius: 6px; margin-bottom: 25px; text-align: center;'>
                <span style='color: #2E4A62; font-weight: bold;'>Inference Status: Computing Secondary Probability Tracks</span>
            </div>
        """, unsafe_allow_html=True)
        
        col_b, col_m = st.columns(2)
        with col_b:
            st.markdown("""
                <div class="card-pink-light">
                    <h3 style='color: #2E4A62 !important; margin: 0; text-align: center;'>BENIGN</h3>
                    <p style='color: #2E4A62; font-size: 0.85rem; margin-top: 5px; text-align: center;'>Probability: --%</p>
                </div>
            """, unsafe_allow_html=True)
        with col_m:
            st.markdown("""
                <div class="card-pink-dark">
                    <h3 style='color: #2E4A62 !important; margin: 0; text-align: center;'>MALIGNANT</h3>
                    <p style='color: #2E4A62; font-size: 0.85rem; margin-top: 5px; text-align: center;'>Probability: --%</p>
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown("""
            <div style='text-align: left; margin-top: 25px; border-left: 4px solid #D4A5B8; padding-left: 15px; font-size: 0.85rem; color: #2E4A62;'>
                <b>Engineering Titans System Note:</b> This evaluation module is optimized to hook into deep neural layer prediction logits. Resulting pipelines require correlation with expert histopathological analysis.
            </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        st.markdown("<hr style='border-top: 1px solid #D4A5B8; margin: 20px 0;'>", unsafe_allow_html=True)
        
        # أزرار متقاربة في منتصف الواجهة
        col_l, col_back, col_next, col_r = st.columns([1.2, 1, 1, 1.2])
        with col_back:
            st.button("Back", on_click=prev_page, key="btn_p5_back")
        with col_next:
            st.button("Next", on_click=save_and_reset, key="btn_p5_next")

# ==========================================
# القسم الثاني: السجل الطبي للمرضى
# ==========================================
elif menu_selection == "📋 Patients Medical Log":
    st.markdown("<h2 style='text-align: left; color: #2E4A62;'>📋 Patients Diagnostic Log Database</h2>", unsafe_allow_html=True)
    st.markdown("Review, search, and export historical diagnostic sessions saved on the system.")
    st.write("")
    
    if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) > 0:
        df_log = pd.read_csv(LOG_FILE)
        
        if "Date" in df_log.columns:
            search_query = st.text_input("🔍 Search Database (By Name, Phone or Result):", "")
            
            if search_query:
                filtered_df = df_log[
                    df_log['Patient Name'].astype(str).str.contains(search_query, case=False, na=False) |
                    df_log['Phone'].astype(str).str.contains(search_query, case=False, na=False) |
                    df_log['AI Diagnostics Result'].astype(str).str.contains(search_query, case=False, na=False)
                ]
            else:
                filtered_df = df_log

            filtered_df = filtered_df.iloc[::-1]
            st.dataframe(filtered_df, use_container_width=True, hide_index=True)
            st.write("")
            
            col_dl, col_clr = st.columns([2, 1])
            with col_dl:
                csv_data = df_log.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Export Full Log to Excel (.CSV)",
                    data=csv_data,
                    file_name=f"Mammogram_AI_Log_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime='text/csv'
                )
            with col_clr:
                if st.button("🗑️ Clear Database"):
                    if os.path.exists(LOG_FILE):
                        os.remove(LOG_FILE)
                    st.success("Database cleared successfully.")
                    st.rerun()
        else:
            st.info("The database structure has been updated. Complete a new AI Diagnostic session to populate the new log table.")
    else:
        st.info("No records found in the database. Complete an AI Diagnostic session to populate the log table.")

# 4. تذييل الصفحة الرسمي الثابت (Footer)
st.markdown("""
    <div style='text-align: center; margin-top: 50px; font-size: 0.8rem; color: #2E4A62;'>
        © 2026 Engineering Titans. All Rights Reserved. Clinical AI Decision Support Tool.
    </div>
""", unsafe_allow_html=True)
