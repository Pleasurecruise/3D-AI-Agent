from deepface import DeepFace

# 进行人脸识别
result = DeepFace.analyze(
    "test.jpg",
    actions=['age', 'gender', 'emotion', 'race'],
)

# 打印识别结果
print(result)
