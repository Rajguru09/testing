import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getUserDashboard } from "../components/services/api";

// Loading Spinner Component
const LoadingSpinner = () => (
  <div className="spinner-container">
    <div className="spinner"></div>
    <p>Loading your dashboard...</p>
  </div>
);

export default function Dashboard() {
  const [userData, setUserData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchDashboardData = async () => {
      const token = localStorage.getItem("access_token");

      if (!token) {
        navigate("/login");
        return;
      }

      try {
        const data = await getUserDashboard(token);
        setUserData(data);
      } catch (err) {
        setError(err.message || "Failed to fetch dashboard data.");
        navigate("/login");  // Redirect to login if there's an error fetching data
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, [navigate]);

  const handleServiceClick = (service) => {
    const redirectTo =
      service === "idle" ? "/idle-resources/dashboard" : "/audit";

    navigate("/aws-credentials", {
      state: { redirectTo },
    });
  };

  if (loading) return <LoadingSpinner />;
  if (error) return <div className="text-red-500 text-center">{error}</div>;

  return (
    <div className="p-8 max-w-xl mx-auto">
      <h1 className="text-2xl font-bold text-center mb-6">Welcome to Tech Solution</h1>
      <p className="text-center mb-8">Please select a service to proceed</p>

      <div className="space-y-4">
        <button
          onClick={() => handleServiceClick("idle")}
          className="bg-green-600 hover:bg-green-700 text-white px-4 py-3 rounded w-full"
        >
          Cloud Idle Resources
        </button>

        <button
          onClick={() => handleServiceClick("audit")}
          className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-3 rounded w-full"
        >
          Cloud Audit Accountability
        </button>
      </div>
    </div>
  );
}
