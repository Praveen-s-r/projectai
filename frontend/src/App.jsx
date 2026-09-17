import { useState } from "react";
import axios from "axios";
import "./app.css";

function App() {
  const [text, setText] = useState("");
  const [voice, setVoice] = useState("kannada");
  const [speed, setSpeed] = useState(1.0);
  const [audioUrl, setAudioUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const generateSpeech = async () => {
    if (!text.trim()) {
      setError("Please enter some Kannada text.");
      return;
    }

    setLoading(true);
    setError("");
    setAudioUrl("");

    try {
      const response = await axios.post(
        "/generate-speech",
        {
          text: text,
          voice: voice,
          speed: Number(speed),
        }
      );

      setAudioUrl(response.data.audio_url);
    } catch (err) {
      console.error(err);
      setError("Failed to generate speech.");
    } finally {
      setLoading(false);
    }
  };

  const downloadAudio = () => {
    if (!audioUrl) return;

    const link = document.createElement("a");
    link.href = audioUrl;
    link.download = "kannada-speech.wav";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="app">
      <div className="container">

        <h1>Kannada Text to Speech</h1>

        <p className="subtitle">
          Convert Kannada text into speech using Meta MMS
        </p>

        <label>Enter Kannada Text</label>

        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="ಇಲ್ಲಿ ಕನ್ನಡ ಪಠ್ಯವನ್ನು ನಮೂದಿಸಿ..."
          rows="8"
        />

        <div className="controls">

          <div className="control">
            <label>Voice</label>

            <select
              value={voice}
              onChange={(e) => setVoice(e.target.value)}
            >
              <option value="kannada">Kannada</option>
            </select>
          </div>

          <div className="control">
            <label>Speed: {speed}x</label>

            <select
              value={speed}
              onChange={(e) => setSpeed(e.target.value)}
            >
              <option value="0.5">0.5x</option>
              <option value="0.75">0.75x</option>
              <option value="1.0">1.0x</option>
              <option value="1.25">1.25x</option>
              <option value="1.5">1.5x</option>
              <option value="1.75">1.75x</option>
              <option value="2.0">2.0x</option>
            </select>
          </div>

        </div>

        <button
          className="generate-button"
          onClick={generateSpeech}
          disabled={loading}
        >
          {loading ? "Generating..." : "Generate Speech"}
        </button>

        {error && (
          <p className="error">
            {error}
          </p>
        )}

        {audioUrl && (
          <div className="audio-section">

            <h2>Your Kannada Speech</h2>

            <audio
              controls
              src={audioUrl}
              className="audio-player"
            >
              Your browser does not support audio.
            </audio>

            <button
              className="download-button"
              onClick={downloadAudio}
            >
              Download Audio
            </button>

          </div>
        )}

      </div>
    </div>
  );
}

export default App;
