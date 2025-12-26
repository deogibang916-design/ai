# ✅ 나의 체크리스트 앱

Streamlit으로 만든 하루/한달 체크리스트 관리 앱입니다.

## 📋 주요 기능

### 1. 하루 체크리스트
- 오늘 해야 할 일들을 체크리스트 형식으로 관리
- 할 일 추가 및 완료 체크
- 실시간 진행률 표시
- 모든 할 일 완료 시 축하 효과

### 2. AI 응원 메시지
- 체크박스를 클릭할 때마다 다양한 응원 메시지 제공
- 긍정적인 피드백으로 동기부여

### 3. 한달 체크리스트
- 월간 목표 관리
- 장기 목표 추적
- 진행률 시각화

## 🚀 실행 방법

### 1. 필요한 패키지 설치
```bash
pip install streamlit
```

### 2. app.py 파일 생성

아래 코드를 복사해서 `app.py` 파일로 저장하세요:

```python
import streamlit as st
import json
from datetime import datetime
import random

# 페이지 설정
st.set_page_config(page_title="나의 체크리스트", page_icon="✅", layout="wide")

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
    st.header("오늘의 할 일")
    
    # 새 할일 추가
    col1, col2 = st.columns([4, 1])
    with col1:
        new_daily_task = st.text_input("새로운 할 일을 추가하세요", key="new_daily")
    with col2:
        if st.button("추가", key="add_daily"):
            if new_daily_task:
                st.session_state.daily_tasks.append({
                    'task': new_daily_task,
                    'completed': False,
                    'id': len(st.session_state.daily_tasks)
                })
                st.rerun()
    
    st.markdown("---")
    
    # 응원 메시지 표시
    if st.session_state.show_message:
        st.success(st.session_state.message)
        st.session_state.show_message = False
    
    # 체크리스트 표시
    if st.session_state.daily_tasks:
        for i, task in enumerate(st.session_state.daily_tasks):
            col1, col2 = st.columns([0.1, 0.9])
            
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
                    st.markdown(f"~~{task['task']}~~")
                else:
                    st.markdown(f"{task['task']}")
        
        # 진행률 표시
        completed = sum(1 for task in st.session_state.daily_tasks if task['completed'])
        total = len(st.session_state.daily_tasks)
        progress = completed / total if total > 0 else 0
        
        st.markdown("---")
        st.subheader(f"진행률: {completed}/{total} ({int(progress * 100)}%)")
        st.progress(progress)
        
        # 모두 완료 시 축하 메시지
        if completed == total and total > 0:
            st.balloons()
            st.success("🎊 오늘의 모든 할 일을 완료했어요! 정말 대단해요!")
        
        # 초기화 버튼
        if st.button("오늘 리스트 초기화", key="reset_daily"):
            st.session_state.daily_tasks = []
            st.rerun()
    else:
        st.info("아직 할 일이 없습니다. 위에서 새로운 할 일을 추가해보세요!")

# 한달 체크리스트 탭
with tab2:
    st.header("이번 달의 목표")
    
    # 새 목표 추가
    col1, col2 = st.columns([4, 1])
    with col1:
        new_monthly_task = st.text_input("새로운 월간 목표를 추가하세요", key="new_monthly")
    with col2:
        if st.button("추가", key="add_monthly"):
            if new_monthly_task:
                st.session_state.monthly_tasks.append({
                    'task': new_monthly_task,
                    'completed': False,
                    'id': len(st.session_state.monthly_tasks)
                })
                st.rerun()
    
    st.markdown("---")
    
    # 응원 메시지 표시
    if st.session_state.show_message:
        st.success(st.session_state.message)
        st.session_state.show_message = False
    
    # 체크리스트 표시
    if st.session_state.monthly_tasks:
        for i, task in enumerate(st.session_state.monthly_tasks):
            col1, col2 = st.columns([0.1, 0.9])
            
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
                    st.markdown(f"~~{task['task']}~~")
                else:
                    st.markdown(f"{task['task']}")
        
        # 진행률 표시
        completed = sum(1 for task in st.session_state.monthly_tasks if task['completed'])
        total = len(st.session_state.monthly_tasks)
        progress = completed / total if total > 0 else 0
        
        st.markdown("---")
        st.subheader(f"진행률: {completed}/{total} ({int(progress * 100)}%)")
        st.progress(progress)
        
        # 모두 완료 시 축하 메시지
        if completed == total and total > 0:
            st.balloons()
            st.success("🏆 이번 달 모든 목표를 달성했어요! 정말 자랑스러워요!")
        
        # 초기화 버튼
        if st.button("월간 리스트 초기화", key="reset_monthly"):
            st.session_state.monthly_tasks = []
            st.rerun()
    else:
        st.info("아직 월간 목표가 없습니다. 위에서 새로운 목표를 추가해보세요!")

# 푸터
st.markdown("---")
st.markdown("💡 **팁**: 체크박스를 클릭하면 AI가 응원 메시지를 보내드려요!")
```

### 3. 앱 실행
```bash
streamlit run app.py
```

## 📦 파일 구조
```
checklist-app/
│
├── app.py          # 메인 애플리케이션 파일
└── README.md       # 프로젝트 설명서
```

## 💡 사용 방법

1. **할 일 추가하기**
   - 텍스트 입력창에 할 일을 입력
   - "추가" 버튼 클릭

2. **할 일 완료하기**
   - 체크박스를 클릭하여 완료 표시
   - AI가 응원 메시지를 보내드립니다!

3. **진행률 확인하기**
   - 화면 하단에서 전체 진행률 확인
   - 모든 할 일 완료 시 축하 메시지

4. **리스트 초기화**
   - "리스트 초기화" 버튼으로 모든 항목 삭제

## 🎨 특징

- 📱 반응형 디자인
- 🎉 완료 시 시각적 피드백 (풍선 효과)
- 📊 실시간 진행률 시각화
- 💬 다양한 AI 응원 메시지
- 🔄 탭 전환으로 쉬운 네비게이션

## 🔮 향후 개선 사항

- 데이터 영구 저장 (JSON 파일)
- 완료된 할 일 히스토리
- 카테고리별 분류
- 우선순위 설정
- 알림 기능

## 📝 라이선스

이 프로젝트는 개인 사용 및 학습 목적으로 자유롭게 사용 가능합니다.

---

Made with ❤️ using Streamlit