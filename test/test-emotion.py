from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
import config

download_dir = config.StructBERT
semantic_cls = pipeline(
    Tasks.text_classification,
    model=download_dir
)
result = semantic_cls(input='我爱你')
print(result)
