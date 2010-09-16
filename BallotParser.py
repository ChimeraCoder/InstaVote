from __future__ import division, print_function
import unittest

class Ballot:
    '''A Ballot contains a ranked list of candidate names'''
    #Keep track of candidates who have been eliminated

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

    eliminated_candidates = set()
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
        '''Create a three-way ballot and check that the candidates are correct'''
        ballot = Ballot(self.abc_candidate_list)
        self.assertEqual(ballot.candidates, self.abc_candidate_list)

    def test_candidate_name_generator(self):
        '''Test that the ballot can eliminate candidates and return the next eligible candidate accurately'''
        for rank, candidate in enumerate(self.defghijk_ballot.next_candidate()):
            self.assertEqual(self.defghijk_candidates_list[rank], candidate)
            #Eliminate the current candidate so that he/she is no longer the top eligible candidate
            self.defghijk_ballot.eliminated_candidates.add(candidate)

    def test_candidate_name_generator_with_elimination(self):
        '''Test that the ballot can yield the same candidate twice, then yield a different candidate once the first candidate is eliminated'''
        count = 0
        for rank, candidate in enumerate(self.defghijk_ballot.next_candidate()):
            #Check that the candidate that .next_candidate() yields is not in the list of eliminated candidates
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


class BallotBox:

    def __init__(self, filename):
        self.ballots = self.BallotGenerator(filename)
        self.candidate_names = self.name_candidates()

    def BallotGenerator(self, filename):
        '''Generate a ballot box (list of ballots) from a .csv that contains the ballot information'''
        list_of_ballots = []
        with open(filename) as ballot_file:
            for line in ballot_file:
                linesplit = line.split(',')
                linesplit = [name.strip() for name in linesplit]
                current_ballot = Ballot(linesplit)
                list_of_ballots.append(current_ballot)
        return list_of_ballots      
    
    def name_candidates(self):
        '''Create a set that contains the names of all eligible candidates'''
        candidate_names = set()
        for ballot in self.ballots:
            for name in ballot.candidates:
                candidate_names.add(name)
        return candidate_names

class BallotBoxTester(unittest.TestCase):

    def setUp(self):
        self. known_values = [
            ('Kaley', 'Roxanne', 'Aditya'),
            ('Roxanne', 'Kaley', 'Aditya'),
            ('Aditya', 'Kaley', 'Roxanne'),
            ('Aditya', 'Roxanne', 'Kaley'),
            ('Roxanne', 'Aditya', 'Kaley'),
            ('Roxanne', 'Aditya', 'Michael'),
            ]
        self.test_ballot_file = 'testfiles/test_ballot.csv'
        self.ballot_box = BallotBox(self.test_ballot_file)

    def test_ballot_generator(self):
        '''Test that a ballot is being constructed correctly from a .csv file'''
        for ballot_number, ballot in enumerate(self.ballot_box.ballots):
            for candidate_number, candidate in enumerate(ballot.candidates):
                expected_candidate = self.known_values[ballot_number][candidate_number]
                self.assertEqual(candidate, expected_candidate)

    def test_name_all_candidates(self):
        '''Test that the candidates' names are being aggregated correctly in the master set of eligible candidates'''
        expected = set(('Kaley', 'Roxanne', 'Aditya', 'Michael'))
        self.assertEqual(self.ballot_box.candidate_names, expected)

    



if __name__ == '__main__':
    unittest.main()


