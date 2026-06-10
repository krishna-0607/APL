using System;

namespace AISuperpowerCamera.Core
{
    [Serializable]
    public class PowerEvent
    {
        public string type;
        public string power;
        public float confidence;
        public double timestamp;
        public string state;
        public float remaining;
    }
}
