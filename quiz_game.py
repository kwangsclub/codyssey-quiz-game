"""게임 전체(메뉴, 퀴즈 풀기/추가/목록/삭제, 점수, 저장)를 관리하는 QuizGame 클래스."""

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
            1: self.not_ready,
            2: self.not_ready,
            3: self.not_ready,
            4: self.not_ready,
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
    # 파일 저장 / 불러오기
    # ------------------------------------------------------------------
    def load_state(self):
        """(파일 저장 기능 구현 전) 기본 퀴즈로 시작한다."""
        self.quizzes = []

    def save_state(self):
        """파일 저장 기능은 이후 구현 예정."""
        return True
