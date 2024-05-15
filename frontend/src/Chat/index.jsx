import "./chatBot.css";
import { IoMdSend } from "react-icons/io";
import { BiBot, BiUser } from "react-icons/bi";
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

// Thêm giọng nói tiếng Việt vào danh sách
// speech.synth.getVoices().push({
//   name: "Vietnamese Female",
//   lang: "vi-VN",
// });

// Cài đặt giọng nói mặc định cho tiếng Việt
// speech.synth.defaultVoice = "Vietnamese Female";
const Chat = () => {
  const [chat, setChat] = useState([]);
  const [inputMessage, setInputMessage] = useState("");
  const [botTyping, setbotTyping] = useState(false);
  const mimeType = "audio/wav"; //Kiểu dữ liệu âm thanh (audio/wav).
  const mediaRecorder = useRef(null);
  const [recordingStatus, setRecordingStatus] = useState("inactive");
  const [stream, setStream] = useState(null); //Dòng dữ liệu âm thanh từ microphone.
  const [audioChunks, setAudioChunks] = useState([]);
  useEffect(() => {
    console.log("called");
    // eslint-disable-next-line no-undef
    const objDiv = document.getElementById("messageArea");
    objDiv.scrollTop = objDiv.scrollHeight;
  }, [chat]);
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
      handleSubmit(null, audioBlob);
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
  const handleSubmit = (evt, audioBlob) => {
    evt?.preventDefault();
    const name = "shreyas";
    const request_temp = { sender: "user", sender_id: name, msg: inputMessage };

    if (inputMessage !== "") {
      setChat((chat) => [...chat, request_temp]);
      setbotTyping(true);
      setInputMessage("");
      rasaAPI(name, inputMessage);
      if (audioBlob) {
        sendAudioToBackend(audioBlob);
      }
    } else if (audioBlob) {
      sendAudioToBackend(audioBlob);
    } else {
      // eslint-disable-next-line no-undef
      window.alert("Please enter valid message");
    }
  };
  const sendAudioToBackend = (audioBlob) => {
    const formData = new FormData();
    formData.append("audio", audioBlob, "recording.wav");
    console.log("Request Sent");
    axios
      .post("/api/v1/bot", formData)
      .then((response) => {
        // if (response.data?.message === "Error processing your request.") {
        //   const response_temp = {
        //     sender: "bot",
        //     // recipient_id: ,
        //     msg: "Tôi không hiểu câu nói của bạn, vui lòng hỏi lại <3",
        //   };
        //   window.alert("Tôi không hiểu câu nói của bạn, vui lòng hỏi lại <3");
        //   setbotTyping(false);
        //   setChat((chat) => [...chat, response_temp]);
        // }
        console.log("speaking");
        const name = "shreyas";
        const request_temp = {
          sender: "bot",
          sender_id: name,
          msg: response.data.message + "(" + new Date() + ")",
        };
        setChat((chat) => [...chat, request_temp]);
        setbotTyping(true);
        speak(response.data.message);
        setRecordingStatus("inactive");
      })
      .catch((error) => {
        setRecordingStatus("inactive");
        console.error("Error sending audio:", error);
      });
  };
  const speak = (text) => {
    console.log(text);
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
  };
  const rasaAPI = async function handleClick(name, msg) {
    //chatData.push({sender : "user", sender_id : name, msg : msg});

    await fetch("http://localhost:5005/webhooks/rest/webhook", {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        charset: "UTF-8",
      },
      credentials: "same-origin",
      body: JSON.stringify({ sender: name, message: msg }),
    })
      .then((response) => response.json())
      .then((response) => {
        if (response.length > 0) {
          const temp = response[0];
          const recipient_id = temp["recipient_id"];
          const recipient_msg = temp["text"];

          const response_temp = {
            sender: "bot",
            recipient_id: recipient_id,
            msg: recipient_msg,
          };
          setbotTyping(false);

          setChat((chat) => [...chat, response_temp]);
          // scrollBottom();
        } else {
          // const recipient_id = temp["recipient_id"];
          // const recipient_msg = temp["text"];

          const response_temp = {
            sender: "bot",
            // recipient_id: ,
            msg: "Tôi không hiểu câu nói của bạn, vui lòng hỏi lại <3",
          };
          window.alert("Tôi không hiểu câu nói của bạn, vui lòng hỏi lại <3");
          setbotTyping(false);

          setChat((chat) => [...chat, response_temp]);
        }
      });
  };

  const stylecard = {
    maxWidth: "35rem",
    // border: "1px solid black",
    paddingLeft: "0px",
    paddingRight: "0px",
    borderRadius: "3px",
    boxShadow: "0 16px 20px 0 rgba(0,0,0,0.4)",
    marginLeft: "150px",
  };
  const styleHeader = {
    // height: "4.5rem",
    // borderBottom: "1px solid black",
    borderRadius: "4px 4px 0px 0px",
    backgroundImage: "linear-gradient(#FF90BC, #FFC0D9)",
    color: "white",

    // backgroundColor: "#8012c4",
  };
  const styleFooter = {
    //maxWidth : '32rem',
    // borderTop: "1px solid black",
    // borderRadius: "0px 0px 30px 30px",
    backgroundColor: "#8012c4",
  };
  const styleBody = {
    paddingTop: "10px",
    height: "28rem",
    overflowY: "a",
    overflowX: "hidden",
  };
  useEffect(() => {
    // const script = document.createElement("script");

    // script.src = "/script/chatbot-script.js";
    // script.async = true;

    // document.body.appendChild(script);

    // return () => {
    //   document.body.removeChild(script);
    // };
  }, []);

  return (
    <div>
      {/* <button onClick={()=>rasaAPI("shreyas","hi")}>Try this</button> */}

      <div className="container">
        <div className="row justify-content-center">
          <div className="card" style={stylecard}>
            <div className="cardHeader text-white" style={styleHeader}>
              <h1 style={{ marginBottom: "0px", padding: "16px" }}>
                AI Assistant
              </h1>
              {/* {botTyping || recordingStatus === "waiting" ? <h6>Bot Typing....</h6> : null} */}
            </div>
            {recordingStatus === "inactive" ? (
              <button
                className="button-voice"
                onClick={startRecording}
                type="button"
              >
                Start Voice
              </button>
            ) : null}
            {recordingStatus === "recording" ? (
              <button
                className="button-voice"
                onClick={stopRecording}
                type="button"
              >
                Send
              </button>
            ) : null}
            {recordingStatus === "waiting" ? (
              <img src="loading.gif" alt="Waiting.." className="loading-icon" />
            ) : null}
            <div className="cardBody" id="messageArea" style={styleBody}>
              <div className="row msgarea">
                {chat.map((user, key) => (
                  <div key={key}>
                    {user.sender === "bot" ? (
                      <div className="msgalignstart">
                        <BiBot className="botIcon" />
                        <h5 className="botmsg">{user.msg}</h5>
                      </div>
                    ) : (
                      <div className="msgalignend">
                        <h5 className="usermsg">{user.msg}</h5>
                        <BiUser className="userIcon" />
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
            <div className="cardFooter text-white" style={styleFooter}>
              <div className="row">
                <form style={{ display: "flex" }} onSubmit={handleSubmit}>
                  <div className="col-10" style={{ paddingRight: "0px" }}>
                    <input
                      onChange={(e) => setInputMessage(e.target.value)}
                      value={inputMessage}
                      type="text"
                      className="msginp"
                      placeholder="Type here..."
                    ></input>
                  </div>
                  <div className="col-2 cola">
                    <button type="submit" className="circleBtn">
                      <IoMdSend className="sendBtn" />
                    </button>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Chat;


