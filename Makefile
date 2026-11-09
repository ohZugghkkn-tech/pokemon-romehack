# Project entrypoints; SoulGold's own build stays in soulgold/.
PYTHON ?= python3
.DEFAULT_GOAL := help
.PHONY: help check rom target-tests

help:
	@printf '%s\n' 'make check        Host checks (requires development dependencies)' 'make rom          ARM build, no ROM publication' 'make target-tests Full ARM/mGBA test suite' 'See TESTING.md for prerequisites and limitations.'

check:
	$(PYTHON) scripts/check.py

rom:
	$(MAKE) -C soulgold all

target-tests:
	$(MAKE) -C soulgold check-all
