import { useEffect, useState } from "react";

import StatCard from "../components/StatCard";
import DashboardCharts from "../components/DashboardCharts";
import api from "../services/api";


function Dashboard() {

    const [sessionData, setSessionData] = useState(null);
    const [loading, setLoading] = useState(true);


    // ==========================================
    // GET CURRENT SESSION
    // ==========================================

    const fetchCurrentSession = async () => {

        try {

            const sessionId =
                sessionStorage.getItem(
                    "currentAnalysisSessionId"
                );


            // No current session
            if (!sessionId) {

                setSessionData(null);

                return;

            }


            const response = await api.get(
                `/analysis-sessions/${sessionId}`
            );


            setSessionData(response.data);

        } catch (error) {

            console.error(
                "Error loading current dashboard session:",
                error
            );

            setSessionData(null);

        } finally {

            setLoading(false);

        }

    };


    // ==========================================
    // INITIAL LOAD
    // ==========================================

    useEffect(() => {

        fetchCurrentSession();

    }, []);


    // ==========================================
    // AUTO REFRESH
    // ==========================================

    useEffect(() => {

        const interval = setInterval(() => {

            fetchCurrentSession();

        }, 3000);


        return () => clearInterval(interval);

    }, []);


    // ==========================================
    // CURRENT SESSION DATA
    // ==========================================

    const results =
        sessionData?.results || [];


    const totalRecords =
        sessionData?.total_records || 0;


    const safeTraffic =
        sessionData?.safe_traffic || 0;


    const attacksDetected =
        sessionData?.attacks_detected || 0;


    const attackCounts =
        sessionData?.attack_distribution || {};


    const highestAttack =
        Object.keys(attackCounts).length > 0
            ? Object.keys(attackCounts).reduce(
                (a, b) =>
                    attackCounts[a] > attackCounts[b]
                        ? a
                        : b
            )
            : "None";


    // ==========================================
    // CONVERT DATA FOR CHARTS
    // ==========================================

    const dashboardLogs = results.map(
        (item) => ({
            id: item.id,
            attack_type:
                item.attack || item.attack_type,
            severity:
                item.severity,
            status:
                item.status ||
                (
                    item.attack === "BENIGN"
                        ? "Normal"
                        : "Threat Detected"
                ),
            source_ip:
                item.source_ip || "-",
            destination_ip:
                item.destination_ip || "-",
            created_at:
                item.created_at
        })
    );


    const recentLogs =
        dashboardLogs.slice(0, 10);


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
                    />

                    <p className="text-muted mt-3">
                        Loading security dashboard...
                    </p>

                </div>

            </div>
        );

    }


    // ==========================================
    // NO CURRENT SESSION
    // ==========================================

    if (!sessionData) {

        return (
            <div className="container-fluid">

                <div className="mb-4">

                    <h2 className="fw-bold">
                        Security Dashboard
                    </h2>

                    <p className="text-muted">
                        AI-Powered Intrusion Detection & Network Monitoring
                    </p>

                </div>


                <div className="row">

                    <div className="col-md-3 mb-3">
                        <StatCard
                            title="Total Records"
                            value={0}
                            color="primary"
                        />
                    </div>

                    <div className="col-md-3 mb-3">
                        <StatCard
                            title="Attacks Detected"
                            value={0}
                            color="danger"
                        />
                    </div>

                    <div className="col-md-3 mb-3">
                        <StatCard
                            title="Safe Traffic"
                            value={0}
                            color="success"
                        />
                    </div>

                    <div className="col-md-3 mb-3">
                        <StatCard
                            title="Highest Attack"
                            value="None"
                            color="warning"
                        />
                    </div>

                </div>


                <div className="alert alert-info mt-3">

                    <strong>
                        No current analysis session.
                    </strong>

                    <br />

                    Upload a CSV file or start live monitoring
                    to create a new analysis session.

                </div>

            </div>
        );

    }


    // ==========================================
    // UI
    // ==========================================

    return (

        <div className="container-fluid">

            <div className="mb-4">

                <h2 className="fw-bold">
                    Security Dashboard
                </h2>

                <p className="text-muted">
                    AI-Powered Intrusion Detection & Network Monitoring
                </p>

            </div>


            {/* CURRENT SESSION */}

            <div className="alert alert-primary">

                <strong>
                    Current Session:
                </strong>{" "}

                {sessionData.session?.source_type === "CSV"
                    ? "📄 CSV Prediction"
                    : "🛡️ Live Monitoring"}

                {" — "}

                {sessionData.session?.name || "Analysis Session"}

            </div>


            {/* STATISTICS */}

            <div className="row">

                <div className="col-md-3 mb-3">

                    <StatCard
                        title="Total Records"
                        value={totalRecords}
                        color="primary"
                    />

                </div>


                <div className="col-md-3 mb-3">

                    <StatCard
                        title="Attacks Detected"
                        value={attacksDetected}
                        color="danger"
                    />

                </div>


                <div className="col-md-3 mb-3">

                    <StatCard
                        title="Safe Traffic"
                        value={safeTraffic}
                        color="success"
                    />

                </div>


                <div className="col-md-3 mb-3">

                    <StatCard
                        title="Highest Attack"
                        value={highestAttack}
                        color="warning"
                    />

                </div>

            </div>


            {/* RECENT ALERTS */}

            <div className="card shadow mt-4">

                <div className="card-header bg-dark text-white">
                    🚨 Recent Security Alerts
                </div>

                <div className="card-body">

                    {recentLogs.length === 0 ? (

                        <div className="text-center text-muted p-4">
                            No records in this session.
                        </div>

                    ) : (

                        <div className="table-responsive">

                            <table className="table table-hover align-middle">

                                <thead className="table-dark">

                                    <tr>

                                        <th>ID</th>
                                        <th>Attack Type</th>
                                        <th>Severity</th>
                                        <th>Status</th>

                                    </tr>

                                </thead>

                                <tbody>

                                    {recentLogs.map(
                                        (log) => (

                                            <tr key={log.id}>

                                                <td>
                                                    {log.id}
                                                </td>

                                                <td>
                                                    <strong>
                                                        {log.attack_type}
                                                    </strong>
                                                </td>

                                                <td>

                                                    <span
                                                        className={
                                                            log.severity === "High"
                                                                ? "badge bg-danger"
                                                                : log.severity === "Medium"
                                                                ? "badge bg-warning text-dark"
                                                                : "badge bg-success"
                                                        }
                                                    >
                                                        {log.severity}
                                                    </span>

                                                </td>

                                                <td>

                                                    {log.attack_type !== "BENIGN" ? (

                                                        <span className="badge bg-danger">
                                                            Threat Detected
                                                        </span>

                                                    ) : (

                                                        <span className="badge bg-success">
                                                            Normal
                                                        </span>

                                                    )}

                                                </td>

                                            </tr>

                                        )
                                    )}

                                </tbody>

                            </table>

                        </div>

                    )}

                </div>

            </div>


            {/* CHARTS */}

            <DashboardCharts
                attackLogs={dashboardLogs}
            />

        </div>
    );
}


export default Dashboard;