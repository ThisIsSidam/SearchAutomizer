from random_word import RandomWords
import random
import sys
import os
import prefix

def get_file_path(filename):
    if getattr(sys, 'frozen', False):
        # Running in a PyInstaller bundle
        bundle_dir = sys._MEIPASS
    else:
        # Running in a normal Python environment
        bundle_dir = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(bundle_dir, filename)


class RandomQuestion:

    def get_random_question(self):
        question = random.choice(prefix.prefix_list)
        word = RandomWords()
        return question.rstrip('\n') + word.get_random_word()
    



