import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Signup from "../pages/Signup";
import Login from "../pages/Login";
import Dashboard from "../pages/Dashboard"; // Home Page
import Settings from "../pages/Settings";
import IdleResources from "../pages/IdleResources";
import CloudAudit from "../pages/CloudAudit";

// Protected route component
const ProtectedRoute = ({ element }) => {
  const isAuthenticated = localStorage.getItem("access_token");
  return isAuthenticated ? element : <Navigate to="/login" replace />;
};

function App() {
  const [loading, setLoading] = React.useState(true);

  React.useEffect(() => {
    setTimeout(() => {
      setLoading(false);
    }, 1000);
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />

        {/* Main homepage after login */}
        <Route path="/dashboard" element={<ProtectedRoute element={<Dashboard />} />} />

        {/* Additional protected service routes */}
        <Route path="/idle-resources/dashboard" element={<ProtectedRoute element={<IdleResources />} />} />
        <Route path="/audit" element={<ProtectedRoute element={<CloudAudit />} />} />
        <Route path="/settings" element={<ProtectedRoute element={<Settings />} />} />

        {/* Fallback */}
        <Route path="*" element={<h2>Oops! 404 - Page Not Found <a href="/login">Go to Login</a></h2>} />
      </Routes>
    </Router>
  );
}

export default App;
