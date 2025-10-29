import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000/api";

// ✅ Bucket Endpoints
export const getBuckets = async () => {
  const res = await axios.get(`${API_BASE_URL}/buckets`);
  return res.data;
};

export const createBucket = async (bucketName) => {
  const res = await axios.post(`${API_BASE_URL}/buckets`, { name: bucketName });
  return res.data;
};

export const deleteBucket = async (bucketName) => {
  const res = await axios.delete(`${API_BASE_URL}/buckets/${bucketName}`);
  return res.data;
};

// ✅ Object Endpoints
export const getObjects = async (bucketName) => {
  const res = await axios.get(`${API_BASE_URL}/${bucketName}`);
  return res.data;
};

export const uploadObject = async (bucketName, file) => {
  const formData = new FormData();
  formData.append("file", file);

  const res = await axios.put(`${API_BASE_URL}/${bucketName}/${file.name}`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return res.data;
};

export const deleteObject = async (bucketName, objectKey) => {
  const res = await axios.delete(`${API_BASE_URL}/${bucketName}/${objectKey}`);
  return res.data;
};
