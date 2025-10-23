import { useEffect, useState } from "react";
import { getBuckets, createBucket } from "../api/api";
import BucketList from "../components/BucketList";

export default function Dashboard() {
  const [buckets, setBuckets] = useState([]);
  const [newBucket, setNewBucket] = useState("");

  const fetchBuckets = async () => {
    const res = await getBuckets();
    setBuckets(res.data);
  };

  const handleCreate = async () => {
    if (!newBucket) return;
    await createBucket(newBucket);
    setNewBucket("");
    fetchBuckets();
  };

  useEffect(() => { fetchBuckets(); }, []);

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Loco3 Dashboard</h1>
      <div className="mb-4">
        <input
          value={newBucket}
          onChange={(e) => setNewBucket(e.target.value)}
          className="border p-2 mr-2"
          placeholder="New Bucket"
        />
        <button onClick={handleCreate} className="bg-blue-500 text-white px-4 py-2 rounded">Create</button>
      </div>
      <BucketList buckets={buckets} refresh={fetchBuckets} />
    </div>
  );
}
