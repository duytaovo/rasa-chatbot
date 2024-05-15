!(function () {
  let e = document.createElement("script"),
    t = document.head || document.getElementsByTagName("head")[0];
  (e.src = "https://cdn.jsdelivr.net/npm/rasa-webchat/lib/index.js"),
    (e.async = !0),
    (e.onload = () => {
      window.WebChat.default(
        {
          customData: { language: "en" },
          socketUrl: "http://localhost:5005/",
          title: "E-Commerce",
          subtitle: "Phone or Laptop",
          initPayload: "/greet",
          profileAvatar: "https://img.icons8.com/fluency/344/chatbot.png",
          openLauncherImage: "./assets/svg/comment.svg",
          closeImage: "./assets/svg/down.svg",
          showMessageDate: true,
          inputTextFieldHint: "Type your query",
          embedded: true,
        },
        null,
      );
    }),
    t.insertBefore(e, t.firstChild);
})();
localStorage.clear();
