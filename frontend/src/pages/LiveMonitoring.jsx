import { useEffect, useState } from "react";
import api from "../services/api";
import generateLiveReport from "../utils/generateLiveReport";


function LiveMonitoring() {

    const [isMonitoring, setIsMonitoring] = useState(false);
    const [logs, setLogs] = useState([]);
    const [loading, setLoading] = useState(false);
    const [initialLoading, setInitialLoading] = useState(true);


    // ============================================
    // GET STORED SESSION ID
    // ============================================

    const getSessionId = () => {

        return sessionStorage.getItem(
            "liveMonitoringSessionId"
        );

    };


    // ============================================
    // FETCH SESSION LOGS
    // ============================================

    const fetchCurrentSessionLogs = async (
        sessionId = null
    ) => {

        try {

            const currentSessionId =
                sessionId || getSessionId();

            if (!currentSessionId) {

                setLogs([]);

                return;

            }

            const response = await api.get(
                `/attack-logs/?session_id=${currentSessionId}`
            );

            setLogs(
                Array.isArray(response.data)
                    ? response.data
                    : []
            );

        } catch (error) {

            console.error(
                "Error fetching session logs:",
                error
            );

            setLogs([]);

        }

    };


    // ============================================
    // CHECK BACKEND STATUS
    // ============================================

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


    // ============================================
    // INITIAL LOAD
    // ============================================

    useEffect(() => {

        const loadData = async () => {

            setInitialLoading(true);

            try {

                const statusData =
                    await fetchMonitoringStatus();


                const running =
                    statusData.status === "running";


                setIsMonitoring(running);


                // ------------------------------------
                // If backend is running
                // ------------------------------------

                if (
                    running &&
                    statusData.session_id
                ) {

                    sessionStorage.setItem(
                        "liveMonitoringSessionId",
                        statusData.session_id
                    );
                    sessionStorage.setItem(
                        "currentAnalysisSessionId",
                        newSessionId
                    );

                    await fetchCurrentSessionLogs(
                        statusData.session_id
                    );

                }

                // ------------------------------------
                // If backend is stopped
                //
                // DO NOT DELETE sessionStorage.
                //
                // We want to display the completed
                // session until a new session starts.
                // ------------------------------------

                else {

                    const savedSessionId =
                        getSessionId();

                    if (savedSessionId) {

                        await fetchCurrentSessionLogs(
                            savedSessionId
                        );

                    } else {

                        setLogs([]);

                    }

                }

            } catch (error) {

                console.error(
                    "Error loading monitoring page:",
                    error
                );

                setIsMonitoring(false);

            } finally {

                setInitialLoading(false);

            }

        };


        loadData();

    }, []);


    // ============================================
    // POLLING WHILE MONITORING
    // ============================================

    useEffect(() => {

        if (!isMonitoring) {

            return;

        }


        const interval = setInterval(() => {

            fetchCurrentSessionLogs();

        }, 3000);


        return () => {

            clearInterval(interval);

        };

    }, [isMonitoring]);


    // ============================================
    // START MONITORING
    // ============================================

    const startMonitoring = async () => {

        try {

            setLoading(true);


            // ------------------------------------
            // Clear previous session from display
            // ------------------------------------

            setLogs([]);


            // ------------------------------------
            // Start new backend session
            // ------------------------------------

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


            // ------------------------------------
            // Store NEW session ID
            // ------------------------------------

            sessionStorage.setItem(
                "liveMonitoringSessionId",
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
                error.response?.data?.detail ||
                "Failed to start live monitoring."
            );

        } finally {

            setLoading(false);

        }

    };


    // ============================================
    // STOP MONITORING
    // ============================================

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


            // ------------------------------------
            // IMPORTANT
            //
            // Keep the session ID.
            // Do NOT clear it.
            // ------------------------------------

            if (response.data.session_id) {

                sessionStorage.setItem(
                    "liveMonitoringSessionId",
                    response.data.session_id
                );

            }


            // Load the final completed records

            if (response.data.session_id) {

                await fetchCurrentSessionLogs(
                    response.data.session_id
                );

            }


            setIsMonitoring(false);


        } catch (error) {

            console.error(
                "Error stopping live capture:",
                error
            );


            alert(
                error.response?.data?.detail ||
                "Failed to stop live capture."
            );

        } finally {

            setLoading(false);

        }

    };


    // ============================================
    // STATISTICS
    // ============================================

    const totalRecords =
        logs.length;


    const safeTraffic =
        logs.filter(
            (log) =>
                log.attack_type === "BENIGN"
        ).length;


    const attacksDetected =
        logs.filter(
            (log) =>
                log.attack_type !== "BENIGN"
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


    // ============================================
    // LOADING
    // ============================================

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


    // ============================================
    // UI
    // ============================================

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
                    style={{
                        fontSize: "18px"
                    }}
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


            {/* COMPLETED SESSION MESSAGE */}

            {!isMonitoring && logs.length > 0 && (

                <div className="alert alert-info">

                    <strong>
                        Completed Monitoring Session
                    </strong>

                    <br />

                    These records belong to your latest
                    completed live-monitoring session.

                    <br />

                    They are permanently stored in the database.

                    <br />

                    Starting a new monitoring session will
                    create a fresh session and reset the
                    Dashboard to zero.

                </div>

            )}


            {/* NO SESSION */}

            {!isMonitoring && logs.length === 0 && (

                <div className="alert alert-secondary">

                    <strong>
                        No monitoring session.
                    </strong>

                    <br />

                    Click <strong>Start Monitoring</strong>
                    to begin a new session.

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
                        🚨 Live Monitoring Security Alerts
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
                                No monitoring records
                            </h5>

                            <p>
                                Start live monitoring to
                                analyze network traffic.
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
                                                    : "-"
                                                }
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