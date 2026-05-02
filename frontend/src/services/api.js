import axios from "axios";
const API = axios.create({ baseURL: "http://localhost:5050/api" });
API.interceptors.request.use((c)=>{ 
const t=localStorage.getItem("token");
if(t) c.headers.Authorization=`Bearer ${t}`;
return c;
});
export default API;
