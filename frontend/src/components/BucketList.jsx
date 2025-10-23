import { useState, useEffect } from "react";
import { deleteBucket, listObjects } from "../api/api";
import ObjectTable from "./objectTable";

export default function BucketList({ buckets, refresh }) {
  const [selectedBucket, setSelectedBucket] = useState(null);
  const [objects, setObjects] = useState([]);

  const fetchObjects = async (bucketName) => {
    const res = await listObjects(bucketName);
    setObjects(res.data);
  };

  useEffect(() => {
    if (selectedBucket) fetchObjects(selectedBucket.name);
  }, [selectedBucket]);

  return (
    <div className="flex">
      <div className="w-1/3 border-r pr-2">
        {buckets.map((b) => (
          <div key={b.id} className="flex justify-between items-center mb-2">
            <span className="cursor-pointer" onClick={() => setSelectedBucket(b)}>{b.name}</span>
            <button
              onClick={async () => { await deleteBucket(b.id); refresh(); if(selectedBucket?.id===b.id) setSelectedBucket(null); }}
              className="text-red-500"
            >Delete</button>
          </div>
        ))}
      </div>
      <div className="w-2/3 pl-4">
        {selectedBucket && <ObjectTable bucket={selectedBucket} objects={objects} refresh={() => fetchObjects(selectedBucket.name)} />}
      </div>
    </div>
  );
}
