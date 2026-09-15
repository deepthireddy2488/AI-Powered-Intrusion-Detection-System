import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../services/api";
import DashboardCharts from "../components/DashboardCharts";

function ReportDetails() {
    const { sessionId } = useParams();
    const navigate = useNavigate();

    const [report, setReport] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        const loadReport = async () => {
            try {
                setLoading(true);
                setError("");

                const response = await api.get(
                    `/analysis-sessions/${sessionId}`
                );

                setReport(response.data);

            } catch (err) {
                console.error(
                    "Failed to load report:",
                    err
                );

                setError(
                    err.response?.data?.detail ||
                    "Failed to load report details."
                );
            } finally {
                setLoading(false);
            }
        };

        loadReport();
    }, [sessionId]);

    if (loading) {
        return (
            <div className="container-fluid">
                <div className="text-center p-5">
                    <div
                        className="spinner-border text-primary"
                        role="status"
                    />

                    <p className="text-muted mt-3">
                        Loading report details...
                    </p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="container-fluid">
                <button
                    className="btn btn-secondary mb-4"
                    onClick={() => navigate("/reports")}
                >
                    ← Back to Reports
                </button>

                <div className="alert alert-danger">
                    {error}
                </div>
            </div>
        );
    }

    if (!report) {
        return null;
    }

    const session = report.session;

    // Convert CSV results to the format expected by DashboardCharts
    const chartLogs = (report.results || []).map((item) => ({
        id: item.id,
        attack_type: item.attack,
        severity: item.severity,
        source_ip: item.source_ip || "-",
        destination_ip: item.destination_ip || "-",
        status: item.status || (
            item.attack === "BENIGN"
                ? "Normal"
                : "Threat Detected"
        ),
        created_at: item.created_at
    }));

    return (
        <div className="container-fluid">

            {/* HEADER */}

            <div className="d-flex justify-content-between align-items-center mb-4">

                <div>
                    <h2 className="fw-bold">
                        Security Report Details
                    </h2>

                    <p className="text-muted mb-0">
                        {session.source_type === "CSV"
                            ? "📄 CSV Prediction"
                            : "🛡️ Live Monitoring"}
                    </p>
                </div>

                <button
                    className="btn btn-secondary"
                    onClick={() => navigate("/reports")}
                >
                    ← Back to Reports
                </button>

            </div>


            {/* SESSION INFORMATION */}

            <div className="card shadow-sm mb-4">
                <div className="card-body">

                    <div className="row">

                        <div className="col-md-4 mb-3">
                            <strong>Type</strong>
                            <div className="mt-1">
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
                        </div>

                        <div className="col-md-4 mb-3">
                            <strong>Name</strong>
                            <div className="mt-1">
                                {session.name || "-"}
                            </div>
                        </div>

                        <div className="col-md-4 mb-3">
                            <strong>Started</strong>
                            <div className="mt-1">
                                {session.created_at
                                    ? new Date(
                                        session.created_at
                                    ).toLocaleString()
                                    : "-"}
                            </div>
                        </div>

                        <div className="col-md-4">
                            <strong>Completed</strong>
                            <div className="mt-1">
                                {session.completed_at
                                    ? new Date(
                                        session.completed_at
                                    ).toLocaleString()
                                    : "-"}
                            </div>
                        </div>

                    </div>

                </div>
            </div>


            {/* SUMMARY */}

            <div className="row">

                <div className="col-md-3 mb-4">
                    <div className="card shadow h-100">
                        <div className="card-body text-center">
                            <h6 className="text-muted">
                                Total Records
                            </h6>

                            <h2 className="text-primary fw-bold">
                                {report.total_records}
                            </h2>
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
                                {report.safe_traffic}
                            </h2>
                        </div>
                    </div>
                </div>


                <div className="col-md-3 mb-4">
                    <div className="card shadow h-100">
                        <div className="card-body text-center">
                            <h6 className="text-muted">
                                Attacks Detected
                            </h6>

                            <h2 className="text-danger fw-bold">
                                {report.attacks_detected}
                            </h2>
                        </div>
                    </div>
                </div>


                <div className="col-md-3 mb-4">
                    <div className="card shadow h-100">
                        <div className="card-body text-center">
                            <h6 className="text-muted">
                                Attack Types
                            </h6>

                            <h2 className="fw-bold">
                                {
                                    Object.keys(
                                        report.attack_distribution || {}
                                    ).length
                                }
                            </h2>
                        </div>
                    </div>
                </div>

            </div>


            {/* CHARTS */}

            <DashboardCharts
                attackLogs={chartLogs}
            />


            {/* DISTRIBUTIONS */}

            <div className="row mt-2">

                <div className="col-md-6 mb-4">

                    <div className="card shadow h-100">

                        <div className="card-header bg-dark text-white">
                            Attack Distribution
                        </div>

                        <div className="card-body">

                            {Object.keys(
                                report.attack_distribution || {}
                            ).length === 0 ? (

                                <p className="text-muted mb-0">
                                    No attacks detected.
                                </p>

                            ) : (

                                <div className="table-responsive">

                                    <table className="table table-hover">

                                        <thead>
                                            <tr>
                                                <th>
                                                    Attack Type
                                                </th>

                                                <th>
                                                    Count
                                                </th>
                                            </tr>
                                        </thead>

                                        <tbody>

                                            {Object.entries(
                                                report.attack_distribution
                                            ).map(
                                                ([attack, count]) => (
                                                    <tr key={attack}>
                                                        <td>
                                                            {attack}
                                                        </td>

                                                        <td>
                                                            {count}
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

                </div>


                <div className="col-md-6 mb-4">

                    <div className="card shadow h-100">

                        <div className="card-header bg-dark text-white">
                            Severity Distribution
                        </div>

                        <div className="card-body">

                            <div className="table-responsive">

                                <table className="table table-hover">

                                    <thead>
                                        <tr>
                                            <th>
                                                Severity
                                            </th>

                                            <th>
                                                Count
                                            </th>
                                        </tr>
                                    </thead>

                                    <tbody>

                                        {Object.entries(
                                            report.severity_distribution || {}
                                        ).map(
                                            ([severity, count]) => (
                                                <tr key={severity}>
                                                    <td>
                                                        {severity}
                                                    </td>

                                                    <td>
                                                        {count}
                                                    </td>
                                                </tr>
                                            )
                                        )}

                                    </tbody>

                                </table>

                            </div>

                        </div>

                    </div>

                </div>

            </div>


            {/* COMPLETE RECORDS */}

            <div className="card shadow mt-2">

                <div className="card-header bg-dark text-white">
                    Complete Records
                </div>

                <div className="card-body">

                    {report.results?.length === 0 ? (

                        <p className="text-muted mb-0">
                            No records available.
                        </p>

                    ) : (

                        <div className="table-responsive">

                            <table className="table table-hover align-middle">

                                <thead className="table-dark">

                                    <tr>
                                        <th>ID</th>
                                        <th>Attack Type</th>
                                        <th>Severity</th>
                                        <th>Confidence</th>
                                        <th>Recommendation</th>
                                    </tr>

                                </thead>

                                <tbody>

                                    {report.results.map((item) => (

                                        <tr key={item.id}>

                                            <td>
                                                {item.id}
                                            </td>

                                            <td>
                                                {item.attack}
                                            </td>

                                            <td>
                                                <span
                                                    className={
                                                        item.severity === "High"
                                                            ? "badge bg-danger"
                                                            : item.severity === "Medium"
                                                            ? "badge bg-warning text-dark"
                                                            : "badge bg-success"
                                                    }
                                                >
                                                    {item.severity}
                                                </span>
                                            </td>

                                            <td>
                                                {item.confidence != null
                                                    ? `${(
                                                        Number(item.confidence) * 100
                                                    ).toFixed(2)}%`
                                                    : "-"}
                                            </td>

                                            <td>
                                                {item.recommendation || "-"}
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

export default ReportDetails;