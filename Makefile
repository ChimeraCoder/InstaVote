test:
	nosetests2 tests/BallotClassTester.py tests/BallotBoxTester.py

clean:
	find . -name *.pyc -delete
