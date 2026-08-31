import { useEffect, useState } from "react";

function AlertTable() {

    const [attackLogs, setAttackLogs] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {

        fetch("http://127.0.0.1:8000/attack-logs/")
            .then((response) => {

                if (!response.ok) {
                    throw new Error("Failed to fetch attack logs");
                }

                return response.json();

            })
            .then((data) => {

                setAttackLogs(data);
                setLoading(false);

            })
            .catch((error) => {

                console.error("Error fetching attack logs:", error);
                setLoading(false);

            });

    }, []);

    return (

        <div className="card shadow mt-4">

            <div className="card-header bg-dark text-white">
                🚨 Recent Security Alerts
            </div>

            <div className="card-body">

                {loading ? (

                    <div className="text-center text-muted p-4">
                        Loading attack logs...
                    </div>

                ) : attackLogs.length === 0 ? (

                    <div className="text-center text-muted p-4">
                        No attack logs available.
                    </div>

                ) : (

                    <div className="table-responsive">

                        <table className="table table-hover">

                            <thead>

                                <tr>
                                    <th>ID</th>
                                    <th>Attack Type</th>
                                    <th>Source IP</th>
                                    <th>Destination IP</th>
                                    <th>Severity</th>
                                    <th>Status</th>
                                    <th>Time</th>
                                </tr>

                            </thead>

                            <tbody>

                                {attackLogs.map((item) => (

                                    <tr key={item.id}>

                                        <td>
                                            {item.id}
                                        </td>

                                        <td>
                                            {item.attack_type}
                                        </td>

                                        <td>
                                            {item.source_ip}
                                        </td>

                                        <td>
                                            {item.destination_ip}
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
                                            {item.status}
                                        </td>

                                        <td>
                                            {new Date(
                                                item.created_at
                                            ).toLocaleString()}
                                        </td>

                                    </tr>

                                ))}

                            </tbody>

                        </table>

                    </div>

                )}

            </div>

        </div>

    );
}

export default AlertTable;