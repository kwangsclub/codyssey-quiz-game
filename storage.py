"""state.json 파일 저장/불러오기를 담당하는 StateStorage 클래스."""

import json
import os

from quiz import Quiz

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DEFAULT_STATE_PATH = os.path.join(PROJECT_ROOT, "state.json")


class StateStorage:
    """퀴즈 목록, 최고 점수, 게임 기록을 JSON 파일로 저장하고 불러온다."""

    def __init__(self, path=DEFAULT_STATE_PATH):
        self.path = path

    def load(self):
        """파일을 읽어 (상태 dict, 상태 메시지) 를 반환한다.

        - 파일 없음: (None, "missing")
        - 파일 손상: (None, "corrupted")
        - 정상: (state, "ok")
        """
        if not os.path.exists(self.path):
            return None, "missing"
        try:
            with open(self.path, "r", encoding="utf-8") as file:
                raw = json.load(file)
            state = {
                "quizzes": [Quiz.from_dict(item) for item in raw["quizzes"]],
                "best_score": raw.get("best_score"),
                "history": list(raw.get("history", [])),
            }
            return state, "ok"
        except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError):
            return None, "corrupted"

    def save(self, quizzes, best_score, history):
        """현재 상태를 UTF-8 JSON 으로 저장한다. 성공 여부를 반환한다."""
        data = {
            "quizzes": [quiz.to_dict() for quiz in quizzes],
            "best_score": best_score,
            "history": history,
        }
        temp_path = self.path + ".tmp"
        try:
            with open(temp_path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            os.replace(temp_path, self.path)  # 저장 도중 오류가 나도 기존 파일 보호
            return True
        except OSError as error:
            print(f"⚠️ 파일 저장 중 오류가 발생했습니다: {error}")
            return False
