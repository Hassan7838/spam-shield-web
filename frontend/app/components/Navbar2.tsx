"use client";
import Link from "next/link";

export default function Navbar2() {
  return (
    <nav className="bg-white shadow p-4 flex justify-between items-center">
      <h1 className="text-xl font-bold text-blue-600">Spam Shield</h1>
      <div className="space-x-5">
        <Link href="/" className="text-gray-700 hover:text-blue-600">Login / Sign Up</Link>
      </div>
    </nav>
  );
}
