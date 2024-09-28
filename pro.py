import random
import time
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional

@dataclass
class Player:
    username: str
    password: str
    score: int = 0

@dataclass
class Game:
    players: List[Player] = field(default_factory=list)
    current_player_index: int = 0
    board: List[List[str]] = field(default_factory=list)
    revealed: List[List[bool]] = field(default_factory=list)
    theme: List[str] = field(default_factory=list)

    def register_player(self, username: str, password: str):
        self.players.append(Player(username, password))

    def select_theme(self, choice: str):
        themes = {
            "animales": ["🐶", "🐱", "🐭", "🐹", "🐰", "🦊", "🐻", "🐼"],
            "frutas": ["🍎", "🍌", "🍇", "🍉", "🍓", "🍒", "🍑", "🍍"],
            "emojis": ["😀", "😂", "😍", "😎", "😜", "😡", "😱", "😭"],
            "objetos": ["🚗", "✈️", "🚀", "🛸", "🚢", "🚲", "🏠", "🏢"]
        }
        self.theme = themes.get(choice, [])
        if not self.theme:
            print("Tema no válido. Selecciona uno de los temas disponibles.")

    def setup_board(self, difficulty: str):
        size = 4 if difficulty == "fácil" else 6 if difficulty == "medio" else 8
        icons = self.theme * 2
        random.shuffle(icons)
        self.board = [icons[i:i + size] for i in range(0, len(icons), size)]
        self.revealed = [[False] * size for _ in range(size)]

    def display_board(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.revealed[i][j]:
                    print(self.board[i][j], end=" ")
                else:
                    print("❓", end=" ")
            print()
        print()

    def check_match(self, first: Tuple[int, int], second: Tuple[int, int]) -> bool:
        return self.board[first[0]][first[1]] == self.board[second[0]][second[1]]

    def play_turn(self):
        current_player = self.players[self.current_player_index]
        print(f"Turno de {current_player.username}. Tu puntaje actual es: {current_player.score}")
        self.display_board()

        first_choice = self.get_choice("Elige la primera ficha (fila columna): ")
        self.revealed[first_choice[0]][first_choice[1]] = True
        self.display_board()

        second_choice = self.get_choice("Elige la segunda ficha (fila columna): ")
        self.revealed[second_choice[0]][second_choice[1]] = True
        self.display_board()

        if self.check_match(first_choice, second_choice):
            print("¡Coincidencia encontrada!")
            current_player.score += 10
            self.board[first_choice[0]][first_choice[1]] = None  # Eliminar fichas
            self.board[second_choice[0]][second_choice[1]] = None
        else:
            print("No coinciden. Volteando de nuevo...")
            time.sleep(2)
            self.revealed[first_choice[0]][first_choice[1]] = False
            self.revealed[second_choice[0]][second_choice[1]] = False
            current_player.score -= 5

        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def get_choice(self, prompt: str) -> Tuple[int, int]:
        while True:
            try:
                choice = input(prompt)
                row, col = map(int, choice.split())
                if 0 <= row < len(self.board) and 0 <= col < len(self.board[0]):
                    return row, col
                else:
                    print("Elección fuera de rango. Intenta de nuevo.")
            except ValueError:
                print("Entrada no válida. Por favor, ingresa fila y columna separadas por un espacio.")

    def show_scores(self):
        print("Tabla de posiciones:")
        for player in self.players:
            print(f"{player.username}: {player.score} puntos")

def main():
    game = Game()
    
    # Registro de jugadores
    num_players = int(input("¿Cuántos jugadores? (mínimo 2): "))
    for _ in range(num_players):
        username = input("Ingresa el nombre de usuario: ")
        password = input("Ingresa la contraseña: ")
        game.register_player(username, password)

    # Selección de temática
    theme_choice = input("Selecciona un tema (animales, frutas, emojis, objetos): ")
    game.select_theme(theme_choice)

    # Configuración del tablero
    difficulty = input("Selecciona la dificultad (fácil, medio, difícil): ")
    game.setup_board(difficulty)

    # Juego
    while any(any(not revealed for revealed in row) for row in game.revealed):
        game.play_turn()
        game.show_scores()

    print("¡Juego terminado!")

if __name__ == "__main__":
    main()
