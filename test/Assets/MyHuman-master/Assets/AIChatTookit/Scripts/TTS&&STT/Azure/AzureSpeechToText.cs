using System;
using System.Collections;
using System.Collections.Generic;
using System.Net;
using UnityEngine;
using UnityEngine.Networking;

[RequireComponent(typeof(AzureSettings))]
public class AzureSpeechToText : STT
{
    /// <summary>
    /// Azure设置
    /// </summary>
    [SerializeField] private AzureSettings m_AzureSettings;
    public string mode = "conversation";

    private void Awake()
    {
        // 初始化设置
        m_AzureSettings = this.GetComponent<AzureSettings>();
        GetUrl();
    }
    
    /// <summary>
    /// 构建请求URL
    /// </summary>
    private void GetUrl()
    {
        if (m_AzureSettings == null)
            return;

        m_SpeechRecognizeURL = "https://" +
            m_AzureSettings.serviceRegion +
            ".stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?language=" +
            m_AzureSettings.language;
    }
    
    /// <summary>
    /// 语音识别（音频剪辑）
    /// </summary>
    /// <param name="_clip"></param>
    /// <param name="_callback"></param>
    public override void SpeechToText(AudioClip _clip, Action<string> _callback)
    {
        byte[] _audioData = WavUtility.FromAudioClip(_clip);
        StartCoroutine(SendAudioData(_audioData, _callback));
    }

    /// <summary>
    /// 语音识别（字节数据）
    /// </summary>
    /// <param name="_audioData"></param>
    /// <param name="_callback"></param>
    public override void SpeechToText(byte[] _audioData, Action<string> _callback)
    {
        StartCoroutine(SendAudioData(_audioData, _callback));
    }

    /// <summary>
    /// 发送音频数据
    /// </summary>
    /// <param name="audioData"></param>
    /// <param name="_callback"></param>
    /// <returns></returns>
    private IEnumerator SendAudioData(byte[] audioData, Action<string> _callback)
    {
        stopwatch.Restart();
        
        // 验证API密钥是否已设置
        if (string.IsNullOrEmpty(m_AzureSettings.subscriptionKey) || 
            m_AzureSettings.subscriptionKey == "请在Azure门户网站获取您的订阅密钥")
        {
            Debug.LogError("Azure Speech Recognition Error: No valid subscription key");
            _callback("Azure service key not set, please configure in AzureSettings");
            yield break;
        }
        
        // 创建请求
        UnityWebRequest request = new UnityWebRequest(m_SpeechRecognizeURL, "POST");
        request.uploadHandler = new UploadHandlerRaw(audioData);
        request.downloadHandler = new DownloadHandlerBuffer();
        
        // 设置请求头
        request.SetRequestHeader("Ocp-Apim-Subscription-Key", m_AzureSettings.subscriptionKey);
        request.SetRequestHeader("Content-Type", "audio/wav; codec=audio/pcm; samplerate=16000");
        request.SetRequestHeader("Accept", "application/json");

        // 发送请求并等待响应
        yield return request.SendWebRequest();

        // 检查错误
        if (request.result != UnityWebRequest.Result.Success)
        {
            Debug.LogError("Speech recognition request failed: " + request.error);
            _callback("Speech recognition request failed: " + request.error);
            yield break;
        }

        try 
        {
            // 解析响应JSON并提取识别结果
            string json = request.downloadHandler.text;
            Debug.Log("Azure Response: " + json);
            
            SpeechRecognitionResult result = JsonUtility.FromJson<SpeechRecognitionResult>(json);
            
            if (result != null && !string.IsNullOrEmpty(result.DisplayText))
            {
                Debug.Log("Recognition Result: " + result.DisplayText);
                _callback(result.DisplayText);
            }
            else
            {
                _callback("Could not recognize speech");
            }
        }
        catch (Exception ex)
        {
            Debug.LogError("Error parsing recognition result: " + ex.Message);
            _callback("Error parsing result");
        }

        stopwatch.Stop();
        Debug.Log("Azure Speech Recognition Time: " + stopwatch.Elapsed.TotalSeconds);
    }
}

[System.Serializable]
public class SpeechRecognitionResult
{
    public string RecognitionStatus;
    public string DisplayText;
    public string Offset;
    public string Duration;
}
