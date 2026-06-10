using System;
using System.Diagnostics;
using AISuperpowerCamera.UI;
using UnityEngine;

namespace AISuperpowerCamera.Recording
{
    public class RecordingController : MonoBehaviour
    {
        [SerializeField] private string ffmpegPath = "ffmpeg";
        [SerializeField] private string outputDirectory = "Videos";
        [SerializeField] private int fps = 30;
        [SerializeField] private HUDController hudController;

        private Process ffmpeg;
        private float recordingStart;

        public bool IsRecording
        {
            get { return ffmpeg != null && !ffmpeg.HasExited; }
        }

        public void StartRecording()
        {
            if (IsRecording)
            {
                return;
            }

            string filename = $"{outputDirectory}/unity-{DateTime.UtcNow:yyyyMMdd-HHmmss}.mp4";
            string args = $"-y -f gdigrab -framerate {fps} -i desktop -c:v libx264 \"{filename}\"";

            ffmpeg = new Process
            {
                StartInfo = new ProcessStartInfo
                {
                    FileName = ffmpegPath,
                    Arguments = args,
                    RedirectStandardInput = true,
                    UseShellExecute = false,
                    CreateNoWindow = true,
                }
            };

            ffmpeg.Start();
            recordingStart = Time.time;
        }

        public void StopRecording()
        {
            if (!IsRecording)
            {
                return;
            }

            ffmpeg.StandardInput.WriteLine("q");
            ffmpeg.WaitForExit();
            ffmpeg.Dispose();
            ffmpeg = null;
        }

        private void Update()
        {
            if (hudController != null)
            {
                hudController.SetRecording(IsRecording, IsRecording ? Time.time - recordingStart : 0f);
            }
        }
    }
}
