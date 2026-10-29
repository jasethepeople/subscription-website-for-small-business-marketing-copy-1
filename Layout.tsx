import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { 
  LayoutDashboard, 
  FileText, 
  LayoutTemplate, 
  CreditCard, 
  Settings as SettingsIcon, 
  LogOut, 
  Menu, 
  X 
} from 'lucide-react';
import { useState } from 'react';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout = ({ children }: LayoutProps) => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Mobile sidebar toggle */}
      <div className="fixed top-4 left-4 z-50 md:hidden">
        <button 
          className="bg-white p-2 rounded-md shadow-md"
          onClick={toggleSidebar}
        >
          {sidebarOpen ? <X size={20} /> : <Menu size={20} />}
        </button>
      </div>

      {/* Sidebar */}
      <div 
        className={`fixed inset-y-0 left-0 z-40 w-64 bg-white shadow-lg transform transition-transform duration-300 ease-in-out md:translate-x-0 ${
          sidebarOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <div className="flex flex-col h-full">
          <div className="p-4 border-b">
            <h1 className="text-xl font-bold">Marketing Platform</h1>
            <p className="text-sm text-gray-500">Content Creation Suite</p>
          </div>

          <nav className="flex-1 p-4 space-y-1">
            <Link 
              to="/" 
              className="flex items-center px-4 py-3 text-gray-700 rounded-md hover:bg-gray-100"
              onClick={() => setSidebarOpen(false)}
            >
              <LayoutDashboard className="mr-3 h-5 w-5" />
              Dashboard
            </Link>
            <Link 
              to="/content/create" 
              className="flex items-center px-4 py-3 text-gray-700 rounded-md hover:bg-gray-100"
              onClick={() => setSidebarOpen(false)}
            >
              <FileText className="mr-3 h-5 w-5" />
              Create Content
            </Link>
            <Link 
              to="/templates" 
              className="flex items-center px-4 py-3 text-gray-700 rounded-md hover:bg-gray-100"
              onClick={() => setSidebarOpen(false)}
            >
              <LayoutTemplate className="mr-3 h-5 w-5" />
              Templates
            </Link>
            <Link 
              to="/subscriptions" 
              className="flex items-center px-4 py-3 text-gray-700 rounded-md hover:bg-gray-100"
              onClick={() => setSidebarOpen(false)}
            >
              <CreditCard className="mr-3 h-5 w-5" />
              Subscription
            </Link>
            <Link 
              to="/settings" 
              className="flex items-center px-4 py-3 text-gray-700 rounded-md hover:bg-gray-100"
              onClick={() => setSidebarOpen(false)}
            >
              <SettingsIcon className="mr-3 h-5 w-5" />
              Settings
            </Link>
          </nav>

          <div className="p-4 border-t">
            <div className="flex items-center mb-4">
              <div className="h-10 w-10 rounded-full bg-gray-200 flex items-center justify-center">
                {user?.name?.charAt(0) || 'U'}
              </div>
              <div className="ml-3">
                <p className="font-medium">{user?.name || 'User'}</p>
                <p className="text-xs text-gray-500">{user?.email || 'user@example.com'}</p>
              </div>
            </div>
            <button 
              className="w-full flex items-center justify-center px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
              onClick={handleLogout}
            >
              <LogOut className="mr-2 h-4 w-4" />
              Sign Out
            </button>
          </div>
        </div>
      </div>

      {/* Main content */}
      <div className="flex-1 md:ml-64 overflow-auto">
        <main className="p-4 md:p-8">
          {children}
        </main>
      </div>

      {/* Overlay for mobile */}
      {sidebarOpen && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 z-30 md:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}
    </div>
  );
};

export default Layout;
