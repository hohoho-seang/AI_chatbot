import google.generativeai as genai
import streamlit as st


# Gemini 설정
genai.configure(api_key="AIzaSyBUb315t4UmesRgf3xhNnyW15yFh_0KO1M") 
@st.cache_resource
def load_model():
    model = genai.GenerativeModel("gemini-2.0-flash") 
    return model

model = load_model()


# Puzzle 클래스- 퍼즐 여러개 정의
class Puzzle:
    def __init__(self, title, question, answer, success_message):
        self.title = title
        self.question = question
        self.answer = answer
        self.success_message = success_message


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
                return  None
            else:
                return current.success_message + "\n\n👉 다음 퍼즐로 이동합니다!"
        else:
            return "❌ 오답입니다. 다시 시도하세요!"


# 퍼즐 만들기
puzzle1 = Puzzle(
    title="문제 1",
    question="11",
    answer="11",
    success_message="정답입니다!"
)

puzzle2 = Puzzle(
    title="""문제 2",
    question="깊은 밤, 당신은 오래된 어느 저택의 서재에서 깨어났습니다. 
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

puzzle3 = Puzzle(
    title="문제 3",
    question="우리 학교 이름은?",
    answer="남한고",
    success_message="정답입니다!"
)

# 세션 초기화 
if "puzzle_game" not in st.session_state:
    st.session_state.puzzle_game = PuzzleGame([puzzle1, puzzle2, puzzle3])
    st.session_state.chat_history = [puzzle1.question]

game = st.session_state.puzzle_game

st.title("🔐 AI 방탈출 퀴즈")

# 현재 퍼즐 출력
if not game.game_over:
    current = game.current_puzzle()
    st.subheader(current.title)
    st.write(current.question)

    # 정답 학인
    answer = st.chat_input("정답을 입력하세요")

    if answer:
        result = game.check_answer(answer)

        if "오답" in result:
            st.error(result)
            hint_prompt = f"퍼즐 문제: {current.question}\n\n정답은 '{current.answer}'이고, 사용자 답은 '{answer}'입니다. 사용자가 정답을 유추할수 있게 힌트를 주세요. 하지만 학생에게 바로 답을 알려주지 말고, 간접적인 힌트를 한 줄만 주세요."
            try:
                hint_response = model.generate_content(hint_prompt)
                hint_text = hint_response.text.strip()
            except Exception as e:
                hint_text = "⚠️ 힌트를 가져오지 못했습니다. 다시 시도하세요."

            with st.chat_message("ai"):
                st.info(f"{hint_text}")
        else:
            st.success(result)
            st.session_state.chat_history.append(result)

            # 다음 퍼즐로 이동 시 rerun
            if not game.game_over:
                st.rerun()

else:
    st.success("🏆 축하합니다! 모든 퍼즐을 해결했습니다!", icon="🎉")
    
