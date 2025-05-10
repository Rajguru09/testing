//frontend/src/pages/Signup.jsx
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function Signup() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState(''); // Added confirm password
  const [mobileNumber, setMobileNumber] = useState(''); // Added mobile number
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSignup = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(''); // Clear any previous errors

    // Basic validation for email, password, confirm password, and mobile number
    if (!email || !password || !confirmPassword || !mobileNumber) {
      setError('Please fill in all fields.');
      setLoading(false);
      return;
    }

    // Confirm that passwords match
    if (password !== confirmPassword) {
      setError('Passwords do not match.');
      setLoading(false);
      return;
    }

    try {
      const res = await fetch('http://localhost:8000/signup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password, mobile_number: mobileNumber }),
      });

      const data = await res.json();

      if (res.ok) {
        localStorage.setItem('token', data.access_token);
        alert('Signup successful!');
        navigate('/dashboard');  // Navigate to dashboard on success
      } else {
        setError(data.detail || 'Signup failed');
      }
    } catch (error) {
      setError('An error occurred. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="h-screen flex flex-col items-center justify-center bg-gray-100">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-blue-600">Welcome to Tech Solution</h1>
      </div>

      <div className="p-8 max-w-md mx-auto bg-white shadow-lg rounded-lg">
        {error && <p className="text-red-500 mb-4">{error}</p>} {/* Display error message */}
        
        <form onSubmit={handleSignup} className="space-y-4">
          <input
            className="border p-2 w-full rounded-md text-sm"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            disabled={loading}  // Disable inputs while loading
          />
          
          <input
            className="border p-2 w-full rounded-md text-sm"
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            disabled={loading}  // Disable inputs while loading
          />
          
          <input
            className="border p-2 w-full rounded-md text-sm"
            type="password"
            placeholder="Confirm Password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            disabled={loading}  // Disable inputs while loading
          />

          <input
            className="border p-2 w-full rounded-md text-sm"
            placeholder="Mobile Number"
            value={mobileNumber}
            onChange={(e) => setMobileNumber(e.target.value)}
            disabled={loading}  // Disable inputs while loading
          />

          <button
            className="bg-blue-600 text-white px-4 py-2 w-full rounded-md text-sm"
            type="submit"
            disabled={loading}  // Disable button while loading
          >
            {loading ? 'Signing up...' : 'Sign Up'}
          </button>
        </form>
      </div>
    </div>
  );
}
