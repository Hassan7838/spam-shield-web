"use client";
import Link from "next/link";

export default function Home() {
  return (
    <div className="card">
  <div
    style={{
      display: "flex",
      justifyContent: "center",
      alignItems: "center",
      gap: "15px",
      marginTop: "20px",
    }}
  >
    <Link href="/login">
      <button
        style={{
          backgroundColor: "#0070f3",
          color: "white",
          padding: "10px 20px",
          border: "none",
          borderRadius: "6px",
          cursor: "pointer",
        }}
      >
        Login
      </button>
    </Link>

    <Link href="/signup">
      <button
        style={{
          backgroundColor: "#22c55e",
          color: "white",
          padding: "10px 20px",
          border: "none",
          borderRadius: "6px",
          cursor: "pointer",
        }}
      >
        Sign Up
      </button>
    </Link>
  </div>
</div>

  );
}
