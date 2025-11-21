import streamlit as st

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
        if self.current_index < len(self.puzzles):
            return self.puzzles[self.current_index]
        return None

    def check_answer(self, user_answer):
        current = self.current_puzzle()
        if not current:
            return None
        if user_answer.strip() == current.answer:
            self.current_index += 1
            if self.current_index >= len(self.puzzles):
                self.game_over = True
                return None  # 마지막 문제 완료 시 None 반환
            return current.success_message + "\n\n👉 다음 퍼즐로 이동합니다!"
        else:
            return "❌ 오답입니다. 다시 시도하세요!"

# 퍼즐 정의
puzzle1 = Puzzle(
    title="문제 1",
    question="우리 학교 이름은?",
    answer="남한고등학교",
    success_message="정답입니다!"
)

puzzle2 = Puzzle(
    title="문제 2",
    question="전기 패널에는 빨강, 노랑, 파랑 신호등이 있습니다. 빨강이 켜진 순간, 나머지 두 신호등의 상태는 무엇인가요? (노랑 파랑 순서대로 '꺼짐 켜짐' 형태로 입력)",
    answer="꺼짐 꺼짐",
    success_message="정답입니다!"
)

puzzle3 = Puzzle(
    title="문제 3",
    question="깊은 밤 저택의 서재에서 자물쇠를 풀어야 합니다. 금고의 비밀번호는?",
    answer="793",
    success_message="정답입니다!"
)

puzzle4 = Puzzle(
    title="문제 4",
    question="우주 비행사 비상 탈출 캡슐에서 10kg 제한 내 최대 점수를 얻으려면?",
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

    answer = st.text_input("정답을 입력하세요")

    if answer:
        result = game.check_answer(answer)

        if result:
            if "오답" in result:
                st.error(result)
            else:
                st.success(result)
                st.experimental_rerun()
        else:
            # 마지막 문제 완료
            st.success("🏆 축하합니다! 모든 퍼즐을 해결했습니다! 비밀번호는 7932 입니다", icon="🎉")

else:
    st.success("🏆 축하합니다! 모든 퍼즐을 해결했습니다! 비밀번호는 7932 입니다", icon="🎉")
