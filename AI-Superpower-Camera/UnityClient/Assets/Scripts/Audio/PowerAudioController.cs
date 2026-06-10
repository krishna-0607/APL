using System.Collections.Generic;
using AISuperpowerCamera.PowerEngine;
using UnityEngine;

namespace AISuperpowerCamera.Audio
{
    public class PowerAudioController : MonoBehaviour
    {
        [SerializeField] private AudioSource spatialSource;
        [SerializeField] private AudioSource uiSource;
        [SerializeField] private List<PowerDefinition> powers;

        private readonly Dictionary<string, AudioClip> powerClips = new Dictionary<string, AudioClip>();

        private void Awake()
        {
            foreach (var power in powers)
            {
                if (power != null && power.activationSound != null)
                {
                    powerClips[power.powerName] = power.activationSound;
                }
            }

            if (spatialSource != null)
            {
                spatialSource.spatialBlend = 1f;
            }
        }

        public void SetMasterVolume(float value)
        {
            AudioListener.volume = Mathf.Clamp01(value);
        }

        public void PlayPowerSound(string powerName)
        {
            if (spatialSource == null || !powerClips.TryGetValue(powerName, out var clip))
            {
                return;
            }

            spatialSource.PlayOneShot(clip);
        }

        public void PlayUISound(AudioClip clip)
        {
            if (uiSource == null || clip == null)
            {
                return;
            }

            uiSource.PlayOneShot(clip);
        }
    }
}
