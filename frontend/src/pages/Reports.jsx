import { useContext } from "react";
import { PredictionContext } from "../context/PredictionContext";
import generateReport from "../utils/generateReport";

function Reports() {

    const context = useContext(PredictionContext);

    const predictionData = context?.predictionData;


    // ========================================
    // NO REPORT DATA
    // ========================================

    if (!predictionData) {

        return (

            <div className="container mt-4">

                <h2 className="fw-bold">
                    Reports
                </h2>

                <div className="alert alert-info mt-4">

                    No prediction report available yet.

                    <br />

                    Please go to <strong>AI Prediction</strong> and
                    upload a CSV file first.

                </div>

            </div>

        );
    }


    // ========================================
    // ATTACK DISTRIBUTION
    // ========================================

    const attackCounts = {};

    if (Array.isArray(predictionData.results)) {

        predictionData.results.forEach((item) => {

            const attack = item.attack;

            attackCounts[attack] =
                (attackCounts[attack] || 0) + 1;

        });

    }


    return (

        <div className="container mt-4">

            {/* ========================================
                HEADER
            ======================================== */}

            <div className="d-flex justify-content-between align-items-center mb-4">

                <div>

                    <h2 className="fw-bold">
                        Security Reports
                    </h2>

                    <p className="text-muted">
                        AI-powered intrusion detection prediction report
                    </p>

                </div>


                <button
                    className="btn btn-success"
                    onClick={() => generateReport(predictionData)}
                >
                    📄 Download PDF
                </button>

            </div>


            {/* ========================================
                SUMMARY CARDS
            ======================================== */}

            <div className="row">

                <div className="col-md-3 mb-4">

                    <div className="card shadow border-0 text-center">

                        <div className="card-body">

                            <h6 className="text-muted">
                                Total Records
                            </h6>

                            <h2 className="fw-bold">
                                {predictionData.total_records}
                            </h2>

                        </div>

                    </div>

                </div>


                <div className="col-md-3 mb-4">

                    <div className="card shadow border-0 text-center">

                        <div className="card-body">

                            <h6 className="text-muted">
                                Safe Traffic
                            </h6>

                            <h2 className="text-success fw-bold">
                                {predictionData.safe_traffic}
                            </h2>

                        </div>

                    </div>

                </div>


                <div className="col-md-3 mb-4">

                    <div className="card shadow border-0 text-center">

                        <div className="card-body">

                            <h6 className="text-muted">
                                Attacks Detected
                            </h6>

                            <h2 className="text-danger fw-bold">
                                {predictionData.attacks_detected}
                            </h2>

                        </div>

                    </div>

                </div>


                <div className="col-md-3 mb-4">

                    <div className="card shadow border-0 text-center">

                        <div className="card-body">

                            <h6 className="text-muted">
                                Highest Attack
                            </h6>

                            <h5 className="text-danger fw-bold mt-2">
                                {predictionData.highest_attack || "None"}
                            </h5>

                        </div>

                    </div>

                </div>

            </div>


            {/* ========================================
                ATTACK DISTRIBUTION
            ======================================== */}

            <div className="card shadow border-0 mb-4">

                <div className="card-header bg-dark text-white">

                    <h5 className="mb-0">
                        Attack Distribution
                    </h5>

                </div>


                <div className="card-body">

                    {Object.keys(attackCounts).length === 0 ? (

                        <p className="text-muted mb-0">
                            No prediction data available.
                        </p>

                    ) : (

                        <div className="row">

                            {Object.entries(attackCounts).map(
                                ([attack, count]) => (

                                    <div
                                        className="col-md-3 mb-3"
                                        key={attack}
                                    >

                                        <div className="border rounded p-3 text-center">

                                            <h6 className="text-muted">
                                                {attack}
                                            </h6>

                                            <h3 className={
                                                attack === "BENIGN"
                                                    ? "text-success"
                                                    : "text-danger"
                                            }>
                                                {count}
                                            </h3>

                                        </div>

                                    </div>

                                )
                            )}

                        </div>

                    )}

                </div>

            </div>


            {/* ========================================
                PREDICTION TABLE
            ======================================== */}

            <div className="card shadow">

                <div className="card-header">

                    <h5 className="mb-0">
                        Prediction Report
                    </h5>

                </div>


                <div className="card-body">

                    <div className="table-responsive">

                        <table className="table table-bordered table-hover">

                            <thead className="table-dark">

                                <tr>

                                    <th>Row</th>
                                    <th>Attack Type</th>
                                    <th>Severity</th>
                                    <th>Recommendation</th>

                                </tr>

                            </thead>


                            <tbody>

                                {Array.isArray(predictionData.results) &&
                                    predictionData.results.map((item) => (

                                        <tr key={item.row}>

                                            <td>
                                                {item.row}
                                            </td>

                                            <td>
                                                {item.attack}
                                            </td>

                                            <td>

                                                <span
                                                    className={
                                                        item.severity === "High"
                                                            ? "text-danger fw-bold"
                                                            : item.severity === "Medium"
                                                                ? "text-warning fw-bold"
                                                                : "text-success fw-bold"
                                                    }
                                                >
                                                    {item.severity}
                                                </span>

                                            </td>

                                            <td>
                                                {item.recommendation}
                                            </td>

                                        </tr>

                                    ))}

                            </tbody>

                        </table>

                    </div>

                </div>

            </div>

        </div>

    );
}

export default Reports;