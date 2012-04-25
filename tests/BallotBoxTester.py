from __future__ import division, print_function
import unittest
from instavote.BallotParser import Ballot, BallotBox

class BallotBoxTester(unittest.TestCase):
    '''Test the BallotBox class'''
    def setUp(self):
        self.test_ballot_1_known_values = [
            ('Kaley', 'Roxanne', 'Aditya'),
            ('Roxanne', 'Kaley', 'Aditya'),
            ('Aditya', 'Kaley', 'Roxanne'),
            ('Aditya', 'Roxanne', 'Kaley'),
            ('Roxanne', 'Aditya', 'Kaley'),
            ('Roxanne', 'Aditya', 'Michael'),
            ]
        self.test_ballot_1_file = 'tests/testfiles/test_ballot.csv'
        self.ballot_box_1 = BallotBox(self.test_ballot_1_file)
        #Make sure the set of eliminated_candidates is clear at the beginning of each unit test
        Ballot.eliminated_candidates = set()

    def test_ballot_generator(self):
        '''Test that a ballot is being constructed correctly from a .csv file'''
        for ballot_number, ballot in enumerate(self.ballot_box_1.ballots):
            for candidate_number, candidate in enumerate(ballot.candidates):
                expected_candidate = self.test_ballot_1_known_values[ballot_number][candidate_number]
                self.assertEqual(candidate, expected_candidate)

    def test_name_all_candidates(self):
        '''Test that the candidates' names are being aggregated correctly in the master set of eligible candidates'''
        expected = set(('Kaley', 'Roxanne', 'Aditya', 'Michael'))
        self.assertEqual(self.ballot_box_1.candidate_names, expected)

    def test_eliminate_candidates_from_ballot_box(self):
        '''Test that the ballot box is able to eliminate candidates properly'''
        Ballot.eliminate_candidate('Aditya')
        for ballot in self.ballot_box_1.ballots:
            self.assertTrue('Aditya' in ballot.eliminated_candidates)

    def test_count_votes_in_first_round(self):
        '''Test that the BallotBox can count the number of votes in the first round'''
        actual_counts = {
            'Kaley': 1,
            'Roxanne': 3,
            'Aditya' : 2,
            'Michael' : 0,
                }
        vote_results = self.ballot_box_1.count_votes()
        for key in vote_results:
            self.assertTrue(vote_results[key] == actual_counts[key])

    def test_find_minimum_votes_in_round(self):
        '''Test that the BallotBox can correctly identify the first candidate to be eliminated'''
        first_round_vote_resuts = self.ballot_box_1.count_votes()
        round_loser = self.ballot_box_1.find_minimum(first_round_vote_resuts)
        self.assertTrue(round_loser == 'Michael')

    def test_find_minimum_votes_in_round(self):
        '''Test that the BallotBox can correctly identify the candidate with the most votes in a round'''
        first_round_vote_resuts = self.ballot_box_1.count_votes()
        round_loser = self.ballot_box_1.find_maximum(first_round_vote_resuts)
        self.assertTrue(round_loser == 'Roxanne')


    def test_identify_winner(self):
        winner = self.ballot_box_1.identify_winner()
        self.assertTrue(winner == 'Roxanne')


if __name__ == '__main__':
    unittest.main()



