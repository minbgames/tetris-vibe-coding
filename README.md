# Python Tetris

간단한 터미널/데스크톱 환경에서 실행 가능한 Pygame 기반 테트리스 게임입니다.

## 설치 방법 (Setup)

1. Python 3.8 이상이 설치되어 있어야 합니다.
2. 가상 환경(권장)을 생성한 뒤 `requirements.txt` 의 의존성을 설치하세요.

```bash
python -m venv venv
source venv/bin/activate  # Windows 는 venv\Scripts\activate
pip install -r requirements.txt
```

## 실행 방법 (Run)

```bash
python main.py
```

게임 창이 열리면 화살표 키로 블록을 이동하고, 위쪽 화살표(또는 `W`)로 회전, 아래쪽 화살표(또는 `S`)로 빠르게 드롭, 스페이스바로 즉시 하드드롭 할 수 있습니다.

## Controls

* Left Arrow / A  : Move left
* Right Arrow / D : Move right
* Up Arrow / W    : Rotate piece (clockwise)
* Down Arrow / S  : Soft drop (accelerated)
* Spacebar        : Hard drop (instantly place piece)
* P               : Pause / Unpause
* Esc / Q         : Quit game

## 파일 구조 (File structure)

```
├── main.py          # 게임 전체 로직
├── requirements.txt # 의존성 목록
└── README.md        # 이 문서
```

즐겁게 플레이하세요! (Have fun!)