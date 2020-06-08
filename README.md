#### 关键配置
```python
# 去重类
DUPEFILTER_CLASS
# 哈希函数的个数
BLOOMFILTER_HASH_NUMBER
# BloomFilter 的 bit 参数
BLOOMFILTER_BIT
```

#### 数学结论
m: 位数组长度
n: 数据量
k: 哈希函数个数
p: 误判率

![](http://latex.codecogs.com/gif.latex?\\-\frac{n*ln^p}{(ln^2)^2}})

