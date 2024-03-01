.DEFAULT_GOAL := run


.PHONY: format
format:
	-ruff format --line-length=100 .


.PHONY: clean
clean:
	-ruff clean
	rm -rf `find . -name __pycache__`
	rm -rf .cache


.PHONY: run
run:
	@python3 main.py Cache FIFOCache LFUCache LRUCache MRUCache RRCache TTLCache TTLCacheNoDefault
