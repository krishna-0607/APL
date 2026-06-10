using System.Collections.Generic;
using AISuperpowerCamera.PowerEngine;
using UnityEngine;

namespace AISuperpowerCamera.VFX
{
    public class PowerVFXController : MonoBehaviour
    {
        [SerializeField] private Transform spawnPoint;
        [SerializeField] private List<PowerDefinition> powers;

        private readonly Dictionary<string, PowerDefinition> powerMap = new Dictionary<string, PowerDefinition>();

        private void Awake()
        {
            foreach (var power in powers)
            {
                if (power != null && !string.IsNullOrWhiteSpace(power.powerName))
                {
                    powerMap[power.powerName] = power;
                }
            }
        }

        public void Play(string powerName)
        {
            if (!powerMap.TryGetValue(powerName, out var definition) || definition.vfxPrefab == null)
            {
                return;
            }

            Transform target = spawnPoint == null ? transform : spawnPoint;
            Instantiate(definition.vfxPrefab, target.position, target.rotation);
        }
    }
}
