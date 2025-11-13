import axios from "axios";
import { useState } from "react";

export default function UploadPanel() {
  const [file, setFile] = useState(null);
  const [msg, setMsg] = useState("");

  const upload = async () => {
    if (!file) return;
    const form = new FormData();
    form.append("file", file);

    try {
      const res = await axios.post("http://localhost:8000/api/ingest", form);
      setMsg(`Uploaded: ${res.data.filename}`);
    } catch (e) {
      setMsg("Upload failed");
    }
  };

  return (
    <div>
      <h3>Upload Data</h3>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={upload}>Upload</button>
      <p>{msg}</p>
    </div>
  );
}
