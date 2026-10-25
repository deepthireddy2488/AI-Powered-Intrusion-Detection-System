import { NavLink, useNavigate } from "react-router-dom";
import "./Sidebar.css";
import {
    FaBroadcastTower,
    FaChartPie,
    FaFileAlt,
    FaProjectDiagram,
    FaRobot,
    FaShieldAlt,
    FaSignOutAlt,
    FaStream,
} from "react-icons/fa";

function Sidebar() {
    const navigate = useNavigate();

    const logout = () => {
        localStorage.removeItem("access_token");
        localStorage.removeItem("token"); // cleanup for older local builds
        sessionStorage.removeItem("currentAnalysisSessionId");
        sessionStorage.removeItem("liveMonitoringSessionId");
        navigate("/login", { replace: true });
    };

    const navClass = ({ isActive }) => `ids-side-link${isActive ? " active" : ""}`;

    return (
        <aside className="ids-sidebar">
            <div className="ids-sidebar-brand">
                <div className="ids-brand-mark"><FaShieldAlt /></div>
                <div className="ids-brand-title">AI <span>IDS</span></div>
                <div className="ids-brand-caption">INTRUSION DETECTION SYSTEM</div>
            </div>

            <div className="ids-sidebar-section-label">WORKSPACE</div>
            <nav className="ids-side-nav" aria-label="Main navigation">
                <NavLink to="/dashboard" className={navClass}><FaChartPie /><span>Dashboard</span></NavLink>
                <NavLink to="/prediction" className={navClass}><FaRobot /><span>AI Prediction</span></NavLink>
                <NavLink to="/live" className={navClass}><FaBroadcastTower /><span>Live Monitoring</span></NavLink>
                <NavLink to="/reports" className={navClass}><FaFileAlt /><span>Security Reports</span></NavLink>
                <NavLink to="/timeline" className={navClass}><FaStream /><span>Threat Timeline</span><span className="ids-nav-new">NEW</span></NavLink>
            </nav>

            <div className="ids-sidebar-bottom">
                <div className="ids-sidebar-status"><span /> SESSION-AWARE MONITORING</div>
                <button type="button" onClick={logout} className="ids-logout-button">
                    <FaSignOutAlt /><span>Sign out</span>
                </button>
                <div className="ids-sidebar-version"><FaProjectDiagram /> AI · ML · NETWORK SECURITY</div>
            </div>
        </aside>
    );
}

export default Sidebar;