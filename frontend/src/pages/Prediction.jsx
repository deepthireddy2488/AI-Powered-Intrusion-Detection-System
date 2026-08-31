import { useState, useContext } from "react";
import api from "../services/api";
import { PredictionContext } from "../context/PredictionContext";
import generateReport from "../utils/generateReport";

function Prediction() {

    const [file, setFile] = useState(null);
    const [result, setResult] = useState(null);
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    const context = useContext(PredictionContext);


    // ========================================
    // UPLOAD AND PREDICT
    // ========================================

    const uploadFile = async () => {

        console.log("UPLOAD BUTTON CLICKED");

        setError("");
        setResult(null);

        if (!file) {

            setError("Please select a CSV file first.");

            return;

        }

        setLoading(true);

        try {

            const formData = new FormData();

            formData.append("file", file);

            console.log("Sending file:", file.name);

            const response = await api.post(
                "/predict/csv",
                formData
            );

            console.log(
                "Backend Response:",
                response.data
            );

            const data = response.data;


            // ========================================
            // BACKEND ERROR
            // ========================================

            if (data.status === "error") {

                setError(
                    data.message ||
                    data.detail ||
                    "Prediction failed."
                );

                return;

            }


            // ========================================
            // CHECK RESULTS
            // ========================================

            if (!Array.isArray(data.results)) {

                setError(
                    "Backend did not return prediction results."
                );

                console.log(
                    "Unexpected response:",
                    data
                );

                return;

            }


            // ========================================
            // SAVE RESULTS
            // ========================================

            setResult(data);


            // Save prediction for Dashboard and Reports

            if (context?.setPredictionData) {

                context.setPredictionData(data);

            }

        } catch (err) {

            console.error(
                "Prediction Error:",
                err
            );

            setError(
                err.response?.data?.detail ||
                err.message ||
                "Prediction failed. Please check the backend."
            );

        } finally {

            setLoading(false);

        }

    };


    // ========================================
    // FILE SELECTION
    // ========================================

    const handleFileChange = (e) => {

        const selectedFile = e.target.files[0];

        if (!selectedFile) {

            return;

        }

        console.log(
            "Selected file:",
            selectedFile.name
        );

        setFile(selectedFile);
        setResult(null);
        setError("");

    };


    // ========================================
    // UI
    // ========================================

    return (

        <div className="container mt-4">

            <h2 className="mb-2">
                AI Intrusion Detection
            </h2>

            <p className="text-muted mb-4">
                Upload a CSV file to analyze network traffic using AI.
            </p>


            {/* ========================================
                FILE UPLOAD
            ======================================== */}

            <div className="card shadow p-4 mb-4">

                <label className="form-label fw-bold">
                    Select CSV File
                </label>

                <input
                    type="file"
                    className="form-control mb-3"
                    accept=".csv,text/csv"
                    onChange={handleFileChange}
                />


                {/* Selected file */}

                {file && (

                    <div className="alert alert-secondary py-2">

                        <strong>
                            Selected File:
                        </strong>{" "}

                        {file.name}

                    </div>

                )}


                {/* Upload button */}

                <button
                    type="button"
                    className="btn btn-primary"
                    onClick={uploadFile}
                    disabled={loading}
                >

                    {loading
                        ? "Predicting..."
                        : "Upload & Predict"}

                </button>

            </div>


            {/* ========================================
                ERROR
            ======================================== */}

            {error && (

                <div className="alert alert-danger">

                    <strong>
                        Error:
                    </strong>{" "}

                    {error}

                </div>

            )}


            {/* ========================================
                RESULTS
            ======================================== */}

            {result && (

                <>

                    {/* Summary Cards */}

                    <div className="row mt-4">

                        <div className="col-md-3 mb-3">

                            <div className="card text-center shadow h-100">

                                <div className="card-body">

                                    <h6 className="text-muted">
                                        Total Records
                                    </h6>

                                    <h2>
                                        {result.total_records}
                                    </h2>

                                </div>

                            </div>

                        </div>


                        <div className="col-md-3 mb-3">

                            <div className="card text-center shadow h-100">

                                <div className="card-body">

                                    <h6 className="text-muted">
                                        Safe Traffic
                                    </h6>

                                    <h2 className="text-success">
                                        {result.safe_traffic}
                                    </h2>

                                </div>

                            </div>

                        </div>


                        <div className="col-md-3 mb-3">

                            <div className="card text-center shadow h-100">

                                <div className="card-body">

                                    <h6 className="text-muted">
                                        Attacks
                                    </h6>

                                    <h2 className="text-danger">
                                        {result.attacks_detected}
                                    </h2>

                                </div>

                            </div>

                        </div>


                        <div className="col-md-3 mb-3">

                            <div className="card text-center shadow h-100">

                                <div className="card-body">

                                    <h6 className="text-muted">
                                        Highest Attack
                                    </h6>

                                    <h5 className="text-danger mt-2">

                                        {result.highest_attack || "None"}

                                    </h5>

                                </div>

                            </div>

                        </div>

                    </div>


                    {/* ========================================
                        PREDICTION TABLE
                    ======================================== */}

                    <div className="card mt-4 shadow">

                        <div className="card-header bg-dark text-white">

                            <h5 className="mb-0">
                                Prediction Results
                            </h5>

                        </div>


                        <div className="card-body">

                            <div className="table-responsive">

                                <table className="table table-bordered table-hover">

                                    <thead className="table-dark">

                                        <tr>

                                            <th>Row</th>
                                            <th>Attack</th>
                                            <th>Severity</th>
                                            <th>Recommendation</th>

                                        </tr>

                                    </thead>


                                    <tbody>

                                        {result.results.map((item) => (

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


                            {/* PDF */}

                            <div className="text-center mt-4">

                                <button
                                    type="button"
                                    className="btn btn-success"
                                    onClick={() => generateReport(result)}
                                >

                                    📄 Download PDF Report

                                </button>

                            </div>

                        </div>

                    </div>

                </>

            )}

        </div>

    );

}

export default Prediction;