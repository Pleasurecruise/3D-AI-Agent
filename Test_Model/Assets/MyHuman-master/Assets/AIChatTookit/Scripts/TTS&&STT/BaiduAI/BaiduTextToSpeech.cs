using System;
using System.Collections;
using System.Collections.Generic;
using System.Diagnostics;
using UnityEngine;
using UnityEngine.Networking;

[RequireComponent(typeof(BaiduSettings))]
public class BaiduTextToSpeech : TTS
{
    #region 参数
    /// <summary>
    /// token脚本
    /// </summary>
    [SerializeField] private BaiduSettings m_Settings;
    /// <summary>
    /// 语音合成设置
    /// </summary>
    [SerializeField] private PostDataSetting m_Post_Setting;
    /// <summary>
    /// 请求URL
    /// </summary>
    [SerializeField] private new string m_PostURL;
    /// <summary>
    /// 性能计时器
    /// </summary>
    private Stopwatch m_Stopwatch = new Stopwatch();
    #endregion

    // 添加声音角色枚举
    public enum SpeekerRole
    {
        男,
        女,
        儿童,
        老人,
        JP少女,
        JP儿童声音,
        JP中年,
        JP青年,
        JP中年妇女
    }

    private void Awake()
    {
        m_Settings = this.GetComponent<BaiduSettings>();
        m_PostURL = "http://tsn.baidu.com/text2audio";
    }

    #region Public Method


    /// <summary>
    /// 语音合成，返回合成后的音频和文本
    /// </summary>
    /// <param name="_msg"></param>
    /// <param name="_callback"></param>
    public override void Speak(string _msg, Action<AudioClip, string> _callback)
    {
        StartCoroutine(GetSpeech(_msg, _callback));
    }

    #endregion

    #region Private Method

    /// <summary>
    /// 获取语音合成的协程
    /// </summary>
    /// <param name="_msg"></param>
    /// <param name="callback"></param>
    /// <returns></returns>
    private IEnumerator GetSpeech(string _msg, Action<AudioClip, string> _callback)
    {
        m_Stopwatch.Restart();
        var _url = m_PostURL;
        var _postParams = new Dictionary<string, string>();
        _postParams.Add("tex", _msg);
        _postParams.Add("tok", m_Settings.m_Token);
        _postParams.Add("cuid", SystemInfo.deviceUniqueIdentifier);
        _postParams.Add("ctp", m_Post_Setting.ctp);
        _postParams.Add("lan", m_Post_Setting.lan);
        _postParams.Add("spd", m_Post_Setting.spd);
        _postParams.Add("pit", m_Post_Setting.pit);
        _postParams.Add("vol", m_Post_Setting.vol);
        _postParams.Add("per", SetSpeeker(m_Post_Setting.per));
        _postParams.Add("aue", m_Post_Setting.aue);

        //拼接URL参数
        int i = 0;
        foreach (var item in _postParams)
        {
            _url += i != 0 ? "&" : "?";
            _url += item.Key + "=" + item.Value;
            i++;
        }

        //获取语音
        using (UnityWebRequest _speech = UnityWebRequestMultimedia.GetAudioClip(_url, AudioType.WAV))
        {
            yield return _speech.SendWebRequest();
            if (_speech.error == null)
            {
                var type = _speech.GetResponseHeader("Content-Type");
                if (type.Contains("audio"))
                {
                    var _clip = DownloadHandlerAudioClip.GetContent(_speech);
                    _callback(_clip, _msg);
                }
                else
                {
                    var _response = _speech.downloadHandler.data;
                    string _msgBack = System.Text.Encoding.UTF8.GetString(_response);
                    UnityEngine.Debug.LogError(_msgBack);
                }

            }

            m_Stopwatch.Stop();
            UnityEngine.Debug.Log("Synthesis Time: " + m_Stopwatch.Elapsed.TotalSeconds);
        }

    }
    //性别:男=1，女=0，儿童=3，老人=4
    /// 女声:儿童声音=5003，少女=5118，中年=106，老年=110，青年=111，中年妇女=103，儿童=5
    private string SetSpeeker(SpeekerRole _role)
    {
        if (_role == SpeekerRole.男) return "1";
        if (_role == SpeekerRole.女) return "0";
        if (_role == SpeekerRole.儿童) return "3";
        if (_role == SpeekerRole.老人) return "4";
        if (_role == SpeekerRole.JP少女) return "5";
        if (_role == SpeekerRole.JP儿童声音) return "5003";
        if (_role == SpeekerRole.JP少女) return "5118";
        if (_role == SpeekerRole.JP中年) return "106";
        if (_role == SpeekerRole.JP青年) return "110";
        if (_role == SpeekerRole.JP青年) return "111";
        if (_role == SpeekerRole.JP中年妇女) return "5";

        return "0";//默认是男声
    }

    #endregion

    #region 数据格式



    /// <summary>
    /// 语音合成的参数信息
    /// </summary>
    [System.Serializable]
    public class PostDataSetting
    {
        /// <summary>
        /// 选择web模式，固定值1
        /// </summary>
        public string ctp = "1";
        /// <summary>
        /// 固定值zh，选择,目前只支持英语模式，固定值zh
        /// </summary>
        [Header("语言，固定值zh")] public string lan = "zh";
        /// <summary>
        /// 语速，取值0-15，默认值为5
        /// </summary>
        [Header("语速，取值0-15，默认值为5")] public string spd = "5";
        /// <summary>
        /// 音调，取值0-15，默认值为5
        /// </summary>
        [Header("音调，取值0-15，默认值为5")] public string pit = "5";
        /// <summary>
        /// 音量，取值0-15，默认值为5
        /// </summary>
        [Header("音量，取值0-15，默认值为5")] public string vol = "5";
        /// <summary>
        /// 性别:男=1，女=0，儿童=3，老人=4
        /// 女声:儿童声音=5003，少女=5118，中年=106，老年=110，青年=111，中年妇女=103，儿童=5
        /// </summary>
        [Header("性别")] public SpeekerRole per = SpeekerRole.男;
        /// <summary>
        /// 3为mp3格式(默认)，4为pcm-16k，5为pcm-8k，6为wav格式，不同pcm-16k格式；注意aue=4和6格式需要返回音频格式
        /// 如果音频数据不需要返回格式
        /// </summary>
        [Header("音频格式")] public string aue = "3";
    }

    #endregion
}