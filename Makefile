SHELL := /bin/bash

setup:
	@(\
	    python3 -m venv .venv && \
	    source .venv/bin/activate &&  \
			python3 -m pip install --upgrade pip && \
			python3 -m pip install  bigml && \
			python3 -m pip install  flask && \
	    python3 -m pip install quickchart.io \
	)
