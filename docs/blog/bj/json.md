# JSON学习
## 什么是json
* JSON 指的是 JavaScript 对象表示法（JavaScript Object Notation）
* JSON 是轻量级的文本数据交换格式
* JSON 独立于语言：JSON 使用 Javascript语法来描述数据对象，但是 JSON 仍然独立于语言和平台。JSON 解析器和 JSON 库支持许多不同的编程语言。 目前非常多的动态（PHP，JSP，.NET）编程语言都支持 JSON
* JSON 具有自我描述性，更易理解
## JSON vs XML
json实例：
```
{
    "sites": [
    { "name":"菜鸟教程" , "url":"www.runoob.com" }, 
    { "name":"google" , "url":"www.google.com" }, 
    { "name":"微博" , "url":"www.weibo.com" }
    ]
}
```
xml实例：
```
<sites>
  <site>
    <name>菜鸟教程</name> <url>www.runoob.com</url>
  </site>
  <site>
    <name>google</name> <url>www.google.com</url>
  </site>
  <site>
    <name>微博</name> <url>www.weibo.com</url>
  </site>
</sites>
```
**JSON 与 XML 的相同之处：**

>JSON 和 XML 数据都是 "自我描述" ，都易于理解。  
JSON 和 XML 数据都是有层次的结构   
JSON 和 XML 数据可以被大多数编程语言使用   

**JSON 与 XML 的不同之处：**
>JSON 不需要结束标签  
JSON 更加简短  
JSON 读写速度更快  
JSON 可以使用数组  

## Python JSON

使用 JSON 函数需要导入 json 库：**import json**  

|函数|	描述  |
|---|---  |
|json.dumps|	将 Python 对象编码成 JSON 字符串|
|json.loads	|将已编码的 JSON 字符串解码为 Python 对象|

### json.dumps
>json.dumps(obj, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, cls=None, indent=None, separators=None, encoding="utf-8", default=None, sort_keys=False, **kw)

以下实例将数组编码为 JSON 格式数据：

**实例**   
```
import json

data = [ { 'a' : 1, 'b' : 2, 'c' : 3, 'd' : 4, 'e' : 5 } ]

data2 = json.dumps(data)
print(data2)
```
以上代码执行结果为：

``` [{"a": 1, "c": 3, "b": 2, "e": 5, "d": 4}] ```

使用参数让 JSON 数据格式化输出：

```import json

data = [ { 'a' : 1, 'b' : 2, 'c' : 3, 'd' : 4, 'e' : 5 } ]

data2 = json.dumps({'a': 'Runoob', 'b': 7}, sort_keys=True, indent=4, separators=(',', ': '))
print(data2)
```   

以上代码执行结果为：
```
{
    "a": "Runoob",
    "b": 7
}
```
python 原始类型向 json 类型的转化对照表：

Python	|JSON
---|---
dict	|object
list, tuple|	array
str, unicode	|string
int, long, float|	number
True	|true
False	|false
None	|null

### json.loads
>json.loads(s[, encoding[, cls[, object_hook[, parse_float[, parse_int[, parse_constant[, object_pairs_hook[, **kw]]]]]]]])

以下实例展示了Python 如何解码 JSON 对象：  
**实例**    
```
import json

jsonData = '{"a":1,"b":2,"c":3,"d":4,"e":5}';
text = json.loads(jsonData)
print(text)
```
以上代码执行结果为：
```
{'a': 1, 'c': 3, 'b': 2, 'e': 5, 'd': 4}
```

## 总结
Json文本更简洁易懂，对人更友好。适合数据量不大，结构不复杂的场景，如后端接口的参数。    
XML文本，程序处理更方便，对机器更友好。适合数据量大，结构复杂的场景。如，HTML、SVG实质都是建立在XML之上的。

*参考网页：*  
[https://www.runoob.com/json/json-tutorial.html](https://www.runoob.com/json/json-tutorial.html)   
[https://www.runoob.com/python/python-json.html](https://www.runoob.com/python/python-json.html)