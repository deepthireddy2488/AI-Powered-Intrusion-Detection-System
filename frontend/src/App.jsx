import { BrowserRouter, Routes, Route } from "react-router-dom";

import Home from "./pages/Home";
import Login from "./pages/Login";
import Register from "./pages/Register";
import ProtectedRoute from "./components/ProtectedRoute";

import Dashboard from "./pages/Dashboard";
import Prediction from "./pages/Prediction";
import LiveMonitoring from "./pages/LiveMonitoring";
import Reports from "./pages/Reports";

import Layout from "./components/Layout";

function App() {

  return (

    <BrowserRouter>

      <Routes>

        {/* Public Pages */}

        <Route path="/" element={<Home />} />

        <Route path="/login" element={<Login />} />

        <Route path="/register" element={<Register />} />

        {/* Protected Dashboard */}

        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Layout>
                <Dashboard />
              </Layout>
            </ProtectedRoute>
          }
        />

        <Route
          path="/prediction"
          element={
            <ProtectedRoute>
              <Layout>
                <Prediction />
              </Layout>
            </ProtectedRoute>
          }
        />


        <Route
          path="/live"
          element={
            <ProtectedRoute>
              <Layout>
                <LiveMonitoring />
              </Layout>
            </ProtectedRoute>
          }
        />

        <Route
          path="/reports"
          element={
            <ProtectedRoute>
              <Layout>
                <Reports />
              </Layout>
            </ProtectedRoute>
          }
        />

      </Routes>

    </BrowserRouter>

  );

}

export default App;