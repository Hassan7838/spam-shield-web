import Navbar from "./components/Navbar";
import './globals.css';

export const metadata = {
  title: 'Spam Shield',
  description: 'Email tracker and spam detector',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-gray-100 min-h-screen">
        <main className="bg-gray-100 min-h-screen">
          {children}
        </main>
      </body>
    </html>
  );
}
