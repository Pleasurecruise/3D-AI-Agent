from core.api.nlp.baidu import get_emotion

def test_get_emotion():
    content = "我爱你"
    result = get_emotion(content)
    print(f"Evaluation result: {result}")

if __name__ == '__main__':
    test_get_emotion()