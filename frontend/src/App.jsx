import { BrowserRouter, Routes, Route } from "react-router-dom";

import Home from "./pages/Home";
import Login from "./pages/Login";
import Register from "./pages/Register";
import ProtectedRoute from "./components/ProtectedRoute";
import Layout from "./components/Layout";

import Dashboard from "./pages/Dashboard";
import Prediction from "./pages/Prediction";
import LiveMonitoring from "./pages/LiveMonitoring";
import Reports from "./pages/Reports";
import ReportDetails from "./pages/ReportDetails";
import ThreatTimeline from "./pages/ThreatTimeline";

function App() {
    return (
        <BrowserRouter>
            <Routes>
                {/* Public pages */}
                <Route path="/" element={<Home />} />
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />

                {/* Authenticated product pages */}
                <Route
                    path="/dashboard"
                    element={<ProtectedRoute><Layout><Dashboard /></Layout></ProtectedRoute>}
                />
                <Route
                    path="/prediction"
                    element={<ProtectedRoute><Layout><Prediction /></Layout></ProtectedRoute>}
                />
                <Route
                    path="/live"
                    element={<ProtectedRoute><Layout><LiveMonitoring /></Layout></ProtectedRoute>}
                />
                <Route
                    path="/reports"
                    element={<ProtectedRoute><Layout><Reports /></Layout></ProtectedRoute>}
                />
                <Route
                    path="/reports/:sessionId"
                    element={<ProtectedRoute><Layout><ReportDetails /></Layout></ProtectedRoute>}
                />
                {/* Without a session ID, the timeline selects the newest session. */}
                <Route
                    path="/timeline"
                    element={<ProtectedRoute><Layout><ThreatTimeline /></Layout></ProtectedRoute>}
                />
                <Route
                    path="/timeline/:sessionId"
                    element={<ProtectedRoute><Layout><ThreatTimeline /></Layout></ProtectedRoute>}
                />
            </Routes>
        </BrowserRouter>
    );
}

export default App;
