import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

function Reports() {
    const [sessions, setSessions] = useState([]);
    const [loading, setLoading] = useState(true);

    const navigate = useNavigate();

    // ==========================================
    // LOAD ALL USER SESSIONS
    // ==========================================

    const fetchSessions = async () => {
        try {
            const response = await api.get("/analysis-sessions/");

            setSessions(
                Array.isArray(response.data)
                    ? response.data
                    : []
            );

        } catch (error) {
            console.error(
                "Error loading analysis sessions:",
                error
            );
        } finally {
            setLoading(false);
        }
    };

    // ==========================================
    // INITIAL LOAD
    // ==========================================

    useEffect(() => {
        fetchSessions();
    }, []);

    // ==========================================
    // VIEW SESSION DETAILS
    // ==========================================

    const viewDetails = (sessionId) => {
        navigate(`/reports/${sessionId}`);
    };

    // ==========================================
    // FORMAT DATE
    // ==========================================

    const formatDate = (date) => {
        if (!date) {
            return "-";
        }

        return new Date(date).toLocaleString();
    };

    // ==========================================
    // LOADING
    // ==========================================

    if (loading) {
        return (
            <div className="container-fluid">
                <div className="text-center p-5">
                    <div
                        className="spinner-border text-primary"
                        role="status"
                    ></div>

                    <p className="text-muted mt-3">
                        Loading security reports...
                    </p>
                </div>
            </div>
        );
    }

    // ==========================================
    // UI
    // ==========================================

    return (
        <div className="container-fluid">

            {/* ====================================
                TITLE
            ===================================== */}

            <div className="mb-4">
                <h2 className="fw-bold">
                    Security Reports
                </h2>

                <p className="text-muted">
                    View all CSV prediction and live monitoring sessions
                </p>
            </div>


            {/* ====================================
                NO REPORTS
            ===================================== */}

            {sessions.length === 0 ? (

                <div className="card shadow-sm">
                    <div className="card-body text-center p-5">

                        <div
                            style={{
                                fontSize: "50px"
                            }}
                        >
                            🛡️
                        </div>

                        <h5 className="mt-3">
                            No security reports available
                        </h5>

                        <p className="text-muted mb-0">
                            Upload a CSV file or start live monitoring
                            to create a report.
                        </p>

                    </div>
                </div>

            ) : (

                /* ==================================
                   SESSION CARDS
                ================================== */

                <div className="row">

                    {sessions.map((session) => (

                        <div
                            className="col-md-6 col-lg-4 mb-4"
                            key={session.session_id}
                        >

                            <div className="card shadow-sm h-100">

                                {/* HEADER */}

                                <div className="card-header d-flex justify-content-between align-items-center">

                                    <strong>
                                        {session.source_type === "CSV"
                                            ? "📄 CSV Prediction"
                                            : "🛡️ Live Monitoring"}
                                    </strong>

                                    <span
                                        className={
                                            session.source_type === "CSV"
                                                ? "badge bg-primary"
                                                : "badge bg-success"
                                        }
                                    >
                                        {session.source_type}
                                    </span>

                                </div>


                                {/* BODY */}

                                <div className="card-body">

                                    <h5 className="card-title mb-3">
                                        {session.name ||
                                            (session.source_type === "CSV"
                                                ? "CSV Analysis"
                                                : "Live Monitoring")}
                                    </h5>


                                    <p className="text-muted small mb-2">
                                        <strong>Started:</strong>{" "}
                                        {formatDate(
                                            session.created_at
                                        )}
                                    </p>


                                    <p className="text-muted small mb-3">
                                        <strong>Completed:</strong>{" "}
                                        {formatDate(
                                            session.completed_at
                                        )}
                                    </p>


                                    <button
                                        className="btn btn-primary w-100"
                                        onClick={() =>
                                            viewDetails(
                                                session.session_id
                                            )
                                        }
                                    >
                                        View Details
                                    </button>

                                </div>

                            </div>

                        </div>

                    ))}

                </div>
            )}

        </div>
    );
}

export default Reports;