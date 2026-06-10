using UnityEngine;
using UnityEngine.SceneManagement;

namespace AISuperpowerCamera.UI
{
    public class MainMenuController : MonoBehaviour
    {
        [SerializeField] private string gameplaySceneName = "Gameplay";

        public void StartGame()
        {
            SceneManager.LoadScene(gameplaySceneName);
        }

        public void OpenSettings(GameObject settingsPanel)
        {
            if (settingsPanel != null)
            {
                settingsPanel.SetActive(true);
            }
        }

        public void OpenPowerSelection(GameObject powerPanel)
        {
            if (powerPanel != null)
            {
                powerPanel.SetActive(true);
            }
        }

        public void Exit()
        {
            Application.Quit();
        }
    }
}
