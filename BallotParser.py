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

    def count_votes(self):
        vote_counts = dict()
        for candidate in self.candidate_names:
            if candidate in Ballot.eliminated_candidates:
                continue
            vote_counts[candidate] = 0
        for ballot in self.ballots:
            candidate = next(ballot.next_candidate())
            vote_counts[candidate]+= 1
        return vote_counts 

    def find_minimum(self, vote_counts):
        return min(vote_counts, key = lambda x: vote_counts.get(x))

    def find_maximum(self, vote_counts):
        return max(vote_counts, key = lambda x: vote_counts.get(x))

    def identify_winner(self):
        winning_number = len(self.ballots)//2 + 1
        print(winning_number)
        winner_found = False
        while not winner_found:
           vote_counts = self.count_votes()
           best_candidate = self.find_maximum(vote_counts)
           if vote_counts[best_candidate] >= winning_number:
               return best_candidate
           else:
               worst_candidate = self.find_minimum(vote_counts)
               Ballot.eliminate_candidate(worst_candidate)
               print(worst_candidate) 


class BallotBoxTester(unittest.TestCase):
    '''Test the BallotBox class'''
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
        #Make sure the set of eliminated_candidates is clear at the beginning of each unit test
        Ballot.eliminated_candidates = set()

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

    def test_eliminate_candidates_from_ballot_box(self):
        '''Test that the ballot box is able to eliminate candidates properly'''
        Ballot.eliminate_candidate('Aditya')
        for ballot in self.ballot_box.ballots:
            self.assertTrue('Aditya' in ballot.eliminated_candidates)

    def test_count_votes_in_first_round(self):
        '''Test that the BallotBox can count the number of votes in the first round'''
        actual_counts = {
            'Kaley': 1,
            'Roxanne': 3,
            'Aditya' : 2,
            'Michael' : 0,
                }
        vote_results = self.ballot_box.count_votes()
        for key in vote_results:
            self.assertTrue(vote_results[key] == actual_counts[key])

    def test_find_minimum_votes_in_round(self):
        '''Test that the BallotBox can correctly identify the first candidate to be eliminated'''
        first_round_vote_resuts = self.ballot_box.count_votes()
        round_loser = self.ballot_box.find_minimum(first_round_vote_resuts)
        self.assertTrue(round_loser == 'Michael')

    def test_find_minimum_votes_in_round(self):
        '''Test that the BallotBox can correctly identify the candidate with the most votes in a round'''
        first_round_vote_resuts = self.ballot_box.count_votes()
        round_loser = self.ballot_box.find_maximum(first_round_vote_resuts)
        self.assertTrue(round_loser == 'Roxanne')


    def test_identify_winner(self):
        winner = self.ballot_box.identify_winner()
        self.assertTrue(winner == 'Roxanne')


if __name__ == '__main__':
    unittest.main()


