# If the first argument is "testfile"...
ifeq (testfile,$(firstword $(MAKECMDGOALS)))
  # use the rest as arguments for "python"
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(RUN_ARGS):;@:)
endif

testfile:
	$(if $(RUN_ARGS),PYTHONPATH=. python $(RUN_ARGS),@echo "Usage: make testfile tests/<test_case_file>")

test:
	PYTHONPATH=. unit2 discover -s tests/

sdist:
	python setup.py sdist

publish:
	python setup.py sdist bdist_egg upload

