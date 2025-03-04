## Baidu API

Before using the API, you need to activate the corresponding cloud service

### Emotion Analysis

#### 返回说明

| 参数           | 说明                   | 描述                       |
| -------------- | ---------------------- | -------------------------- |
| log\_id        | uint64                 | 请求唯一标识码             |
| sentiment      | int                    | 表示情感极性分类结果，0:负向，1:中性，2:正向 |
| confidence     | float                  | 表示分类的置信度，取值范围\[0,1\] |
| positive\_prob | float                  | 表示属于积极类别的概率 ，取值范围\[0,1\] |
| negative\_prob | float                  | 表示属于消极类别的概率，取值范围\[0,1\] |

#### 返回示例

```
{
    "text":"我爱祖国",
    "items":[
        {
            "sentiment":2,    //表示情感极性分类结果
            "confidence":0.90, //表示分类的置信度
            "positive_prob":0.94, //表示属于积极类别的概率
            "negative_prob":0.06  //表示属于消极类别的概率
        }
    ]
}
```