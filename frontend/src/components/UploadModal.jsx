import { useState } from "react";
import { uploadObject } from "../api/api";

export default function UploadModal({ bucketName, refresh }) {
  const [file, setFile] = useState(null);

  const handleUpload = async () => {
    if (!file) return;
    await uploadObject(bucketName, file);
    setFile(null);
    refresh();
  };

  return (
    <div className="mb-4">
      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
        className="border p-2 mr-2"
      />
      <button
        onClick={handleUpload}
        className="bg-green-500 text-white px-4 py-2 rounded"
      >
        Upload
      </button>
    </div>
  );
}
