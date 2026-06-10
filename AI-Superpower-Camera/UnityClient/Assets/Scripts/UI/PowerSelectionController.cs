using System.Collections.Generic;
using AISuperpowerCamera.PowerEngine;
using UnityEngine;

namespace AISuperpowerCamera.UI
{
    public class PowerSelectionController : MonoBehaviour
    {
        [SerializeField] private List<PowerDefinition> availablePowers;

        private readonly HashSet<string> enabledPowers = new HashSet<string>();

        private void Awake()
        {
            foreach (var power in availablePowers)
            {
                if (power != null)
                {
                    enabledPowers.Add(power.powerName);
                }
            }
        }

        public void SetPowerEnabled(string powerName, bool enabled)
        {
            if (enabled)
            {
                enabledPowers.Add(powerName);
            }
            else
            {
                enabledPowers.Remove(powerName);
            }
        }

        public bool IsEnabled(string powerName)
        {
            return enabledPowers.Contains(powerName);
        }
    }
}
