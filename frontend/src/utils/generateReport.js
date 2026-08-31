import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";

export default function generateReport(data) {

    const doc = new jsPDF();

    doc.setFontSize(18);
    doc.text("AI-Powered Intrusion Detection System", 14, 20);

    doc.setFontSize(12);
    doc.text("Prediction Report", 14, 30);

    doc.text(
        "Generated: " + new Date().toLocaleString(),
        14,
        38
    );

    doc.setFontSize(13);

    doc.text(
        `Total Records : ${data.total_records}`,
        14,
        52
    );

    doc.text(
        `Safe Traffic : ${data.safe_traffic}`,
        14,
        60
    );

    doc.text(
        `Attacks Detected : ${data.attacks_detected}`,
        14,
        68
    );

    doc.text(
        `Highest Attack : ${data.highest_attack}`,
        14,
        76
    );

    autoTable(doc, {

        startY: 88,

        head: [[
            "Row",
            "Attack",
            "Severity",
            "Recommendation"
        ]],

        body: data.results.map(item => [

            item.row,
            item.attack,
            item.severity,
            item.recommendation

        ])

    });

    doc.save("AI_IDS_Report.pdf");

}