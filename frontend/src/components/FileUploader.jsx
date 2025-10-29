import React, { useState } from "react";
import { uploadFile } from "../api/api";

export default function FileUploader({ bucket }) {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("");

  const handleUpload = async () => {
    if (!file) return alert("Select a file first!");
    try {
      const formData = new FormData();
      formData.append("file", file);
      await uploadFile(bucket, formData);
      setStatus("✅ File uploaded successfully!");
    } catch (err) {
      setStatus("❌ Upload failed: " + err.message);
    }
  };

  return (
    <div className="p-4 border rounded-xl bg-gray-50 shadow">
      <h2 className="text-lg font-semibold mb-2">Upload File</h2>
      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
        className="mb-3"
      />
      <button
        onClick={handleUpload}
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        Upload
      </button>
      {status && <p className="mt-3 text-sm">{status}</p>}
    </div>
  );
}
