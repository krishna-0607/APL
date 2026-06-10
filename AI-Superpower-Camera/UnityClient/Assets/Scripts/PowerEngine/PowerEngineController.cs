using System.Collections.Generic;
using AISuperpowerCamera.Audio;
using AISuperpowerCamera.Core;
using AISuperpowerCamera.Networking;
using AISuperpowerCamera.UI;
using AISuperpowerCamera.VFX;
using UnityEngine;

namespace AISuperpowerCamera.PowerEngine
{
    public class PowerEngineController : MonoBehaviour
    {
        [SerializeField] private VisionWebSocketClient visionClient;
        [SerializeField] private PowerVFXController vfxController;
        [SerializeField] private PowerAudioController audioController;
        [SerializeField] private HUDController hudController;
        [SerializeField] private List<PowerDefinition> definitions;

        private readonly Dictionary<string, float> cooldowns = new Dictionary<string, float>();
        private readonly Dictionary<string, float> lastTriggered = new Dictionary<string, float>();

        private void Awake()
        {
            foreach (var definition in definitions)
            {
                if (definition == null || string.IsNullOrWhiteSpace(definition.powerName))
                {
                    continue;
                }

                cooldowns[definition.powerName] = Mathf.Max(0.1f, definition.cooldownSeconds);
                lastTriggered[definition.powerName] = -1000f;
            }
        }

        private void OnEnable()
        {
            if (visionClient != null)
            {
                visionClient.OnPowerEvent += OnPowerEvent;
            }
        }

        private void OnDisable()
        {
            if (visionClient != null)
            {
                visionClient.OnPowerEvent -= OnPowerEvent;
            }
        }

        private void OnPowerEvent(PowerEvent powerEvent)
        {
            if (powerEvent == null || string.IsNullOrWhiteSpace(powerEvent.power))
            {
                return;
            }

            if (powerEvent.type == "cooldown")
            {
                hudController?.SetCooldown(powerEvent.power, powerEvent.remaining);
                return;
            }

            if (!CanTrigger(powerEvent.power))
            {
                return;
            }

            lastTriggered[powerEvent.power] = Time.time;
            vfxController?.Play(powerEvent.power);
            audioController?.PlayPowerSound(powerEvent.power);
            hudController?.NotifyPower(powerEvent.power, powerEvent.confidence);
        }

        private bool CanTrigger(string powerName)
        {
            if (!cooldowns.TryGetValue(powerName, out float cooldown))
            {
                return true;
            }

            if (!lastTriggered.TryGetValue(powerName, out float lastTs))
            {
                return true;
            }

            return Time.time - lastTs >= cooldown;
        }
    }
}
