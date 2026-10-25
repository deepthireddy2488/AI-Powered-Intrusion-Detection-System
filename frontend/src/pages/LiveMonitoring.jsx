import { useEffect, useState } from "react";
import api from "../services/api";
import generateLiveReport from "../utils/generateLiveReport";

function LiveMonitoring() {
    const [isMonitoring, setIsMonitoring] = useState(false);
    const [logs, setLogs] = useState([]);
    const [loading, setLoading] = useState(false);
    const [initialLoading, setInitialLoading] = useState(true);

    // Fetch current session logs only
    const fetchCurrentSessionLogs = async () => {
        try {
            const currentSessionId =
                sessionStorage.getItem(
                    "liveMonitoringSessionId"
                );

            if (!currentSessionId) {
                setLogs([]);
                return;
            }

            const response = await api.get(
                `/attack-logs/?session_id=${currentSessionId}`
            );

            setLogs(response.data || []);
        } catch (error) {
            console.error(
                "Error fetching current session logs:",
                error
            );
        }
    };

    // Check monitoring status
    const fetchMonitoringStatus = async () => {
        try {
            const response = await api.get(
                "/live-capture/status"
            );

            return response.data;
        } catch (error) {
            console.error(
                "Error fetching monitoring status:",
                error
            );

            return {
                status: "stopped",
                session_id: null
            };
        }
    };

    // Load page
    useEffect(() => {
        const loadData = async () => {
            setInitialLoading(true);

            try {
                const statusData =
                    await fetchMonitoringStatus();

                const running =
                    statusData.status === "running";

                setIsMonitoring(running);

                /*
                 * If backend says monitoring is running,
                 * use the backend session ID.
                 */
                if (running && statusData.session_id) {
                    sessionStorage.setItem(
                        "liveMonitoringSessionId",
                        statusData.session_id
                    );
                    sessionStorage.setItem(
                        "currentAnalysisSessionId",
                        statusData.session_id
                    );

                    // Load only this session's records
                    try {
                        const response = await api.get(
                            `/attack-logs/?session_id=${statusData.session_id}`
                        );

                        setLogs(response.data || []);
                    } catch (error) {
                        console.error(
                            "Error loading session logs:",
                            error
                        );

                        setLogs([]);
                    }
                } else {
                    /*
                     * Monitoring is stopped.
                     * Dashboard/Live Monitoring must start
                     * from zero and must not show old records.
                     */
                    sessionStorage.removeItem(
                        "liveMonitoringSessionId"
                    );

                    setLogs([]);
                }
            } catch (error) {
                console.error(
                    "Error loading monitoring page:",
                    error
                );

                setIsMonitoring(false);
                setLogs([]);
            } finally {
                setInitialLoading(false);
            }
        };

        loadData();
    }, []);

    // Poll current session logs
    useEffect(() => {
        if (!isMonitoring) {
            return;
        }

        fetchCurrentSessionLogs();

        const interval = setInterval(() => {
            fetchCurrentSessionLogs();
        }, 3000);

        return () => {
            clearInterval(interval);
        };
    }, [isMonitoring]);

    // START MONITORING
    const startMonitoring = async () => {
        try {
            setLoading(true);

            // Clear any previous session
            sessionStorage.removeItem(
                "liveMonitoringSessionId"
            );
            sessionStorage.removeItem(
                "currentAnalysisSessionId"
            );

            setLogs([]);

            /*
             * Backend creates a completely new UUID session.
             */
            const response = await api.post(
                "/live-capture/start"
            );

            console.log(
                "Live capture start response:",
                response.data
            );

            const newSessionId =
                response.data.session_id;

            if (!newSessionId) {
                throw new Error(
                    "Backend did not return session_id"
                );
            }

            /*
             * Save the NEW session ID.
             */
            sessionStorage.setItem(
                "liveMonitoringSessionId",
                newSessionId
            );
            sessionStorage.setItem(
                "currentAnalysisSessionId",
                newSessionId
            );

            setLogs([]);
            setIsMonitoring(true);
        } catch (error) {
            console.error(
                "Error starting live capture:",
                error
            );

            alert(
                "Failed to start live monitoring."
            );
        } finally {
            setLoading(false);
        }
    };

    // STOP MONITORING
    const stopMonitoring = async () => {
        try {
            setLoading(true);

            const response = await api.post(
                "/live-capture/stop"
            );

            console.log(
                "Live capture stop response:",
                response.data
            );

            /*
             * Monitoring session is finished.
             * Records remain permanently in PostgreSQL.
             *
             * But Live Monitoring display should reset to 0.
             */
            setIsMonitoring(false);
            setLogs([]);

            sessionStorage.removeItem(
                "liveMonitoringSessionId"
            );
        } catch (error) {
            console.error(
                "Error stopping live capture:",
                error
            );

            alert(
                "Failed to stop live capture."
            );
        } finally {
            setLoading(false);
        }
    };

    // Statistics
    const totalRecords = logs.length;

    const safeTraffic = logs.filter(
        (log) => log.attack_type === "BENIGN"
    ).length;

    const attacksDetected = logs.filter(
        (log) => log.attack_type !== "BENIGN"
    ).length;

    const attackCounts = {};

    logs.forEach((log) => {
        if (log.attack_type !== "BENIGN") {
            attackCounts[log.attack_type] =
                (attackCounts[log.attack_type] || 0) + 1;
        }
    });

    const highestAttack =
        Object.keys(attackCounts).length > 0
            ? Object.keys(attackCounts).reduce(
                (a, b) =>
                    attackCounts[a] > attackCounts[b]
                        ? a
                        : b
            )
            : "None";

    if (initialLoading) {
        return (
            <div className="container-fluid">
                <div className="text-center p-5">
                    <div
                        className="spinner-border text-primary"
                        role="status"
                    />

                    <p className="text-muted mt-3">
                        Loading monitoring data...
                    </p>
                </div>
            </div>
        );
    }

    return (
        <div className="container-fluid">

            {/* HEADER */}
            <div className="d-flex justify-content-between align-items-center mb-4">

                <div>
                    <h2 className="fw-bold">
                        Live Monitoring
                    </h2>

                    <p className="text-muted mb-0">
                        Real-time network traffic and
                        intrusion monitoring
                    </p>
                </div>

                <div className="d-flex gap-2">

                    <button
                        type="button"
                        className="btn btn-outline-primary"
                        onClick={() =>
                            generateLiveReport(logs)
                        }
                        disabled={logs.length === 0}
                    >
                        📄 Download PDF
                    </button>

                    {isMonitoring ? (
                        <button
                            type="button"
                            className="btn btn-danger"
                            onClick={stopMonitoring}
                            disabled={loading}
                        >
                            {loading
                                ? "Stopping..."
                                : "⏹ Stop Monitoring"}
                        </button>
                    ) : (
                        <button
                            type="button"
                            className="btn btn-success"
                            onClick={startMonitoring}
                            disabled={loading}
                        >
                            {loading
                                ? "Starting..."
                                : "▶ Start Monitoring"}
                        </button>
                    )}

                </div>
            </div>

            {/* STATUS */}
            <div
                className={
                    isMonitoring
                        ? "alert alert-success d-flex align-items-center"
                        : "alert alert-secondary d-flex align-items-center"
                }
            >
                <span
                    className="me-2"
                    style={{ fontSize: "18px" }}
                >
                    {isMonitoring ? "🟢" : "⚪"}
                </span>

                <div>
                    <strong>
                        System Status:
                    </strong>{" "}

                    {isMonitoring
                        ? "Live packet capture is running"
                        : "Monitoring stopped"}
                </div>
            </div>

            {/* CURRENT SESSION INFO */}
            {!isMonitoring && (
                <div className="alert alert-info">
                    <strong>
                        No active monitoring session.
                    </strong>

                    <br />

                    Previous monitoring records are stored
                    permanently in the database and are not
                    shown here.

                    <br />

                    Click <strong>Start Monitoring</strong> to
                    begin a new session.
                </div>
            )}

            {/* STATISTICS */}
            <div className="row">

                <div className="col-md-3 mb-4">
                    <div className="card shadow h-100">
                        <div className="card-body text-center">

                            <h6 className="text-muted">
                                Current Session
                            </h6>

                            <h2 className="text-primary fw-bold">
                                {totalRecords}
                            </h2>

                            <small className="text-muted">
                                Records
                            </small>

                        </div>
                    </div>
                </div>

                <div className="col-md-3 mb-4">
                    <div className="card shadow h-100">
                        <div className="card-body text-center">

                            <h6 className="text-muted">
                                Safe Traffic
                            </h6>

                            <h2 className="text-success fw-bold">
                                {safeTraffic}
                            </h2>

                        </div>
                    </div>
                </div>

                <div className="col-md-3 mb-4">
                    <div className="card shadow h-100">
                        <div className="card-body text-center">

                            <h6 className="text-muted">
                                Threats Detected
                            </h6>

                            <h2 className="text-danger fw-bold">
                                {attacksDetected}
                            </h2>

                        </div>
                    </div>
                </div>

                <div className="col-md-3 mb-4">
                    <div className="card shadow h-100">
                        <div className="card-body text-center">

                            <h6 className="text-muted">
                                Highest Attack
                            </h6>

                            <h5 className="text-danger fw-bold mt-2">
                                {highestAttack}
                            </h5>

                        </div>
                    </div>
                </div>

            </div>

            {/* ALERT TABLE */}
            <div className="card shadow">

                <div className="card-header bg-dark text-white d-flex justify-content-between align-items-center">

                    <span>
                        🚨 Current Session Security Alerts
                    </span>

                    <span className="small">
                        {logs.length} records
                    </span>

                </div>

                <div className="card-body">

                    {logs.length === 0 ? (

                        <div className="text-center text-muted p-5">

                            <div style={{ fontSize: "40px" }}>
                                🛡️
                            </div>

                            <h5 className="mt-3">
                                No new monitoring records
                            </h5>

                            <p>
                                Start live monitoring to
                                analyze new network traffic.
                            </p>

                        </div>

                    ) : (

                        <div className="table-responsive">

                            <table className="table table-hover align-middle">

                                <thead className="table-dark">

                                    <tr>
                                        <th>ID</th>
                                        <th>Time</th>
                                        <th>Attack Type</th>
                                        <th>Source IP</th>
                                        <th>Destination IP</th>
                                        <th>Severity</th>
                                        <th>Status</th>
                                    </tr>

                                </thead>

                                <tbody>

                                    {logs.map((log) => (

                                        <tr key={log.id}>

                                            <td>
                                                {log.id}
                                            </td>

                                            <td>
                                                {log.created_at
                                                    ? new Date(
                                                        log.created_at
                                                    ).toLocaleString()
                                                    : "-"}
                                            </td>

                                            <td className="fw-semibold">
                                                {log.attack_type || "-"}
                                            </td>

                                            <td>
                                                {log.source_ip || "-"}
                                            </td>

                                            <td>
                                                {log.destination_ip || "-"}
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
                                                    {log.severity || "-"}
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

                                    ))}

                                </tbody>

                            </table>

                        </div>

                    )}

                </div>
            </div>

        </div>
    );
}

export default LiveMonitoring;