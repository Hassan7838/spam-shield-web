"use client";
import { useState } from "react";
import axios from "axios";
import Navbar from "../components/Navbar";

export default function SendEmailPage() {
  const userId = Number(localStorage.getItem("user_id") || 0);
  const [recipient, setRecipient] = useState("");
  const [subject, setSubject] = useState("");
  const [body, setBody] = useState("");

  const handleSend = async () => {
    try {
      await axios.post("http://localhost:8000/send-email", { user_id: userId, recipient, subject, body });
      alert("Email sent!");
      setRecipient(""); setSubject(""); setBody("");
    } catch {
      alert("Failed to send email");
    }
  };

  return (
    <div className="bg-gray-100 min-h-screen">
      <Navbar/>
      <h2 className="text-2xl font-bold mb-4">Send Email</h2>
      <input placeholder="Recipient" value={recipient} onChange={e => setRecipient(e.target.value)} className="w-full mb-2 p-2 border rounded"/>
      <input placeholder="Subject" value={subject} onChange={e => setSubject(e.target.value)} className="w-full mb-2 p-2 border rounded"/>
      <textarea placeholder="Body" value={body} onChange={e => setBody(e.target.value)} className="w-full mb-4 p-2 border rounded"/>
      <button onClick={handleSend} className="w-full bg-blue-600 text-white p-2 rounded hover:bg-blue-700">Send</button>
    </div>
  );
}
