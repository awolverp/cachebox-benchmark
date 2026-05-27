# Caching libraries Benchmarks


According to my new library [cachebox](https://github.com/awolverp/cachebox), I decided to benchmark caching libraries
which are I know, to show the power of [cachebox](https://github.com/awolverp/cachebox) ...

If you know other library, tell me to add it to this page.

> [!NOTE]\
> The `cacheing.VTTLCache` class was excluded from the benchmark because of numerous unreasonable errors.


## 🖥️ System Information
- **Platform**: Linux-6.18.12-1-MANJARO-x86_64-with-glibc2.43
- **Python**: 3.14.3
- **Processor**: 
- **Libraries**:
  - cachebox: 6.0.0
  - cachetools: 7.1.4
  - cacheing: 0.1.1
  - lru-dict: 1.3.0

## 📊 Insertion


![insertion](photos/insertion.png)

- **Performance Range**: 15.5x difference between fastest and slowest
- **Best**: dict (72ns, 13.9M ops/sec)

|Implementation|Mean (ns)|Std Dev (ns)|Ops/sec|Samples|Stability|
| :---: | :---: | :---: | :---: | :---: | :---: |
|dict|72|1|13.9M|97|1.5%|
|lru.LRU|78|2|12.8M|97|2.2%|
|cachebox.RRCache|93|2|10.7M|98|2.1%|
|cachebox.LFUCache|94|2|10.7M|91|1.9%|
|cachebox.Cache|94|2|10.6M|89|2.1%|
|cachebox.LRUCache|94|2|10.6M|87|2.0%|
|cachebox.FIFOCache|95|2|10.5M|99|1.8%|
|cachebox.TTLCache|162|41|6.2M|907|25.2%|
|cacheing.RandomCache|266|24|3.8M|859|9.1%|
|cacheing.LRUCache|294|13|3.4M|863|4.5%|
|cachetools.Cache|297|13|3.4M|883|4.3%|
|cacheing.LFUCache|320|21|3.1M|832|6.4%|
|cachetools.FIFOCache|379|15|2.6M|873|3.9%|
|cachetools.RRCache|396|27|2.5M|861|6.9%|
|cachetools.LFUCache|401|17|2.5M|815|4.1%|
|cachebox.VTTLCache|422|79|2.4M|944|18.7%|
|moka_py.Moka (lru)|488|145|2.1M|951|29.6%|
|cachetools.LRUCache|564|21|1.8M|871|3.8%|
|moka_py.Moka|565|300|1.8M|932|53.1%|
|cacheing.TTLCache|986|43|1.0M|854|4.4%|
|cachetools.TTLCache|1,117|56|0.9M|861|5.0%|

## 📊 Lookup Existing


![lookup_existing](photos/lookup_existing.png)

- **Performance Range**: 13.6x difference between fastest and slowest
- **Best**: dict (73ns, 13.7M ops/sec)

|Implementation|Mean (ns)|Std Dev (ns)|Ops/sec|Samples|Stability|
| :---: | :---: | :---: | :---: | :---: | :---: |
|dict|73|1|13.7M|97|1.4%|
|cachebox.Cache|83|5|12.1M|823|6.2%|
|cachebox.RRCache|92|1|10.9M|95|1.4%|
|cachebox.LFUCache|93|1|10.8M|89|1.3%|
|cachebox.LRUCache|93|1|10.8M|94|1.3%|
|cachebox.FIFOCache|94|1|10.6M|85|1.2%|
|cacheing.RandomCache|105|10|9.5M|911|9.9%|
|lru.LRU|125|8|8.0M|788|6.0%|
|cachetools.RRCache|154|10|6.5M|894|6.6%|
|cachetools.Cache|155|11|6.5M|905|7.3%|
|cachetools.FIFOCache|157|11|6.4M|906|7.0%|
|cachebox.VTTLCache|173|66|5.8M|956|38.2%|
|cachebox.TTLCache|174|79|5.8M|985|45.3%|
|cacheing.LRUCache|191|12|5.2M|806|6.1%|
|cachetools.LRUCache|306|14|3.3M|851|4.4%|
|cacheing.LFUCache|315|15|3.2M|866|4.9%|
|moka_py.Moka (lru)|341|164|2.9M|940|48.0%|
|moka_py.Moka|349|167|2.9M|951|47.9%|
|cachetools.LFUCache|392|15|2.6M|877|3.8%|
|cacheing.TTLCache|681|28|1.5M|893|4.1%|
|cachetools.TTLCache|994|57|1.0M|951|5.7%|

## 📊 Lookup Missing


![lookup_missing](photos/lookup_missing.png)

- **Performance Range**: 61.8x difference between fastest and slowest
- **Best**: dict (76ns, 13.2M ops/sec)

|Implementation|Mean (ns)|Std Dev (ns)|Ops/sec|Samples|Stability|
| :---: | :---: | :---: | :---: | :---: | :---: |
|dict|76|1|13.2M|85|1.4%|
|cachetools.FIFOCache|120|8|8.3M|866|6.7%|
|cachetools.LFUCache|120|8|8.3M|872|7.0%|
|cachetools.LRUCache|120|8|8.3M|871|7.0%|
|cachetools.RRCache|122|10|8.2M|897|7.9%|
|cachetools.Cache|125|12|8.0M|899|9.5%|
|lru.LRU|188|12|5.3M|871|6.5%|
|moka_py.Moka|332|149|3.0M|940|44.7%|
|moka_py.Moka (lru)|341|156|2.9M|940|45.8%|
|cacheing.RandomCache|467|16|2.1M|861|3.4%|
|cacheing.LFUCache|574|18|1.7M|811|3.1%|
|cachetools.TTLCache|653|22|1.5M|887|3.4%|
|cacheing.LRUCache|715|20|1.4M|882|2.8%|
|cachebox.Cache|1,012|394|1.0M|867|39.0%|
|cacheing.TTLCache|1,697|37|0.6M|918|2.2%|
|cachebox.RRCache|3,842|96|0.3M|882|2.5%|
|cachebox.VTTLCache|4,146|107|0.2M|913|2.6%|
|cachebox.LRUCache|4,166|133|0.2M|892|3.2%|
|cachebox.LFUCache|4,206|143|0.2M|943|3.4%|
|cachebox.TTLCache|4,639|111|0.2M|979|2.4%|
|cachebox.FIFOCache|4,683|125|0.2M|926|2.7%|

## 📊 Deletion


![deletion](photos/deletion.png)

- **Performance Range**: 8.6x difference between fastest and slowest
- **Best**: dict (63ns, 15.9M ops/sec)

|Implementation|Mean (ns)|Std Dev (ns)|Ops/sec|Samples|Stability|
| :---: | :---: | :---: | :---: | :---: | :---: |
|dict|63|4|15.9M|822|6.6%|
|cachebox.Cache|71|2|14.1M|865|3.2%|
|cachebox.RRCache|72|3|13.8M|819|4.2%|
|cachebox.FIFOCache|82|3|12.1M|848|3.5%|
|lru.LRU|88|4|11.3M|829|4.8%|
|cachebox.LRUCache|99|8|10.1M|817|8.4%|
|cachebox.LFUCache|101|8|9.9M|804|8.1%|
|cachebox.TTLCache|108|5|9.3M|886|4.3%|
|cachebox.VTTLCache|128|9|7.8M|816|7.3%|
|cachetools.Cache|162|10|6.2M|930|6.0%|
|cacheing.LRUCache|199|12|5.0M|926|5.8%|
|cachetools.FIFOCache|236|12|4.2M|900|5.0%|
|cachetools.LRUCache|238|15|4.2M|948|6.1%|
|cacheing.LFUCache|259|15|3.9M|933|5.8%|
|cachetools.LFUCache|270|16|3.7M|853|6.1%|
|cacheing.RandomCache|288|34|3.5M|913|11.9%|
|cachetools.RRCache|318|39|3.1M|937|12.3%|
|moka_py.Moka|467|82|2.1M|889|17.5%|
|moka_py.Moka (lru)|468|76|2.1M|878|16.2%|
|cachetools.TTLCache|510|18|2.0M|877|3.5%|
|cacheing.TTLCache|539|26|1.9M|878|4.7%|

## 📊 Popitem


![popitem](photos/popitem.png)

- **Performance Range**: 3972.9x difference between fastest and slowest
- **Best**: cachebox.TTLCache (893ns, 1.1M ops/sec)

|Implementation|Mean (ns)|Std Dev (ns)|Ops/sec|Samples|Stability|
| :---: | :---: | :---: | :---: | :---: | :---: |
|cachebox.TTLCache|893|204|1.1M|973|22.8%|
|cachebox.FIFOCache|918|187|1.1M|970|20.4%|
|lru.LRU|989|129|1.0M|930|13.0%|
|cachebox.LRUCache|1,073|111|0.9M|881|10.4%|
|cacheing.LRUCache|1,387|178|0.7M|955|12.8%|
|cachetools.FIFOCache|1,906|246|0.5M|951|12.9%|
|cacheing.LFUCache|1,984|300|0.5M|971|15.1%|
|cachetools.LRUCache|2,090|287|0.5M|979|13.7%|
|cacheing.TTLCache|2,095|299|0.5M|952|14.3%|
|cacheing.RandomCache|2,799|403|0.4M|963|14.4%|
|cachetools.RRCache|3,052|383|0.3M|968|12.5%|
|cachebox.RRCache|7,212|3,757|0.1M|998|52.1%|
|cachetools.LFUCache|16,119|242|0.1M|894|1.5%|
|cachebox.LFUCache|31,176|848|0.0M|911|2.7%|
|cachebox.VTTLCache|37,553|958|0.0M|922|2.6%|
|cachetools.TTLCache|3,548,048|162,835|0.0M|747|4.6%|

## 📊 Hash Collision


![hash_collision](photos/hash_collision.png)

- **Performance Range**: 7.3x difference between fastest and slowest
- **Best**: cachebox.Cache (3838ns, 0.3M ops/sec)

|Implementation|Mean (ns)|Std Dev (ns)|Ops/sec|Samples|Stability|
| :---: | :---: | :---: | :---: | :---: | :---: |
|cachebox.Cache|3,838|2,129|0.3M|1000|55.5%|
|cachebox.RRCache|3,894|2,142|0.3M|994|55.0%|
|cachebox.VTTLCache|4,181|2,296|0.2M|989|54.9%|
|cachebox.LRUCache|4,206|2,350|0.2M|980|55.9%|
|cachebox.LFUCache|4,279|2,362|0.2M|990|55.2%|
|lru.LRU|4,434|2,446|0.2M|960|55.2%|
|cacheing.RandomCache|4,494|2,451|0.2M|999|54.5%|
|dict|4,514|2,466|0.2M|1000|54.6%|
|cachebox.FIFOCache|4,537|2,519|0.2M|1000|55.5%|
|cachebox.TTLCache|4,625|2,626|0.2M|989|56.8%|
|moka_py.Moka (lru)|6,532|3,512|0.2M|999|53.8%|
|moka_py.Moka|6,588|3,495|0.2M|986|53.1%|
|cachetools.FIFOCache|8,858|4,887|0.1M|999|55.2%|
|cachetools.RRCache|8,911|4,946|0.1M|1000|55.5%|
|cachetools.Cache|8,935|4,965|0.1M|999|55.6%|
|cacheing.LRUCache|8,936|4,924|0.1M|1000|55.1%|
|cacheing.TTLCache|9,413|4,898|0.1M|984|52.0%|
|cachetools.LRUCache|17,836|9,988|0.1M|997|56.0%|
|cachetools.TTLCache|18,490|9,945|0.1M|993|53.8%|
|cacheing.LFUCache|23,930|13,365|0.0M|997|55.8%|
|cachetools.LFUCache|28,031|15,270|0.0M|998|54.5%|

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

### Understanding Results

- **🟢 Excellent (A+)**: <2% noise ratio - Highly reliable measurements
- **🟡 Good (A-B)**: 2-10% noise ratio - Acceptable reliability
- **🔴 Poor (C-D)**: >10% noise ratio - Less reliable measurements

**Performance Metrics**:
- **Mean (ns)**: Average execution time in nanoseconds
- **Ops/sec**: Operations per second (throughput)
- **Stability**: Measurement consistency (lower noise = more stable)
