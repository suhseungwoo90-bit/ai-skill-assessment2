"""
AI 활용 역량 진단 시스템 - Streamlit 버전
"""

import streamlit as st
import json
from datetime import datetime
import os
from ai_skill_assessment import AISkillAssessment, ASSESSMENT_DATA, LEVEL_CRITERIA
from generate_html_report import generate_html_report

# 페이지 설정
st.set_page_config(
    page_title="AI 활용 역량 진단",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .score-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    .category-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #667eea;
        margin: 1rem 0;
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 5px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'user_info' not in st.session_state:
    st.session_state.user_info = {}
if 'responses' not in st.session_state:
    st.session_state.responses = {}
if 'results' not in st.session_state:
    st.session_state.results = None

# 결과 저장 디렉토리
RESULTS_DIR = "results"
os.makedirs(RESULTS_DIR, exist_ok=True)

def save_result(user_info, scores, analysis):
    """결과 저장"""
    result_id = datetime.now().strftime('%Y%m%d_%H%M%S')
    result_data = {
        'user_info': user_info,
        'scores': scores,
        'analysis': analysis
    }
    
    filepath = os.path.join(RESULTS_DIR, f'{result_id}.json')
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(result_data, f, ensure_ascii=False, indent=2)
    
    return result_id

def load_all_results():
    """전체 결과 불러오기"""
    results = []
    if os.path.exists(RESULTS_DIR):
        for filename in sorted(os.listdir(RESULTS_DIR), reverse=True):
            if filename.endswith('.json'):
                filepath = os.path.join(RESULTS_DIR, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    results.append({
                        'id': filename.replace('.json', ''),
                        'user_info': data['user_info'],
                        'score': data['scores']['total_score'],
                        'level': data['scores']['level'],
                        'timestamp': data['scores']['timestamp']
                    })
    return results

# ==================== 메인 페이지 ====================
def show_home():
    st.markdown("""
    <div class="main-header">
        <h1>🎯 AI 활용 역량 진단 시스템</h1>
        <p style="font-size: 1.2em;">공공기관 근무자 대상 맞춤형 진단</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("⏱️ **소요 시간**\n\n약 10분")
    with col2:
        st.info("📝 **문항 수**\n\n15개 (5개 영역)")
    with col3:
        st.info("📊 **결과물**\n\n상세 분석 리포트")
    
    st.markdown("### 📊 진단 영역")
    
    areas = [
        ("1️⃣", "AI 기본 이해도", "AI 개념과 기술 이해"),
        ("2️⃣", "업무 자동화", "AI로 업무 효율화"),
        ("3️⃣", "데이터 분석", "데이터 기반 의사결정"),
        ("4️⃣", "실무 활용", "AI 도구 사용 능력"),
        ("5️⃣", "윤리/보안", "책임감 있는 AI 활용")
    ]
    
    cols = st.columns(5)
    for i, (icon, title, desc) in enumerate(areas):
        with cols[i]:
            st.markdown(f"""
            <div style="background: white; padding: 1rem; border-radius: 10px; 
                        box-shadow: 0 2px 5px rgba(0,0,0,0.1); text-align: center;">
                <div style="font-size: 2em;">{icon}</div>
                <div style="font-weight: bold; margin: 0.5rem 0;">{title}</div>
                <div style="font-size: 0.9em; color: #666;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        if st.button("🚀 진단 시작하기", use_container_width=True):
            st.session_state.page = 'assessment'
            st.rerun()

# ==================== 진단 페이지 ====================
def show_assessment():
    st.markdown("""
    <div class="main-header">
        <h1>📝 AI 활용 역량 진단</h1>
        <p>솔직하게 답변해주세요 (약 10분 소요)</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 사용자 정보 입력
    st.markdown("### 👤 기본 정보")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        name = st.text_input("이름 *", placeholder="예: 홍길동")
    with col2:
        department = st.text_input("부서명 *", placeholder="예: 디지털혁신과")
    with col3:
        position = st.text_input("직위 *", placeholder="예: 주무관")
    
    if not all([name, department, position]):
        st.warning("⚠️ 모든 기본 정보를 입력해주세요.")
        return
    
    st.session_state.user_info = {
        'name': name,
        'department': department,
        'position': position
    }
    
    # 진단 문항
    st.markdown("---")
    responses = {}
    
    for cat_idx, category in enumerate(ASSESSMENT_DATA['categories'], 1):
        st.markdown(f"""
        <div class="category-card">
            <h3>{cat_idx}. {category['name']}</h3>
            <p style="color: #666; font-style: italic;">{category['description']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        for question in category['questions']:
            st.markdown(f"**{question['id']}. {question['text']}**")
            
            response = st.radio(
                "",
                options=[1, 2, 3, 4, 5],
                format_func=lambda x: ASSESSMENT_DATA['likert_scale'][x],
                key=question['id'],
                horizontal=True
            )
            responses[question['id']] = response
            st.markdown("<br>", unsafe_allow_html=True)
    
    st.session_state.responses = responses
    
    # 제출 버튼
    st.markdown("---")
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        if st.button("✅ 진단 완료 및 결과 확인", use_container_width=True):
            if len(responses) == 15:
                assessment = AISkillAssessment()
                scores = assessment.calculate_scores(responses)
                analysis = assessment.generate_analysis(scores)
                
                result_id = save_result(st.session_state.user_info, scores, analysis)
                
                st.session_state.results = {
                    'user_info': st.session_state.user_info,
                    'scores': scores,
                    'analysis': analysis,
                    'result_id': result_id
                }
                
                st.session_state.page = 'result'
                st.rerun()
            else:
                st.error("모든 문항에 응답해주세요!")

# ==================== 결과 페이지 ====================
def show_result():
    if st.session_state.results is None:
        st.error("진단 결과가 없습니다. 먼저 진단을 완료해주세요.")
        if st.button("🏠 처음으로"):
            st.session_state.page = 'home'
            st.rerun()
        return
    
    results = st.session_state.results
    scores = results['scores']
    analysis = results['analysis']
    user_info = results['user_info']
    
    st.markdown(f"""
    <div class="main-header">
        <h1>🎯 진단 결과</h1>
        <p>{user_info['name']} 님의 AI 활용 역량 분석</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="score-card">
        <h2>📊 종합 결과</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("총점", f"{scores['total_score']}/{scores['total_max']}")
    with col2:
        st.metric("달성률", f"{scores['percentage']}%")
    with col3:
        st.metric("레벨", scores['level'])
    
    st.info(f"**📋 전체 평가**\n\n{analysis['overall_assessment']}")
    
    st.markdown("### 📊 영역별 상세 점수")
    
    for cat_id, cat_score in scores['category_scores'].items():
        percentage = cat_score['percentage']
        
        if percentage >= 80:
            status = "🟢"
        elif percentage >= 60:
            status = "🟡"
        else:
            status = "🔴"
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{status} {cat_score['name']}**")
            st.progress(percentage / 100)
        with col2:
            st.markdown(f"**{cat_score['score']}/{cat_score['max_score']}** ({percentage}%)")
    
    st.markdown("### ✨ 강점 영역")
    if analysis['strengths']:
        for strength in analysis['strengths']:
            st.success(f"""
**{strength['category']}** - {strength['score']}%

{strength['comment']}
            """)
    else:
        st.info("현재 두드러진 강점 영역이 없습니다.")
    
    st.markdown("### 📌 개선이 필요한 영역")
    if analysis['weaknesses']:
        for weakness in analysis['weaknesses']:
            st.warning(f"""
**{weakness['category']}** - {weakness['score']}%

{weakness['comment']}
            """)
    else:
        st.success("🎉 모든 영역에서 우수한 역량을 보이고 있습니다!")
    
    st.markdown("### 💡 맞춤형 추천사항")
    for i, rec in enumerate(analysis['recommendations'], 1):
        st.markdown(f"{i}. {rec}")
    
    st.markdown("### 📚 맞춤형 학습 경로")
    
    for path in analysis['learning_path']:
        with st.expander(f"🎯 우선순위 {path['priority']}: {path['category']}"):
            st.markdown(f"**현재 수준:** {path['current_score']}% → **목표 수준:** {path['target_score']}%")
            st.markdown("---")
            
            for resource in path['resources']:
                st.markdown(f"""
- **{resource['type']}**: {resource['title']}
  - 소요시간: {resource['duration']} | 난이도: {resource['level']}
                """)
    
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 HTML 리포트 다운로드", use_container_width=True):
            html_content = generate_html_report(
                {'scores': scores, 'analysis': analysis},
                user_info
            )
            st.download_button(
                label="💾 다운로드",
                data=html_content,
                file_name=f"AI역량진단_{user_info['name']}_{results['result_id']}.html",
                mime="text/html",
                use_container_width=True
            )
    
    with col2:
        if st.button("🔄 다시 진단하기", use_container_width=True):
            st.session_state.page = 'home'
            st.session_state.responses = {}
            st.session_state.results = None
            st.rerun()
    
    with col3:
        if st.button("🏠 처음으로", use_container_width=True):
            st.session_state.page = 'home'
            st.rerun()

# ==================== 관리자 페이지 ====================
def show_admin():
    st.markdown("""
    <div class="main-header">
        <h1>📊 관리자 페이지</h1>
        <p>전체 진단 결과 관리</p>
    </div>
    """, unsafe_allow_html=True)
    
    results = load_all_results()
    
    if not results:
        st.info("아직 진단 결과가 없습니다.")
        if st.button("🏠 처음으로"):
            st.session_state.page = 'home'
            st.rerun()
        return
    
    total_count = len(results)
    avg_score = sum(r['score'] for r in results) / total_count if total_count > 0 else 0
    expert_count = len([r for r in results if r['level'] in ['전문가', '고급']])
    avg_percentage = (avg_score / 75) * 100
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("총 진단 인원", total_count)
    col2.metric("평균 점수", f"{avg_score:.1f}")
    col3.metric("고급 이상", expert_count)
    col4.metric("평균 달성률", f"{avg_percentage:.1f}%")
    
    st.markdown("### 📈 레벨별 분포")
    level_counts = {
        '초급': len([r for r in results if r['level'] == '초급']),
        '중급': len([r for r in results if r['level'] == '중급']),
        '고급': len([r for r in results if r['level'] == '고급']),
        '전문가': len([r for r in results if r['level'] == '전문가'])
    }
    
    col1, col2, col3, col4 = st.columns(4)
    for i, (level, count) in enumerate(level_counts.items()):
        with [col1, col2, col3, col4][i]:
            percentage = (count / total_count * 100) if total_count > 0 else 0
            st.info(f"**{level}**\n\n{count}명 ({percentage:.1f}%)")
    
    st.markdown("### 📋 전체 진단 결과 목록")
    
    for result in results:
        with st.expander(
            f"{result['user_info']['name']} ({result['user_info']['department']}) - "
            f"{result['score']}점 / {result['level']}"
        ):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**이름:** {result['user_info']['name']}")
                st.write(f"**부서:** {result['user_info']['department']}")
                st.write(f"**직위:** {result['user_info']['position']}")
            with col2:
                st.write(f"**점수:** {result['score']}/75")
                st.write(f"**레벨:** {result['level']}")
                st.write(f"**진단일시:** {result['timestamp'][:19]}")
    
    st.markdown("---")
    if st.button("🏠 처음으로"):
        st.session_state.page = 'home'
        st.rerun()

# ==================== 메인 ====================
def main():
    with st.sidebar:
        st.markdown("### 🎯 메뉴")
        
        if st.button("🏠 메인", use_container_width=True):
            st.session_state.page = 'home'
            st.rerun()
        
        if st.button("📝 진단하기", use_container_width=True):
            st.session_state.page = 'assessment'
            st.rerun()
        
        if st.button("📊 관리자", use_container_width=True):
            st.session_state.page = 'admin'
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 📖 사용 안내")
        st.info("""
**진단 절차**
1. 기본 정보 입력
2. 15개 문항 응답
3. 결과 즉시 확인
4. 리포트 다운로드

**소요 시간:** 약 10분
        """)
    
    if st.session_state.page == 'home':
        show_home()
    elif st.session_state.page == 'assessment':
        show_assessment()
    elif st.session_state.page == 'result':
        show_result()
    elif st.session_state.page == 'admin':
        show_admin()

if __name__ == "__main__":
    main()
