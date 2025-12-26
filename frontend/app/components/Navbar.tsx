"use client";
import Link from "next/link";

export default function Navbar() {
  return (
    <nav className="bg-white shadow p-4 flex justify-between items-center">
      <h1 className="text-xl font-bold text-blue-600">Spam Shield</h1>
      <div className="space-x-5">
        <Link href="/emails" className="text-gray-700 hover:text-blue-600">Dashboard</Link>
        <Link href="/send-email" className="text-gray-700 hover:text-blue-600">Send Email</Link>
        <Link href="/check-spam" className="text-gray-700 hover:text-blue-600">Check Spam</Link>
        <Link href="/" className="text-gray-700 hover:text-blue-600">Logout</Link>
      </div>
    </nav>
  );
}
