import {
    PieChart,
    Pie,
    Cell,
    Tooltip,
    Legend,
    ResponsiveContainer,
    BarChart,
    Bar,
    XAxis,
    YAxis,
    CartesianGrid
} from "recharts";


function DashboardCharts({ attackLogs }) {


    // ================================
    // SAFE VS ATTACK
    // ================================

    const safeTraffic = attackLogs.filter(
        (log) => log.attack_type === "BENIGN"
    ).length;


    const attacksDetected = attackLogs.filter(
        (log) => log.attack_type !== "BENIGN"
    ).length;


    const pieData = [
        {
            name: "Safe",
            value: safeTraffic
        },
        {
            name: "Attacks",
            value: attacksDetected
        }
    ];


    // ================================
    // ATTACK DISTRIBUTION
    // ================================

    const attackCounts = {};


    attackLogs.forEach((log) => {

        if (log.attack_type !== "BENIGN") {

            attackCounts[log.attack_type] =
                (attackCounts[log.attack_type] || 0) + 1;

        }

    });


    const barData = Object.entries(
        attackCounts
    ).map(([attack, count]) => ({
        attack,
        count
    }));



    const COLORS = [
        "#198754",
        "#dc3545"
    ];



    return (

        <div className="row mt-4">


            {/* ================================
                SAFE VS ATTACK
            ================================= */}

            <div className="col-md-6 mb-4">

                <div className="card shadow h-100">

                    <div className="card-body">

                        <h5 className="text-center mb-3">
                            Safe vs Attack Traffic
                        </h5>


                        {attackLogs.length === 0 ? (

                            <div className="text-center text-muted mt-5">

                                No traffic data available

                            </div>

                        ) : (

                            <ResponsiveContainer
                                width="100%"
                                height={300}
                            >

                                <PieChart>

                                    <Pie
                                        data={pieData}
                                        dataKey="value"
                                        nameKey="name"
                                        outerRadius={100}
                                        label
                                    >

                                        {pieData.map(
                                            (entry, index) => (

                                                <Cell
                                                    key={index}
                                                    fill={COLORS[index]}
                                                />

                                            )
                                        )}

                                    </Pie>


                                    <Tooltip />

                                    <Legend />

                                </PieChart>

                            </ResponsiveContainer>

                        )}

                    </div>

                </div>

            </div>



            {/* ================================
                ATTACK DISTRIBUTION
            ================================= */}

            <div className="col-md-6 mb-4">

                <div className="card shadow h-100">

                    <div className="card-body">

                        <h5 className="text-center mb-3">
                            Attack Distribution
                        </h5>


                        {barData.length === 0 ? (

                            <div className="text-center text-muted mt-5">

                                No attacks detected

                            </div>

                        ) : (

                            <ResponsiveContainer
                                width="100%"
                                height={300}
                            >

                                <BarChart data={barData}>

                                    <CartesianGrid
                                        strokeDasharray="3 3"
                                    />

                                    <XAxis
                                        dataKey="attack"
                                    />

                                    <YAxis />

                                    <Tooltip />

                                    <Legend />

                                    <Bar
                                        dataKey="count"
                                        fill="#0d6efd"
                                    />

                                </BarChart>

                            </ResponsiveContainer>

                        )}

                    </div>

                </div>

            </div>


        </div>

    );

}


export default DashboardCharts;