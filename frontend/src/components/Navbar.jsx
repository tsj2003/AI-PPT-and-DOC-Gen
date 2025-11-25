import { Link, useNavigate } from 'react-router-dom';
import { LogOut, FileText } from 'lucide-react';
import { logout, isAuthenticated } from '../api/auth';

export default function Navbar() {
  const navigate = useNavigate();
  const authenticated = isAuthenticated();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="bg-blue-600 text-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link to="/dashboard" className="flex items-center space-x-2">
              <FileText className="h-8 w-8" />
              <span className="text-xl font-bold">AI Document Platform</span>
            </Link>
          </div>
          
          {authenticated && (
            <div className="flex items-center space-x-4">
              <Link to="/dashboard" className="hover:bg-blue-700 px-3 py-2 rounded-md">
                Dashboard
              </Link>
              <Link to="/create" className="hover:bg-blue-700 px-3 py-2 rounded-md">
                New Project
              </Link>
              <button
                onClick={handleLogout}
                className="flex items-center space-x-1 hover:bg-blue-700 px-3 py-2 rounded-md"
              >
                <LogOut className="h-4 w-4" />
                <span>Logout</span>
              </button>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
}
