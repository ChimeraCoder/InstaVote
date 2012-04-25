init:
	pip install -r requirements.txt

test:
	nosetests2 BallotParser.py

clean:
	rm *.pyc
