import React, { useState } from "react";
import BucketList from "./components/BucketList";
import FileUploader from "./components/FileUploader";

function App() {
  const [selectedBucket, setSelectedBucket] = useState(null);

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-6 text-center text-blue-700">
        Loco-S3 File Storage UI
      </h1>

      {!selectedBucket ? (
        <BucketList onSelect={setSelectedBucket} />
      ) : (
        <div>
          <button
            onClick={() => setSelectedBucket(null)}
            className="text-sm text-gray-600 mb-3 underline"
          >
            ← Back to Buckets
          </button>
          <h2 className="text-2xl font-semibold mb-4">
            Bucket: {selectedBucket}
          </h2>
          <FileUploader bucket={selectedBucket} />
        </div>
      )}
    </div>
  );
}

export default App;
