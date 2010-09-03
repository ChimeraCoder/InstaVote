from __future__ import division, print_function
import unittest

class Ballot:

    eliminated_candidates = set()

    def __init__(self, candidate_list):
        self.candidates = candidate_list

    def next_candidate(self):
        candidate_index = 0
        while candidate_index < len(self.candidates):
            yield self.candidates[candidate_index]
            candidate_index += 1

class TestAcceptanceTests(unittest.TestCase):

    def setUp(self):
        self.abc_candidate_list = ['Adam', 'Bob', 'Charles']
        self.abc_candidates = Ballot(self.abc_candidate_list)
        self.defghijk_candidates_list = ['Donald', 'Edward', 'Francis', 'Greta', 'Hilda', 'Igor', 'John', 'Kathy']
        self.defghijk_ballot= Ballot(self.defghijk_candidates_list)

    def test_create_sample_three_way_ballot(self):
        ballot = Ballot(self.abc_candidate_list)
        self.assertEqual(ballot.candidates, self.abc_candidate_list)

    def test_candidate_name_generator(self):
        for rank, candidate in enumerate(self.defghijk_ballot.next_candidate()):
            self.assertEqual(self.defghijk_candidates_list[rank], candidate)

    def test_candidate_name_generator_with_elimination(self):
        self.defghijk_ballot.eliminated_candidates.add('Greta', 'Edward')
        for rank, candidate in enumerate(self.defghijk_ballot.next_candidate()):
            self.assertTrue(candidate not in self.defghijk_ballot.eliminated_candidates)






    def test_setup_feature(self):
        '''Test that the setUp() method is functioning properly'''
        self.assertEqual(self.abc_candidates.candidates, ['Adam', 'Bob', 'Charles'])


if __name__ == '__main__':
    unittest.main()



