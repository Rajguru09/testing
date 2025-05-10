const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

// Centralized response handler with improved error handling
const handleResponse = async (res) => {
  let data;
  try {
    // Try parsing the response as JSON
    data = await res.json();
  } catch (err) {
    throw new Error("Invalid response from server.");
  }

  // Handle non-200 status codes by throwing an error with the appropriate message
  if (!res.ok) {
    throw new Error(data?.detail || "Something went wrong with the request.");
  }

  return data;
};

// Helper: Create headers with optional token
const createHeaders = (token = null) => {
  const headers = {
    "Content-Type": "application/json",
  };
  if (token) headers["Authorization"] = `Bearer ${token}`;
  return headers;
};

// Helper function to add timeout to fetch
const fetchWithTimeout = async (url, options, timeout = 10000) => {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeout);

  try {
    const res = await fetch(url, { ...options, signal: controller.signal });
    clearTimeout(timeoutId); // Clear the timeout if fetch is successful
    return res;
  } catch (err) {
    clearTimeout(timeoutId); // Clear the timeout if fetch fails
    throw err;
  }
};

// Generic fetch API function to reduce redundancy
const fetchAPI = async (url, method, data = null, token = null) => {
  const options = {
    method: method,
    headers: createHeaders(token), // Attach token if present
  };

  // If there's data (POST or PUT request), stringify it
  if (data) {
    options.body = JSON.stringify(data);
  }

  try {
    const res = await fetchWithTimeout(`${API_BASE_URL}${url}`, options); // Using timeout wrapper
    if (!res.ok) {
      // If the response status is 401, token may have expired
      if (res.status === 401) {
        throw new Error("Session expired. Please log in again.");
      }
      const errorData = await res.json();
      throw new Error(errorData?.detail || "Something went wrong with the request.");
    }
    return await handleResponse(res); // Wait and return the response data
  } catch (err) {
    // Handle error gracefully by providing a clear message
    throw new Error(`Error: ${err.message}`);
  }
};

// API Calls

// User signup
export async function signupUser(userData) {
  console.log("Signup payload:", userData); // For debugging
  return fetchAPI('/auth/signup', 'POST', userData);
}

// User login
export async function loginUser(userData) {
  return fetchAPI('/auth/login', 'POST', userData);
}

// Get user dashboard with token
export async function getUserDashboard(token) {
  return fetchAPI('/users/dashboard', 'GET', null, token);
}

// Get Cloud Audit Data
export async function getCloudAuditData(token) {
  return fetchAPI('/cloud-audit', 'GET', null, token);
}

// Get Idle Resources
export async function getIdleResources(token) {
  return fetchAPI('/idle-resources', 'GET', null, token);
}
