import time
import random

class TicTacToe:
    def __init__(self):
        # using a single list to represent a 3x3 board
        self.board = [" " for _ in range(9)]
        self.current_winner = None  # keep track of the winner!

    def print_board(self):
        # this method prints the current board rows
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')
            
    def empty_squares(self):
        return ' ' in self.board

    def num_empty_squares(self):
        return self.board.count(' ')
    
    @staticmethod
    def print_board_nums():
        # prints the board with number labels so players know which square is which
        number_board = [[str(i) for i in range(j*3, (j+1)*3)] for j in range(3)]
        for row in number_board:
            print('| ' + ' | '.join(row) + ' |')

    def available_moves(self):
        # return a list of available moves (i.e., indexes in the board that are still blank)
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def make_move(self, square, letter):
        # if valid move, then assign the square to the letter and check for a winner
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        # check row
        row_index = square // 3
        row = self.board[row_index*3:(row_index+1)*3]
        if all(spot == letter for spot in row):
            return True
        
        # check column
        col_index = square % 3
        column = [self.board[col_index+i*3] for i in range(3)]
        if all(spot == letter for spot in column):
            return True
        
        # check diagonals
        # only even-numbered squares are possible candidates for diagonals.
        if square % 2 == 0:
            # left to right diagonal
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all(spot == letter for spot in diagonal1):
                return True
            # right to left diagonal
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all(spot == letter for spot in diagonal2):
                return True
        
        return False

class HumanPlayer:
    def __init__(self, letter):
        self.letter = letter

    def get_move(self, game):
        # repeatedly ask the user until they provide a valid move.
        valid_square = False
        val = None
        while not valid_square:
            move_str = input(f"{self.letter}'s turn. Input move (0-8): ")
            # check if input is a number and if it's a valid move.
            try:
                val = int(move_str)
                if val not in game.available_moves():
                    raise ValueError
                valid_square = True  
            except ValueError:
                print("Invalid move. Please try again.")
        return val

class RandomComputerPlayer:
    def __init__(self, letter):
        self.letter = letter

    def get_move(self, game):
        # pick a random valid move from available moves
        square = random.choice(game.available_moves())
        print(f'Computer ({self.letter}) chooses square {square}')
        return square

def play(game, x_player, o_player, print_game=True):
    # let’s start by showing the number board
    if print_game:
        game.print_board_nums()
    
    letter = 'X'  # starting letter
    while game.empty_squares():
        # get the move from the appropriate player
        if letter == 'O':
            square = o_player.get_move(game)
        else:
            square = x_player.get_move(game)
        
        # define a move function to make a move for that square
        if game.make_move(square, letter):
            if print_game:
                print(letter + f' makes a move to square {square}')
                game.print_board()
                print('')  # just an empty line for spacing
            
            if game.current_winner:
                if print_game:
                    print(letter + ' wins!')
                return letter  # end the game
            # after move, alternate letters
            letter = 'O' if letter == 'X' else 'X'
            
        # pause briefly after each move (adjust or remove as needed)
        time.sleep(0.8)
    
    if print_game:
        print("It's a tie!")

if __name__ == '__main__':
    x_player = HumanPlayer('X')
    o_player = RandomComputerPlayer('O')
    t = TicTacToe()
    play(t, x_player, o_player, print_game=True)
