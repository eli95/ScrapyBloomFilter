#### 使用
- 安装
```
git clone https://github.com/ELI95/ScrapyBloomFilter.git
cd ScrapyBloomFilter
python setup.py build
python setup.py install
```

- 配置
```python
SCHEDULER = "scrapy_bloomfilter.scheduler.Scheduler"

DUPEFILTER_CLASS = "scrapy_bloomfilter.dupefilter.RedisDupeFilter"

REDIS_URL = 'redis://@localhost:6379'

BLOOMFILTER_HASH_NUMBER = 6

BLOOMFILTER_BIT = 10

SCHEDULER_PERSIST = False
```


#### 数学结论
- n: 数据量
- p: 误判率
- m: 位数组长度
- k: 哈希函数个数

> ![](http://latex.codecogs.com/png.latex?m=-\frac{nln^p}{(ln^2)^2})

> ![](http://latex.codecogs.com/png.latex?k=\frac{m}{n}ln^2)
