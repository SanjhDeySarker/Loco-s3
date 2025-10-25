import { FiDatabase, FiSettings } from "react-icons/fi";
import { Link } from "react-router-dom";

export default function Sidebar() {
  return (
    <aside className="w-60 h-full bg-white border-r border-gray-200 p-4 flex flex-col">
      <h2 className="text-lg font-semibold mb-6">Menu</h2>
      <nav className="flex flex-col gap-2">
        <Link
          to="/"
          className="flex items-center gap-2 px-3 py-2 rounded-md hover:bg-blue-50 hover:text-blue-600 transition"
        >
          <FiDatabase /> Buckets
        </Link>
        <Link
          to="/settings"
          className="flex items-center gap-2 px-3 py-2 rounded-md hover:bg-blue-50 hover:text-blue-600 transition"
        >
          <FiSettings /> Settings
        </Link>
      </nav>
    </aside>
  );
}
