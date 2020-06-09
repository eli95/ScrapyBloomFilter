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
- n: 数据量
- p: 误判率
- m: 位数组长度
- k: 哈希函数个数


<p align="center">![](http://latex.codecogs.com/png.latex?m=-\frac{nln^p}{(ln^2)^2})</p>

![](http://latex.codecogs.com/png.latex?k=\frac{m}{n}ln^2)
