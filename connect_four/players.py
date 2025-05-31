import random
import re
from typing import Optional, List
import logging

from openai import OpenAI
from .config import COLS, COL_LETTERS
from .board import Board, is_valid_location

logger = logging.getLogger(__name__)

class Player:
    def __init__(self, name: str):
        self.name = name
        self.fallbacks = 0
        self.last_error: Optional[str] = None
        self.symbol: str = ""
        self.piece_code: int = 0

    def get_move(self, board: Board) -> int:
        raise NotImplementedError

class GPTAgentPlayer(Player):
    client = OpenAI()

    def __init__(self, name: str, model: str = "gpt-4o-mini", temperature: float = 0.3, max_tokens: int = 1024):
        super().__init__(name)
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.logger = logger.getChild(f"{self.__class__.__name__}.{self.name}")

    @staticmethod
    def _ascii_board(board: Board) -> str:
        lines = ["  " + " ".join(COL_LETTERS)]
        for r, row in enumerate(board):
            label = len(board) - r
            cells = ['.' if cell == 0 else ('X' if cell == 1 else 'O') for cell in row]
            lines.append(f"{label} " + " ".join(cells))
        return "\n".join(lines)

    def get_move(self, board: Board) -> int:
        self.last_error = None
        prompt = (
            f"You're playing connect four, X goes first. You're {self.symbol}.\n"
            f"Current board:\n{self._ascii_board(board)}\n"
            "End with your move in brackets like [A-G]."
        )
        self.logger.info(f"PROMPT:\n{prompt}")

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                timeout=15,
            )
            text = response.choices[0].message.content
            self.logger.info(f"LLM RESPONSE:\n{text}")
            matches = re.findall(r"\[([A-G])\]", text, flags=re.I)
            if not matches:
                raise ValueError("no [A-G] found")
            move = matches[-1].upper()
            self.logger.info(f"PARSED MOVE: {move} (col {COL_LETTERS.index(move)})")
            return COL_LETTERS.index(move)
        except Exception as e:
            self.last_error = str(e)
            self.fallbacks += 1
            self.logger.error(f"ERROR in get_move(): {self.last_error}. Falling back to random.")
            fallback_choices = [c for c in range(COLS) if is_valid_location(board, c)]
            self.logger.info(f"FALLBACK_CHOICES: {fallback_choices}")
            return random.choice(fallback_choices)

class VLLMAgentPlayer(GPTAgentPlayer):
    def __init__(self, name: str, model: str = "granite_c4", temperature: float = 0.3, max_tokens: int = 1024, base_url: str = "http://localhost:8000/v1"):
        super().__init__(name, model, temperature, max_tokens)
        self.client = OpenAI(base_url=base_url)
        self.logger = logger.getChild(f"{self.__class__.__name__}.{self.name}")

    def get_move(self, board: Board) -> int:
        self.last_error = None
        prompt = f"<state:{self.symbol}>\n```\n{self._ascii_board(board)}\n```"
        self.logger.info(f"PROMPT:\n{prompt}")

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "GAME_MODE=CONNECT_FOUR <top3><optimal_move>"},
                    {"role": "user", "content": prompt},
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                timeout=15,
            )
            text = response.choices[0].message.content
            self.logger.info(f"LLM RESPONSE:\n{text}")
            matches = re.findall(r"\[([A-G])\]", text, flags=re.I)
            if not matches:
                raise ValueError("no [A-G] found")
            move = matches[-1].upper()
            self.logger.info(f"PARSED MOVE: {move} (col {COL_LETTERS.index(move)})")
            return COL_LETTERS.index(move)
        except Exception as e:
            self.last_error = str(e)
            self.fallbacks += 1
            self.logger.error(f"ERROR in get_move(): {self.last_error}. Falling back to random.")
            fallback_choices = [c for c in range(COLS) if is_valid_location(board, c)]
            self.logger.info(f"FALLBACK_CHOICES: {fallback_choices}")
            return random.choice(fallback_choices)

class RandomPlayer(Player):
    def get_move(self, board: Board) -> int:
        return random.randint(0, COLS - 1)

