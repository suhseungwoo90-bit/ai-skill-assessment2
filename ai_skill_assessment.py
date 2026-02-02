#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
공공기관 근무자 AI 활용 역량 진단 시스템
"""

import json
from datetime import datetime
from typing import Dict, List, Tuple

# 진단 문항 데이터베이스
ASSESSMENT_DATA = {
    "categories": [
        {
            "id": "basic",
            "name": "AI 기본 이해도",
            "description": "AI 기술에 대한 기본적인 이해와 개념 파악",
            "questions": [
                {
                    "id": "Q1",
                    "text": "생성형 AI(ChatGPT, Claude 등)가 무엇인지 이해하고 설명할 수 있다",
                    "type": "likert"
                },
                {
                    "id": "Q2", 
                    "text": "AI와 자동화의 차이점을 이해하고 있다",
                    "type": "likert"
                },
                {
                    "id": "Q3",
                    "text": "AI가 공공서비스 혁신에 어떻게 활용될 수 있는지 알고 있다",
                    "type": "likert"
                }
            ]
        },
        {
            "id": "automation",
            "name": "업무 자동화 활용",
            "description": "반복 업무와 문서 작업의 AI 자동화 능력",
            "questions": [
                {
                    "id": "Q4",
                    "text": "AI를 활용하여 보고서나 공문을 작성한 경험이 있다",
                    "type": "likert"
                },
                {
                    "id": "Q5",
                    "text": "엑셀, 문서 작업 시 AI 도구를 활용하여 시간을 단축하고 있다",
                    "type": "likert"
                },
                {
                    "id": "Q6",
                    "text": "회의록, 요약문 등을 AI로 생성하고 검토하여 활용한다",
                    "type": "likert"
                }
            ]
        },
        {
            "id": "data_analysis",
            "name": "데이터 분석 및 의사결정",
            "description": "데이터 기반 정책 수립 및 분석 역량",
            "questions": [
                {
                    "id": "Q7",
                    "text": "AI를 활용하여 데이터를 분석하고 인사이트를 도출한 경험이 있다",
                    "type": "likert"
                },
                {
                    "id": "Q8",
                    "text": "정책 수립이나 의사결정 시 AI 분석 결과를 참고한다",
                    "type": "likert"
                },
                {
                    "id": "Q9",
                    "text": "민원 데이터나 업무 데이터를 AI로 분석하여 개선점을 찾는다",
                    "type": "likert"
                }
            ]
        },
        {
            "id": "practical_tools",
            "name": "AI 도구 실무 활용",
            "description": "실제 AI 도구 사용 경험과 숙련도",
            "questions": [
                {
                    "id": "Q10",
                    "text": "ChatGPT, Claude, Copilot 등 AI 챗봇을 업무에 주 3회 이상 활용한다",
                    "type": "likert"
                },
                {
                    "id": "Q11",
                    "text": "프롬프트(질문 방법)를 효과적으로 작성하여 원하는 결과를 얻는다",
                    "type": "likert"
                },
                {
                    "id": "Q12",
                    "text": "업무에 필요한 새로운 AI 도구를 스스로 찾아서 학습한다",
                    "type": "likert"
                }
            ]
        },
        {
            "id": "ethics_security",
            "name": "AI 윤리 및 보안 인식",
            "description": "공공기관 특성에 맞는 AI 활용 시 주의사항 이해",
            "questions": [
                {
                    "id": "Q13",
                    "text": "AI 활용 시 개인정보 보호와 보안 규정을 준수한다",
                    "type": "likert"
                },
                {
                    "id": "Q14",
                    "text": "AI가 생성한 결과물의 정확성을 검증하고 책임감 있게 활용한다",
                    "type": "likert"
                },
                {
                    "id": "Q15",
                    "text": "AI 편향성과 윤리적 문제를 인식하고 있다",
                    "type": "likert"
                }
            ]
        }
    ],
    "likert_scale": {
        1: "전혀 그렇지 않다",
        2: "그렇지 않다",
        3: "보통이다",
        4: "그렇다",
        5: "매우 그렇다"
    }
}

# 레벨 기준
LEVEL_CRITERIA = {
    "초급": {"min": 0, "max": 30, "description": "AI 활용 시작 단계"},
    "중급": {"min": 31, "max": 50, "description": "AI 기본 활용 가능"},
    "고급": {"min": 51, "max": 65, "description": "AI 능숙한 활용"},
    "전문가": {"min": 66, "max": 75, "description": "AI 고도화 활용"}
}

class AISkillAssessment:
    """AI 활용 역량 진단 클래스"""
    
    def __init__(self):
        self.data = ASSESSMENT_DATA
        self.responses = {}
        
    def calculate_scores(self, responses: Dict[str, int]) -> Dict:
        """점수 계산"""
        self.responses = responses
        
        # 영역별 점수 계산
        category_scores = {}
        for category in self.data["categories"]:
            cat_id = category["id"]
            questions = [q["id"] for q in category["questions"]]
            score = sum(responses.get(q_id, 0) for q_id in questions)
            max_score = len(questions) * 5
            percentage = (score / max_score) * 100
            
            category_scores[cat_id] = {
                "name": category["name"],
                "score": score,
                "max_score": max_score,
                "percentage": round(percentage, 1)
            }
        
        # 총점 계산
        total_score = sum(cs["score"] for cs in category_scores.values())
        total_max = sum(cs["max_score"] for cs in category_scores.values())
        
        # 레벨 판정
        level = self._determine_level(total_score)
        
        return {
            "total_score": total_score,
            "total_max": total_max,
            "percentage": round((total_score / total_max) * 100, 1),
            "level": level,
            "category_scores": category_scores,
            "timestamp": datetime.now().isoformat()
        }
    
    def _determine_level(self, score: int) -> str:
        """레벨 판정"""
        for level, criteria in LEVEL_CRITERIA.items():
            if criteria["min"] <= score <= criteria["max"]:
                return level
        return "초급"
    
    def generate_analysis(self, scores: Dict) -> Dict:
        """상세 분석 생성"""
        analysis = {
            "overall_assessment": self._generate_overall_assessment(scores),
            "strengths": self._identify_strengths(scores),
            "weaknesses": self._identify_weaknesses(scores),
            "recommendations": self._generate_recommendations(scores),
            "learning_path": self._create_learning_path(scores)
        }
        return analysis
    
    def _generate_overall_assessment(self, scores: Dict) -> str:
        """전체 평가 생성"""
        level = scores["level"]
        percentage = scores["percentage"]
        
        assessments = {
            "초급": f"현재 AI 활용 역량은 '{level}' 수준입니다 ({percentage}점). "
                   "AI 도구에 대한 기본적인 이해와 경험이 부족한 상태입니다. "
                   "체계적인 학습을 통해 업무에 AI를 적용하기 시작하는 것이 필요합니다.",
            
            "중급": f"현재 AI 활용 역량은 '{level}' 수준입니다 ({percentage}점). "
                   "AI 도구를 업무에 부분적으로 활용하고 있으나, 더 깊이 있는 활용이 가능합니다. "
                   "실무 적용 사례를 늘리고 고급 기능을 학습하면 업무 효율을 크게 높일 수 있습니다.",
            
            "고급": f"현재 AI 활용 역량은 '{level}' 수준입니다 ({percentage}점). "
                   "AI 도구를 능숙하게 활용하여 업무 효율을 높이고 있습니다. "
                   "이제는 팀 내 AI 활용을 선도하고, 고도화된 AI 전략을 수립할 수 있는 단계입니다.",
            
            "전문가": f"현재 AI 활용 역량은 '{level}' 수준입니다 ({percentage}점). "
                    "AI 도구를 전문가 수준으로 활용하고 있으며, 조직의 디지털 전환을 이끌 수 있습니다. "
                    "다른 구성원들의 멘토 역할과 AI 활용 문화 확산에 기여할 수 있습니다."
        }
        
        return assessments.get(level, assessments["초급"])
    
    def _identify_strengths(self, scores: Dict) -> List[Dict]:
        """강점 영역 파악"""
        strengths = []
        category_scores = scores["category_scores"]
        
        # 70% 이상인 영역을 강점으로 판단
        for cat_id, cat_score in category_scores.items():
            if cat_score["percentage"] >= 70:
                category = next(c for c in self.data["categories"] if c["id"] == cat_id)
                strengths.append({
                    "category": cat_score["name"],
                    "score": cat_score["percentage"],
                    "description": category["description"],
                    "comment": self._get_strength_comment(cat_id)
                })
        
        # 점수 순으로 정렬
        strengths.sort(key=lambda x: x["score"], reverse=True)
        return strengths[:3]  # 상위 3개만
    
    def _identify_weaknesses(self, scores: Dict) -> List[Dict]:
        """약점 영역 파악"""
        weaknesses = []
        category_scores = scores["category_scores"]
        
        # 60% 미만인 영역을 약점으로 판단
        for cat_id, cat_score in category_scores.items():
            if cat_score["percentage"] < 60:
                category = next(c for c in self.data["categories"] if c["id"] == cat_id)
                weaknesses.append({
                    "category": cat_score["name"],
                    "score": cat_score["percentage"],
                    "description": category["description"],
                    "comment": self._get_weakness_comment(cat_id)
                })
        
        # 점수 순으로 정렬 (낮은 순)
        weaknesses.sort(key=lambda x: x["score"])
        return weaknesses[:3]  # 하위 3개만
    
    def _get_strength_comment(self, category_id: str) -> str:
        """강점 코멘트"""
        comments = {
            "basic": "AI 기술에 대한 이해도가 높아 새로운 AI 도구를 빠르게 습득할 수 있습니다.",
            "automation": "업무 자동화를 잘 활용하여 효율성을 높이고 있습니다.",
            "data_analysis": "데이터 기반 의사결정 능력이 우수하여 정책 수립에 강점이 있습니다.",
            "practical_tools": "다양한 AI 도구를 실전에서 능숙하게 활용하고 있습니다.",
            "ethics_security": "AI 윤리와 보안에 대한 인식이 높아 책임감 있게 활용하고 있습니다."
        }
        return comments.get(category_id, "")
    
    def _get_weakness_comment(self, category_id: str) -> str:
        """약점 코멘트"""
        comments = {
            "basic": "AI 기본 개념 학습이 필요합니다. 입문 과정부터 시작하는 것을 추천합니다.",
            "automation": "반복 업무를 AI로 자동화하는 연습이 필요합니다. 실습 중심 학습을 추천합니다.",
            "data_analysis": "데이터 분석 도구 활용 경험을 쌓아야 합니다. 실제 업무 데이터로 실습해보세요.",
            "practical_tools": "AI 도구 사용 경험이 부족합니다. 매일 조금씩 사용해보는 것을 추천합니다.",
            "ethics_security": "AI 윤리와 보안에 대한 이해가 필요합니다. 공공기관 가이드라인을 숙지하세요."
        }
        return comments.get(category_id, "")
    
    def _generate_recommendations(self, scores: Dict) -> List[str]:
        """맞춤형 추천사항"""
        level = scores["level"]
        recommendations = []
        
        if level == "초급":
            recommendations = [
                "📚 생성형 AI 기초 강의를 수강하여 개념을 이해하세요",
                "💻 ChatGPT 또는 Claude를 업무에 하루 10분씩 사용해보세요",
                "👥 AI 활용 사례를 동료들과 공유하며 학습하세요",
                "📝 간단한 문서 작성부터 AI를 활용해보세요"
            ]
        elif level == "중급":
            recommendations = [
                "🎯 프롬프트 엔지니어링 기술을 학습하세요",
                "🔧 업무별 AI 도구(문서작성, 데이터분석 등)를 심화 학습하세요",
                "📊 데이터 분석을 위한 AI 활용법을 익히세요",
                "🤝 팀 내에서 AI 활용 사례를 공유하고 확산하세요"
            ]
        elif level == "고급":
            recommendations = [
                "🚀 조직의 AI 활용 전략 수립에 참여하세요",
                "👨‍🏫 다른 구성원들의 AI 활용을 지도하고 멘토링하세요",
                "🔬 고급 AI 도구와 자동화 워크플로우를 구축하세요",
                "📈 AI 활용 성과를 측정하고 개선점을 도출하세요"
            ]
        else:  # 전문가
            recommendations = [
                "🎓 AI 최신 트렌드를 지속적으로 학습하고 공유하세요",
                "🏢 조직의 디지털 전환을 이끄는 리더 역할을 하세요",
                "✍️ AI 활용 가이드라인과 베스트 프랙티스를 문서화하세요",
                "🌟 외부 컨퍼런스나 세미나에서 경험을 공유하세요"
            ]
        
        return recommendations
    
    def _create_learning_path(self, scores: Dict) -> List[Dict]:
        """학습 경로 생성"""
        category_scores = scores["category_scores"]
        learning_path = []
        
        # 점수가 낮은 순서대로 학습 우선순위 설정
        sorted_categories = sorted(
            category_scores.items(),
            key=lambda x: x[1]["percentage"]
        )
        
        for idx, (cat_id, cat_score) in enumerate(sorted_categories[:3], 1):
            learning_resources = self._get_learning_resources(cat_id)
            learning_path.append({
                "priority": idx,
                "category": cat_score["name"],
                "current_score": cat_score["percentage"],
                "target_score": min(cat_score["percentage"] + 20, 100),
                "resources": learning_resources
            })
        
        return learning_path
    
    def _get_learning_resources(self, category_id: str) -> List[Dict]:
        """카테고리별 학습 자료"""
        resources = {
            "basic": [
                {"type": "온라인 강의", "title": "생성형 AI 이해하기", "duration": "2시간", "level": "입문"},
                {"type": "도서", "title": "ChatGPT 제대로 활용하기", "duration": "자율학습", "level": "입문"},
                {"type": "실습", "title": "AI 챗봇 기본 사용법", "duration": "1시간", "level": "입문"}
            ],
            "automation": [
                {"type": "온라인 강의", "title": "공공기관 문서 작성 AI 자동화", "duration": "3시간", "level": "초급"},
                {"type": "실습", "title": "보고서 작성 실전 프로젝트", "duration": "2시간", "level": "초급"},
                {"type": "가이드", "title": "업무별 AI 자동화 템플릿", "duration": "자율학습", "level": "초급"}
            ],
            "data_analysis": [
                {"type": "온라인 강의", "title": "AI 데이터 분석 기초", "duration": "4시간", "level": "중급"},
                {"type": "실습", "title": "정책 데이터 분석 프로젝트", "duration": "3시간", "level": "중급"},
                {"type": "도구", "title": "데이터 분석 AI 도구 활용", "duration": "2시간", "level": "중급"}
            ],
            "practical_tools": [
                {"type": "실습", "title": "프롬프트 엔지니어링 마스터", "duration": "3시간", "level": "중급"},
                {"type": "워크샵", "title": "업무별 AI 도구 실전", "duration": "4시간", "level": "중급"},
                {"type": "커뮤니티", "title": "AI 활용 사례 스터디", "duration": "지속", "level": "중급"}
            ],
            "ethics_security": [
                {"type": "필수교육", "title": "공공기관 AI 활용 가이드라인", "duration": "2시간", "level": "필수"},
                {"type": "온라인 강의", "title": "AI 윤리와 책임", "duration": "2시간", "level": "초급"},
                {"type": "문서", "title": "개인정보보호 체크리스트", "duration": "30분", "level": "필수"}
            ]
        }
        
        return resources.get(category_id, [])
