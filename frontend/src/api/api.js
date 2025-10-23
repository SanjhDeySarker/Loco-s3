import axios from "axios";

const API = axios.create({ baseURL: "http://localhost:8000/api" });

export const getBuckets = () => API.get("/buckets");
export const createBucket = (name) => API.post("/buckets", { name });
export const deleteBucket = (id) => API.delete(`/buckets/${id}`);

export const uploadObject = (bucketName, file) => {
  const formData = new FormData();
  formData.append("file", file);
  return API.post(`/objects/${bucketName}`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
};

export const listObjects = (bucketName) => API.get(`/objects/${bucketName}`);
export const deleteObject = (bucketName, key) => API.delete(`/objects/${bucketName}/${key}`);
export const downloadObject = (bucketName, key) => `${API.defaults.baseURL}/objects/${bucketName}/${key}`;
