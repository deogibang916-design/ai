import streamlit as st
import json
from datetime import datetime, date
import random
import calendar

# 페이지 설정
st.set_page_config(page_title="나의 체크리스트", page_icon="✅", layout="wide", initial_sidebar_state="collapsed")

# 고급스러운 CSS 스타일링
st.markdown("""
<style>
    /* 전체 배경 그라데이션 */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    /* 메인 컨테이너 스타일 */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* 제목 스타일 */
    h1 {
        color: white !important;
        text-align: center;
        font-size: 3rem !important;
        font-weight: 700 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        margin-bottom: 1rem !important;
    }
    
    /* 탭 스타일 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(255,255,255,0.1);
        border-radius: 10px;
        padding: 5px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255,255,255,0.1);
        border-radius: 8px;
        color: white;
        font-weight: 600;
        padding: 10px 20px;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* 헤더 스타일 */
    h2, h3 {
        color: white !important;
        font-weight: 600 !important;
    }
    
    /* 입력 필드 스타일 */
    .stTextInput > div > div > input {
        background-color: rgba(255,255,255,0.95);
        border-radius: 10px;
        border: 2px solid rgba(255,255,255,0.3);
        padding: 10px;
    }
    
    /* 버튼 스타일 */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 25px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    
    /* 체크박스 스타일 */
    .stCheckbox {
        color: white;
    }
    
    /* 카드 스타일 */
    .task-card {
        background: rgba(255,255,255,0.95);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        transition: all 0.3s ease;
    }
    
    .task-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.15);
    }
    
    /* 진행률 바 스타일 */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    /* 성공 메시지 스타일 */
    .stSuccess {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        border-radius: 10px;
        padding: 15px;
        color: white;
        font-weight: 600;
    }
    
    /* 정보 메시지 스타일 */
    .stInfo {
        background: rgba(255,255,255,0.95);
        border-radius: 15px;
        border-left: 5px solid #667eea;
    }
    
    /* 달력 컨테이너 */
    .calendar-container {
        background: rgba(255,255,255,0.95);
        border-radius: 20px;
        padding: 25px;
        margin: 20px 0;
        box-shadow: 0 10px 40px rgba(0,0,0,0.15);
    }
    
    /* 마크다운 텍스트 스타일 */
    .stMarkdown {
        color: white;
    }
    
    /* 구분선 제거 */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# AI 응원 메시지 목록
ENCOURAGEMENT_MESSAGES = [
    "🎉 훌륭해요! 한 걸음 더 나아갔네요!",
    "💪 잘하고 있어요! 계속 이 조자로!",
    "🌟 멋져요! 당신은 해낼 수 있어요!",
    "🚀 대단해요! 목표를 향해 달려가고 있어요!",
    "✨ 완벽해요! 오늘도 성공적인 하루네요!",
    "🎯 좋아요! 하나씩 달성하고 있어요!",
    "💫 최고예요! 이런 노력이 성장을 만들어요!",
    "🌈 환상적이에요! 계속 앞으로 나아가요!",
]

# 세션 상태 초기화
if 'daily_tasks' not in st.session_state:
    st.session_state.daily_tasks = []
if 'monthly_tasks' not in st.session_state:
    st.session_state.monthly_tasks = []
if 'show_message' not in st.session_state:
    st.session_state.show_message = False
if 'message' not in st.session_state:
    st.session_state.message = ""

# 제목
st.title("✅ 나의 체크리스트 앱")
st.markdown("---")

# 탭 생성
tab1, tab2 = st.tabs(["📅 하루 체크리스트", "📆 한달 체크리스트"])

# 하루 체크리스트 탭
with tab1:
    st.header("📅 오늘의 할 일")
    
    # 오늘 날짜 표시
    today = date.today()
    weekday_kr = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
    st.markdown(f'<div style="text-align: center; color: white; font-size: 18px; margin-bottom: 20px; opacity: 0.9;">{today.year}년 {today.month}월 {today.day}일 {weekday_kr[today.weekday()]}</div>', unsafe_allow_html=True)
    
    # 새 할일 추가
    st.markdown('<div style="background: rgba(255,255,255,0.95); border-radius: 15px; padding: 20px; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">', unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    with col1:
        new_daily_task = st.text_input("새로운 할 일을 추가하세요", key="new_daily", label_visibility="collapsed")
    with col2:
        if st.button("➕ 추가", key="add_daily", use_container_width=True):
            if new_daily_task:
                st.session_state.daily_tasks.append({
                    'task': new_daily_task,
                    'completed': False,
                    'id': len(st.session_state.daily_tasks)
                })
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 응원 메시지 표시
    if st.session_state.show_message:
        st.success(st.session_state.message)
        st.session_state.show_message = False
    
    # 체크리스트 표시
    if st.session_state.daily_tasks:
        st.markdown('<div style="background: rgba(255,255,255,0.95); border-radius: 15px; padding: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">', unsafe_allow_html=True)
        for i, task in enumerate(st.session_state.daily_tasks):
            col1, col2 = st.columns([0.15, 0.85])
            
            with col1:
                checked = st.checkbox("", value=task['completed'], key=f"daily_{i}")
                if checked != task['completed']:
                    st.session_state.daily_tasks[i]['completed'] = checked
                    if checked:
                        st.session_state.show_message = True
                        st.session_state.message = random.choice(ENCOURAGEMENT_MESSAGES)
                        st.rerun()
            
            with col2:
                if task['completed']:
                    st.markdown(f'<div style="color: #999; text-decoration: line-through; padding: 8px;">{task["task"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div style="color: #333; padding: 8px; font-size: 16px;">{task["task"]}</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 진행률 표시
        completed = sum(1 for task in st.session_state.daily_tasks if task['completed'])
        total = len(st.session_state.daily_tasks)
        progress = completed / total if total > 0 else 0
        
        st.markdown("---")
        st.markdown(f'<div style="background: rgba(255,255,255,0.95); border-radius: 15px; padding: 20px; margin-top: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">', unsafe_allow_html=True)
        st.subheader(f"📊 진행률: {completed}/{total} ({int(progress * 100)}%)")
        st.progress(progress)
        
        # 진행률 시각화
        if progress > 0:
            progress_color = "#38ef7d" if progress == 1.0 else "#667eea"
            st.markdown(f"""
            <div style="background: linear-gradient(90deg, {progress_color} {int(progress*100)}%, rgba(0,0,0,0.1) {int(progress*100)}%);
                        height: 30px; border-radius: 15px; display: flex; align-items: center; justify-content: center;
                        color: {'white' if progress > 0.5 else '#333'}; font-weight: 600; margin-top: 10px;">
                {int(progress * 100)}% 완료
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 모두 완료 시 축하 메시지
        if completed == total and total > 0:
            st.balloons()
            st.success("🎊 오늘의 모든 할 일을 완료했어요! 정말 대단해요!")
        
        # 초기화 버튼
        if st.button("🗑️ 오늘 리스트 초기화", key="reset_daily", use_container_width=True):
            st.session_state.daily_tasks = []
            st.rerun()
    else:
        st.info("💡 아직 할 일이 없습니다. 위에서 새로운 할 일을 추가해보세요!")

# 한달 체크리스트 탭
with tab2:
    st.header("📆 이번 달의 목표")
    
    # 현재 날짜 정보
    today = date.today()
    current_month = today.month
    current_year = today.year
    
    # 달력과 목표를 나란히 배치
    col_calendar, col_tasks = st.columns([1, 1])
    
    with col_calendar:
        st.markdown('<div class="calendar-container">', unsafe_allow_html=True)
        st.subheader(f"📅 {current_year}년 {current_month}월")
        
        # 달력 생성
        cal = calendar.monthcalendar(current_year, current_month)
        month_name = calendar.month_name[current_month]
        
        # 달력 HTML 생성
        calendar_html = f"""
        <div style="background: white; border-radius: 15px; padding: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
            <table style="width: 100%; border-collapse: collapse;">
                <thead>
                    <tr style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 10px;">
                        <th style="padding: 12px; text-align: center; font-weight: 600;">일</th>
                        <th style="padding: 12px; text-align: center; font-weight: 600;">월</th>
                        <th style="padding: 12px; text-align: center; font-weight: 600;">화</th>
                        <th style="padding: 12px; text-align: center; font-weight: 600;">수</th>
                        <th style="padding: 12px; text-align: center; font-weight: 600;">목</th>
                        <th style="padding: 12px; text-align: center; font-weight: 600;">금</th>
                        <th style="padding: 12px; text-align: center; font-weight: 600;">토</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        for week in cal:
            calendar_html += "<tr>"
            for day in week:
                if day == 0:
                    calendar_html += '<td style="padding: 10px; text-align: center;"></td>'
                elif day == today.day:
                    calendar_html += f'<td style="padding: 10px; text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 50%; font-weight: 700; font-size: 16px;">{day}</td>'
                else:
                    calendar_html += f'<td style="padding: 10px; text-align: center; color: #333;">{day}</td>'
            calendar_html += "</tr>"
        
        calendar_html += """
                </tbody>
            </table>
        </div>
        """
        
        st.markdown(calendar_html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_tasks:
        # 새 목표 추가
        st.markdown('<div style="background: rgba(255,255,255,0.95); border-radius: 15px; padding: 20px; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">', unsafe_allow_html=True)
        col1, col2 = st.columns([3, 1])
        with col1:
            new_monthly_task = st.text_input("새로운 월간 목표를 추가하세요", key="new_monthly", label_visibility="collapsed")
        with col2:
            if st.button("➕ 추가", key="add_monthly", use_container_width=True):
                if new_monthly_task:
                    st.session_state.monthly_tasks.append({
                        'task': new_monthly_task,
                        'completed': False,
                        'id': len(st.session_state.monthly_tasks),
                        'created_date': today.isoformat()
                    })
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 응원 메시지 표시
        if st.session_state.show_message:
            st.success(st.session_state.message)
            st.session_state.show_message = False
        
        # 체크리스트 표시
        if st.session_state.monthly_tasks:
            st.markdown('<div style="background: rgba(255,255,255,0.95); border-radius: 15px; padding: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">', unsafe_allow_html=True)
            for i, task in enumerate(st.session_state.monthly_tasks):
                col1, col2 = st.columns([0.15, 0.85])
                
                with col1:
                    checked = st.checkbox("", value=task['completed'], key=f"monthly_{i}")
                    if checked != task['completed']:
                        st.session_state.monthly_tasks[i]['completed'] = checked
                        if checked:
                            st.session_state.show_message = True
                            st.session_state.message = random.choice(ENCOURAGEMENT_MESSAGES)
                            st.rerun()
                
                with col2:
                    if task['completed']:
                        st.markdown(f'<div style="color: #999; text-decoration: line-through; padding: 8px;">{task["task"]}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div style="color: #333; padding: 8px; font-size: 16px;">{task["task"]}</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # 진행률 표시
            completed = sum(1 for task in st.session_state.monthly_tasks if task['completed'])
            total = len(st.session_state.monthly_tasks)
            progress = completed / total if total > 0 else 0
            
            st.markdown("---")
            st.markdown(f'<div style="background: rgba(255,255,255,0.95); border-radius: 15px; padding: 20px; margin-top: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">', unsafe_allow_html=True)
            st.subheader(f"📊 진행률: {completed}/{total} ({int(progress * 100)}%)")
            st.progress(progress)
            
            # 진행률 시각화
            if progress > 0:
                progress_color = "#38ef7d" if progress == 1.0 else "#667eea"
                st.markdown(f"""
                <div style="background: linear-gradient(90deg, {progress_color} {int(progress*100)}%, rgba(0,0,0,0.1) {int(progress*100)}%);
                            height: 30px; border-radius: 15px; display: flex; align-items: center; justify-content: center;
                            color: {'white' if progress > 0.5 else '#333'}; font-weight: 600; margin-top: 10px;">
                    {int(progress * 100)}% 완료
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # 모두 완료 시 축하 메시지
            if completed == total and total > 0:
                st.balloons()
                st.success("🏆 이번 달 모든 목표를 달성했어요! 정말 자랑스러워요!")
            
            # 초기화 버튼
            if st.button("🗑️ 월간 리스트 초기화", key="reset_monthly", use_container_width=True):
                st.session_state.monthly_tasks = []
                st.rerun()
        else:
            st.info("💡 아직 월간 목표가 없습니다. 위에서 새로운 목표를 추가해보세요!")

# 푸터
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: white; padding: 20px; opacity: 0.8;">
    <p style="font-size: 16px; margin: 10px 0;">💡 <strong>팁</strong>: 체크박스를 클릭하면 AI가 응원 메시지를 보내드려요!</p>
    <p style="font-size: 14px; margin-top: 15px;">Made with ❤️ using Streamlit</p>
</div>
""", unsafe_allow_html=True)

