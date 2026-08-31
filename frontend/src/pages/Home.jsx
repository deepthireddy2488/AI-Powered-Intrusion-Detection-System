import { Link } from "react-router-dom";

function Home() {
  return (
    <div
      className="container d-flex justify-content-center align-items-center"
      style={{ height: "100vh" }}
    >
      <div className="text-center">

        <h1 className="mb-4">
          🛡 AI-Powered Intrusion Detection System
        </h1>

        <p className="mb-4">
          Detect network attacks using Artificial Intelligence.
        </p>

        <Link
          to="/login"
          className="btn btn-primary me-3"
        >
          Login
        </Link>

        <Link
          to="/register"
          className="btn btn-success"
        >
          Register
        </Link>

      </div>
    </div>
  );
}

export default Home;