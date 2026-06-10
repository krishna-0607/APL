using System;
using System.Net.WebSockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using UnityEngine;

namespace AISuperpowerCamera.Networking
{
    public class MultiplayerRelayClient : MonoBehaviour
    {
        [SerializeField] private string relayServerUrl = "ws://127.0.0.1:9000";

        private ClientWebSocket socket;

        public async Task ConnectAsync(CancellationToken token)
        {
            socket = new ClientWebSocket();
            await socket.ConnectAsync(new Uri(relayServerUrl), token);
        }

        public async Task SendPowerHitAsync(string power, float damage, CancellationToken token)
        {
            if (socket == null || socket.State != WebSocketState.Open)
            {
                return;
            }

            string json = $"{{\"type\":\"power_hit\",\"power\":\"{power}\",\"damage\":{damage}}}";
            byte[] bytes = Encoding.UTF8.GetBytes(json);
            await socket.SendAsync(new ArraySegment<byte>(bytes), WebSocketMessageType.Text, true, token);
        }
    }
}
