"use client";
import { useState } from "react";
import axios from "axios";
import { useRouter } from "next/navigation";
import Navbar2 from "../components/Navbar2";

export default function SignupPage() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const router = useRouter();

  const handleSignup = async () => {
    try {
      await axios.post("http://localhost:8000/signup", { username, email, password });
      alert("User created");
      router.push("/login");
    } catch {
      alert("Error creating user");
    }
  };

  return (
    <div className="bg-gray-100 min-h-screen">
          <Navbar2/>
      <h2 className="text-2xl font-bold mb-4">Signup</h2>
      <input placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} className="w-full mb-2 p-2 border rounded"/>
      <input placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} className="w-full mb-2 p-2 border rounded"/>
      <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} className="w-full mb-4 p-2 border rounded"/>
      <button onClick={handleSignup} className="w-full bg-green-600 text-white p-2 rounded hover:bg-green-700">Signup</button>
    </div>
  );
}
