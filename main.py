import google.generativeai as genai
import streamlit as st


# Gemini 설정
genai.configure(api_key="AIzaSyBUb315t4UmesRgf3xhNnyW15yFh_0KO1M") 

@st.cache_resource
def load_model():
    return genai.GenerativeModel("gemini-2.0-flash")

model = load_model()


# Puzzle 클래스
class Puzzle:
    def __init__(self, title, question, answer, success_message):
        self.title = title
        self.question = question
        self.answer = answer
        self.success_message = success_message


# PuzzleGame 클래스
class PuzzleGame:
    def __init__(self, puzzles):
        self.puzzles = puzzles
        self.current_index = 0
        self.game_over = False

    def current_puzzle(self):
        return self.puzzles[self.current_index]

    def check_answer(self, user_answer):
        current = self.current_puzzle()
        if user_answer.strip() == current.answer:
            self.current_index += 1
            if self.current_index >= len(self.puzzles):
                self.game_over = True
                # 마지막 퍼즐 → None 반환
                return None
            else:
                return current.success_message + "\n\n👉 다음 퍼즐로 이동합니다!"
        else:
            return "❌ 오답입니다. 다시 시도하세요!"


# 퍼즐 생성
puzzle1 = Puzzle(
    title="문제 1",
    question="우리 학교 이름은?",
    answer="남한고등학교",
    success_message="정답입니다!"
)

puzzle2 = Puzzle(
    title="문제 2",
    question="""전기 패널에는 빨강, 노랑, 파랑 신호등이 있습니다.
규칙 :
1. 빨강은 파랑보다 먼저 켜야 합니다.
2. 노랑은 빨강과 동시에 켤 수 없습니다.
3. 파랑은 노랑이 켜진 직후에 켜집니다.

빨강이 켜진 순간, 나머지 두 신호등의 상태는 무엇인가요?(노랑 파랑 순서대로 '꺼짐 켜짐'처럼 뛰어쓰기로 각각입력 )""",
    answer="꺼짐 꺼짐",
    success_message="정답입니다!"
)

puzzle3 = Puzzle(
    title="문제 3",
    question="""깊은 밤, 당신은 오래된 어느 저택의 서재에서 깨어났습니다. 
    눈을 떠보니 방안은 고요하였지만, 당신은 자물쇠가 잠겨있어 나갈 수가 없었습니다. 
    당신은 이방을 나가기 위해 주의를 둘러보니 책장과 벽시계 그리고 테이블 위 낡은 편지 하나만이 놓여 있었죠.
    
    책장은 여섯 권의 책으로 꽉 채워져 있었고, 각 책에는 고유한 번호와 제목이 적혀있었습니다.
    1-ORACLE
    2-PYRAMID
    3-ECLIPSE
    4-LABYRINTH
    5-ELEPHANT
    6-MOSAIC
    
    벽시계는 엄청 낡고 멈춰 있었지만, 시계의 숫자에는 각각의 알파벳이 적혀있었습니다.
    1시= F ,2시= I, 3시= L, 4시= A, 5시= M, 6시= E, 7시= R, 8시= O, 9시= C, 10시= K, 11시= S, 12시= T
    
    편지의 내용은 다음과 같았습니다.
    금고의 첫 숫자는 세번 째 책 제목의 글자 수에서, 
    두번 째 숫자는 책장 순서를 따라 시계 속 불꽃(FLAME)을 찾아서 10으로 나눈 나머지,
    마지막 숫자는 가장 긴 책과 가장 짧은 책의 글자 수 차이에서
    
    행운을 빈다.""",
    answer="793",
    success_message="정답입니다!"
)

puzzle4 = Puzzle(
    title="문제 4",
    question="""당신은 갑작스러운 비상 상황으로 인해 잠시 동안 비상 탈출 캡슐로 대피해야 하는 우주 비행사입니다. 
    캡슐로 가져갈 수 있는 물건은 제한되어 있습니다. 생존과 임무 완수에 도움이 되는 물건들 중 가장 중요한 것들을 골라야 합니다.

    A. 비상 산소통(대) / 5kg / 50점
    B. 통신 장비 (소) / 3kg / 40점
    C. 고열량 비상 식량 / 4kg / 35점
    D. 정밀 수리 도구 세트 / 2kg / 5점
    E. 응급 처치 키트 / 1kg / 10점

    위의 물품들 중 무게 제한 10kg 을 넘지 않으면서도 중요도 점수의 합계를 최대로 하도록 짐을 꾸렸을 때의 점수를 구하세요.
    """,
    answer="100",
   	success_message="정답입니다!"
)


# 세션 초기화
if "puzzle_game" not in st.session_state:
    st.session_state.puzzle_game = PuzzleGame([puzzle1, puzzle2, puzzle3, puzzle4])

game = st.session_state.puzzle_game

st.title("🔐 AI 방탈출 퀴즈")


# 게임 진행
if not game.game_over:
    current = game.current_puzzle()

    st.subheader(current.title)
    st.write(current.question)

    user_answer = st.chat_input("정답을 입력하세요")

    if user_answer:
        result = game.check_answer(user_answer)

        # ▣ 정답 (result == None → 마지막 퍼즐)
        if result is None:
            if game.game_over:
                st.success("🏆 축하합니다! 모든 퍼즐을 해결했습니다 비밀번호는 7932 입니다", icon="🎉")
            else:
                st.success(current.success_message)
                st.rerun()

        # ▣ 오답
        elif isinstance(result, str) and "오답" in result:
            st.error(result)

            hint_prompt = (
                f"퍼즐 문제: {current.question}\n\n"
                f"정답은 '{current.answer}'이고, 사용자 답은 '{user_answer}'입니다.\n"
                "학생이 정답을 떠올릴 수 있도록 아주 간접적인 한 줄 힌트를 작성하세요. "
                "정답은 절대 직접 말하지 마세요."
            )

            try:
                hint_response = model.generate_content(hint_prompt)
                hint_text = hint_response.text.strip()
            except Exception:
                hint_text = "⚠️ 힌트를 가져오지 못했습니다. 다시 시도하세요."

            with st.chat_message("ai"):
                st.info(hint_text)

        # ▣ 정답 + 다음 퍼즐 있을 때
        else:
            st.success(result)
            st.rerun()

else:
    st.success("🏆 축하합니다! 모든 퍼즐을 해결했습니다! 비밀번호는 7932 입니다.", icon="🎉")
