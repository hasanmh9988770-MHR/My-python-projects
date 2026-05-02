import {useState,useEffect} from "react";
import {useNavigate} from "react-router-dom";
import API from "../services/api";

export default function Login(){
const n=useNavigate();
const [u,setU]=useState("admin");
const [p,setP]=useState("1234");

useEffect(()=>{ if(localStorage.getItem("token")) n("/billing"); },[]);

const go=async()=>{
const r=await API.post("/auth/login",{username:u,password:p});
localStorage.setItem("token",r.data.token);
n("/billing");
};

return <div style={{height:"100vh",display:"flex",justifyContent:"center",alignItems:"center",background:"#0f172a",color:"white"}}>
<div>
<h2>POS LOGIN</h2>
<input value={u} onChange={e=>setU(e.target.value)} />
<input type="password" value={p} onChange={e=>setP(e.target.value)} />
<button onClick={go}>LOGIN</button>
</div>
</div>;
}
