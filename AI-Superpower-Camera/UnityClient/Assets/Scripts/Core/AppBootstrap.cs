using UnityEngine;

namespace AISuperpowerCamera.Core
{
    public class AppBootstrap : MonoBehaviour
    {
        [SerializeField] private int targetFps = 60;

        private void Awake()
        {
            QualitySettings.vSyncCount = 0;
            Application.targetFrameRate = targetFps;
        }
    }
}
