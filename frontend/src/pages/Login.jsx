import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import api from "../services/api";

function Login() {

    const navigate = useNavigate();

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const login = async (e) => {

        e.preventDefault();

        setError("");
        setLoading(true);

        try {

            const response = await api.post("/auth/login", {
                email,
                password
            });
            // Clear any live-monitoring session from a previous login
            sessionStorage.removeItem(
                "liveMonitoringSessionId"
            );
            // Save JWT token

            localStorage.setItem(
                "access_token",
                response.data.access_token
            );

            // Redirect to Dashboard

            navigate("/dashboard");

        } catch (error) {

            console.log(error);

            if (error.response) {

                setError(
                    error.response.data.detail || "Login failed."
                );

            } else {

                setError(
                    "Unable to connect to the server. Please try again."
                );

            }

        } finally {

            setLoading(false);

        }

    };


    return (

        <div
            className="min-vh-100 d-flex align-items-center"
            style={{
                background:
                    "linear-gradient(135deg, #081120 0%, #102a43 50%, #071a2e 100%)"
            }}
        >

            <div className="container">

                <div className="row justify-content-center align-items-center g-5">


                    {/* LEFT SIDE - PROJECT INFORMATION */}

                    <div className="col-lg-6 text-white">

                        <div className="mb-4">

                            <div
                                className="d-flex align-items-center gap-3 mb-4"
                            >

                                <div
                                    className="d-flex align-items-center justify-content-center"
                                    style={{
                                        width: "65px",
                                        height: "65px",
                                        borderRadius: "16px",
                                        background:
                                            "linear-gradient(135deg, #00c6ff, #0072ff)",
                                        fontSize: "32px",
                                        boxShadow:
                                            "0 0 25px rgba(0, 198, 255, 0.4)"
                                    }}
                                >
                                    🛡️
                                </div>

                                <div>

                                    <h2 className="fw-bold mb-0">
                                        AI IDS
                                    </h2>

                                    <small
                                        style={{
                                            color: "#8fa9c4"
                                        }}
                                    >
                                        Advanced Cybersecurity Platform
                                    </small>

                                </div>

                            </div>


                            <h1
                                className="fw-bold mb-3"
                                style={{
                                    fontSize: "42px",
                                    lineHeight: "1.2"
                                }}
                            >
                                AI-Powered Intrusion
                                <br />
                                Detection System
                            </h1>


                            <p
                                style={{
                                    color: "#aabed0",
                                    fontSize: "18px",
                                    lineHeight: "1.7"
                                }}
                            >
                                Secure your network with intelligent threat
                                detection, machine learning analysis, and
                                real-time security monitoring.
                            </p>

                        </div>


                        {/* FEATURES */}

                        <div className="mt-4">

                            <div className="d-flex align-items-center mb-3">

                                <span
                                    className="me-3 d-flex align-items-center justify-content-center"
                                    style={{
                                        width: "35px",
                                        height: "35px",
                                        borderRadius: "50%",
                                        background:
                                            "rgba(0, 198, 255, 0.15)",
                                        color: "#00c6ff"
                                    }}
                                >
                                    🛡
                                </span>

                                <span
                                    style={{
                                        color: "#d9e6f2"
                                    }}
                                >
                                    Real-Time Threat Detection
                                </span>

                            </div>


                            <div className="d-flex align-items-center mb-3">

                                <span
                                    className="me-3 d-flex align-items-center justify-content-center"
                                    style={{
                                        width: "35px",
                                        height: "35px",
                                        borderRadius: "50%",
                                        background:
                                            "rgba(0, 198, 255, 0.15)",
                                        color: "#00c6ff"
                                    }}
                                >
                                    🤖
                                </span>

                                <span
                                    style={{
                                        color: "#d9e6f2"
                                    }}
                                >
                                    AI-Powered Attack Analysis
                                </span>

                            </div>


                            <div className="d-flex align-items-center">

                                <span
                                    className="me-3 d-flex align-items-center justify-content-center"
                                    style={{
                                        width: "35px",
                                        height: "35px",
                                        borderRadius: "50%",
                                        background:
                                            "rgba(0, 198, 255, 0.15)",
                                        color: "#00c6ff"
                                    }}
                                >
                                    📊
                                </span>

                                <span
                                    style={{
                                        color: "#d9e6f2"
                                    }}
                                >
                                    Intelligent Security Monitoring
                                </span>

                            </div>

                        </div>

                    </div>


                    {/* RIGHT SIDE - LOGIN CARD */}

                    <div className="col-lg-5">

                        <div
                            className="card border-0"
                            style={{
                                borderRadius: "20px",
                                background: "#ffffff",
                                boxShadow:
                                    "0 20px 60px rgba(0, 0, 0, 0.35)"
                            }}
                        >

                            <div
                                className="card-body p-4 p-md-5"
                            >

                                <div className="text-center mb-4">

                                    <div
                                        className="mb-3"
                                        style={{
                                            fontSize: "42px"
                                        }}
                                    >
                                        🔐
                                    </div>

                                    <h2 className="fw-bold">
                                        Welcome Back
                                    </h2>

                                    <p className="text-muted mb-0">
                                        Sign in to access your security
                                        dashboard
                                    </p>

                                </div>


                                {/* ERROR MESSAGE */}

                                {error && (

                                    <div
                                        className="alert alert-danger"
                                    >
                                        {error}
                                    </div>

                                )}


                                <form onSubmit={login}>


                                    {/* EMAIL */}

                                    <div className="mb-3">

                                        <label className="form-label fw-semibold">

                                            Email Address

                                        </label>

                                        <input
                                            type="email"
                                            className="form-control form-control-lg"
                                            placeholder="Enter your email"
                                            value={email}
                                            onChange={(e) =>
                                                setEmail(e.target.value)
                                            }
                                            required
                                            disabled={loading}
                                        />

                                    </div>


                                    {/* PASSWORD */}

                                    <div className="mb-4">

                                        <label className="form-label fw-semibold">

                                            Password

                                        </label>

                                        <input
                                            type="password"
                                            className="form-control form-control-lg"
                                            placeholder="Enter your password"
                                            value={password}
                                            onChange={(e) =>
                                                setPassword(e.target.value)
                                            }
                                            required
                                            disabled={loading}
                                        />

                                    </div>


                                    {/* LOGIN BUTTON */}

                                    <button
                                        type="submit"
                                        className="btn btn-primary btn-lg w-100"
                                        disabled={loading}
                                        style={{
                                            borderRadius: "10px",
                                            padding: "12px",
                                            background:
                                                "linear-gradient(90deg, #0072ff, #00c6ff)",
                                            border: "none"
                                        }}
                                    >

                                        {loading
                                            ? "Signing In..."
                                            : "🔐 Secure Login"}

                                    </button>


                                    {/* REGISTER LINK */}

                                    <div className="text-center mt-4">

                                        <span className="text-muted">

                                            Don't have an account?{" "}

                                        </span>

                                        <Link
                                            to="/register"
                                            className="text-decoration-none fw-bold"
                                        >

                                            Create Account

                                        </Link>

                                    </div>

                                </form>

                            </div>

                        </div>


                        <p
                            className="text-center mt-3 mb-0"
                            style={{
                                color: "#7890a8",
                                fontSize: "13px"
                            }}
                        >
                            🔒 Secure Authentication • AI-Powered Security
                        </p>

                    </div>

                </div>

            </div>

        </div>

    );

}

export default Login;