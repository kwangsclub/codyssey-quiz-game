"""퀴즈 게임 실행 파일. 사용법: python main.py"""

import sys

from quiz_game import QuizGame


def main():
    # Windows 콘솔에서도 한글/이모지가 깨지지 않도록 UTF-8 로 출력
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    game = QuizGame()
    game.run()


if __name__ == "__main__":
    main()
