using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace AISuperpowerCamera.UI
{
    public class HUDController : MonoBehaviour
    {
        [SerializeField] private TMP_Text powerText;
        [SerializeField] private TMP_Text recordingText;
        [SerializeField] private Slider cooldownSlider;

        public void NotifyPower(string powerName, float confidence)
        {
            if (powerText == null)
            {
                return;
            }

            powerText.text = $"{powerName} ({confidence:P0})";
        }

        public void SetCooldown(string powerName, float remaining)
        {
            if (cooldownSlider != null)
            {
                cooldownSlider.value = Mathf.Max(0f, remaining);
            }

            if (powerText != null)
            {
                powerText.text = $"{powerName} cooldown: {remaining:0.00}s";
            }
        }

        public void SetRecording(bool isRecording, float duration)
        {
            if (recordingText == null)
            {
                return;
            }

            recordingText.text = isRecording ? $"REC {duration:0.0}s" : "REC OFF";
        }
    }
}
