import axios from "axios";

const API_BASE = "http://127.0.0.1:8000/api";

export const api = axios.create({
  baseURL: API_BASE,
});

// Example API helpers
export const listBuckets = () => api.get("/buckets");
export const createBucket = (name) => api.post("/buckets", { name });
export const deleteBucket = (name) => api.delete(`/buckets/${name}`);

export const listObjects = (bucket) => api.get(`/objects/${bucket}`);
export const uploadObject = (bucket, formData) =>
  api.post(`/objects/${bucket}/upload`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
export const deleteObject = (bucket, key) =>
  api.delete(`/objects/${bucket}/${key}`);
