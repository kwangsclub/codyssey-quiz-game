"""개별 퀴즈 한 문제를 표현하는 Quiz 클래스."""


class Quiz:
    """문제(question), 선택지(choices), 정답 번호(answer), 힌트(hint)를 가진 퀴즈."""

    CHOICE_COUNT = 4

    def __init__(self, question, choices, answer, hint=""):
        if len(choices) != self.CHOICE_COUNT:
            raise ValueError(f"선택지는 {self.CHOICE_COUNT}개여야 합니다.")
        if not 1 <= int(answer) <= self.CHOICE_COUNT:
            raise ValueError("정답은 1~4 사이의 번호여야 합니다.")
        self.question = str(question)
        self.choices = [str(choice) for choice in choices]
        self.answer = int(answer)  # 정답은 1~4 번호로 관리
        self.hint = str(hint)

    def display(self, number=None):
        """문제와 선택지를 화면에 출력한다."""
        title = f"[문제 {number}]" if number is not None else "[문제]"
        print(title)
        print(self.question)
        print()
        for index, choice in enumerate(self.choices, start=1):
            print(f"{index}. {choice}")
        print()

    def is_correct(self, user_answer):
        """사용자가 고른 번호가 정답인지 확인한다."""
        return user_answer == self.answer

    def has_hint(self):
        return bool(self.hint.strip())

    def to_dict(self):
        """JSON 저장을 위해 dict 로 변환한다."""
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
            "hint": self.hint,
        }

    @classmethod
    def from_dict(cls, data):
        """dict(JSON) 데이터로부터 Quiz 인스턴스를 만든다."""
        return cls(
            question=data["question"],
            choices=data["choices"],
            answer=data["answer"],
            hint=data.get("hint", ""),
        )
