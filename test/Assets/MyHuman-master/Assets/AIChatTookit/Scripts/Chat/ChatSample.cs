using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;
using WebGLSupport;

public class ChatSample : MonoBehaviour
{
    /// <summary>
    /// Chat Configuration
    /// </summary>
    [SerializeField] private ChatSetting m_ChatSettings;
    #region UI Definition
    /// <summary>
    /// Chat UI Panel
    /// </summary>
    [SerializeField] private GameObject m_ChatPanel;
    /// <summary>
    /// Input Message
    /// </summary>
    [SerializeField] public InputField m_InputWord;
    /// <summary>
    /// Response Message
    /// </summary>
    [SerializeField] private Text m_TextBack;
    /// <summary>
    /// Audio Source
    /// </summary>
    [SerializeField] private AudioSource m_AudioSource;
    /// <summary>
    /// Send Message Button
    /// </summary>
    [SerializeField] private Button m_CommitMsgBtn;

    #endregion

    #region Parameter Definition
    /// <summary>
    /// Animation Controller
    /// </summary>
    [SerializeField] private Animator m_Animator;
    /// <summary>
    /// Text-to-speech mode, set to false, then do not synthesize through text-to-speech
    /// </summary>
    [Header("Enable text-to-speech playback")]
    [SerializeField] private bool m_IsVoiceMode = true;
    [Header("Check to synthesize input text directly without sending to LLM")]
    [SerializeField] private bool m_CreateVoiceMode = false;

    #endregion

    private void Awake()
    {
        m_CommitMsgBtn.onClick.AddListener(delegate { SendData(); });
        RegistButtonEvent();
        InputSettingWhenWebgl();
    }

    #region Message Sending

    /// <summary>
    /// Handle WebGL input, support Chinese input
    /// </summary>
    private void InputSettingWhenWebgl()
    {
#if UNITY_WEBGL
        m_InputWord.gameObject.AddComponent<WebGLSupport.WebGLInput>();
#endif
    }


    /// <summary>
    /// Send Message
    /// </summary>
    public void SendData()
    {
        if (m_InputWord.text.Equals(""))
            return;

        if (m_CreateVoiceMode)//Synthesize input as voice
        {
            CallBack(m_InputWord.text);
            m_InputWord.text = "";
            return;
        }


        //Add to chat history
        m_ChatHistory.Add(m_InputWord.text);
        //Prompt
        string _msg = m_InputWord.text;

        //Send data
        m_ChatSettings.m_ChatModel.PostMsg(_msg, CallBack);

        m_InputWord.text = "";
        m_TextBack.text = "Thinking...";

        //Switch to thinking animation
        SetAnimator("state", 1);
    }
    /// <summary>
    /// Send with text
    /// </summary>
    /// <param name="_postWord"></param>
    public void SendData(string _postWord)
    {
        if (_postWord.Equals(""))
            return;

        if (m_CreateVoiceMode)//合成输入为语音
        {
            CallBack(_postWord);
            m_InputWord.text = "";
            return;
        }


        //添加记录聊天
        m_ChatHistory.Add(_postWord);
        //提示词
        string _msg = _postWord;

        //发送数据
        m_ChatSettings.m_ChatModel.PostMsg(_msg, CallBack);

        m_InputWord.text = "";
        m_TextBack.text = "Thinking...";

        //切换思考动作
        SetAnimator("state", 1);
    }

    /// <summary>
    /// AI reply information callback
    /// </summary>
    /// <param name="_response"></param>
    private void CallBack(string _response)
    {
        _response = _response.Trim();
        m_TextBack.text = "";

        
        Debug.Log("Received AI reply: "+ _response);

        //记录聊天
        m_ChatHistory.Add(_response);

        if (!m_IsVoiceMode||m_ChatSettings.m_TextToSpeech == null)
        {
            //开始逐个显示返回的文本
            StartTypeWords(_response);
            return;
        }


        m_ChatSettings.m_TextToSpeech.Speak(_response, PlayVoice);
    }

#endregion

#region Voice Input
    /// <summary>
    /// Whether the text recognized by voice input is directly sent to LLM
    /// </summary>
    [SerializeField] private bool m_AutoSend = true;
    /// <summary>
    /// Voice input button
    /// </summary>
    [SerializeField] private Button m_VoiceInputBotton;
    /// <summary>
    /// Text of recording button
    /// </summary>
    [SerializeField]private Text m_VoiceBottonText;
    /// <summary>
    /// Recording prompt information
    /// </summary>
    [SerializeField] private Text m_RecordTips;
    /// <summary>
    /// Voice input processing class
    /// </summary>
    [SerializeField] private VoiceInputs m_VoiceInputs;
    /// <summary>
    /// Register button event
    /// </summary>
    private void RegistButtonEvent()
    {
        if (m_VoiceInputBotton == null || m_VoiceInputBotton.GetComponent<EventTrigger>())
            return;

        EventTrigger _trigger = m_VoiceInputBotton.gameObject.AddComponent<EventTrigger>();

        //Add button press event
        EventTrigger.Entry _pointDown_entry = new EventTrigger.Entry();
        _pointDown_entry.eventID = EventTriggerType.PointerDown;
        _pointDown_entry.callback = new EventTrigger.TriggerEvent();

        //Add button release event
        EventTrigger.Entry _pointUp_entry = new EventTrigger.Entry();
        _pointUp_entry.eventID = EventTriggerType.PointerUp;
        _pointUp_entry.callback = new EventTrigger.TriggerEvent();

        //Add delegate event
        _pointDown_entry.callback.AddListener(delegate { StartRecord(); });
        _pointUp_entry.callback.AddListener(delegate { StopRecord(); });

        _trigger.triggers.Add(_pointDown_entry);
        _trigger.triggers.Add(_pointUp_entry);
    }

    /// <summary>
    /// Start recording
    /// </summary>
    public void StartRecord()
    {
        m_VoiceBottonText.text = "Recording...";
        m_RecordTips.text = "Please speak...";
        m_RecordTips.gameObject.SetActive(true);
        m_VoiceInputs.StartRecordAudio();
    }
    /// <summary>
    /// End recording
    /// </summary>
    public void StopRecord()
    {
        m_VoiceBottonText.text = "Voice";
        m_VoiceInputs.StopRecordAudio(GetRecordData);
    }

    /// <summary>
    /// Process recorded audio data
    /// </summary>
    /// <param name="_data"></param>
    private void AcceptData(byte[] _data)
    {
        if (m_ChatSettings.m_SpeechToText == null)
            return;

        m_ChatSettings.m_SpeechToText.SpeechToText(_data, ToRecognitionText);
    }

    /// <summary>
    /// Process recorded audio data
    /// </summary>
    /// <param name="_data"></param>
    private void AcceptClip(AudioClip _audioClip)
    {
        if (m_ChatSettings.m_SpeechToText == null)
            return;

        m_ChatSettings.m_SpeechToText.SpeechToText(_audioClip, ToRecognitionText);
    }
    
    /// <summary>
    /// Process recorded audio data from voice input
    /// </summary>
    /// <param name="_clip"></param>
    private void GetRecordData(AudioClip _clip)
    {
        if (_clip != null)
        {
            AcceptClip(_clip);
        }
    }
    
    /// <summary>
    /// Process recognized text
    /// </summary>
    /// <param name="_msg"></param>
    private void ToRecognitionText(string _msg)
    {
        m_InputWord.text = _msg;
        m_RecordTips.text = _msg;
        StartCoroutine(SetTextVisible(m_RecordTips));
        //Automatic sending
        if (m_AutoSend)
        {
            SendData();
        }
    }

    /// <summary>
    /// Delay hiding prompt message
    /// </summary>
    /// <param name="_text"></param>
    /// <returns></returns>
    private IEnumerator SetTextVisible(Text _text)
    {
        yield return new WaitForSeconds(3f);
        _text.gameObject.SetActive(false);
    }

#endregion

#region Text-to-speech

    private void PlayVoice(AudioClip _clip, string _response)
    {
        m_AudioSource.clip = _clip;
        m_AudioSource.Play();
        Debug.Log("Audio length: " + _clip.length);
        //开始逐个显示返回的文本
        StartTypeWords(_response);
        //Switch to speaking animation
        SetAnimator("state", 2);
    }

#endregion

#region Text Display One by One
    //Text display interval
    [SerializeField] private float m_WordWaitTime = 0.2f;
    //Whether display is complete
    [SerializeField] private bool m_WriteState = false;

    /// <summary>
    /// Start displaying one by one
    /// </summary>
    /// <param name="_msg"></param>
    private void StartTypeWords(string _msg)
    {
        if (_msg == "")
            return;

        m_WriteState = true;
        StartCoroutine(SetTextPerWord(_msg));
    }

    private IEnumerator SetTextPerWord(string _msg)
    {
        int currentPos = 0;
        while (m_WriteState)
        {
            yield return new WaitForSeconds(m_WordWaitTime);
            currentPos++;
            //Update displayed content
            m_TextBack.text = _msg.Substring(0, currentPos);

            m_WriteState = currentPos < _msg.Length;

        }

        //Switch to waiting animation
        SetAnimator("state",0);
    }

#endregion

#region Chat History
    //Save chat history
    [SerializeField] private List<string> m_ChatHistory;
    //Cache created chat bubbles
    [SerializeField] private List<GameObject> m_TempChatBox;
    //Chat history display layer
    [SerializeField] private GameObject m_HistoryPanel;
    //Chat text placement layer
    [SerializeField] private RectTransform m_rootTrans;
    //Send chat bubble
    [SerializeField] private ChatPrefab m_PostChatPrefab;
    //Reply chat bubble
    [SerializeField] private ChatPrefab m_RobotChatPrefab;
    //Scroll bar
    [SerializeField] private ScrollRect m_ScroTectObject;
    //Get chat history
    public void OpenAndGetHistory()
    {
        m_ChatPanel.SetActive(false);
        m_HistoryPanel.SetActive(true);

        ClearChatBox();
        StartCoroutine(GetHistoryChatInfo());
    }
    //Return
    public void BackChatMode()
    {
        m_ChatPanel.SetActive(true);
        m_HistoryPanel.SetActive(false);
    }

    //Clear created conversation box
    private void ClearChatBox()
    {
        while (m_TempChatBox.Count != 0)
        {
            if (m_TempChatBox[0])
            {
                Destroy(m_TempChatBox[0].gameObject);
                m_TempChatBox.RemoveAt(0);
            }
        }
        m_TempChatBox.Clear();
    }

    //Get chat history list
    private IEnumerator GetHistoryChatInfo()
    {

        yield return new WaitForEndOfFrame();

        for (int i = 0; i < m_ChatHistory.Count; i++)
        {
            if (i % 2 == 0)
            {
                ChatPrefab _sendChat = Instantiate(m_PostChatPrefab, m_rootTrans.transform);
                _sendChat.SetText(m_ChatHistory[i]);
                m_TempChatBox.Add(_sendChat.gameObject);
                continue;
            }

            ChatPrefab _reChat = Instantiate(m_RobotChatPrefab, m_rootTrans.transform);
            _reChat.SetText(m_ChatHistory[i]);
            m_TempChatBox.Add(_reChat.gameObject);
        }

        //Recalculate container size
        LayoutRebuilder.ForceRebuildLayoutImmediate(m_rootTrans);
        StartCoroutine(TurnToLastLine());
    }

    private IEnumerator TurnToLastLine()
    {
        yield return new WaitForEndOfFrame();
        //Scroll to the latest message
        m_ScroTectObject.verticalNormalizedPosition = 0;
    }


#endregion

    /// <summary>
    /// Set animation state
    /// </summary>
    /// <param name="_key"></param>
    /// <param name="_value"></param>
    public void SetAnimator(string _key, int _value)
    {
        if (m_Animator)
            m_Animator.SetInteger(_key, _value);
    }

    /// <summary>
    /// Additional function buttons
    /// </summary>
    [SerializeField] private Button m_CreateVoiceModeBtn;
    [SerializeField] private Text m_CreateVoiceText;

    /// <summary>
    /// Set whether to generate voice directly without sending
    /// </summary>
    public void OnOpenVoiceCreate()
    {
        m_CreateVoiceMode = !m_CreateVoiceMode;
        m_CreateVoiceText.text = m_CreateVoiceMode ? "Voice Mode" : "Chat Mode";
    }

    /// <summary>
    /// Input field placeholder content
    /// </summary>
    public void OnInputPalceholder()
    {
        m_InputWord.placeholder.GetComponent<Text>().text = m_CreateVoiceMode ? "Enter text to convert to speech here" : "Type your question here!";
    }
}
