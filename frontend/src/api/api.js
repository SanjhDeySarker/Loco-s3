import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
});

export const listBuckets = () => api.get("/buckets");
export const createBucket = (bucket) => api.post(`/buckets/${bucket}`);
export const uploadFile = (bucket, file) =>
  api.put(`/buckets/${bucket}/${file.name}`, file, {
    headers: { "Content-Type": "multipart/form-data" },
  });
export const listFiles = (bucket) => api.get(`/buckets/${bucket}/objects`);
export const downloadFile = (bucket, name) =>
  api.get(`/buckets/${bucket}/${name}`, { responseType: "blob" });
export const deleteFile = (bucket, name) =>
  api.delete(`/buckets/${bucket}/${name}`);

export default api;
