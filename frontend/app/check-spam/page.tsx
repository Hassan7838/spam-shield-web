"use client";
import { useState } from "react";
import axios from "axios";
import Navbar from "../components/Navbar";

export default function CheckSpamPage() {
  const [text, setText] = useState("");
  const [result, setResult] = useState<string | null>(null);

  const handleCheck = async () => {
    const res = await axios.post("http://localhost:8000/check-spam", { email_text: text });
    setResult(res.data.is_spam ? "SPAM" : "NOT SPAM");
  };

  return (
    <div className="bg-gray-100 min-h-screen">
          <Navbar/>
      <h2 className="text-2xl font-bold mb-4">Check Spam</h2>
      <textarea placeholder="Paste email text..." value={text} onChange={e => setText(e.target.value)} className="w-full mb-4 p-2 border rounded"/>
      <button onClick={handleCheck} className="w-full bg-red-600 text-white p-2 rounded hover:bg-red-700 mb-4">Check</button>
      {result && <p className="text-lg font-bold">Result: {result}</p>}
    </div>
  );
}