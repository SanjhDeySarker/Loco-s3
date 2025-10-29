import React, { useState, useEffect } from "react";
import { listBuckets, createBucket } from "../api/api";

export default function BucketList({ onSelect }) {
  const [buckets, setBuckets] = useState([]);
  const [newBucket, setNewBucket] = useState("");

  const fetchBuckets = async () => {
    const res = await listBuckets();
    setBuckets(res.data);
  };

  const handleCreate = async () => {
    if (!newBucket) return;
    await createBucket(newBucket);
    setNewBucket("");
    fetchBuckets();
  };

  useEffect(() => {
    fetchBuckets();
  }, []);

  return (
    <div className="p-4 border rounded-xl bg-gray-50 shadow">
      <h2 className="text-lg font-semibold mb-2">Buckets</h2>
      <div className="flex mb-3">
        <input
          type="text"
          placeholder="New bucket name"
          value={newBucket}
          onChange={(e) => setNewBucket(e.target.value)}
          className="border px-2 py-1 mr-2 rounded"
        />
        <button
          onClick={handleCreate}
          className="bg-green-600 text-white px-3 py-1 rounded hover:bg-green-700"
        >
          Create
        </button>
      </div>
      <ul>
        {buckets.map((b) => (
          <li
            key={b}
            onClick={() => onSelect(b)}
            className="cursor-pointer hover:underline text-blue-600"
          >
            {b}
          </li>
        ))}
      </ul>
    </div>
  );
}
