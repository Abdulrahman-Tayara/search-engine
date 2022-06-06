import axios from "axios";

const baseUrl = "http://localhost:5000";


const axiosBase = axios.create({
    baseURL: baseUrl
});


export default axiosBase;