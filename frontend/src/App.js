import "./App.css";
import axios from "axios";
import { useState, useRef, useEffect, React } from "react";
import Speech from "speak-tts";

axios.defaults.baseURL = "http://localhost:5001/";
let speech = new Speech();
speech.init({
  volume: 1,
  lang: "en-GB",
  rate: 1,
  pitch: 1,
  voice: "Google UK English Male",
  splitSentences: true,
  listeners: {
    onvoiceschanged: (voices) => {
      console.log("Event voiceschanged", voices);
    },
  },
});

function App() {
  const mimeType = "audio/wav"; //Kiểu dữ liệu âm thanh (audio/wav).
  const mediaRecorder = useRef(null);
  const [recordingStatus, setRecordingStatus] = useState("inactive");
  const [stream, setStream] = useState(null); //Dòng dữ liệu âm thanh từ microphone.
  const [audioChunks, setAudioChunks] = useState([]);
  const [utters] = useState([]); //Mảng chứa các câu trả lời của bot (cập nhật theo thời gian).

  const getMicrophonePermission = async () => {
    if ("MediaRecorder" in window) {
      try {
        const streamData = await navigator.mediaDevices.getUserMedia({
          audio: true,
          video: false,
        });
        setStream(streamData);
      } catch (err) {
        alert(err.message);
      }
    } else {
      alert("The MediaRecorder API is not supported in your browser.");
    }
  };

  getMicrophonePermission();

  const stopRecording = () => {
    setRecordingStatus("waiting");

    mediaRecorder.current.stop();
    mediaRecorder.current.onstop = () => {
      const audioBlob = new Blob(audioChunks, { type: mimeType });
      sendAudioToBackend(audioBlob);
      setAudioChunks([]);
    };
  };

  const startRecording = async () => {
    setRecordingStatus("recording");
    const media = new MediaRecorder(stream, { type: mimeType });
    mediaRecorder.current = media;
    mediaRecorder.current.start();
    let localAudioChunks = [];
    mediaRecorder.current.ondataavailable = (event) => {
      if (typeof event.data === "undefined") return;
      if (event.data.size === 0) return;
      localAudioChunks.push(event.data);
    };
    setAudioChunks(localAudioChunks);
  };

  const sendAudioToBackend = (audioBlob) => {
    const formData = new FormData();
    formData.append("audio", audioBlob, "recording.wav");
    console.log("Request Sent");
    axios
      .post("/api/v1/bot", formData)
      .then((response) => {
        console.log("speaking");
        utters.push(response.data.message + "(" + new Date() + ")");
        speak(response.data.message);
        setRecordingStatus("inactive");
      })
      .catch((error) => {
        setRecordingStatus("inactive");
        console.error("Error sending audio:", error);
      });
  };

  function speak(text) {
    speech
      .speak({
        text: text,
      })
      .then(() => {
        console.log("Success !");
      })
      .catch((e) => {
        console.error("An error occurred :", e);
      });
    speech.speaking();
  }

  useEffect(() => {
    const script = document.createElement("script");

    script.src = "/script/chatbot-script.js";
    script.async = true;

    document.body.appendChild(script);

    return () => {
      document.body.removeChild(script);
    };
  }, []);

  return (
    <div className="main-container">
      <h2>Voice Bot</h2>
      {recordingStatus === "inactive" ? (
        <button onClick={startRecording} type="button">
          Start Recording
        </button>
      ) : null}
      {recordingStatus === "recording" ? (
        <button onClick={stopRecording} type="button">
          Send
        </button>
      ) : null}
      {recordingStatus === "waiting" ? (
        <img src="loading.gif" alt="Waiting.." />
      ) : null}
      <div className="bot-container">
        <ul>
          {utters.map((text, key) => (
            <li key={key}>{text}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default App;

