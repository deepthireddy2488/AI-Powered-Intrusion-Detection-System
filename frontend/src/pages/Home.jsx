import { Link } from "react-router-dom";

function Home() {
    return (
        <div
            style={{
                minHeight: "100vh",
                background:
                    "linear-gradient(135deg, #0f172a, #111827, #020617)",
                color: "white",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                padding: "40px 20px"
            }}
        >
            <div
                className="container text-center"
                style={{ maxWidth: "950px" }}
            >

                {/* LOGO / ICON */}

                <div
                    style={{
                        fontSize: "70px",
                        marginBottom: "20px"
                    }}
                >
                    🛡️
                </div>


                {/* TITLE */}

                <h1
                    className="fw-bold"
                    style={{
                        fontSize: "clamp(2.2rem, 5vw, 4rem)",
                        marginBottom: "20px"
                    }}
                >
                    AI-Powered Intrusion Detection System
                </h1>


                {/* DESCRIPTION */}

                <p
                    className="text-light"
                    style={{
                        fontSize: "1.2rem",
                        maxWidth: "750px",
                        margin: "0 auto 35px",
                        opacity: "0.85"
                    }}
                >
                    Detect, classify, and monitor network attacks
                    in real time using Artificial Intelligence
                    and Machine Learning.
                </p>


                {/* BUTTONS */}

                <div className="d-flex justify-content-center gap-3 flex-wrap">

                    <Link
                        to="/login"
                        className="btn btn-primary btn-lg px-5"
                    >
                        Login
                    </Link>


                    <Link
                        to="/register"
                        className="btn btn-outline-light btn-lg px-5"
                    >
                        Register
                    </Link>

                </div>


                {/* FEATURES */}

                <div className="row mt-5 pt-4">

                    <div className="col-md-4 mb-3">

                        <div
                            className="p-4 rounded-4 h-100"
                            style={{
                                background:
                                    "rgba(255,255,255,0.06)",
                                border:
                                    "1px solid rgba(255,255,255,0.1)"
                            }}
                        >

                            <div
                                style={{
                                    fontSize: "35px"
                                }}
                            >
                                🤖
                            </div>

                            <h5 className="fw-bold mt-3">
                                AI Detection
                            </h5>

                            <p
                                className="text-light mb-0"
                                style={{ opacity: "0.75" }}
                            >
                                Machine-learning based
                                intrusion detection.
                            </p>

                        </div>

                    </div>


                    <div className="col-md-4 mb-3">

                        <div
                            className="p-4 rounded-4 h-100"
                            style={{
                                background:
                                    "rgba(255,255,255,0.06)",
                                border:
                                    "1px solid rgba(255,255,255,0.1)"
                            }}
                        >

                            <div
                                style={{
                                    fontSize: "35px"
                                }}
                            >
                                📡
                            </div>

                            <h5 className="fw-bold mt-3">
                                Live Monitoring
                            </h5>

                            <p
                                className="text-light mb-0"
                                style={{ opacity: "0.75" }}
                            >
                                Monitor network traffic
                                and detect threats in real time.
                            </p>

                        </div>

                    </div>


                    <div className="col-md-4 mb-3">

                        <div
                            className="p-4 rounded-4 h-100"
                            style={{
                                background:
                                    "rgba(255,255,255,0.06)",
                                border:
                                    "1px solid rgba(255,255,255,0.1)"
                            }}
                        >

                            <div
                                style={{
                                    fontSize: "35px"
                                }}
                            >
                                📊
                            </div>

                            <h5 className="fw-bold mt-3">
                                Security Reports
                            </h5>

                            <p
                                className="text-light mb-0"
                                style={{ opacity: "0.75" }}
                            >
                                Analyze attacks and view
                                detailed security reports.
                            </p>

                        </div>

                    </div>

                </div>


                {/* FOOTER TEXT */}

                <p
                    className="mt-5 mb-0"
                    style={{
                        opacity: "0.5",
                        fontSize: "0.9rem"
                    }}
                >
                    AI • Machine Learning • Network Security
                </p>

            </div>
        </div>
    );
}

export default Home;