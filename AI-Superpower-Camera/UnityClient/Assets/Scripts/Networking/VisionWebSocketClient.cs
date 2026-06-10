using System;
using System.Net.WebSockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using AISuperpowerCamera.Core;
using UnityEngine;

namespace AISuperpowerCamera.Networking
{
    public class VisionWebSocketClient : MonoBehaviour
    {
        [SerializeField] private string wsUrl = "ws://127.0.0.1:8765";
        public event Action<PowerEvent> OnPowerEvent;

        private ClientWebSocket socket;
        private CancellationTokenSource cts;

        private async void Start()
        {
            cts = new CancellationTokenSource();
            await ConnectLoop();
        }

        private async Task ConnectLoop()
        {
            while (!cts.IsCancellationRequested)
            {
                try
                {
                    socket = new ClientWebSocket();
                    await socket.ConnectAsync(new Uri(wsUrl), cts.Token);
                    await ReceiveLoop();
                }
                catch (Exception ex)
                {
                    Debug.LogWarning($"Vision websocket reconnecting: {ex.Message}");
                    await Task.Delay(1000, cts.Token);
                }
            }
        }

        private async Task ReceiveLoop()
        {
            var buffer = new byte[8192];
            while (socket != null && socket.State == WebSocketState.Open && !cts.IsCancellationRequested)
            {
                WebSocketReceiveResult result = await socket.ReceiveAsync(new ArraySegment<byte>(buffer), cts.Token);
                if (result.MessageType == WebSocketMessageType.Close)
                {
                    await socket.CloseAsync(WebSocketCloseStatus.NormalClosure, "closing", cts.Token);
                    break;
                }

                var text = Encoding.UTF8.GetString(buffer, 0, result.Count);
                var evt = JsonUtility.FromJson<PowerEvent>(text);
                if (evt != null && (evt.type == "power_trigger" || evt.type == "cooldown"))
                {
                    OnPowerEvent?.Invoke(evt);
                }
            }
        }

        public async Task SendJsonAsync(string json)
        {
            if (socket == null || socket.State != WebSocketState.Open)
            {
                return;
            }

            byte[] bytes = Encoding.UTF8.GetBytes(json);
            await socket.SendAsync(new ArraySegment<byte>(bytes), WebSocketMessageType.Text, true, cts.Token);
        }

        private async void OnDestroy()
        {
            cts?.Cancel();
            if (socket != null && socket.State == WebSocketState.Open)
            {
                await socket.CloseAsync(WebSocketCloseStatus.NormalClosure, "destroy", CancellationToken.None);
            }
            socket?.Dispose();
        }
    }
}
