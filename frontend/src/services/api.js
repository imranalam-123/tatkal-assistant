import axios from "axios";

const api = axios.create({
  baseURL: "https://tatkal-assistant-1.onrender.com",
});

export default api;