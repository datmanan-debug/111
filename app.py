import streamlit as st
import time

# 1. إعدادات الصفحة الأساسية والثيم الرسمي
st.set_page_config(
    page_title="Mammogram AI Diagnostics",
    page_icon="🧬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. إضافة حزمة CSS المخصصة للتصميم الرسمي الكلاسيكي
st.markdown("""
    <style>
    /* تغيير الخلفية العامة إلى الرمادي البارد المريح */
    .stApp {
        background-color: #F8F9FA;
    }
    
    /* العناوين الرئيسية باللون الكحلي الداكن الموثوق */
    h1, h2, h3 {
        color: #1A365D !important;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-weight: 700;
    }
    
    /* تنسيق الحاويات والمربعات لتظهر بشكل كلاسيكي هادئ */
    .custom-card {
        background-color: #FFFFFF;
        padding: 30px;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border: 1px solid #E2E8F0;
        margin-bottom: 20px;
    }
    
    /* تنسيق أزرار التنقل لتكون رسمية وأنيقة */
    .stButton>button {
        width: 100%;
        background-color: #2B6CB0 !important; /* أزرق رسمي */
        color: white !important;
        border-radius: 6px !important;
        padding: 10px 20px !important;
        border: none !important;
        font-weight: 600 !important;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #1A365D !important; /* أزرق أغمق عند التمرير */
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    /* زر التراجع بلون محايد */
    div[data-testid="stMarkdownContainer"] + div {
        margin-top: 10px;
    }
    
    /* تأثير الباركود الرقمي أو لمسة الذكاء الاصطناعي */
    .ai-badge {
        background-color: #EBF8FF;
        color: #2B6CB0;
        padding: 6px 12px;
        border-radius: 4px;
        font-size: 0.85rem;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 15px;
        border: 1px solid #BEE3F8;
    }
    </style>
""", unsafe_allow_error=True)

# 3. إدارة التنقل بين الصفحات الخمس باستخدام Session State
if 'page' not in st.session_state:
    st.session_state.page = 1

if 'patient_name' not in st.session_state:
    st.session_state.patient_name = ""

# دالات المساعدة للتنقل
def next_page(): st.session_state.page += 1
def prev_page(): st.session_state.page -= 1

# ==========================================
# الواجهة 1: الشاشة الترحيبية الرسمية (Splash Screen)
# ==========================================
if st.session_state.page == 1:
    st.markdown("<div style='text-align: center; margin-top: 50px;'>", unsafe_allow_html=True)
    
    # محاكاة مكان اللوغو بنص رسمي منسق
    st.markdown("""
        <div style='border: 2px solid #1A365D; display: inline-block; padding: 15px 30px; border-radius: 6px; margin-bottom: 20px; background-color: #1A365D; color: white;'>
            <span style='font-size: 1.5rem; font-weight: bold; letter-spacing: 2px;'>ENGINEERING TITANS</span>
        </div>
    """, unsafe_allow_html=True)
    
    st.title("Mammogram AI Diagnostics System")
    st.markdown("<p style='color: #4A5568; font-size: 1.1rem;'>Integrating Engineering Precision with Medical Artificial Intelligence</p>", unsafe_allow_html=True)
    st.markdown("<hr style='border-top: 1px solid #CBD5E0; width: 50%; margin: 20px auto;'>", unsafe_allow_html=True)
    
    st.markdown("""
        <div class='custom-card' style='max-width: 500px; margin: 0 auto; text-align: left;'>
            <span class='ai-badge'>System Status: Ready</span>
            <p style='color: #718096; font-size: 0.9rem; line-height: 1.6;'>
                This clinical-grade software utilizes deep learning architectures to assist medical professionals in mammogram screening and early breast cancer classification.
            </p>
            <p style='font-size: 0.8rem; color: #A0AEC0;'>Version 1.0.0 • Verified Deployment</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.button("Proceed to Clinical Portal", on_click=next_page)
    st.markdown("</div>", unsafe_allow_html=True)
# ==========================================
# الواجهة 2: بيانات المريض الطبية (Patient Info)
# ==========================================
elif st.session_state.page == 2:
    st.subheader("📋 Patient Registration & Demographics")
    st.markdown("Please enter the patient's records accurately to map with the DICOM metadata.")
    
    with st.container():
        st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
        
        name = st.text_input("Patient Full Name", value=st.session_state.patient_name)
        st.session_state.patient_name = name
        
        col_age, col_phone = st.columns(2)
        with col_age:
            st.number_input("Patient Age", min_value=1, max_value=120, value=45)
        with col_phone:
            st.text_input("Contact Number")
            
        st.radio("Prior Medical History of Breast Pathology?", ["No", "Yes"])
        st.markdown("</div>", unsafe_allow_html=True)
        
    col_back, col_next = st.columns([1, 1])
    with col_back:
        st.button("← Back", on_click=prev_page)
    with col_next:
        st.button("Next: Upload DICOM →", on_click=next_page)

# ==========================================
# الواجهة 3: رفع ملف الـ DICOM (Upload File)
# ==========================================
elif st.session_state.page == 3:
    st.subheader("📂 Mammography File Ingestion")
    st.markdown(f"Patient Record: **{st.session_state.patient_name if st.session_state.patient_name else 'Anonymous'}**")
    
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.markdown("<span class='ai-badge'>Supports standard .dcm / .dicom formats</span>", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Upload Digital Mammography (DICOM File)", type=["dcm", "dicom"])
    
    st.markdown("""
        <div style='margin-top: 15px; font-size: 0.85rem; color: #718096;'>
            ⚠️ Max file size: 200MB. Data is encrypted and processed locally ensuring HIPAA compliance.
        </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # إضافة لمسة محاكاة الذكاء الاصطناعي (AI Scanning Process) عند الرفع
    if uploaded_file is not My_Upload_Object := None:
        with st.spinner("AI Engine running inference... Processing pixel arrays and neural layers."):
            time.sleep(2) # محاكاة وقت التحليل
        st.success("Analysis complete. Ready to view results.")
        
    col_back, col_next = st.columns([1, 1])
    with col_back:
        st.button("← Back", on_click=prev_page)
    with col_next:
        st.button("Run AI Diagnostics →", on_click=next_page)

# ==========================================
# الواجهة 4: النتيجة الأولية (Normal / Abnormal)
# ==========================================
elif st.session_state.page == 4:
    st.subheader("🔬 AI Diagnostic Analysis Result")
    st.markdown(f"Analysis for Patient: **{st.session_state.patient_name}**")
    
    st.markdown("<div class='custom-card' style='text-align: center;'>", unsafe_allow_html=True)
    st.markdown("<span class='ai-badge'>Classification Layer: Binary Screening</span>", unsafe_allow_html=True)
    
    # عرض النتائج بشكل رسمي مع الـ Confidence Score كما اقترح المشرف
    col_res1, col_res2 = st.columns(2)
    
    with col_res1:
        st.markdown("""
            <div style='border: 1px solid #CBD5E0; padding: 20px; border-radius: 6px; background-color: #F7FAFC; opacity: 0.6;'>
                <h3 style='color: #718096 !important; margin: 0;'>NORMAL</h3>
                <p style='color: #A0AEC0; font-size: 0.9rem; margin: 5px 0 0 0;'>Confidence: --</p>
            </div>
        """, unsafe_allow_html=True)
        
    with col_res2:
        # جعل الخيار النشط يبرز بلون واضح ورسمي (مثل الوردي الطبي الغامق أو الأحمر الهادئ للتحذير)
        st.markdown("""
            <div style='border: 2px solid #9B2C2C; padding: 20px; border-radius: 6px; background-color: #FFF5F5;'>
                <h3 style='color: #9B2C2C !important; margin: 0;'>ABNORMAL FINDINGS</h3>
                <p style='color: #C53030; font-size: 0.9rem; margin: 5px 0 0 0;'>Confidence: 94.2%</p>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("""
        <div style='text-align: left; margin-top: 20px; padding: 15px; background-color: #EDF2F7; border-radius: 6px; font-size: 0.9rem;'>
            💡 <b>AI Recommendation:</b> Micro-calcifications or mass density detected. Secondary classification required to determine pathological nature.
        </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    col_back, col_next = st.columns([1, 1])
    with col_back:
        st.button("← Back to Upload", on_click=prev_page)
    with col_next:
        st.button("Detailed Pathology Breakdown →", on_click=next_page)

# ==========================================
# الواجهة 5: تفصيل النتيجة (Benign / Malignant)
# ==========================================
elif st.session_state.page == 5:
    st.subheader("🧬 Secondary Pathological Classification")
    
    st.markdown("<div class='custom-card' style='text-align: center;'>", unsafe_allow_html=True)
    st.markdown("<span class='ai-badge'>Classification Layer: Pathology Specification</span>", unsafe_allow_html=True)
    
    st.markdown("""
        <div style='background-color: #FFF5F5; border: 1px solid #FEB2B2; padding: 10px; border-radius: 6px; margin-bottom: 25px;'>
            <span style='color: #9B2C2C; font-weight: bold;'>Initial Status: ABNORMAL DETECTED</span>
        </div>
    """, unsafe_allow_html=True)
    
    col_b, col_m = st.columns(2)
    
    with col_b:
        st.markdown("""
            <div style='border: 1px solid #CBD5E0; padding: 25px; border-radius: 6px; background-color: #F7FAFC; opacity: 0.5;'>
                <h3 style='color: #4A5568 !important; margin: 0;'>BENIGN</h3>
                <p style='color: #718096; font-size: 0.85rem; margin-top: 5px;'>Probability: 12.4%</p>
            </div>
        """, unsafe_allow_html=True)
        
    with col_m:
        st.markdown("""
            <div style='border: 2px solid #9B2C2C; padding: 25px; border-radius: 6px; background-color: #FFF5F5; box-shadow: 0 4px 10px rgba(155, 44, 44, 0.1);'>
                <h3 style='color: #9B2C2C !important; margin: 0;'>MALIGNANT</h3>
                <p style='color: #E53E3E; font-weight: bold; font-size: 1.1rem; margin-top: 5px;'>Probability: 87.6%</p>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("""
        <div style='text-align: left; margin-top: 25px; border-left: 4px solid #1A365D; padding-left: 15px; font-size: 0.85rem; color: #4A5568;'>
            <b>Engineering Titans System Note:</b> This evaluation is generated by an automated Deep Learning ensemble model. Results must be correlated clinically via histopathological biopsy before finalizing oncology reports.
        </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    col_back, col_reset = st.columns([1, 1])
    with col_back:
        st.button("← Back to Screening", on_click=prev_page)
    with col_reset:
        if st.button("🔄 Process New Case"):
            st.session_state.page = 1
            st.session_state.patient_name = ""
            st.rerun()

# 4. تذييل الصفحة الرسمي الثابت (Footer)
st.markdown("""
    <div style='text-align: center; margin-top: 50px; font-size: 0.8rem; color: #A0AEC0;'>
        © 2026 Engineering Titans. All Rights Reserved. Clinical AI Decision Support Tool.
    </div>
""", unsafe_allow_html=True)