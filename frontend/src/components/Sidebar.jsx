import { Link, useNavigate } from "react-router-dom";

import {
  FaShieldAlt,
  FaChartPie,
  FaRobot,
  FaUpload,
  FaBroadcastTower,
  FaFileAlt,
  FaSignOutAlt
} from "react-icons/fa";

function Sidebar() {

  const navigate = useNavigate();

  const logout = () => {

    localStorage.removeItem("token");

    navigate("/login");

  };

  return (

    <div
      className="bg-dark text-white d-flex flex-column shadow"
      style={{
        width: "260px",
        minHeight: "100vh"
      }}
    >

      <div className="text-center py-4 border-bottom">

        <FaShieldAlt
          size={45}
          className="text-info mb-2"
        />

        <h4>
          AI IDS
        </h4>

        <small className="text-secondary">
          Intrusion Detection System
        </small>

      </div>

      <ul className="nav flex-column p-3">

        <li className="nav-item mb-2">

          <Link
            className="nav-link text-white"
            to="/dashboard"
          >

            <FaChartPie className="me-2" />

            Dashboard

          </Link>

        </li>

        <li className="nav-item mb-2">

          <Link
            className="nav-link text-white"
            to="/prediction"
          >

            <FaRobot className="me-2" />

            AI Prediction

          </Link>

        </li>


        <li className="nav-item mb-2">

          <Link
            className="nav-link text-white"
            to="/live"
          >

            <FaBroadcastTower className="me-2" />

            Live Monitoring

          </Link>

        </li>

        <li className="nav-item mb-2">

          <Link
            className="nav-link text-white"
            to="/reports"
          >

            <FaFileAlt className="me-2" />

            Reports

          </Link>

        </li>

      </ul>

      <div className="mt-auto p-3">

        <button
          onClick={logout}
          className="btn btn-danger w-100"
        >

          <FaSignOutAlt className="me-2" />

          Logout

        </button>

      </div>

    </div>

  );

}

export default Sidebar;