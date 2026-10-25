import { useCallback, useEffect, useMemo, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import {
    FaBolt,
    FaCheckCircle,
    FaChevronDown,
    FaChevronRight,
    FaCircle,
    FaClock,
    FaFilter,
    FaGlobe,
    FaHeartbeat,
    FaNetworkWired,
    FaRedoAlt,
    FaSearch,
    FaShieldAlt,
    FaSkullCrossbones,
    FaStream,
    FaTimesCircle,
} from "react-icons/fa";

import api from "../services/api";
import "./ThreatTimeline.css";

const PAGE_SIZE = 50;

function asDate(value) {
    if (!value) return null;
    const date = new Date(value);
    return Number.isNaN(date.getTime()) ? null : date;
}

function formatTime(value) {
    const date = asDate(value);
    return date ? date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" }) : "Time unavailable";
}

function formatDate(value) {
    const date = asDate(value);
    return date ? date.toLocaleString() : "—";
}

function severityClass(value) {
    const severity = String(value || "unknown").toLowerCase();
    if (severity.includes("critical")) return "critical";
    if (severity.includes("high")) return "high";
    if (severity.includes("medium")) return "medium";
    if (severity.includes("low")) return "low";
    return "unknown";
}

function MetricCard({ label, value, icon, kind = "default" }) {
    return (
        <div className={`threat-metric threat-metric-${kind}`}>
            <div className="threat-metric-icon">{icon}</div>
            <div>
                <div className="threat-metric-label">{label}</div>
                <div className="threat-metric-value">{value}</div>
            </div>
        </div>
    );
}

function ThreatTimeline() {
    const { sessionId } = useParams();
    const navigate = useNavigate();

    const [sessions, setSessions] = useState([]);
    const [sessionsLoading, setSessionsLoading] = useState(true);
    const [sessionsError, setSessionsError] = useState("");

    const [events, setEvents] = useState([]);
    const [total, setTotal] = useState(0);
    const [summary, setSummary] = useState({ total: 0, threats: 0, benign: 0, critical: 0 });
    const [timelineLoading, setTimelineLoading] = useState(false);
    const [timelineError, setTimelineError] = useState("");
    const [selectedEventId, setSelectedEventId] = useState(null);

    const [draftAttack, setDraftAttack] = useState("");
    const [draftIp, setDraftIp] = useState("");
    const [draftSeverity, setDraftSeverity] = useState("");
    const [draftThreatsOnly, setDraftThreatsOnly] = useState(false);
    const [filters, setFilters] = useState({ attackType: "", ipAddress: "", severity: "", threatsOnly: false });

    const selectedSession = useMemo(
        () => sessions.find((session) => session.session_id === sessionId) || null,
        [sessions, sessionId]
    );

    // Load the user's available sessions. The endpoint enforces ownership server-side.
    useEffect(() => {
        let cancelled = false;

        const loadSessions = async () => {
            setSessionsLoading(true);
            setSessionsError("");
            try {
                const response = await api.get("/analysis-sessions/");
                if (cancelled) return;
                const rows = Array.isArray(response.data) ? response.data : [];
                setSessions(rows);

                if (!sessionId && rows.length > 0) {
                    navigate(`/timeline/${rows[0].session_id}`, { replace: true });
                }
            } catch (error) {
                if (cancelled) return;
                setSessionsError(
                    error.response?.data?.detail || "Could not load analysis sessions."
                );
            } finally {
                if (!cancelled) setSessionsLoading(false);
            }
        };

        loadSessions();
        return () => { cancelled = true; };
    }, [navigate, sessionId]);

    const loadTimeline = useCallback(async (offset = 0, append = false) => {
        if (!sessionId) {
            setEvents([]);
            setTotal(0);
            setSummary({ total: 0, threats: 0, benign: 0, critical: 0 });
            return;
        }

        setTimelineLoading(true);
        setTimelineError("");
        try {
            const response = await api.get(
                `/analysis-sessions/${sessionId}/timeline`,
                {
                    params: {
                        limit: PAGE_SIZE,
                        offset,
                        severity: filters.severity || undefined,
                        attack_type: filters.attackType.trim() || undefined,
                        ip_address: filters.ipAddress.trim() || undefined,
                        threats_only: filters.threatsOnly,
                    },
                }
            );

            const newEvents = Array.isArray(response.data.events)
                ? response.data.events
                : [];
            setTotal(Number(response.data.total || 0));
            setSummary(response.data.summary || { total: Number(response.data.total || 0), threats: 0, benign: 0, critical: 0 });
            setEvents((previous) => append ? [...previous, ...newEvents] : newEvents);
            if (!append) {
                setSelectedEventId((previousId) =>
                    newEvents.some((event) => event.event_id === previousId)
                        ? previousId
                        : (newEvents[0]?.event_id || null)
                );
            }
        } catch (error) {
            setTimelineError(
                error.response?.data?.detail || "Could not load the threat timeline."
            );
            if (!append) {
                setEvents([]);
                setTotal(0);
                setSummary({ total: 0, threats: 0, benign: 0, critical: 0 });
            }
        } finally {
            setTimelineLoading(false);
        }
    }, [filters, sessionId]);

    useEffect(() => {
        loadTimeline(0, false);
    }, [loadTimeline]);

    // Keep a currently running LIVE session fresh; completed sessions remain historical.
    useEffect(() => {
        if (!selectedSession || selectedSession.source_type !== "LIVE" || selectedSession.completed_at) {
            return undefined;
        }
        const timer = setInterval(() => loadTimeline(0, false), 5000);
        return () => clearInterval(timer);
    }, [loadTimeline, selectedSession]);

    const selectedEvent = useMemo(
        () => events.find((event) => event.event_id === selectedEventId) || events[0] || null,
        [events, selectedEventId]
    );

    // Server-side aggregates cover every matching record, not just the 50 loaded rows.
    const totals = summary;

    const applyFilters = (event) => {
        event.preventDefault();
        setFilters({
            attackType: draftAttack,
            ipAddress: draftIp,
            severity: draftSeverity,
            threatsOnly: draftThreatsOnly,
        });
    };

    const chooseSession = (event) => {
        const value = event.target.value;
        if (!value) return;
        // Filters are session-specific; don't carry a live IP search into a CSV run.
        setDraftAttack("");
        setDraftIp("");
        setDraftSeverity("");
        setDraftThreatsOnly(false);
        setFilters({ attackType: "", ipAddress: "", severity: "", threatsOnly: false });
        navigate(`/timeline/${value}`);
    };

    const hasMore = events.length < total;
    const activeSession = selectedSession?.source_type === "LIVE" && !selectedSession?.completed_at;

    if (sessionsLoading && sessions.length === 0) {
        return (
            <div className="threat-timeline-page">
                <div className="threat-page-loading"><span className="threat-spinner" /> Loading investigation workspace…</div>
            </div>
        );
    }

    return (
        <main className="threat-timeline-page">
            <div className="threat-page-shell">
                <header className="threat-hero">
                    <div className="threat-hero-glow" aria-hidden="true" />
                    <div className="threat-hero-content">
                        <div className="threat-eyebrow"><FaShieldAlt /> SECURITY OPERATIONS <span /> INVESTIGATION VIEW</div>
                        <div className="threat-hero-row">
                            <div>
                                <h1>Threat <em>Timeline</em></h1>
                                <p>Trace detections, inspect flow evidence, and review what the IDS observed in each analysis session.</p>
                            </div>
                            <div className={`threat-live-state ${activeSession ? "is-live" : "is-complete"}`}>
                                <FaCircle /> {activeSession ? "LIVE SESSION" : "SESSION HISTORY"}
                            </div>
                        </div>
                        <div className="threat-session-control">
                            <label htmlFor="threat-session-select">ANALYSIS SESSION</label>
                            <div className="threat-select-wrap">
                                <select
                                    id="threat-session-select"
                                    value={sessionId || ""}
                                    onChange={chooseSession}
                                    disabled={sessions.length === 0}
                                >
                                    {sessions.length === 0 && <option value="">No sessions available</option>}
                                    {sessions.map((session) => (
                                        <option key={session.session_id} value={session.session_id}>
                                            {(session.source_type === "CSV" ? "CSV" : "LIVE") + " · " + (session.name || "Analysis") + " · " + formatDate(session.created_at)}
                                        </option>
                                    ))}
                                </select>
                                <FaChevronDown />
                            </div>
                            {selectedSession && (
                                <div className="threat-session-meta">
                                    <span>{selectedSession.source_type === "CSV" ? "CSV ANALYSIS" : "LIVE MONITORING"}</span>
                                    <span>Started {formatDate(selectedSession.created_at)}</span>
                                    <span>{selectedSession.completed_at ? `Completed ${formatDate(selectedSession.completed_at)}` : "Not marked complete"}</span>
                                </div>
                            )}
                        </div>
                    </div>
                </header>

                {sessionsError && <div className="threat-error"><FaTimesCircle /> {sessionsError}</div>}
                {timelineError && <div className="threat-error"><FaTimesCircle /> {timelineError}</div>}

                {!sessionsLoading && sessions.length === 0 ? (
                    <section className="threat-empty-state">
                        <FaStream />
                        <h2>No analysis sessions yet</h2>
                        <p>Run a CSV prediction or start live monitoring. Each run will appear here as a separate investigation timeline.</p>
                    </section>
                ) : (
                    <>
                        <section className="threat-metrics-grid">
                            <MetricCard label="MATCHING EVENTS" value={totals.total} icon={<FaStream />} />
                            <MetricCard label="THREATS MATCHING FILTER" value={totals.threats} icon={<FaSkullCrossbones />} kind="danger" />
                            <MetricCard label="BENIGN MATCHING FILTER" value={totals.benign} icon={<FaCheckCircle />} kind="safe" />
                            <MetricCard label="CRITICAL MATCHING FILTER" value={totals.critical} icon={<FaBolt />} kind="critical" />
                        </section>

                        <section className="threat-filter-panel">
                            <div className="threat-panel-title"><FaFilter /> <span>Filter investigation</span><small>SERVER-SIDE FILTERS</small></div>
                            <form className="threat-filter-form" onSubmit={applyFilters}>
                                <label className="threat-search-field">
                                    <span>ATTACK TYPE</span>
                                    <div><FaSearch /><input value={draftAttack} onChange={(e) => setDraftAttack(e.target.value)} placeholder="Search attack label…" maxLength={100} /></div>
                                </label>
                                <label className="threat-search-field">
                                    <span>IP ADDRESS</span>
                                    <div><FaGlobe /><input value={draftIp} onChange={(e) => setDraftIp(e.target.value)} placeholder={selectedSession?.source_type === "CSV" ? "Unavailable for CSV rows" : "Search source/destination IP…"} maxLength={100} disabled={selectedSession?.source_type === "CSV"} /></div>
                                </label>
                                <label className="threat-search-field">
                                    <span>SEVERITY</span>
                                    <div className="threat-select-wrap">
                                        <select value={draftSeverity} onChange={(e) => setDraftSeverity(e.target.value)}>
                                            <option value="">All severities</option>
                                            <option value="Critical">Critical</option>
                                            <option value="High">High</option>
                                            <option value="Medium">Medium</option>
                                            <option value="Low">Low</option>
                                        </select>
                                        <FaChevronDown />
                                    </div>
                                </label>
                                <label className="threat-check-field">
                                    <input type="checkbox" checked={draftThreatsOnly} onChange={(e) => setDraftThreatsOnly(e.target.checked)} />
                                    <span>Threats only</span>
                                </label>
                                <button className="threat-button threat-button-primary" type="submit"><FaFilter /> Apply filters</button>
                                <button className="threat-button threat-button-ghost" type="button" onClick={() => { setDraftAttack(""); setDraftIp(""); setDraftSeverity(""); setDraftThreatsOnly(false); setFilters({ attackType: "", ipAddress: "", severity: "", threatsOnly: false }); }}><FaTimesCircle /> Reset</button>
                            </form>
                        </section>

                        <div className="threat-content-grid">
                            <section className="threat-events-panel">
                                <div className="threat-panel-header">
                                    <div><FaClock /><div><h2>Event stream</h2><p>{total.toLocaleString()} matching records in this session</p></div></div>
                                    <button className="threat-icon-button" type="button" onClick={() => loadTimeline(0, false)} title="Refresh timeline" disabled={timelineLoading}><FaRedoAlt className={timelineLoading ? "threat-spin-icon" : ""} /></button>
                                </div>

                                {timelineLoading && events.length === 0 ? (
                                    <div className="threat-panel-loading"><span className="threat-spinner" /> Loading session events…</div>
                                ) : events.length === 0 ? (
                                    <div className="threat-empty-events"><FaHeartbeat /><strong>No events match these filters</strong><span>Try a different attack type or reset the filters.</span></div>
                                ) : (
                                    <div className="threat-event-list">
                                        {events.map((event, index) => (
                                            <button
                                                type="button"
                                                key={event.event_id}
                                                className={`threat-event ${selectedEvent?.event_id === event.event_id ? "is-selected" : ""} ${event.is_threat ? "is-threat" : "is-benign"}`}
                                                onClick={() => setSelectedEventId(event.event_id)}
                                            >
                                                <div className="threat-event-rail"><span className="threat-event-dot">{event.is_threat ? <FaBolt /> : <FaCheckCircle />}</span>{index !== events.length - 1 && <span className="threat-event-line" />}</div>
                                                <div className="threat-event-body">
                                                    <div className="threat-event-topline"><span className="threat-event-time">{formatTime(event.timestamp)}</span><span className={`threat-severity severity-${severityClass(event.severity)}`}>{event.severity || "Unknown"}</span></div>
                                                    <h3>{event.title || event.attack_type || "Unclassified event"}</h3>
                                                    <div className="threat-event-tags"><span>{event.source_type}</span><span>{event.protocol || (event.row_number ? `CSV ROW ${event.row_number}` : "FLOW EVENT")}</span><span>{event.is_threat ? "THREAT" : "BENIGN"}</span></div>
                                                    {event.source_ip && <p className="threat-event-route">{event.source_ip}{event.source_port ? `:${event.source_port}` : ""} <FaChevronRight /> {event.destination_ip || "Unknown destination"}{event.destination_port ? `:${event.destination_port}` : ""}</p>}
                                                </div>
                                                <FaChevronRight className="threat-event-chevron" />
                                            </button>
                                        ))}
                                    </div>
                                )}

                                {hasMore && (
                                    <div className="threat-load-more-wrap">
                                        <button className="threat-button threat-button-ghost" type="button" onClick={() => loadTimeline(events.length, true)} disabled={timelineLoading}>
                                            {timelineLoading ? "Loading…" : `Load more events (${Math.max(total - events.length, 0)} remaining)`}
                                        </button>
                                    </div>
                                )}
                            </section>

                            <aside className="threat-detail-panel">
                                <div className="threat-panel-header"><div><FaNetworkWired /><div><h2>Event evidence</h2><p>Selected record details</p></div></div></div>
                                {!selectedEvent ? (
                                    <div className="threat-empty-events"><FaSearch /><strong>Select an event</strong><span>Choose an item in the event stream to inspect its evidence.</span></div>
                                ) : (
                                    <div className="threat-detail-content">
                                        <div className={`threat-detail-banner ${selectedEvent.is_threat ? "banner-threat" : "banner-benign"}`}>
                                            <div className="threat-detail-banner-icon">{selectedEvent.is_threat ? <FaBolt /> : <FaCheckCircle />}</div>
                                            <div><span>{selectedEvent.is_threat ? "DETECTION EVENT" : "BENIGN EVENT"}</span><h3>{selectedEvent.attack_type || "Unknown"}</h3></div>
                                        </div>

                                        <div className="threat-detail-subtitle">EVENT SUMMARY</div>
                                        <div className="threat-detail-grid">
                                            <div><span>Severity</span><strong className={`threat-severity-text severity-text-${severityClass(selectedEvent.severity)}`}>{selectedEvent.severity || "Unknown"}</strong></div>
                                            <div><span>Confidence</span><strong>{selectedEvent.confidence == null ? "—" : `${Number(selectedEvent.confidence).toFixed(2)}%`}</strong></div>
                                            <div><span>Source type</span><strong>{selectedEvent.source_type}</strong></div>
                                            <div><span>Record ID</span><strong>#{selectedEvent.record_id}</strong></div>
                                            <div><span>Timestamp</span><strong>{formatDate(selectedEvent.timestamp)}</strong></div>
                                            <div><span>Status</span><strong>{selectedEvent.status || (selectedEvent.is_threat ? "Detected" : "Normal")}</strong></div>
                                        </div>

                                        <div className="threat-detail-subtitle">NETWORK CONTEXT</div>
                                        <div className="threat-network-card">
                                            {selectedEvent.source_type === "LIVE" ? (
                                                <>
                                                    <div className="threat-network-endpoint"><span>SOURCE</span><strong>{selectedEvent.source_ip || "—"}{selectedEvent.source_port ? `:${selectedEvent.source_port}` : ""}</strong></div>
                                                    <div className="threat-network-arrow"><FaChevronRight /> <span>{selectedEvent.protocol || "Protocol unknown"}</span> <FaChevronRight /></div>
                                                    <div className="threat-network-endpoint"><span>DESTINATION</span><strong>{selectedEvent.destination_ip || "—"}{selectedEvent.destination_port ? `:${selectedEvent.destination_port}` : ""}</strong></div>
                                                    <div className="threat-network-footer"><span>Packets in flow window</span><strong>{selectedEvent.packet_count ?? "—"}</strong></div>
                                                </>
                                            ) : (
                                                <>
                                                    <div className="threat-network-endpoint"><span>INPUT SOURCE</span><strong>Uploaded traffic CSV</strong></div>
                                                    <div className="threat-network-arrow"><FaStream /><span>Model classification</span><FaChevronRight /></div>
                                                    <div className="threat-network-endpoint"><span>CSV RECORD</span><strong>{selectedEvent.row_number ? `Row ${selectedEvent.row_number}` : `Record #${selectedEvent.record_id}`}</strong></div>
                                                    <p className="threat-csv-note">The uploaded dataset row does not contain live source/destination context in the saved prediction record.</p>
                                                </>
                                            )}
                                        </div>

                                        <div className="threat-detail-subtitle">RECOMMENDED ACTION</div>
                                        <div className="threat-recommendation">
                                            <FaShieldAlt />
                                            <p>{selectedEvent.recommendation || (selectedEvent.is_threat ? "Investigate the event and verify supporting network evidence before taking action." : "No action required for a benign classification. Continue monitoring for related signals.")}</p>
                                        </div>
                                        <div className="threat-evidence-footnote">Model output is an investigation signal, not proof by itself. Validate high-impact decisions against relevant logs and network context.</div>
                                    </div>
                                )}
                            </aside>
                        </div>
                    </>
                )}

                <footer className="threat-footer"><span><FaShieldAlt /> AI-POWERED INTRUSION DETECTION</span><span>Session-scoped evidence · User-authenticated access</span></footer>
            </div>
        </main>
    );
}

export default ThreatTimeline;
