"use client";
import { useEffect, useState } from "react";
import axios from "axios";
import Navbar from "../components/Navbar";

interface Email {
  id: number;
  recipient: string;
  subject: string;
  sent_at: string;
  opened_at: string | null;
}

export default function EmailsPage() {
  const [emails, setEmails] = useState<Email[]>([]);
  //const userId = Number(localStorage.getItem("user_id") || 0);
  const userId =
  typeof window !== "undefined"
    ? Number(localStorage.getItem("user_id") || 0)
    : 0;



  useEffect(() => {
    axios.get(`http://localhost:8000/emails?user_id=${userId}`).then(res => setEmails(res.data));
  }, []);

  return (
    <div className="bg-gray-100 min-h-screen">
      <Navbar/>
      <h2 className="text-2xl font-bold mb-4">Your Emails</h2>
      <table className="w-full table-auto border-collapse">
        <thead>
          <tr className="bg-gray-200">
            <th className="border p-2">Subject</th>
            <th className="border p-2">Recipient</th>
            <th className="border p-2">Status</th>
          </tr>
        </thead>
        <tbody>
          {emails.map(e => (
            <tr key={e.id} className="bg-white border-b">
              <td className="border p-2">{e.subject}</td>
              <td className="border p-2">{e.recipient}</td>
              <td className="border p-2">{e.opened_at ? "OPENED" : "NOT OPENED"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
