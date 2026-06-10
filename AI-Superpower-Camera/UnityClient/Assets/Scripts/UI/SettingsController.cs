using AISuperpowerCamera.Audio;
using UnityEngine;

namespace AISuperpowerCamera.UI
{
    public class SettingsController : MonoBehaviour
    {
        [SerializeField] private PowerAudioController audioController;

        public void SetFPS(int fps)
        {
            Application.targetFrameRate = Mathf.Clamp(fps, 30, 120);
        }

        public void SetResolution(int width, int height, bool fullscreen)
        {
            Screen.SetResolution(width, height, fullscreen);
        }

        public void SetVolume(float value)
        {
            audioController?.SetMasterVolume(value);
        }
    }
}
