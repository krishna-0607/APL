using UnityEngine;

namespace AISuperpowerCamera.PowerEngine
{
    [CreateAssetMenu(fileName = "PowerDefinition", menuName = "AI Superpower Camera/Power Definition")]
    public class PowerDefinition : ScriptableObject
    {
        public string powerName;
        public float cooldownSeconds = 1f;
        public Color primaryColor = Color.white;
        public Color secondaryColor = Color.cyan;
        public AudioClip activationSound;
        public GameObject vfxPrefab;
    }
}
