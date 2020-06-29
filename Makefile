.PHONY: help black black-format build clean clean-build clean-pyc coverage lint release test-release test test-all

help:
	@echo "black - run black code formatter check"
	@echo "black-format - run black code formatter format"

black:
	black --check ./

black-format:
	black ./