export default function Navbar() {
  return (
    <nav className="bg-white shadow-sm border-b border-gray-200 px-6 py-3 flex items-center justify-between">
      <h1 className="text-xl font-semibold tracking-tight text-gray-800">
        Loco<span className="text-blue-600">S3</span>
      </h1>
      <div className="flex items-center gap-4">
        <button className="text-sm px-3 py-1 rounded-md bg-blue-600 text-white hover:bg-blue-700">
          Upload
        </button>
        <img
          src="https://ui-avatars.com/api/?name=Admin"
          alt="user"
          className="w-8 h-8 rounded-full"
        />
      </div>
    </nav>
  );
}
