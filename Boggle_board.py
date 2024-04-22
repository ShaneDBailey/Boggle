import random
from collections import defaultdict
import Constants

class TrieNode:
    def __init__(self):
        self.children = defaultdict(TrieNode)
        self.is_end_of_word = False

class BoggleBoard():

    def __init__(self, size = 4):
        self.board_size = size
        self.board = self.populate_board()
        self.dictionary = self.build_trie('scrabble_word_list.txt')
        self.valid_word_list = {} # word, highlight_table
        self.find_valid_words()

    def populate_board(self):
        board = [[None] * self.board_size for _ in range(self.board_size)]
        dice = [die for die in Constants.boggle_dice]
        random.shuffle(dice)
        
        index = 0
        for row in range(self.board_size):
            for column in range(self.board_size):
                board[row][column] = random.choice(dice[index])
                index += 1

        return board
#------------------------------Trie Functions----------------------------
    def build_trie(self, file_path):
        root = TrieNode()
        with open(file_path, 'r') as file:
            for line in file:
                word = line.strip()
                if word:
                    node = root
                    for char in word:
                        node = node.children[char]
                    node.is_end_of_word = True
        return root
    
    def is_prefix_in_trie(self, prefix):
        node = self.dictionary
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True if node else False
    
    def is_word_in_trie(self, word):
        node = self.dictionary
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word
#--------------------------------------------------------------------------------------------------
    def find_valid_words(self):
        for row in range(self.board_size):
            for column in range(self.board_size):
                self.depth_first_search(row, column, "", [[False] * self.board_size for _ in range(self.board_size)])

    def depth_first_search(self,row, column, prefix, has_visited):
        if not (0 <= row < self.board_size and 0 <= column < self.board_size) or has_visited[row][column]:
            return

        prefix += self.board[row][column]
        #prune the branching if the prefix does not exist in any of the words
        if not self.is_prefix_in_trie(prefix):
            return

        has_visited[row][column] = True
        if len(prefix) > 2 and self.is_word_in_trie(prefix):
            self.valid_word_list[prefix] = has_visited

        for dir in Constants.directions:
            new_row, new_column = row + dir[0], column + dir[1]
            self.depth_first_search(new_row, new_column, prefix, [list(row) for row in has_visited])

    def print_words_onboard(self):
        for word, highlight in self.valid_word_list.items():
            print(word)
            for i, row in enumerate(self.board):
                for j, letter in enumerate(row):
                    if highlight[i][j]:
                        print("\033[92m" + letter + "\033[0m", end=" ")  # Highlight in green
                    else:
                        print(letter, end=" ")
                print() 
            print()  

    def print_board(self):
        words = list(game.valid_word_list.keys())
        print(", ".join(words))
        print("Boggle Board:")
        for row in self.board:
            print(row)
    

if __name__ == "__main__":

    game = BoggleBoard()
    #game.print_board()
    game.print_words_onboard()
    #input()