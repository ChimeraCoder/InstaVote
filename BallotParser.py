from __future__ import division, print_function
import unittest

class Ballot:
    '''A Ballot contains a ranked list of candidate names'''
    #Keep track of candidates who have been eliminated
    eliminated_candidates = set()

    def __init__(self, candidate_list):
        '''Create a ballot from a ranked list of candidate names'''
        self.candidates = candidate_list

    def next_candidate(self):
        '''Determine the next candidate who has not yet been eliminated'''
        candidate_index = 0
        while candidate_index < len(self.candidates):
            if self.candidates[candidate_index] in Ballot.eliminated_candidates:
                candidate_index += 1
            else:
                yield self.candidates[candidate_index]

    @classmethod
    def eliminate_candidate(cls, newly_eliminated_candidate):
        '''Update the set of eliminated candidates with the newly eliminated candidate'''
        cls.eliminated_candidates.add(newly_eliminated_candidate)


class BallotClassTester(unittest.TestCase):
    '''Test the Ballot class'''
    def setUp(self):
        self.abc_candidate_list = ['Adam', 'Bob', 'Charles']
        self.abc_ballot = Ballot(self.abc_candidate_list)
        self.defghijk_candidates_list = ['Donald', 'Edward', 'Francis', 'Greta', 'Hilda', 'Igor', 'John', 'Kathy']
        self.defghijk_ballot= Ballot(self.defghijk_candidates_list)
        self.abcdefghijk_candidate_list = list(self.abc_candidate_list)
        self.abcdefghijk_candidate_list.extend(self.defghijk_candidates_list)
        self.abcdefghijk_ballot = Ballot(self.abcdefghijk_candidate_list)


    def test_create_sample_three_way_ballot(self):
        ballot = Ballot(self.abc_candidate_list)
        self.assertEqual(ballot.candidates, self.abc_candidate_list)

    def test_candidate_name_generator(self):
        for rank, candidate in enumerate(self.defghijk_ballot.next_candidate()):
            self.assertEqual(self.defghijk_candidates_list[rank], candidate)
            #Eliminate the current candidate so that he/she is no longer the top eligible candidate
            self.defghijk_ballot.eliminated_candidates.add(candidate)

    def test_candidate_name_generator_with_elimination(self):
        count = 0
        for rank, candidate in enumerate(self.defghijk_ballot.next_candidate()):
            self.assertTrue(candidate not in self.defghijk_ballot.eliminated_candidates)
            count += 1
            if count > 2:
                count = 0
                self.defghijk_ballot.eliminated_candidates.add(candidate)


    def test_eliminate_candidate_function(self):
        '''Test Ballot.eliminate_candidate()'''
        first_candidate_ballot_1 = self.abc_ballot.next_candidate()
        Ballot.eliminate_candidate(first_candidate_ballot_1)
        second_candidate_ballot_1 = self.abc_ballot.next_candidate()
        second_candidate_ballot_2 = self.abcdefghijk_ballot.next_candidate
        self.assertTrue(first_candidate_ballot_1 != second_candidate_ballot_2)
        self.assertTrue(second_candidate_ballot_1, second_candidate_ballot_2)

    def test_setup_feature(self):
        '''Test that the setUp() method is functioning properly'''
        self.assertEqual(self.abc_ballot.candidates, ['Adam', 'Bob', 'Charles'])



def BallotGenerator(filename):
    '''Generate a ballot box (list of ballots) from a .csv that contains the ballot information'''

    ballot_box = []
    with open(filename) as ballot_file:
        for line in ballot_file:
            linesplit = line.split(',')
            linesplit = [name.strip() for name in linesplit]
            current_ballot = Ballot(linesplit)
    return ballot_box        


class BallotGeneratorTester(unittest.TestCase):

    def test_ballot_generator(self):
        known_values = [
            ('Kaley', 'Roxanne', 'Aditya'),
            ('Roxanne', 'Kaley', 'Aditya'),
            ('Aditya', 'Kaley', 'Roxanne'),
            ('Aditya', 'Roxanne', 'Kaley'),
            ('Roxanne', 'Aditya', 'Kaley'),
            ('Roxanne', 'Aditya', 'Michael'),
            ]
        test_ballot = 'testfiles/test_ballot.csv'
        ballot_box = BallotGenerator(test_ballot)
        for ballot_number, ballot in enumerate(ballot_box):
            for candidate_number, candidate in enumerate(ballot.candidates):
                expected_candidate = known_values[ballot_number][candidate_number]
                self.assertEqual(candidate, expected_candidate)





if __name__ == '__main__':
    unittest.main()


