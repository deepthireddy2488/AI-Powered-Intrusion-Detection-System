import { useContext } from "react";

import StatCard from "../components/StatCard";
import DashboardCharts from "../components/DashboardCharts";
import { PredictionContext } from "../context/PredictionContext";

function Dashboard() {

    const context = useContext(PredictionContext);

    const predictionData = context?.predictionData;

    // ========================================
    // DEFAULT EMPTY DASHBOARD
    // ========================================

    const totalRecords = predictionData
        ? predictionData.total_records
        : 0;

    const safeTraffic = predictionData
        ? predictionData.safe_traffic
        : 0;

    const attacksDetected = predictionData
        ? predictionData.attacks_detected
        : 0;

    const highestAttack = predictionData
        ? predictionData.highest_attack
        : "None";


    // ========================================
    // CREATE DASHBOARD DATA FROM PREDICTION
    // ========================================

    const predictionLogs = predictionData?.results
        ? predictionData.results.map((item, index) => ({

            id: index + 1,

            attack_type: item.attack,

            severity: item.severity,

            status:
                item.attack === "BENIGN"
                    ? "Normal"
                    : "Threat Detected"

        }))
        : [];


    return (

        <div>

            {/* ====================================
                TITLE
            ===================================== */}

            <div className="mb-4">

                <h2 className="fw-bold">
                    Security Dashboard
                </h2>

                <p className="text-muted">
                    AI-Powered Intrusion Detection & Network Monitoring
                </p>

            </div>


            {/* ====================================
                STATISTICS
            ===================================== */}

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


            {/* ====================================
                RECENT PREDICTION ACTIVITY
            ===================================== */}

            <div className="card shadow mt-4">

                <div className="card-header bg-dark text-white">

                    🚨 Recent Security Alerts

                </div>


                <div className="card-body">

                    {predictionLogs.length === 0 ? (

                        <div className="text-center text-muted p-4">

                            No activity available yet.
                            Upload a CSV file or start live monitoring.

                        </div>

                    ) : (

                        <div className="table-responsive">

                            <table className="table table-hover">

                                <thead>

                                    <tr>

                                        <th>ID</th>
                                        <th>Attack Type</th>
                                        <th>Severity</th>
                                        <th>Status</th>

                                    </tr>

                                </thead>


                                <tbody>

                                    {predictionLogs
                                        .slice(0, 10)
                                        .map((log) => (

                                            <tr key={log.id}>

                                                <td>
                                                    {log.id}
                                                </td>

                                                <td>
                                                    {log.attack_type}
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


            {/* ====================================
                CHARTS
            ===================================== */}

            <DashboardCharts
                attackLogs={predictionLogs}
            />

        </div>

    );

}

export default Dashboard;