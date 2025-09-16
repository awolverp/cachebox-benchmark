# Caching libraries Benchmarks

According to my new library [cachebox](https://github.com/awolverp/cachebox), I decided to benchmark caching libraries
which are I know, to show the power of [cachebox](https://github.com/awolverp/cachebox) ...

If you know other library, tell me to add it to this page.

> [!NOTE]\
> The `cacheing.VTTLCache` class was excluded from the benchmark because of numerous unreasonable errors.


## 🖥️ System Information
- **Platform**: Linux-6.15.11-2-MANJARO-x86_64-with-glibc2.42
- **Python**: 3.13.7
- **Libraries**:
  - cachebox: 5.0.2
  - cachetools: 6.2.0
  - cacheing: 0.1.1
  - lru-dict: 1.3.0

## 📊 Insertion


![insertion](photos/insertion.png)

- **Performance Range**: 16.3x difference between fastest and slowest
- **Best**: builtins.dict (85ns, 11.8M ops/sec)
- **Analysis**: 9 of 19 implementations show stable measurements


|Implementation|Mean (ns)|Std Dev (ns)|Ops/sec|Samples|Stability|
| :---: | :---: | :---: | :---: | :---: | :---: |
|builtins.dict|85|0|11.8M|89|0.5%|
|_lru.LRU|100|1|10.0M|88|1.0%|
|cachebox.Cache|195|39|5.1M|943|20.2%|
|cachebox.RRCache|196|38|5.1M|944|19.4%|
|cachebox.FIFOCache|203|45|4.9M|922|22.1%|
|cachebox.TTLCache|232|45|4.3M|922|19.4%|
|cachebox.LRUCache|268|75|3.7M|938|27.9%|
|cachebox.LFUCache|272|77|3.7M|941|28.2%|
|cacheing.RandomCache|301|21|3.3M|857|6.8%|
|cachetools.Cache|329|16|3.0M|909|4.8%|
|cacheing.LRUCache|332|13|3.0M|887|3.8%|
|cacheing.LFUCache|362|19|2.8M|875|5.1%|
|cachetools.RRCache|422|23|2.4M|876|5.4%|
|cachebox.VTTLCache|431|71|2.3M|937|16.6%|
|cachetools.LFUCache|441|20|2.3M|873|4.5%|
|cachetools.FIFOCache|595|22|1.7M|875|3.7%|
|cachetools.LRUCache|616|27|1.6M|893|4.5%|
|cacheing.TTLCache|1,123|41|0.9M|865|3.7%|
|cachetools.TTLCache|1,383|68|0.7M|907|4.9%|

## 📊 Lookup Existing


![lookup_existing](photos/lookup_existing.png)

- **Performance Range**: 13.5x difference between fastest and slowest
- **Best**: builtins.dict (82ns, 12.2M ops/sec)
- **Analysis**: 9 of 19 implementations show stable measurements


|Implementation|Mean (ns)|Std Dev (ns)|Ops/sec|Samples|Stability|
| :---: | :---: | :---: | :---: | :---: | :---: |
|builtins.dict|82|1|12.2M|98|1.3%|
|cacheing.RandomCache|103|3|9.7M|792|2.6%|
|cachebox.Cache|104|5|9.6M|811|4.6%|
|cachebox.RRCache|106|8|9.4M|936|7.7%|
|cachebox.FIFOCache|111|8|9.0M|925|7.7%|
|cachebox.LRUCache|121|28|8.3M|875|22.9%|
|_lru.LRU|130|7|7.7M|751|5.0%|
|cachebox.LFUCache|154|60|6.5M|956|38.6%|
|cachetools.FIFOCache|159|8|6.3M|912|5.3%|
|cachetools.RRCache|163|10|6.1M|935|6.1%|
|cachetools.Cache|167|12|6.0M|950|7.2%|
|cachebox.TTLCache|195|9|5.1M|935|4.8%|
|cacheing.LRUCache|211|10|4.8M|875|4.6%|
|cachebox.VTTLCache|235|61|4.3M|935|26.1%|
|cachetools.LRUCache|315|13|3.2M|860|4.1%|
|cacheing.LFUCache|376|25|2.7M|897|6.5%|
|cachetools.LFUCache|405|14|2.5M|906|3.6%|
|cacheing.TTLCache|729|23|1.4M|909|3.2%|
|cachetools.TTLCache|1,106|51|0.9M|950|4.6%|

## 📊 Lookup Missing


![lookup_missing](photos/lookup_missing.png)

- **Performance Range**: 61.7x difference between fastest and slowest
- **Best**: builtins.dict (83ns, 12.0M ops/sec)
- **Analysis**: 12 of 19 implementations show stable measurements


|Implementation|Mean (ns)|Std Dev (ns)|Ops/sec|Samples|Stability|
| :---: | :---: | :---: | :---: | :---: | :---: |
|builtins.dict|83|1|12.0M|84|0.8%|
|cachetools.RRCache|127|7|7.9M|890|5.7%|
|cachetools.LFUCache|127|8|7.9M|887|6.3%|
|cachetools.FIFOCache|129|8|7.7M|891|6.2%|
|cachetools.LRUCache|130|8|7.7M|888|6.2%|
|cachetools.Cache|132|11|7.6M|912|8.2%|
|_lru.LRU|207|11|4.8M|902|5.3%|
|cacheing.RandomCache|505|19|2.0M|914|3.7%|
|cacheing.LFUCache|624|19|1.6M|901|3.0%|
|cacheing.LRUCache|744|20|1.3M|911|2.7%|
|cachetools.TTLCache|826|25|1.2M|921|3.0%|
|cachebox.Cache|1,202|543|0.8M|998|45.2%|
|cacheing.TTLCache|1,709|64|0.6M|963|3.8%|
|cachebox.RRCache|4,601|124|0.2M|977|2.7%|
|cachebox.LRUCache|4,768|126|0.2M|939|2.7%|
|cachebox.LFUCache|4,808|145|0.2M|958|3.0%|
|cachebox.VTTLCache|4,817|141|0.2M|949|2.9%|
|cachebox.FIFOCache|5,121|145|0.2M|979|2.8%|
|cachebox.TTLCache|5,128|131|0.2M|944|2.6%|

## 📊 Deletion


![deletion](photos/deletion.png)

- **Performance Range**: 8.3x difference between fastest and slowest
- **Best**: builtins.dict (72ns, 13.9M ops/sec)
- **Analysis**: 13 of 19 implementations show stable measurements


|Implementation|Mean (ns)|Std Dev (ns)|Ops/sec|Samples|Stability|
| :---: | :---: | :---: | :---: | :---: | :---: |
|builtins.dict|72|2|13.9M|861|3.3%|
|_lru.LRU|94|3|10.6M|796|3.0%|
|cachebox.Cache|129|5|7.8M|836|3.6%|
|cachebox.LRUCache|138|3|7.3M|856|2.0%|
|cachebox.FIFOCache|141|6|7.1M|870|4.1%|
|cachebox.LFUCache|151|8|6.6M|902|5.4%|
|cachebox.RRCache|165|3|6.1M|849|1.5%|
|cachetools.Cache|172|10|5.8M|974|5.6%|
|cachebox.TTLCache|211|9|4.7M|932|4.5%|
|cachebox.VTTLCache|213|4|4.7M|820|2.1%|
|cacheing.LRUCache|228|10|4.4M|944|4.3%|
|cachetools.FIFOCache|248|10|4.0M|901|3.9%|
|cachetools.LRUCache|250|13|4.0M|941|5.1%|
|cachetools.LFUCache|276|14|3.6M|921|5.0%|
|cacheing.LFUCache|294|13|3.4M|942|4.4%|
|cacheing.RandomCache|309|24|3.2M|945|7.8%|
|cachetools.RRCache|316|31|3.2M|964|9.7%|
|cachetools.TTLCache|537|33|1.9M|965|6.1%|
|cacheing.TTLCache|602|22|1.7M|900|3.7%|

## 📊 Popitem


![popitem](photos/popitem.png)

- **Performance Range**: 4023.3x difference between fastest and slowest
- **Best**: cachebox.LRUCache (887ns, 1.1M ops/sec)
- **Analysis**: 4 of 16 implementations show stable measurements


|Implementation|Mean (ns)|Std Dev (ns)|Ops/sec|Samples|Stability|
| :---: | :---: | :---: | :---: | :---: | :---: |
|cachebox.LRUCache|887|153|1.1M|939|17.2%|
|cachebox.FIFOCache|899|148|1.1M|949|16.4%|
|_lru.LRU|996|177|1.0M|959|17.7%|
|cachebox.TTLCache|1,029|144|1.0M|959|14.0%|
|cacheing.LRUCache|1,245|118|0.8M|919|9.5%|
|cachetools.FIFOCache|1,682|206|0.6M|962|12.2%|
|cachetools.LRUCache|1,949|300|0.5M|986|15.4%|
|cacheing.TTLCache|2,158|270|0.5M|968|12.5%|
|cacheing.LFUCache|2,178|335|0.5M|970|15.4%|
|cacheing.RandomCache|2,825|321|0.4M|927|11.4%|
|cachetools.RRCache|3,137|371|0.3M|962|11.8%|
|cachebox.RRCache|7,081|3,668|0.1M|998|51.8%|
|cachetools.LFUCache|13,224|339|0.1M|935|2.6%|
|cachebox.LFUCache|24,739|701|0.0M|933|2.8%|
|cachebox.VTTLCache|26,367|554|0.0M|907|2.1%|
|cachetools.TTLCache|3,567,183|121,611|0.0M|782|3.4%|

## 📊 Hash Collision


![hash_collision](photos/hash_collision.png)

- **Performance Range**: 7.2x difference between fastest and slowest
- **Best**: cachebox.Cache (4394ns, 0.2M ops/sec)
- **Analysis**: 0 of 19 implementations show stable measurements


|Implementation|Mean (ns)|Std Dev (ns)|Ops/sec|Samples|Stability|
| :---: | :---: | :---: | :---: | :---: | :---: |
|cachebox.Cache|4,394|2,444|0.2M|1000|55.6%|
|cachebox.RRCache|4,395|2,442|0.2M|1000|55.6%|
|cachebox.LFUCache|4,496|2,503|0.2M|999|55.7%|
|cachebox.LRUCache|4,504|2,493|0.2M|999|55.3%|
|cachebox.VTTLCache|4,602|2,510|0.2M|999|54.5%|
|cachebox.FIFOCache|4,825|2,681|0.2M|1000|55.6%|
|cachebox.TTLCache|4,949|2,708|0.2M|1000|54.7%|
|builtins.dict|4,996|2,781|0.2M|1000|55.7%|
|cacheing.RandomCache|5,080|2,781|0.2M|1000|54.7%|
|_lru.LRU|5,145|2,869|0.2M|1000|55.8%|
|cachetools.RRCache|9,972|5,558|0.1M|1000|55.7%|
|cachetools.Cache|10,042|5,514|0.1M|1000|54.9%|
|cachetools.FIFOCache|10,065|5,703|0.1M|1000|56.7%|
|cacheing.LRUCache|10,094|5,547|0.1M|1000|55.0%|
|cacheing.TTLCache|10,655|5,657|0.1M|1000|53.1%|
|cachetools.LRUCache|20,029|11,498|0.0M|979|57.4%|
|cachetools.TTLCache|21,014|11,344|0.0M|1000|54.0%|
|cacheing.LFUCache|26,688|14,823|0.0M|997|55.5%|
|cachetools.LFUCache|31,750|17,571|0.0M|988|55.3%|

## 🚀 Usage


### Prerequisites
```bash
uv sync
```

### Run Benchmarks
```bash
# All benchmarks
python main.py

# Specific benchmark
python main.py insertion
python main.py lookup_existing
```

**Performance Metrics**:
- **Mean (ns)**: Average execution time in nanoseconds
- **Ops/sec**: Operations per second (throughput)
- **Stability**: Measurement consistency (lower noise = more stable)
