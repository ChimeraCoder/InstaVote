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


class BallotBox:

    def __init__(self, filename):
        self.ballots = self.BallotGenerator(filename)
        self.candidate_names = self.name_candidates()
        #if positive, self.number_rounds represents the number of rounds required to determine the winner
        self.number_rounds = -1


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
            try: candidate = next(ballot.next_candidate())
            except StopIteration:
                #If the ballot has no more valid candidates, then skip the ballot
                continue
            vote_counts[candidate]+= 1
        return vote_counts 

    def find_minimum(self, vote_counts):
        return min(vote_counts, key = lambda x: vote_counts.get(x))

    def find_maximum(self, vote_counts):
        return max(vote_counts, key = lambda x: vote_counts.get(x))

    def identify_winner(self):
        winning_number = len(self.ballots)//2 + 1
        winner_found = False
        number_rounds = 0
        while not winner_found:
            number_rounds +=1
            vote_counts = self.count_votes()
            best_candidate = self.find_maximum(vote_counts)
            if vote_counts[best_candidate] >= winning_number:
               self.number_rounds = number_rounds
               return best_candidate
            else:
                worst_candidate = self.find_minimum(vote_counts)
                worst_number_of_votes = vote_counts[worst_candidate]
                #If there is a tie for worst_candidate, the candidate returned by find_minimum will be arbitrary, so it is necessary to eliminate all candidates with this same number of votes to ensure that the outcome is predictable
                for candidate in vote_counts:
                    if vote_counts[candidate] == worst_number_of_votes:
                        Ballot.eliminate_candidate(candidate)



