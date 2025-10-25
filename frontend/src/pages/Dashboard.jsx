import { useEffect, useState } from "react";
import { listBuckets, listObjects } from "../utils/api";
import UploadModal from "../components/UploadModal";

export default function Dashboard() {
  const [buckets, setBuckets] = useState([]);
  const [selectedBucket, setSelectedBucket] = useState(null);
  const [objects, setObjects] = useState([]);
  const [showUpload, setShowUpload] = useState(false);

  useEffect(() => {
    loadBuckets();
  }, []);

  const loadBuckets = async () => {
    const { data } = await listBuckets();
    setBuckets(data);
  };

  const loadObjects = async (bucket) => {
    setSelectedBucket(bucket);
    const { data } = await listObjects(bucket);
    setObjects(data);
  };

  return (
    <div className="p-6 flex-1 overflow-y-auto">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-semibold">
          {selectedBucket ? `Objects in ${selectedBucket}` : "Buckets"}
        </h2>
        <button
          onClick={() => setShowUpload(true)}
          className="bg-blue-600 text-white px-3 py-2 rounded-md hover:bg-blue-700"
        >
          Upload
        </button>
      </div>

      {!selectedBucket ? (
        <div className="grid grid-cols-3 gap-4">
          {buckets.map((b) => (
            <div
              key={b.name}
              onClick={() => loadObjects(b.name)}
              className="border p-4 rounded-lg bg-white shadow hover:shadow-md cursor-pointer"
            >
              <h3 className="font-medium">{b.name}</h3>
              <p className="text-sm text-gray-500">{b.objects_count} objects</p>
            </div>
          ))}
        </div>
      ) : (
        <div className="grid grid-cols-3 gap-4">
          {objects.map((o) => (
            <div
              key={o.key}
              className="border p-4 rounded-lg bg-white shadow hover:shadow-md"
            >
              <p className="font-medium">{o.key}</p>
              <p className="text-xs text-gray-500">{o.size} bytes</p>
            </div>
          ))}
        </div>
      )}

      {showUpload && (
        <UploadModal
          onClose={() => setShowUpload(false)}
          onUpload={(file) => {
            console.log("Uploading:", file);
            setShowUpload(false);
          }}
        />
      )}
    </div>
  );
}
