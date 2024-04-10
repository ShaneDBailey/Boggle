import random

boggle_dice = (
    ('R', 'I', 'F', 'O', 'B', 'X'),
    ('I', 'F', 'E', 'H', 'E', 'Y'),
    ('D', 'E', 'N', 'O', 'W', 'S'),
    ('U', 'T', 'O', 'K', 'N', 'D'),
    ('H', 'M', 'S', 'R', 'A', 'O'),
    ('L', 'U', 'P', 'E', 'T', 'S'),
    ('A', 'C', 'I', 'T', 'O', 'A'),
    ('Y', 'L', 'G', 'K', 'U', 'E'),
    ('QU', 'B', 'M', 'J', 'O', 'A'),
    ('E', 'H', 'I', 'S', 'P', 'N'),
    ('V', 'E', 'T', 'I', 'G', 'N'),
    ('B', 'A', 'L', 'I', 'Y', 'T'),
    ('E', 'Z', 'A', 'V', 'N', 'D'),
    ('R', 'A', 'L', 'E', 'S', 'C'),
    ('U', 'W', 'I', 'L', 'R', 'G'),
    ('P', 'A', 'C', 'E', 'M', 'D')
)
directions = ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))

def dictionary(file_path):
    words = set()  
    with open(file_path, 'r') as file:
        for line in file:
            word = line.strip()
            if word:
                words.add(word)
    return words

class BoggleBoard():

    def __init__(self, size = 4):
        self.board_size = 4
        self.board = [[None] * size for _ in range(size)]
        self.populate_board()
        self.dictionary = dictionary('scrabble_word_list.txt')
        self.valid_word_list = set()
        self.find_valid_words()

    def populate_board(self):
        dice = [die for die in boggle_dice]
        random.shuffle(dice)
        
        index = 0
        for row in range(self.board_size):
            for col in range(self.board_size):
                self.board[row][col] = random.choice(dice[index])
                index += 1

    def find_valid_words(self):

        for row in range(self.board_size):
            for column in range(self.board_size):
                self.depth_first_search(row, column, "", [[False] * self.board_size for _ in range(self.board_size)])

    def depth_first_search(self,row, column, prefix,has_visited):
        if not (0 <= row < self.board_size and 0 <= column < self.board_size) or has_visited[row][column]:
            return

        prefix += self.board[row][column]
        #prune the branching if the prefix does not exist in any of the words
        if not self.is_prefix_in_dictionary(prefix, self.dictionary):
            return

        has_visited[row][column] = True
        if  len(prefix) > 2 and prefix not in self.valid_word_list and prefix in self.dictionary:
            self.valid_word_list.add(prefix)

        for dir in directions:
            new_row, new_column = row + dir[0], column + dir[1]
            self.depth_first_search(new_row, new_column, prefix, [list(row) for row in has_visited])

    def is_prefix_in_dictionary(self, prefix, dictionary):
        for word in dictionary:
            if word.startswith(prefix):
                return True
        return False
    
    def print_board(self):
        print("Boggle Board:")
        for row in self.board:
            print(row)
    

if __name__ == "__main__":

    game = BoggleBoard()
    print(game.valid_word_list)
    game.print_board()