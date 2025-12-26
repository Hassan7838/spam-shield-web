"use client";
import { useState } from "react";
import axios from "axios";
import { useRouter } from "next/navigation";
import Navbar2 from "../components/Navbar2";

export default function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const router = useRouter();

  const handleLogin = async () => {
    try {
      const res = await axios.post("http://localhost:8000/login", { username, password });
      localStorage.setItem("user_id", res.data.user_id);
      router.push("/emails");
    } catch {
      alert("Invalid credentials");
    }
  };

  return (
    
    <div className="bg-gray-100 min-h-screen">
          <Navbar2/>
      <h2 className="text-2xl font-bold mb-4">Login</h2>
      <input placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} className="w-full mb-2 p-2 border rounded"/>
      <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} className="w-full mb-4 p-2 border rounded"/>
      <button onClick={handleLogin} className="w-full bg-blue-600 text-white p-2 rounded hover:bg-blue-700">Login</button>
    </div>
  );
}
