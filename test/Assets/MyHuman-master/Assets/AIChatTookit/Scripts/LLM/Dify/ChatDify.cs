using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

public class ChatDify : MonoBehaviour
{
    [SerializeField] private string api_key = "YOUR-API-KEY";  // Dify API Key
    private string url = "https://api.dify.ai/v1/chat-messages"; // Dify API Endpoint

    /// <summary>
    /// Send message to Dify API
    /// </summary>
    public void PostMsg(string userInput, Action<string> callback)
    {
        StartCoroutine(Request(userInput, callback));
    }

    /// <summary>
    /// Make HTTP request to Dify API
    /// </summary>
    private IEnumerator Request(string userInput, Action<string> callback)
    {
        // Create the request data
        PostData postData = new PostData
        {
            inputs = new Dictionary<string, string>(),
            query = userInput,
            response_mode = "streaming",
            conversation_id = "",
            user = "user"
        };

        // Convert to JSON
        string jsonData = JsonUtility.ToJson(postData);

        // Create and configure the web request
        using (UnityWebRequest request = new UnityWebRequest(url, "POST"))
        {
            byte[] bodyRaw = System.Text.Encoding.UTF8.GetBytes(jsonData);
            request.uploadHandler = new UploadHandlerRaw(bodyRaw);
            request.downloadHandler = new DownloadHandlerBuffer();
            request.SetRequestHeader("Content-Type", "application/json");
            request.SetRequestHeader("Authorization", "Bearer " + api_key);

            // Send the request
            yield return request.SendWebRequest();

            // Process the response
            if (request.result == UnityWebRequest.Result.Success)
            {
                string responseText = request.downloadHandler.text;
                MessageBack response = JsonUtility.FromJson<MessageBack>(responseText);
                
                if (response != null && response.answer != null)
                {
                    callback(response.answer);
                }
                else
                {
                    callback("AI did not return a valid message");
                }
            }
            else
            {
                Debug.LogError("Request failed: " + request.error);
                callback("Request failed: " + request.error);
            }
        }
    }

    #region Data Structures
    [Serializable]
    private class PostData
    {
        public Dictionary<string, string> inputs;
        public string query;
        public string response_mode;
        public string conversation_id;
        public string user;
    }

    [Serializable]
    private class MessageBack
    {
        public string answer;
    }
    #endregion
}
