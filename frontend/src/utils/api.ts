import axios from "axios";
import { handleUnauthenticated } from "./authUtils";

const API_URL = import.meta.env.VITE_API_URL;

const api = axios.create({
	baseURL: API_URL
});

api.interceptors.request.use(
	(config) => {
		const token = sessionStorage.getItem('auth_token');
		if (token)
			config.headers.Authorization = `Bearer ${token}`;
		return config;
	},
	(error) => {
		return Promise.reject(error);
	}
);

api.interceptors.response.use(
	(response) => {
	  return response;
	},
	async (error) => {
	  if (error.response && error.response.status === 401) {
		sessionStorage.removeItem('auth_token');
		handleUnauthenticated();
	  }
	  return Promise.reject(error);
	}
  );

  export default api;
