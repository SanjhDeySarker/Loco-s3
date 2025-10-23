import { deleteObject, downloadObject, uploadObject } from "../api/api";

export default function ObjectTable({ bucket, objects, refresh }) {
  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    await uploadObject(bucket.name, file);
    refresh();
  };

  return (
    <div>
      <h2 className="text-xl font-bold mb-2">{bucket.name} Objects</h2>
      <input type="file" onChange={handleUpload} className="mb-2" />
      <table className="w-full border">
        <thead>
          <tr>
            <th className="border p-2">Key</th>
            <th className="border p-2">Actions</th>
          </tr>
        </thead>
        <tbody>
          {objects.map((obj) => (
            <tr key={obj.id}>
              <td className="border p-2">{obj.key}</td>
              <td className="border p-2">
                <a href={downloadObject(bucket.name, obj.key)} className="text-blue-500 mr-2" target="_blank">Download</a>
                <button onClick={async () => { await deleteObject(bucket.name, obj.key); refresh(); }} className="text-red-500">Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
