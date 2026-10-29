import { Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import ContentCreator from './pages/ContentCreator';
import Templates from './pages/Templates';
import Subscriptions from './pages/Subscriptions';
import Settings from './pages/Settings';
import NotFound from './pages/NotFound';
import Layout from './components/Layout';

const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
  const { user, loading } = useAuth();
  
  if (loading) {
    return <div className="flex items-center justify-center h-screen">Loading...</div>;
  }
  
  if (!user) {
    return <Navigate to="/login" />;
  }
  
  return <>{children}</>;
};

function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        
        <Route path="/" element={
          <ProtectedRoute>
            <Layout>
              <Dashboard />
            </Layout>
          </ProtectedRoute>
        } />
        
        <Route path="/content/create" element={
          <ProtectedRoute>
            <Layout>
              <ContentCreator />
            </Layout>
          </ProtectedRoute>
        } />
        
        <Route path="/templates" element={
          <ProtectedRoute>
            <Layout>
              <Templates />
            </Layout>
          </ProtectedRoute>
        } />
        
        <Route path="/subscriptions" element={
          <ProtectedRoute>
            <Layout>
              <Subscriptions />
            </Layout>
          </ProtectedRoute>
        } />
        
        <Route path="/settings" element={
          <ProtectedRoute>
            <Layout>
              <Settings />
            </Layout>
          </ProtectedRoute>
        } />
        
        <Route path="*" element={<NotFound />} />
      </Routes>
    </AuthProvider>
  );
}

export default App;
