import {
    FaChartLine,
    FaBug,
    FaCheckCircle,
    FaServer
} from "react-icons/fa";

function StatCard({ title, value, color }) {

    let icon;

    switch (title) {

        case "Total Records":
        case "Total Scans":
            icon = <FaChartLine size={35} />;
            break;

        case "Attacks Detected":
        case "Attacks":
            icon = <FaBug size={35} />;
            break;

        case "Safe Traffic":
            icon = <FaCheckCircle size={35} />;
            break;

        default:
            icon = <FaServer size={35} />;
    }

    return (

        <div className="card shadow border-0 h-100">

            <div className="card-body">

                <div className="d-flex justify-content-between align-items-center">

                    <div>

                        <h6 className="text-muted">
                            {title}
                        </h6>

                        <h2 className={`text-${color} fw-bold`}>
                            {value}
                        </h2>

                    </div>

                    <div className={`text-${color}`}>
                        {icon}
                    </div>

                </div>

            </div>

        </div>

    );
}

export default StatCard;