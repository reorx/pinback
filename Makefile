.PHONY: clean test

all: bundle

bundle:
	@bash make_bundle.sh

test:
	PYTHONPATH=. pytest

clean:
	rm -rf build dist *.egg-info
