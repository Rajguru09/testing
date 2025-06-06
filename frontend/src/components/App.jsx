import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Signup from "../pages/Signup";
import Login from "../pages/Login";
import Dashboard from "../pages/Dashboard";
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
    // Simulate loading or authentication state, could be replaced with more real checks
    const timer = setTimeout(() => {
      setLoading(false);
    }, 1000); // 1 second simulated loading
    return () => clearTimeout(timer); // Cleanup timeout if the component is unmounted
  }, []);

  if (loading) {
    return (
      <div className="loading-container">
        <div className="spinner"></div> {/* Add a spinner or any loading animation */}
        <p>Loading...</p>
      </div>
    );
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
