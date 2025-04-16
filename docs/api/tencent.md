## Tencent API

Before using the API, you need to activate the corresponding cloud service

### ASR

[语言识别概览](https://console.cloud.tencent.com/asr)

[API 录音文件识别](https://cloud.tencent.com/document/product/1093/37823)

### TTS

[语言合成概览](https://console.cloud.tencent.com/tts)

[API文档](https://cloud.tencent.com/document/product/1073/37995)

### Emotion Analysis

[NLP服务情感分析](https://console.cloud.tencent.com/nlp/analyze-sentiment)

[API文档](https://cloud.tencent.com/document/api/271/94294)

#### 输出参数

| 参数名称  | 类型   | 描述                                      |
| -------- | ------ | ----------------------------------------- |
| Positive | Float  | 正面情感概率。                            |
| Neutral  | Float  | 中性情感概率。                            |
| Negative | Float  | 负面情感概率。                            |
| Sentiment| String | 情感分类结果：positive：正面情感，negative：负面情感，neutral：中性、无情感 |
| RequestId| String | 唯一请求 ID，由服务端生成，每次请求都会返回（若请求因其他原因未能抵达服务端，则该次请求不会获得 RequestId）。定位问题时需要提供该次请求的 RequestId。 |

#### 输出示例

```
{
    "Response": {
        "Negative": 0.004367333836853504,
        "Neutral": 0.06927284598350525,
        "Positive": 0.9263598322868347,
        "RequestId": "848b909b-5ed7-44ad-b4d0-72bcf0be4f2a",
        "Sentiment": "positive"
    }
}
```