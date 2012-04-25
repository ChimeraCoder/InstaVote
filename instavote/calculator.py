from __future__ import division, print_function
import BallotParser
import sys

def process_ballots(infile):
    ballot_created = False

    while not ballot_created:
        try:
            ballots_file = infile
            ballot_box = BallotParser.BallotBox(ballots_file)
            ballot_created = True
        except (IndexError, IOError):
            print('Please enter the relative path to the file')
            sys.argv = [None, raw_input(),]


    for ballot in ballot_box.ballots:
        print(ballot.candidates)
     
     

    print(ballot_box.identify_winner(), 'is the winner')
    print(ballot_box.number_rounds, 'rounds of voting were run')

if __name__ == '__main__':
    process_ballots(sys.argv[1])
