.DEFAULT_GOAL := help

.PHONY: Cache
Cache:
	-@rm data-files/*.Cache.json data-files/dictionary

	python3 benches/_dictionary.py --fast -o data-files/dictionary.json
	@sleep 1

	python3 benches/_cachebox_cache.py --fast -o data-files/cachebox.Cache.json
	@sleep 1
	
	python3 benches/_cachetools_cache.py --fast -o data-files/cachetools.Cache.json
	@sleep 1
		
	python3 -m pyperf compare_to --table data-files/dictionary.json data-files/cachebox.Cache.json data-files/cachetools.Cache.json

.PHONY: FIFOCache
FIFOCache:
	-@rm data-files/*.FIFOCache.json

	python3 benches/_cachebox_fifo.py --fast -o data-files/cachebox.FIFOCache.json
	@sleep 1
	
	python3 benches/_cachetools_fifo.py --fast -o data-files/cachetools.FIFOCache.json
	@sleep 1
	
	python3 -m pyperf compare_to --table data-files/cachebox.FIFOCache.json data-files/cachetools.FIFOCache.json

.PHONY: LFUCache
LFUCache:
	-@rm data-files/*.LFUCache.json

	python3 benches/_cachebox_lfu.py --fast -o data-files/cachebox.LFUCache.json
	@sleep 1
	
	python3 benches/_cachetools_lfu.py --fast -o data-files/cachetools.LFUCache.json
	@sleep 1

	python3 benches/_cacheing_lfu.py --fast -o data-files/cacheing.LFUCache.json
	@sleep 1
	
	python3 -m pyperf compare_to --table data-files/cachebox.LFUCache.json data-files/cachetools.LFUCache.json data-files/cacheing.LFUCache.json

.PHONY: LRUCache
LRUCache:
	-@rm data-files/*.LRUCache.json

	python3 benches/_cachebox_lru.py --fast -o data-files/cachebox.LRUCache.json
	@sleep 1
	
	python3 benches/_cachetools_lru.py --fast -o data-files/cachetools.LRUCache.json
	@sleep 1

	python3 benches/_cacheing_lru.py --fast -o data-files/cacheing.LRUCache.json
	@sleep 1
	
	python3 -m pyperf compare_to --table data-files/cachebox.LRUCache.json data-files/cachetools.LRUCache.json data-files/cacheing.LRUCache.json

.PHONY: RRCache
RRCache:
	-@rm data-files/*.RRCache.json

	python3 benches/_cachebox_rr.py --fast -o data-files/cachebox.RRCache.json
	@sleep 1
	
	python3 benches/_cachetools_rr.py --fast -o data-files/cachetools.RRCache.json
	@sleep 1

	python3 benches/_cacheing_rr.py --fast -o data-files/cacheing.RRCache.json
	@sleep 1
	
	python3 -m pyperf compare_to --table data-files/cachebox.RRCache.json data-files/cachetools.RRCache.json data-files/cacheing.RRCache.json

.PHONY: TTLCache
TTLCache:
	-@rm data-files/*.TTLCache.json

	python3 benches/_cachebox_ttl.py --fast -o data-files/cachebox.TTLCache.json
	@sleep 1
	
	python3 benches/_cachetools_ttl.py --fast -o data-files/cachetools.TTLCache.json
	@sleep 1

	python3 benches/_cacheing_ttl.py --fast -o data-files/cacheing.TTLCache.json
	@sleep 1
	
	python3 -m pyperf compare_to --table data-files/cachebox.TTLCache.json data-files/cachetools.TTLCache.json data-files/cacheing.TTLCache.json

.PHONY: VTTLCache
VTTLCache:
	-@rm data-files/*.VTTLCache.json

	python3 benches/_cachebox_vttl.py --fast -o data-files/cachebox.VTTLCache.json
	@sleep 1

	python3 benches/_cacheing_vttl.py --fast -o data-files/cacheing.VTTLCache.json
	@sleep 1
	
	python3 -m pyperf compare_to --table data-files/cachebox.VTTLCache.json data-files/cacheing.VTTLCache.json

.PHONY: show
show:
	-@python3 -m pyperf compare_to --table --table-format md data-files/dictionary.json data-files/cachebox.Cache.json data-files/cachetools.Cache.json
	-@echo ""
	
	-@python3 -m pyperf compare_to --table --table-format md data-files/cachebox.FIFOCache.json data-files/cachetools.FIFOCache.json
	-@echo ""
	-@python3 -m pyperf compare_to --table --table-format md data-files/cachebox.LFUCache.json data-files/cachetools.LFUCache.json data-files/cacheing.LFUCache.json
	-@echo ""
	-@python3 -m pyperf compare_to --table --table-format md data-files/cachebox.LRUCache.json data-files/cachetools.LRUCache.json data-files/cacheing.LRUCache.json
	-@echo ""
	-@python3 -m pyperf compare_to --table --table-format md data-files/cachebox.RRCache.json data-files/cachetools.RRCache.json data-files/cacheing.RRCache.json
	-@echo ""
	-@python3 -m pyperf compare_to --table --table-format md data-files/cachebox.TTLCache.json data-files/cachetools.TTLCache.json data-files/cacheing.TTLCache.json
	-@echo ""
	-@python3 -m pyperf compare_to --table --table-format md data-files/cachebox.VTTLCache.json data-files/cacheing.VTTLCache.json

.PHONY: hist
hist:
	@python3 -m pyperf hist data-files/dictionary.json data-files/cachebox.Cache.json data-files/cachetools.Cache.json
	@echo ""
	
	@python3 -m pyperf hist data-files/cachebox.FIFOCache.json data-files/cachetools.FIFOCache.json
	@echo ""
	@python3 -m pyperf hist data-files/cachebox.LFUCache.json data-files/cachetools.LFUCache.json data-files/cacheing.LFUCache.json
	@echo ""
	@python3 -m pyperf hist data-files/cachebox.LRUCache.json data-files/cachetools.LRUCache.json data-files/cacheing.LRUCache.json
	@echo ""
	@python3 -m pyperf hist data-files/cachebox.RRCache.json data-files/cachetools.RRCache.json data-files/cacheing.RRCache.json
	@echo ""
	@python3 -m pyperf hist data-files/cachebox.TTLCache.json data-files/cachetools.TTLCache.json data-files/cacheing.TTLCache.json
	@echo ""
	@python3 -m pyperf hist data-files/cachebox.VTTLCache.json data-files/cacheing.VTTLCache.json

