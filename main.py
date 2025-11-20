import google.generativeai as genai
import streamlit as st

# Gemini 설정
genai.configure(api_key="YOUR_API_KEY")

@st.cache_resource
def load_model():
    model = genai.GenerativeModel("gemini-2.0-flash")
    return model

model = load_model()


# Puzzle 클래스
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

        # 정답 여부 확인
        if user_answer.strip() == current.answer:
            self.current_index += 1

            if self.current_index >= len(self.puzzles):
                self.game_over = True
                return None

            return current.success_message + "\n\n👉 다음 퍼즐로 이동합니다!"
        else:
            return "❌ 오답입니다. 다시 시도하세요!"


# 퍼즐 만들기
puzzle1 = Puzzle(
    title="문제 1",
    question="""전기 패널에는 빨강, 노랑, 파랑 신호등이 있습니다.
    규칙 :
1. 빨강은 파랑보다 먼저 켜야 합니다.
2. 노랑은 빨강과 동시에 켤 수 없습니다.
3. 파랑은 노랑이 꺼진 직후에 켜집니다.

빨강이 켜진 순간, 나머지 두 신호등의 상태는 무엇인가요?(노랑 파랑 순서대로 꺼짐/켜짐 으로 입력 )""",
    answer="꺼짐 꺼짐",
    success_message="정답입니다!"
)

puzzle2 = Puzzle(
    title="문제 2",
    question="2 * 5 = ?",
    answer="10",
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

    answer = st.chat_input("정답을 입력하세요")

    if answer:
        result = game.check_answer(answer)

        if result and "오답" in result:
            st.error(result)

            hint_prompt = (
                f"퍼즐 문제: {current.question}\n\n"
                f"정답은 '{current.answer}'입니다. "
                f"학생에게 바로 답을 주지 말고, 간접적인 힌트를 한 줄로 생성하세요."
            )

            try:
                hint_response = model.generate_content(hint_prompt)
                hint_text = hint_response.text.strip()
            except:
                hint_text = "⚠️ 힌트를 가져오지 못했습니다."

            with st.chat_message("ai"):
                st.info(hint_text)

        else:
            st.success(result)
            st.session_state.chat_history.append(result)

            if not game.game_over:
                st.rerun()

else:
    st.success("🏆 축하합니다! 모든 퍼즐을 해결했습니다!", icon="🎉")
