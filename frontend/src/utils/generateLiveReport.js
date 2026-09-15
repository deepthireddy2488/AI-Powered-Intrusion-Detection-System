import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";

export default function generateLiveReport(logs) {
    if (!logs || logs.length === 0) {
        return;
    }

    const doc = new jsPDF();

    const totalRecords = logs.length;

    const safeTraffic = logs.filter(
        (log) => log.attack_type === "BENIGN"
    ).length;

    const attacksDetected = logs.filter(
        (log) => log.attack_type !== "BENIGN"
    ).length;

    const attackCounts = {};

    logs.forEach((log) => {
        if (log.attack_type !== "BENIGN") {
            attackCounts[log.attack_type] =
                (attackCounts[log.attack_type] || 0) + 1;
        }
    });

    const highestAttack =
        Object.keys(attackCounts).length > 0
            ? Object.keys(attackCounts).reduce(
                (a, b) =>
                    attackCounts[a] > attackCounts[b]
                        ? a
                        : b
            )
            : "None";

    doc.setFontSize(18);
    doc.text(
        "AI-Powered Intrusion Detection System",
        14,
        20
    );

    doc.setFontSize(13);
    doc.text(
        "Live Monitoring Report",
        14,
        30
    );

    doc.setFontSize(10);
    doc.text(
        "Generated: " + new Date().toLocaleString(),
        14,
        38
    );

    doc.setFontSize(12);

    doc.text(
        `Total Records : ${totalRecords}`,
        14,
        52
    );

    doc.text(
        `Safe Traffic : ${safeTraffic}`,
        14,
        60
    );

    doc.text(
        `Attacks Detected : ${attacksDetected}`,
        14,
        68
    );

    doc.text(
        `Highest Attack : ${highestAttack}`,
        14,
        76
    );

    autoTable(doc, {
        startY: 88,

        head: [[
            "ID",
            "Time",
            "Attack",
            "Source IP",
            "Destination IP",
            "Severity",
            "Status"
        ]],

        body: logs.map((log) => [
            log.id,

            log.created_at
                ? new Date(log.created_at).toLocaleString()
                : "-",

            log.attack_type || "-",

            log.source_ip || "-",

            log.destination_ip || "-",

            log.severity || "-",

            log.attack_type === "BENIGN"
                ? "Normal"
                : "Threat Detected"
        ]),

        styles: {
            fontSize: 7
        },

        headStyles: {
            fontSize: 8
        }
    });

    doc.save(
        "AI_IDS_Live_Monitoring_Report.pdf"
    );
}