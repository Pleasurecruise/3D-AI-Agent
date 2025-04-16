using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class AzureSettings : MonoBehaviour
{
    [Header("Azure Cognitive Services Subscription Key")]
    [Tooltip("The subscription key obtained from Azure Portal for Speech Services")]
    public string subscriptionKey = "Please get your subscription key from Azure Portal";
    
    [Header("Azure Service Region")]
    [Tooltip("Select the closest Azure service region, e.g. eastasia, eastus")]
    public string serviceRegion = "eastasia";
    
    [Header("Language Settings")]
    [Tooltip("Target language for speech recognition, e.g. zh-CN(Chinese), en-US(English)")]
    public string language = "zh-CN";
}
