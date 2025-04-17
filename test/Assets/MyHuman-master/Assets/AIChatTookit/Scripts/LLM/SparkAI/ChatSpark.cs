using System;
using System.Collections;
using System.Collections.Generic;
using System.Net.WebSockets;
using System.Text;
using System.Threading;
using UnityEngine;

public class ChatSpark : LLM
{

    #region ����
    /// <summary>
    /// Ѷ�ɵ�Ӧ������
    /// </summary>
    [SerializeField] private XunfeiSettings m_XunfeiSettings;
    /// <summary>
    /// ѡ���ǻ��ģ�Ͱ汾
    /// </summary>
    [Header("选择星火模型版本")]
    [SerializeField] private ModelType m_SparkModel = ModelType.星火模型V15;


    #endregion
    
    private void Awake()
    {
        OnInit();
    }
    /// <summary>
    /// ��ʼ��
    /// </summary>
    private void OnInit()
    {
        m_XunfeiSettings = this.GetComponent<XunfeiSettings>();
        if (m_SparkModel == ModelType.星火模型V15)
        {
            url= "https://spark-api.xf-yun.com/v1.1/chat";
            return;
        }

        url = "https://spark-api.xf-yun.com/v2.1/chat";
    }

    /// <summary>
    /// ������Ϣ
    /// </summary>
    /// <returns></returns>
    public override void PostMsg(string _msg, Action<string> _callback)
    {
        base.PostMsg(_msg, _callback);
    }

    /// <summary>
    /// ��������
    /// </summary> 
    /// <param name="_postWord"></param>
    /// <param name="_callback"></param>
    /// <returns></returns>
    public override IEnumerator Request(string _postWord, System.Action<string> _callback)
    {
        yield return null;
        //������������
        RequestData requestData = new RequestData();
        requestData.header.app_id = m_XunfeiSettings.m_AppID;

        //�ж�v1.5����v2
        requestData.parameter.chat.domain = GetDomain();

        //���ӶԻ��б�
        List<PostMsgData> _tempList = new List<PostMsgData>();
        for(int i=0;i<m_DataList.Count;i++)
        {
            PostMsgData _msg = new PostMsgData()
            {
                role = m_DataList[i].role,
                content = m_DataList[i].content
            };
            _tempList.Add(_msg);
        }
       
        requestData.payload.message.text= _tempList;

        string _json = JsonUtility.ToJson(requestData);

        //websocket����
        ConnectHost(_json, _callback);

    }

    /// <summary>
    /// ָ�����ʵ�����
    /// generalָ��V1.5�汾
    /// generalv2ָ��V2�汾
    /// </summary>
    /// <returns></returns>
    private string GetDomain()
    {
        if (m_SparkModel == ModelType.星火模型V15)
            return "general";

        return "generalv2";
    }


    #region ȡ��ȨUrl

    /// <summary>
    /// ��ȡ��Ȩurl
    /// </summary>
    /// <returns></returns>
    private string GetAuthUrl()
    {
        string date = DateTime.UtcNow.ToString("r");

        Uri uri = new Uri(url);
        StringBuilder builder = new StringBuilder("host: ").Append(uri.Host).Append("\n").//
                                Append("date: ").Append(date).Append("\n").//
                                Append("GET ").Append(uri.LocalPath).Append(" HTTP/1.1");

        string sha = HMACsha256(m_XunfeiSettings.m_APISecret, builder.ToString());
        string authorization = string.Format("api_key=\"{0}\", algorithm=\"{1}\", headers=\"{2}\", signature=\"{3}\"", m_XunfeiSettings.m_APIKey, "hmac-sha256", "host date request-line", sha);

        string NewUrl = "https://" + uri.Host + uri.LocalPath;

        string path1 = "authorization" + "=" + Convert.ToBase64String(System.Text.Encoding.UTF8.GetBytes(authorization));
        date = date.Replace(" ", "%20").Replace(":", "%3A").Replace(",", "%2C");
        string path2 = "date" + "=" + date;
        string path3 = "host" + "=" + uri.Host;

        NewUrl = NewUrl + "?" + path1 + "&" + path2 + "&" + path3;
        return NewUrl;
    }

    public string HMACsha256(string apiSecretIsKey, string buider)
    {
        byte[] bytes = System.Text.Encoding.UTF8.GetBytes(apiSecretIsKey);
        System.Security.Cryptography.HMACSHA256 hMACSHA256 = new System.Security.Cryptography.HMACSHA256(bytes);
        byte[] date = System.Text.Encoding.UTF8.GetBytes(buider);
        date = hMACSHA256.ComputeHash(date);
        hMACSHA256.Clear();

        return Convert.ToBase64String(date);

    }

    #endregion

    #region websocket����
    /// <summary>
    /// websocket
    /// </summary>
    private ClientWebSocket m_WebSocket;
    private CancellationToken m_CancellationToken;
    /// <summary>
    /// ���ӷ���������ȡ�ظ�
    /// </summary>
    private async void ConnectHost(string text,Action<string> _callback)
    {
        try
        {
            stopwatch.Restart();

            m_WebSocket = new ClientWebSocket();
            m_CancellationToken = new CancellationToken();
            string authUrl = GetAuthUrl();
            string url = authUrl.Replace("http://", "ws://").Replace("https://", "wss://");

            //Uri uri = new Uri(GetUrl());
            Uri uri = new Uri(url);
            await m_WebSocket.ConnectAsync(uri, m_CancellationToken);

            //����json
            string _jsonData = text;
            await m_WebSocket.SendAsync(new ArraySegment<byte>(Encoding.UTF8.GetBytes(_jsonData)), WebSocketMessageType.Binary, true, m_CancellationToken); //��������
            StringBuilder sb = new StringBuilder();
            //����ƴ�ӷ��صĴ�
            string _callBackMessage = "";

            //���Ŷ���.Clear();
            while (m_WebSocket.State == WebSocketState.Open)
            {
                var result = new byte[4096];
                await m_WebSocket.ReceiveAsync(new ArraySegment<byte>(result), m_CancellationToken);//��������
                List<byte> list = new List<byte>(result); while (list[list.Count - 1] == 0x00) list.RemoveAt(list.Count - 1);//ȥ�����ֽ�  
                var str = Encoding.UTF8.GetString(list.ToArray());
                sb.Append(str);
                if (str.EndsWith("}"))
                {
                    //��ȡ���ص�����
                    ResponseData _responseData = JsonUtility.FromJson<ResponseData>(sb.ToString());
                    sb.Clear();

                    if (_responseData.header.code != 0)
                    {
                        //���ش���
                        //PrintErrorLog(_responseData.code);
                        Debug.Log("�����룺" + _responseData.header.code);
                        m_WebSocket.Abort();
                        break;
                    }
                    //û�лظ�����
                    if (_responseData.payload.choices.text.Count == 0)
                    {
                        Debug.LogError("û�л�ȡ���ظ�����Ϣ��");
                        m_WebSocket.Abort();
                        break;
                    }
                    //ƴ�ӻظ�������
                    _callBackMessage += _responseData.payload.choices.text[0].content;

                    if (_responseData.payload.choices.status == 2)
                    {
                        stopwatch.Stop();
                        Debug.Log("ChatSpark��ʱ��" + stopwatch.Elapsed.TotalSeconds);

                        //���Ӽ�¼
                        m_DataList.Add(new SendData("assistant", _callBackMessage));

                        //�ص�
                        _callback(_callBackMessage);
                        m_WebSocket.Abort();
                        break;
                    }
                }
            }

        }
        catch (Exception ex)
        {
            Debug.LogError("������Ϣ: " + ex.Message);
            m_WebSocket.Dispose();
        }
    }

    #endregion

    #region ���ݶ���

    //���͵�����
    [Serializable]
    private class RequestData
    {
        public HeaderData header=new HeaderData();
        public ParameterData parameter = new ParameterData();
        public MessageData payload = new MessageData();
    }
    [Serializable]
    private class HeaderData
    {
        public string app_id = string.Empty;//����
        public string uid="admin";//ѡ��û���ID
    }
    [Serializable]
    private class ParameterData
    {
        public ChatParameter chat=new ChatParameter();
    }
    [Serializable]
    private class ChatParameter
    {
        public string domain = "general";
        public float temperature = 0.5f;
        public int max_tokens = 1024;
    }

    [Serializable]
    private class MessageData
    {
        public TextData message=new TextData();
    }
    [Serializable]
    private class TextData
    {
        public List<PostMsgData> text = new List<PostMsgData>();
    }
    [Serializable]
    private class PostMsgData
    {
        public string role = string.Empty;
        public string content = string.Empty;
    }

    //���յ�����
    [Serializable]
    private class ResponseData
    {
        public ReHeaderData header = new ReHeaderData();
        public PayloadData payload = new PayloadData();
    }

    [Serializable]
    private class ReHeaderData{
        public int code;//�����룬0��ʾ��������0��ʾ����
        public string message=string.Empty;//�Ự�Ƿ�ɹ���������Ϣ
        public string sid=string.Empty;
        public int status;//�Ự״̬��ȡֵΪ[0,1,2]��0�����״ν����1�����м�����2�������һ�����
    }
    [Serializable]
    private class PayloadData
    {
        public ChoicesData choices = new ChoicesData();
        //usage ��ʱû�ã���Ҫ�Ļ�������չ
    }
    [Serializable]
    private class ChoicesData
    {
        public int status;
        public int seq;
        public List<ReTextData> text = new List<ReTextData>();
    }
    [Serializable]
    private class ReTextData
    {
        public string content = string.Empty;
        public string role = string.Empty;
        public int index;
    }

    private enum ModelType
    {
        星火模型V15 = 0,
        星火模型V20 = 1
    }

    #endregion


}
