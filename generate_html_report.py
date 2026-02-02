"""
AI 활용 역량 진단 시스템 - HTML 리포트 생성
상세한 분석 결과를 HTML 형식으로 출력
"""

from datetime import datetime
import json

def generate_html_report(user_info, scores, analysis):
    """
    HTML 형식의 상세 리포트 생성
    
    Args:
        user_info: 사용자 정보 (이름, 부서, 직위)
        scores: 점수 데이터
        analysis: 분석 결과
    
    Returns:
        HTML 문자열
    """
    
    # 레벨별 색상
    level_colors = {
        "초급": "#ff6b6b",
        "중급": "#4ecdc4",
        "고급": "#45b7d1",
        "전문가": "#96ceb4"
    }
    
    level = scores["level"]
    level_color = level_colors.get(level, "#4ecdc4")
    
    html = f"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI 활용 역량 진단 리포트 - {user_info['name']}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', 'Malgun Gothic', sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        .header .subtitle {{
            font-size: 1.2em;
            opacity: 0.9;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .user-info {{
            background: #f8f9fa;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            border-left: 5px solid {level_color};
        }}
        
        .user-info h2 {{
            color: #2c3e50;
            margin-bottom: 20px;
            font-size: 1.8em;
        }}
        
        .info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
        }}
        
        .info-item {{
            background: white;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        
        .info-label {{
            font-weight: bold;
            color: #7f8c8d;
            font-size: 0.9em;
            margin-bottom: 5px;
        }}
        
        .info-value {{
            color: #2c3e50;
            font-size: 1.1em;
        }}
        
        .score-summary {{
            background: linear-gradient(135deg, {level_color} 0%, {level_color}dd 100%);
            color: white;
            border-radius: 15px;
            padding: 40px;
            margin-bottom: 30px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}
        
        .score-summary h2 {{
            font-size: 2em;
            margin-bottom: 20px;
        }}
        
        .total-score {{
            font-size: 4em;
            font-weight: bold;
            margin: 20px 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        .level-badge {{
            display: inline-block;
            background: rgba(255,255,255,0.3);
            padding: 10px 30px;
            border-radius: 50px;
            font-size: 1.5em;
            font-weight: bold;
            margin-top: 10px;
        }}
        
        .section {{
            margin-bottom: 40px;
        }}
        
        .section h2 {{
            color: #2c3e50;
            font-size: 1.8em;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid {level_color};
        }}
        
        .category-scores {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .category-card {{
            background: #f8f9fa;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s, box-shadow 0.3s;
        }}
        
        .category-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        }}
        
        .category-name {{
            font-size: 1.3em;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 15px;
        }}
        
        .progress-bar {{
            background: #e0e0e0;
            border-radius: 10px;
            height: 30px;
            overflow: hidden;
            margin-bottom: 10px;
        }}
        
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, {level_color} 0%, {level_color}cc 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            transition: width 1s ease-out;
        }}
        
        .score-detail {{
            color: #7f8c8d;
            font-size: 0.95em;
        }}
        
        .assessment-box {{
            background: #fff3cd;
            border-left: 5px solid #ffc107;
            padding: 25px;
            border-radius: 10px;
            margin-bottom: 25px;
        }}
        
        .assessment-box p {{
            line-height: 1.8;
            font-size: 1.1em;
            color: #856404;
        }}
        
        .strength-weakness {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        @media (max-width: 768px) {{
            .strength-weakness {{
                grid-template-columns: 1fr;
            }}
        }}
        
        .strength-box, .weakness-box {{
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        
        .strength-box {{
            background: #d4edda;
            border-left: 5px solid #28a745;
        }}
        
        .weakness-box {{
            background: #f8d7da;
            border-left: 5px solid #dc3545;
        }}
        
        .strength-box h3 {{
            color: #155724;
            margin-bottom: 15px;
        }}
        
        .weakness-box h3 {{
            color: #721c24;
            margin-bottom: 15px;
        }}
        
        .item-list {{
            list-style: none;
        }}
        
        .item-list li {{
            padding: 10px;
            margin-bottom: 10px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        
        .item-category {{
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 5px;
        }}
        
        .item-percentage {{
            color: #7f8c8d;
            font-size: 0.9em;
        }}
        
        .item-comment {{
            color: #555;
            font-size: 0.95em;
            margin-top: 5px;
        }}
        
        .recommendations {{
            background: #e7f3ff;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
        }}
        
        .recommendations h3 {{
            color: #004085;
            margin-bottom: 20px;
            font-size: 1.5em;
        }}
        
        .recommendations ul {{
            list-style: none;
        }}
        
        .recommendations li {{
            padding: 15px;
            margin-bottom: 10px;
            background: white;
            border-radius: 8px;
            border-left: 4px solid #007bff;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        
        .recommendations li:before {{
            content: "✓ ";
            color: #007bff;
            font-weight: bold;
            margin-right: 10px;
        }}
        
        .learning-path {{
            margin-bottom: 30px;
        }}
        
        .learning-card {{
            background: white;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            border-left: 5px solid {level_color};
        }}
        
        .learning-priority {{
            display: inline-block;
            background: {level_color};
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        
        .learning-title {{
            font-size: 1.4em;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 15px;
        }}
        
        .learning-progress {{
            display: flex;
            align-items: center;
            margin-bottom: 15px;
        }}
        
        .learning-progress .current {{
            font-size: 1.2em;
            color: #e74c3c;
            font-weight: bold;
        }}
        
        .learning-progress .arrow {{
            margin: 0 15px;
            color: #7f8c8d;
        }}
        
        .learning-progress .target {{
            font-size: 1.2em;
            color: #27ae60;
            font-weight: bold;
        }}
        
        .learning-resources {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
        }}
        
        .learning-resources h4 {{
            color: #2c3e50;
            margin-bottom: 10px;
        }}
        
        .learning-resources ul {{
            list-style: none;
        }}
        
        .learning-resources li {{
            padding: 8px 0;
            color: #555;
            border-bottom: 1px solid #e0e0e0;
        }}
        
        .learning-resources li:last-child {{
            border-bottom: none;
        }}
        
        .learning-resources li:before {{
            content: "📚 ";
            margin-right: 8px;
        }}
        
        .footer {{
            background: #2c3e50;
            color: white;
            text-align: center;
            padding: 30px;
            font-size: 0.9em;
        }}
        
        .footer p {{
            margin: 5px 0;
        }}
        
        @media print {{
            body {{
                background: white;
                padding: 0;
            }}
            
            .container {{
                box-shadow: none;
            }}
            
            .category-card:hover {{
                transform: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- 헤더 -->
        <div class="header">
            <h1>🎯 AI 활용 역량 진단 리포트</h1>
            <div class="subtitle">공공기관 근무자 AI 역량 평가</div>
        </div>
        
        <!-- 컨텐츠 -->
        <div class="content">
            <!-- 사용자 정보 -->
            <div class="user-info">
                <h2>📋 진단 정보</h2>
                <div class="info-grid">
                    <div class="info-item">
                        <div class="info-label">이름</div>
                        <div class="info-value">{user_info['name']}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">소속 부서</div>
                        <div class="info-value">{user_info['department']}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">직위</div>
                        <div class="info-value">{user_info['position']}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">진단 일시</div>
                        <div class="info-value">{datetime.now().strftime('%Y년 %m월 %d일')}</div>
                    </div>
                </div>
            </div>
            
            <!-- 종합 점수 -->
            <div class="score-summary">
                <h2>종합 점수</h2>
                <div class="total-score">{scores['total_score']} / {scores['total_max']}</div>
                <div style="font-size: 1.5em; margin: 10px 0;">달성률: {scores['percentage']}%</div>
                <div class="level-badge">{level} 레벨</div>
            </div>
            
            <!-- 전체 평가 -->
            <div class="section">
                <h2>📊 전체 평가</h2>
                <div class="assessment-box">
                    <p>{analysis['overall_assessment']}</p>
                </div>
            </div>
            
            <!-- 영역별 상세 점수 -->
            <div class="section">
                <h2>📈 영역별 상세 점수</h2>
                <div class="category-scores">
"""
    
    # 영역별 점수 카드
    for category_id, category_data in scores['category_scores'].items():
        percentage = category_data['percentage']
        
        # 퍼센트에 따른 색상
        if percentage >= 70:
            bar_color = "#28a745"
        elif percentage >= 50:
            bar_color = "#ffc107"
        else:
            bar_color = "#dc3545"
        
        html += f"""
                    <div class="category-card">
                        <div class="category-name">{category_data['name']}</div>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: {percentage}%; background: {bar_color};">
                                {percentage}%
                            </div>
                        </div>
                        <div class="score-detail">
                            {category_data['score']} / {category_data['max_score']} 점
                        </div>
                    </div>
"""
    
    html += """
                </div>
            </div>
            
            <!-- 강점과 약점 -->
            <div class="section">
                <h2>💪 강점 및 개선 영역</h2>
                <div class="strength-weakness">
                    <div class="strength-box">
                        <h3>✨ 강점 영역</h3>
"""
    
    # 강점
    if analysis['strengths']:
        html += '<ul class="item-list">'
        for item in analysis['strengths']:
            html += f"""
                        <li>
                            <div class="item-category">{item['category']}</div>
                            <div class="item-percentage">달성률: {item['percentage']}%</div>
                            <div class="item-comment">{item['comment']}</div>
                        </li>
"""
        html += '</ul>'
    else:
        html += '<p style="color: #155724;">모든 영역에서 균형 잡힌 발전이 필요합니다.</p>'
    
    html += """
                    </div>
                    
                    <div class="weakness-box">
                        <h3>📌 개선 영역</h3>
"""
    
    # 약점
    if analysis['weaknesses']:
        html += '<ul class="item-list">'
        for item in analysis['weaknesses']:
            html += f"""
                        <li>
                            <div class="item-category">{item['category']}</div>
                            <div class="item-percentage">달성률: {item['percentage']}%</div>
                            <div class="item-comment">{item['comment']}</div>
                        </li>
"""
        html += '</ul>'
    else:
        html += '<p style="color: #721c24;">모든 영역에서 우수한 수준입니다!</p>'
    
    html += """
                    </div>
                </div>
            </div>
            
            <!-- 맞춤형 추천사항 -->
            <div class="section">
                <h2>💡 맞춤형 추천사항</h2>
                <div class="recommendations">
                    <h3>{} 레벨 맞춤 추천</h3>
                    <ul>
""".format(level)
    
    for rec in analysis['recommendations']:
        html += f'                        <li>{rec}</li>\n'
    
    html += """
                    </ul>
                </div>
            </div>
            
            <!-- 우선순위 학습 경로 -->
            <div class="section">
                <h2>🎓 우선순위 학습 경로</h2>
                <div class="learning-path">
"""
    
    # 학습 경로
    for path in analysis['learning_path']:
        html += f"""
                    <div class="learning-card">
                        <span class="learning-priority">우선순위 {path['priority']}</span>
                        <div class="learning-title">{path['category']}</div>
                        <div class="learning-progress">
                            <span class="current">현재 {path['current_score']}%</span>
                            <span class="arrow">→</span>
                            <span class="target">목표 {path['target_score']}%</span>
                        </div>
                        <div class="learning-resources">
                            <h4>추천 학습 자료</h4>
                            <ul>
"""
        
        for resource in path['resources']:
            html += f'                                <li>{resource}</li>\n'
        
        html += """
                            </ul>
                        </div>
                    </div>
"""
    
    html += """
                </div>
            </div>
        </div>
        
        <!-- 푸터 -->
        <div class="footer">
            <p><strong>AI 활용 역량 진단 시스템</strong></p>
            <p>본 리포트는 개인의 AI 활용 역량 향상을 위한 참고 자료입니다.</p>
            <p>© 2024 AI Skill Assessment System. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
"""
    
    return html


def save_html_report(html_content, filename="ai_skill_report.html"):
    """HTML 리포트를 파일로 저장"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        return True
    except Exception as e:
        print(f"파일 저장 중 오류 발생: {e}")
        return False


# 테스트용 코드
if __name__ == "__main__":
    # 샘플 데이터
    user_info = {
        "name": "홍길동",
        "department": "디지털혁신과",
        "position": "주무관"
    }
    
    scores = {
        "total_score": 52,
        "total_max": 75,
        "percentage": 69.3,
        "level": "고급",
        "category_scores": {
            "basic": {
                "name": "AI 기본 이해도",
                "score": 12,
                "max_score": 15,
                "percentage": 80.0
            },
            "automation": {
                "name": "업무 자동화 활용",
                "score": 10,
                "max_score": 15,
                "percentage": 66.7
            },
            "data_analysis": {
                "name": "데이터 분석 및 의사결정",
                "score": 9,
                "max_score": 15,
                "percentage": 60.0
            },
            "practical_tools": {
                "name": "AI 도구 실무 활용",
                "score": 11,
                "max_score": 15,
                "percentage": 73.3
            },
            "ethics_security": {
                "name": "AI 윤리 및 보안 인식",
                "score": 10,
                "max_score": 15,
                "percentage": 66.7
            }
        }
    }
    
    analysis = {
        "overall_assessment": "현재 AI 활용 역량은 고급(69.3%)입니다...",
        "strengths": [
            {
                "category": "AI 기본 이해도",
                "score": 12,
                "percentage": 80.0,
                "comment": "AI 기본 개념에 대한 이해가 우수합니다."
            }
        ],
        "weaknesses": [
            {
                "category": "데이터 분석 및 의사결정",
                "score": 9,
                "percentage": 60.0,
                "comment": "데이터 분석 역량 강화가 필요합니다."
            }
        ],
        "recommendations": [
            "조직 내 AI 활용 가이드 작성하기",
            "AI 활용 워크숍 개최하기"
        ],
        "learning_path": [
            {
                "priority": 1,
                "category": "데이터 분석 및 의사결정",
                "current_score": 60.0,
                "target_score": 80.0,
                "resources": [
                    "온라인 강의: AI 데이터 분석",
                    "도서: 데이터 기반 의사결정"
                ]
            }
        ]
    }
    
    # HTML 생성 및 저장
    html = generate_html_report(user_info, scores, analysis)
    if save_html_report(html):
        print("✅ HTML 리포트가 생성되었습니다: ai_skill_report.html")
    else:
        print("❌ 리포트 생성 실패")
