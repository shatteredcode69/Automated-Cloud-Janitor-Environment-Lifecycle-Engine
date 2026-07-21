test:
	python -m pytest -q

run-compliance:
	python compliance_checker.py

run-janitor:
	python janitor.py
