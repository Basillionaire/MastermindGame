"""
Basil Coughlan
Test mastermind game
"""

import unittest

from mastermind_game import make_secret_code, count_bulls_and_cows, GameRunner, \
     CircleData, ImageData


class TestGameRunner(unittest.TestCase):
##    def test_make_secret_code(self):



    def test_count_bulls_and_cows(self):

        x = count_bulls_and_cows(['red', 'blue', 'black', 'green'], ['red', 'blue',\
                                'black', 'purple'])
        self.assertEqual(len(secret_code), len(guess))



##    def test_show_winners(self):
##
##
##    def test_declare_user(self):
##
##    def test_read_scores(self):
##
##    def test_handle_clicks_on_input_circles(self):
        
        
if __name__ == '__main__':
    unittest.main()
