import UploadPanel from "./components/UploadPanel";
import ChatWindow from "./components/ChatWindow";

export default function App() {
  return (
    <>
      <header>Company AI Assistant</header>

      <div className="container">
        <div className="upload-panel">
          <UploadPanel />
        </div>

        <div className="chat-window">
          <ChatWindow />
        </div>
      </div>
    </>
  );
}
