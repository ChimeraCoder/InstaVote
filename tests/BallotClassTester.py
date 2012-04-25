from __future__ import division, print_function
import unittest
from instavote.BallotParser import BallotBox, Ballot

class BallotClassTester(unittest.TestCase):
    '''Test the Ballot class'''
    def setUp(self):
        #Make sure the set of eliminated_candidates is clear at the beginning of each unit test
        Ballot.eliminated_candidates = set()
        self.a_to_c_candidate_list = ['Adam', 'Bob', 'Charles']
        self.a_to_c_ballot = Ballot(self.a_to_c_candidate_list)
        self.d_to_k_candidates_list = ['Donald', 'Edward', 'Francis', 'Greta', 'Hilda', 'Igor', 'John', 'Kathy']
        self.d_to_k_ballot= Ballot(self.d_to_k_candidates_list)
        self.a_to_k_candidate_list = list(self.a_to_c_candidate_list)
        self.a_to_k_candidate_list.extend(self.d_to_k_candidates_list)
        self.a_to_k_ballot = Ballot(self.a_to_k_candidate_list)

    def test_create_sample_three_way_ballot(self):
        '''Create a three-way ballot and check that the candidates are correct'''
        ballot = Ballot(self.a_to_c_candidate_list)
        self.assertEqual(ballot.candidates, self.a_to_c_candidate_list)

    def test_candidate_name_generator(self):
        '''Test that the ballot can eliminate candidates and return the next eligible candidate accurately'''
        entered_loop = False
        #Use next_candidate() to generate the next eligible candidate
        for rank, candidate in enumerate(self.d_to_k_ballot.next_candidate()):
            entered_loop = True
            self.assertEqual(self.d_to_k_candidates_list[rank], candidate)
            #Eliminate the current candidate so that he/she is no longer the top eligible candidate
            self.d_to_k_ballot.eliminated_candidates.add(candidate)
        #Ensure that the loop was actually executed
        self.assertTrue(entered_loop)

    def test_candidate_name_generator_with_elimination(self):
        '''Test that the ballot can yield the same candidate twice, then yield a different candidate once the first candidate is eliminated'''
        count = 0
        entered_loop = False
        for rank, candidate in enumerate(self.d_to_k_ballot.next_candidate()):
            entered_loop = True
            #Check that the candidate that .next_candidate() yields is not in the list of eliminated candidates
            count += 1
            self.assertTrue(candidate not in self.d_to_k_ballot.eliminated_candidates)
            if count > 1:
                count = 0
                self.d_to_k_ballot.eliminated_candidates.add(candidate)
        #Ensure that the loop was actually executed
        self.assertTrue(entered_loop)

    def test_eliminate_candidate_function(self):
        '''Test Ballot.eliminate_candidate()'''
        first_candidate_ballot_1 = self.a_to_c_ballot.next_candidate()
        Ballot.eliminate_candidate(first_candidate_ballot_1)
        second_candidate_ballot_1 = self.a_to_c_ballot.next_candidate()
        second_candidate_ballot_2 = self.a_to_k_ballot.next_candidate
        self.assertTrue(first_candidate_ballot_1 != second_candidate_ballot_2)
        self.assertTrue(second_candidate_ballot_1, second_candidate_ballot_2)

    def test_setup_feature(self):
        '''Test that the setUp() method is functioning properly'''
        self.assertEqual(self.a_to_c_ballot.candidates, ['Adam', 'Bob', 'Charles'])


