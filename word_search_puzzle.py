import numpy as np
from numpy import ndarray


INPUT_PUZZLE = "sghaiooaicviavas\nvsqejclajvaslvpf\nwiljldlgtcdsplna\nyglailoaicviavas\nkgoaiooaicviavas\nnheploogicviavas"
INPUT_WORD = "hello"


class Game:
    """Game dataclass representing the puzzle and the word."""

    def __init__(self, input_puzzle: str, input_word: str) -> None:
        self.puzzle: ndarray = np.array([[*c] for c in input_puzzle.split("\n")])
        self.word: str = input_word
        self.word_len: int = len(input_word)

    def get_start_indices(self):
        return np.argwhere(game.puzzle == game.word[0])

    def get_stops_indices(self, start_index: ndarray) -> ndarray:
        wl = self.word_len - 1
        i = start_index[0]
        j = start_index[1]

        raw_indices = np.array([
            [i, j + wl],
            [i + wl, j + wl],
            [i + wl, j],
            [i + wl, j - wl],
            [i, j - wl],
            [i - wl, j - wl],
            [i - wl, j],
            [i - wl, j + wl],
        ])

        mask = (
            (raw_indices[:, 0] >= 0)
            & (raw_indices[:, 1] >= 0)
            & (raw_indices[:, 0] < self.puzzle.shape[0])
            & (raw_indices[:, 1] < self.puzzle.shape[1])
        )

        return raw_indices[mask]

    def _get_chars_indices(self, start_index, stop_index) -> ndarray:
        wl = self.word_len
        start_i = start_index[0]
        start_j = start_index[1]
        stop_i = stop_index[0]
        stop_j = stop_index[1]

        if start_i == stop_i and start_j < stop_j:  # towart east
            return np.array([[start_i] * wl, list(range(start_j, stop_j + 1))]).T

        if start_i == stop_i and start_j > stop_j:  # towart west
            return np.array([[start_i] * wl, list(range(start_j, stop_j - 1, -1))]).T

        if start_j == stop_j and start_i < stop_i:  # towart south
            return np.array([list(range(start_i, stop_i + 1)), [start_j] * wl]).T

        if start_j == stop_j and start_i > stop_i:  # towart north
            return np.array([list(range(start_i, stop_i - 1, -1)), [start_j] * wl]).T

        if start_i < stop_i and start_j < stop_j:  # towart south-east
            return np.array([
                list(range(start_i, stop_i + 1)),
                list(range(start_j, stop_j + 1)),
            ]).T

        if start_i < stop_i and start_j > stop_j:  # towart south-west
            return np.array([
                list(range(start_i, stop_i + 1)),
                list(range(start_j, stop_j - 1, -1)),
            ]).T

        if start_i > stop_i and start_j > stop_j:  # towart north-west
            return np.array([
                list(range(start_i, stop_i - 1, -1)),
                list(range(start_j, stop_j - 1, -1)),
            ]).T

        if start_i > stop_i and start_j < stop_j:  # towart north-east
            return np.array([
                list(range(start_i, stop_i - 1, -1)),
                list(range(start_j, stop_j + 1)),
            ]).T

        return np.array([[]])

    def _do_word_match(self, chars_indices: ndarray) -> bool:
        chars = []
        for char_index in chars_indices:
            chars.append(self.puzzle[char_index[0], char_index[1]])

        if "".join(chars) == self.word:
            return True

        return False

    def get_puzzle_word(
        self, start_index: ndarray, stops_indices: ndarray
    ) -> tuple[ndarray, ndarray]:
        for stop_index in stops_indices:
            chars_indices = self._get_chars_indices(start_index, stop_index)
            if self._do_word_match(chars_indices):
                return start_index, stop_index

        return np.array([]), np.array([])


if __name__ == "__main__":
    game = Game(input_puzzle=INPUT_PUZZLE, input_word=INPUT_WORD)

    print(game.puzzle, end="\n\n")

    for start_index in game.get_start_indices():
        stops_indices = game.get_stops_indices(start_index)
        word_indices = game.get_puzzle_word(start_index, stops_indices)
        if word_indices[0].size != 0 and word_indices[1].size != 0:
            print(
                f"Word: {game.word}\nStart indices: {word_indices[0]}\nStop indices:  {word_indices[1]}"
            )
