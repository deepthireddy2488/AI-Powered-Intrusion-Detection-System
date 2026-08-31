import { useEffect, useRef, useState } from "react";
import api from "../services/api";

function LiveMonitoring() {

    const [isMonitoring, setIsMonitoring] = useState(false);
    const [logs, setLogs] = useState([]);
    const [loading, setLoading] = useState(false);

    // Stores the latest database ID before monitoring starts
    const startIdRef = useRef(null);


    // ========================================
    // FETCH ONLY CURRENT SESSION LOGS
    // ========================================

    const fetchLogs = async () => {

        try {

            const response = await api.get("/attack-logs/");

            const allLogs = response.data;

            // If monitoring has not started in this page session,
            // do not show old database records
            if (startIdRef.current === null) {
                return;
            }

            // Show only records created after Start Monitoring
            const sessionLogs = allLogs.filter(
                (log) => log.id > startIdRef.current
            );

            setLogs(sessionLogs);

        } catch (error) {

            console.error(
                "Error fetching attack logs:",
                error
            );

        }

    };


    // ========================================
    // AUTO REFRESH WHILE MONITORING
    // ========================================

    useEffect(() => {

        if (!isMonitoring) {
            return;
        }

        const interval = setInterval(
            fetchLogs,
            3000
        );

        return () => clearInterval(interval);

    }, [isMonitoring]);


    // ========================================
    // START LIVE MONITORING
    // ========================================

    const startMonitoring = async () => {

        try {

            setLoading(true);

            // First get the current database records
            const logsResponse = await api.get(
                "/attack-logs/"
            );

            const allLogs = logsResponse.data;

            // Find the highest existing ID
            if (allLogs.length > 0) {

                startIdRef.current = Math.max(
                    ...allLogs.map((log) => log.id)
                );

            } else {

                startIdRef.current = 0;

            }

            // Clear old records from the page
            setLogs([]);

            // Start backend live packet capture
            const response = await api.post(
                "/live-capture/start"
            );

            console.log(response.data);

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


    // ========================================
    // STOP LIVE MONITORING
    // ========================================

    const stopMonitoring = async () => {

        try {

            setLoading(true);

            const response = await api.post(
                "/live-capture/stop"
            );

            console.log(response.data);

            // Get final records from this monitoring session
            await fetchLogs();

            setIsMonitoring(false);

        } catch (error) {

            console.error(
                "Error stopping live capture:",
                error
            );

            alert(
                "Failed to stop live monitoring."
            );

        } finally {

            setLoading(false);

        }

    };


    // ========================================
    // STATISTICS
    // ========================================

    const totalRecords = logs.length;

    const safeTraffic = logs.filter(
        (log) => log.attack_type === "BENIGN"
    ).length;

    const attacksDetected = logs.filter(
        (log) => log.attack_type !== "BENIGN"
    ).length;


    // ========================================
    // UI
    // ========================================

    return (

        <div className="container-fluid">

            <div className="d-flex justify-content-between align-items-center mb-4">

                <div>

                    <h2 className="fw-bold">
                        Live Monitoring
                    </h2>

                    <p className="text-muted mb-0">
                        Real-time network traffic and intrusion monitoring
                    </p>

                </div>


                <div>

                    {isMonitoring ? (

                        <button
                            className="btn btn-danger"
                            onClick={stopMonitoring}
                            disabled={loading}
                        >
                            {loading
                                ? "Stopping..."
                                : "Stop Monitoring"}
                        </button>

                    ) : (

                        <button
                            className="btn btn-success"
                            onClick={startMonitoring}
                            disabled={loading}
                        >
                            {loading
                                ? "Starting..."
                                : "Start Monitoring"}
                        </button>

                    )}

                </div>

            </div>


            <div
                className={
                    isMonitoring
                        ? "alert alert-success"
                        : "alert alert-secondary"
                }
            >

                <strong>
                    System Status:
                </strong>{" "}

                {isMonitoring
                    ? "Live packet capture is running"
                    : "Monitoring stopped"}

            </div>


            <div className="row">

                <div className="col-md-4 mb-4">

                    <div className="card shadow h-100">

                        <div className="card-body text-center">

                            <h6 className="text-muted">
                                Total Records
                            </h6>

                            <h2 className="text-primary fw-bold">
                                {totalRecords}
                            </h2>

                        </div>

                    </div>

                </div>


                <div className="col-md-4 mb-4">

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


                <div className="col-md-4 mb-4">

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

            </div>


            <div className="card shadow">

                <div className="card-header bg-dark text-white">
                    Live Security Alerts
                </div>


                <div className="card-body">

                    {logs.length === 0 ? (

                        <div className="text-center text-muted p-4">
                            No traffic records available.
                        </div>

                    ) : (

                        <div className="table-responsive">

                            <table className="table table-hover">

                                <thead>

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
                                                {new Date(
                                                    log.created_at
                                                ).toLocaleString()}
                                            </td>

                                            <td>
                                                {log.attack_type}
                                            </td>

                                            <td>
                                                {log.source_ip}
                                            </td>

                                            <td>
                                                {log.destination_ip}
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
                                                {log.status}
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