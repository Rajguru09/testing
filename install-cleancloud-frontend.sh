#!/bin/bash

# One-shot script to set up CleanCloud Frontend with Vite + React + TailwindCSS

set -e

echo "🚀 Creating project directory..."
mkdir -p ~/cleancloud/frontend
cd ~/cleancloud/frontend

echo "📦 Initializing npm project..."
npm init -y

echo "🔧 Installing dependencies..."
npm install react react-dom react-router-dom
npm install -D vite tailwindcss postcss autoprefixer

echo "🛠 Initializing Tailwind CSS..."
npx tailwindcss init -p

echo "⚙️ Creating Vite config file..."
cat > vite.config.js <<EOF
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
  }
});
EOF

echo "📁 Creating project structure..."
mkdir -p src/components/services src/pages

cat > index.html <<EOF
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>CleanCloud</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/index.js"></script>
  </body>
</html>
EOF

cat > tailwind.config.js <<EOF
module.exports = {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {},
  },
  plugins: [],
};
EOF

cat > postcss.config.js <<EOF
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};
EOF

cat > src/index.css <<EOF
@tailwind base;
@tailwind components;
@tailwind utilities;
EOF

cat > src/index.js <<EOF
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./components/App";
import "./index.css";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
EOF

cat > src/components/App.jsx <<EOF
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Signup from "../pages/Signup";
import Login from "../pages/Login";
import Dashboard from "../pages/Dashboard";
import Settings from "../pages/Settings";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </Router>
  );
}

export default App;
EOF

echo "✅ CleanCloud frontend setup completed!"
echo "👉 Next steps:"
echo "  1. Fill in your React components in src/pages/"
echo "  2. Run: npm run dev"

