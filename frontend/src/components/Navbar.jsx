import { useNavigate } from "react-router-dom";
import {
  FaShieldAlt,
  FaUserCircle,
  FaBell,
  FaCircle
} from "react-icons/fa";

function Navbar() {

  const navigate = useNavigate();

  const fullName = localStorage.getItem("full_name") || "User";

  const logout = () => {

    localStorage.removeItem("access_token");
    localStorage.removeItem("full_name");

    navigate("/");

  };

  return (

    <nav className="navbar navbar-dark bg-dark shadow px-4">

      <span className="navbar-brand fw-bold">

        <FaShieldAlt className="me-2 text-info" />

        AI-Powered Intrusion Detection System

      </span>

      <div className="d-flex align-items-center">

        <span className="text-success me-4">

          <FaCircle
            size={10}
            className="me-2"
          />

          System Online

        </span>

        <FaBell
          className="text-warning me-4"
          size={20}
        />

        <span className="text-white me-4">

          <FaUserCircle
            className="me-2"
          />

          Welcome, {fullName}

        </span>

        <button
          className="btn btn-danger btn-sm"
          onClick={logout}
        >

          Logout

        </button>

      </div>

    </nav>

  );

}

export default Navbar;