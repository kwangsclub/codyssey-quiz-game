"""게임 전체(메뉴, 퀴즈 풀기/추가/목록/삭제, 점수, 저장)를 관리하는 QuizGame 클래스."""

import random
from datetime import datetime

from default_quizzes import get_default_quizzes
from quiz import Quiz

LINE = "=" * 40
THIN_LINE = "-" * 40
HINT_KEYS = ("h", "H", "ㅗ")


class QuizGame:
    """퀴즈 목록, 최고 점수, 게임 기록을 가지고 게임을 진행한다."""

    MENU_ITEMS = [
        "퀴즈 풀기",
        "퀴즈 추가",
        "퀴즈 목록",
        "점수 확인",
        "퀴즈 삭제",
        "게임 기록",
        "종료",
    ]

    def __init__(self):
        self.quizzes = []
        self.best_score = None  # 아직 퀴즈를 풀지 않았으면 None
        self.history = []
        self.is_running = True

    # ------------------------------------------------------------------
    # 실행 흐름
    # ------------------------------------------------------------------
    def run(self):
        """프로그램 진입점. Ctrl+C / EOF 가 와도 안전하게 저장 후 종료한다."""
        try:
            self.print_title()
            self.load_state()
            while self.is_running:
                self.show_menu()
                choice = self.read_number("선택: ", 1, len(self.MENU_ITEMS))
                self.handle_menu(choice)
        except (KeyboardInterrupt, EOFError):
            print("\n\n⚠️ 입력이 중단되었습니다. 데이터를 저장하고 안전하게 종료합니다.")
            self.save_state()
            print("👋 프로그램을 종료합니다.")

    def handle_menu(self, choice):
        """선택한 메뉴 번호에 맞는 기능을 실행한다."""
        actions = {
            1: self.play_quiz,
            2: self.add_quiz,
            3: self.list_quizzes,
            4: self.show_best_score,
            5: self.not_ready,
            6: self.not_ready,
            7: self.quit,
        }
        actions[choice]()

    def not_ready(self):
        print("\n🚧 아직 준비 중인 기능입니다.")

    def quit(self):
        print("\n👋 프로그램을 종료합니다.")
        self.is_running = False

    # ------------------------------------------------------------------
    # 화면 출력
    # ------------------------------------------------------------------
    def print_title(self):
        print(LINE)
        print("      🎯 파이썬 & 컴퓨터 기초 퀴즈 🎯")
        print(LINE)

    def show_menu(self):
        print()
        print(LINE)
        for number, name in enumerate(self.MENU_ITEMS, start=1):
            print(f"{number}. {name}")
        print(LINE)

    # ------------------------------------------------------------------
    # 입력 처리
    # ------------------------------------------------------------------
    def read_text(self, prompt):
        """앞뒤 공백을 제거한 문자열을 입력받는다. 빈 입력은 다시 받는다."""
        while True:
            text = input(prompt).strip()
            if text:
                return text
            print("⚠️ 입력값이 비어 있습니다. 다시 입력하세요.")

    def read_number(self, prompt, minimum, maximum, allow_hint=False):
        """minimum~maximum 사이의 정수를 입력받는다.

        allow_hint=True 이면 힌트 키(h)를 입력했을 때 "hint" 를 반환한다.
        """
        guide = f"⚠️ 잘못된 입력입니다. {minimum}-{maximum} 사이의 숫자를 입력하세요."
        while True:
            text = input(prompt).strip()
            if not text:
                print(f"⚠️ 입력값이 비어 있습니다. {minimum}-{maximum} 사이의 숫자를 입력하세요.")
                continue
            if allow_hint and text in HINT_KEYS:
                return "hint"
            try:
                number = int(text)
            except ValueError:
                print(guide)
                continue
            if minimum <= number <= maximum:
                return number
            print(guide)

    def confirm(self, prompt):
        """y/n 질문에 대해 True/False 를 반환한다."""
        while True:
            answer = input(prompt).strip().lower()
            if answer in ("y", "yes", "ㅛ"):
                return True
            if answer in ("n", "no", "ㅜ"):
                return False
            print("⚠️ y 또는 n 을 입력하세요.")

    # ------------------------------------------------------------------
    # 1. 퀴즈 풀기
    # ------------------------------------------------------------------
    def play_quiz(self):
        if not self.quizzes:
            print("\n📭 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
            return

        total_available = len(self.quizzes)
        count = self.read_number(
            f"\n몇 문제를 풀까요? (1-{total_available}): ", 1, total_available
        )
        selected = random.sample(self.quizzes, count)  # 랜덤 출제

        print(f"\n📝 퀴즈를 시작합니다! (총 {count}문제)")
        print("💡 정답 대신 h 를 입력하면 힌트를 볼 수 있어요. (해당 문제 점수 절반)")

        correct_count = 0
        hint_count = 0
        earned = 0.0
        point_per_quiz = 100 / count
        for number, quiz in enumerate(selected, start=1):
            print()
            print(THIN_LINE)
            is_correct, used_hint = self.ask_quiz(quiz, number)
            if used_hint:
                hint_count += 1
            if is_correct:
                correct_count += 1
                earned += point_per_quiz / 2 if used_hint else point_per_quiz

        score = round(earned)
        self.show_result(count, correct_count, hint_count, score)
        self.record_result(count, correct_count, hint_count, score)

    def ask_quiz(self, quiz, number):
        """한 문제를 출제하고 (정답 여부, 힌트 사용 여부) 를 반환한다."""
        quiz.display(number)
        used_hint = False
        while True:
            answer = self.read_number("정답 입력: ", 1, Quiz.CHOICE_COUNT, allow_hint=True)
            if answer != "hint":
                break
            if not quiz.has_hint():
                print("🙅 이 문제는 힌트가 없습니다.")
            elif used_hint:
                print(f"💡 힌트: {quiz.hint}")
            else:
                used_hint = True
                print(f"💡 힌트: {quiz.hint} (이 문제 점수는 절반만 인정돼요)")

        if quiz.is_correct(answer):
            print("✅ 정답입니다!")
            return True, used_hint
        print(f"❌ 오답입니다. 정답은 {quiz.answer}번 '{quiz.choices[quiz.answer - 1]}' 입니다.")
        return False, used_hint

    def show_result(self, total, correct, hints, score):
        print()
        print(LINE)
        print(f"🏆 결과: {total}문제 중 {correct}문제 정답! ({score}점)")
        if hints:
            print(f"💡 힌트 사용: {hints}회")
        if self.best_score is None or score > self.best_score:
            print("🎉 새로운 최고 점수입니다!")
        print(LINE)

    def record_result(self, total, correct, hints, score):
        """최고 점수를 비교/갱신하고 게임 기록을 남긴 뒤 저장한다."""
        if self.best_score is None or score > self.best_score:
            self.best_score = score
        self.history.append(
            {
                "played_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "total": total,
                "correct": correct,
                "hints": hints,
                "score": score,
            }
        )
        self.save_state()

    # ------------------------------------------------------------------
    # 2. 퀴즈 추가
    # ------------------------------------------------------------------
    def add_quiz(self):
        print("\n📌 새로운 퀴즈를 추가합니다.\n")
        question = self.read_text("문제를 입력하세요: ")
        choices = []
        for index in range(1, Quiz.CHOICE_COUNT + 1):
            choices.append(self.read_text(f"선택지 {index}: "))
        answer = self.read_number(f"정답 번호 (1-{Quiz.CHOICE_COUNT}): ", 1, Quiz.CHOICE_COUNT)
        hint = input("힌트 (없으면 Enter): ").strip()

        self.quizzes.append(Quiz(question, choices, answer, hint))
        self.save_state()
        print("\n✅ 퀴즈가 추가되었습니다!")

    # ------------------------------------------------------------------
    # 3. 퀴즈 목록
    # ------------------------------------------------------------------
    def list_quizzes(self):
        if not self.quizzes:
            print("\n📭 등록된 퀴즈가 없습니다.")
            return
        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)\n")
        print(THIN_LINE)
        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"[{number}] {quiz.question}")
        print(THIN_LINE)

    # ------------------------------------------------------------------
    # 4. 점수 확인
    # ------------------------------------------------------------------
    def show_best_score(self):
        if self.best_score is None:
            print("\n📭 아직 퀴즈를 풀지 않았습니다. 1번 메뉴에서 퀴즈를 풀어 보세요!")
            return
        detail = ""
        for record in self.history:
            if record.get("score") == self.best_score:
                detail = f" ({record['total']}문제 중 {record['correct']}문제 정답)"
                break
        print(f"\n🏆 최고 점수: {self.best_score}점{detail}")

    # ------------------------------------------------------------------
    # 파일 저장 / 불러오기
    # ------------------------------------------------------------------
    def load_state(self):
        """(파일 저장 기능 구현 전) 기본 퀴즈로 시작한다."""
        self.quizzes = get_default_quizzes()

    def save_state(self):
        """파일 저장 기능은 이후 구현 예정."""
        return True
