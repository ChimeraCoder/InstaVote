init:
	pip install -r requirements.txt

test:
	nosetests2 tests/BallotClassTester.py tests/BallotBoxTester.py

clean:
	rm *.pyc tests/*.pyc
