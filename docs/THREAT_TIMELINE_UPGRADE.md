# IDS reliability + Threat Investigation Timeline upgrade

This is an **incremental overlay** for the existing `AI-Powered-Intrusion-Detection-System` project. It is not a standalone application. Copy the files into the matching paths in your existing repository; do not replace the whole project with this bundle.

## What this upgrade adds

- A black-and-yellow Threat Investigation Timeline page, available at `/timeline` and `/timeline/<session_id>`.
- Session picker for the signed-in user's CSV and live analysis sessions.
- Server-side filtering by attack type, severity, threats-only, and IP address for live sessions.
- Paginated events (50 per request, load-more support) so the UI does not request every timeline event at once.
- Event detail panel for timestamp, attack type, severity, confidence, status, IPs, ports, protocol, packet count and recommendation where the underlying record has those fields.
- Aggregate totals calculated by the backend across all records matching the current filters, not just the currently loaded page.
- Additive PostgreSQL migration for extra live-event evidence columns and CSV row number.
- Better flow lifecycle handling: flow inactivity / maximum-age expiration, reset per monitoring run, and bounded flow-window size.
- Synchronous capture stop behavior using Scapy `AsyncSniffer`, including the no-new-packets case.
- Shared feature-name-safe ML inference for CSV and live traffic, avoiding the scikit-learn warning caused by passing an unnamed list into a model trained with feature names.
- Live session stop/start wiring and logout cleanup for current-session selection.

## Files included

### Backend replacements / additions

- `backend/app/api/analysis_sessions.py`
- `backend/app/api/live_capture.py`
- `backend/app/api/prediction.py`
- `backend/app/main.py`
- `backend/app/ml/prediction.py`
- `backend/app/models/analysis_session.py`
- `backend/app/models/attack_log.py`
- `backend/app/models/prediction.py`
- `backend/app/repositories/analysis_session_repository.py`
- `backend/app/repositories/attack_log_repository.py`
- `backend/app/repositories/prediction_repository.py`
- `backend/app/services/live_capture.py`
- `backend/app/services/flow_tracker.py`
- `backend/app/services/prediction.py`
- `backend/migrations/20261025_threat_timeline.sql`

### Frontend replacements / additions

- `frontend/src/App.jsx`
- `frontend/src/components/Sidebar.jsx`
- `frontend/src/components/Sidebar.css`
- `frontend/src/pages/LiveMonitoring.jsx`
- `frontend/src/pages/ThreatTimeline.jsx`
- `frontend/src/pages/ThreatTimeline.css`

This bundle intentionally does **not** include `.env`, trained `.pkl`/`.joblib` model files, `node_modules`, or `venv`.

## Installation steps

1. **Back up first.** Commit your current code or copy the project folder. Back up the PostgreSQL database through pgAdmin.
2. Copy the included `backend` and `frontend` directories over the same paths in your existing repository. Allow overwriting only the files listed above. Do not copy an `.env` file from anywhere; keep your existing local backend `.env` private.
3. Open pgAdmin Query Tool for the **same database configured in your existing backend `.env`** and execute the SQL in `backend/migrations/20261025_threat_timeline.sql`. The migration uses additive `CREATE TABLE IF NOT EXISTS` / `ADD COLUMN IF NOT EXISTS` statements and does not delete application records.
4. Restart the FastAPI backend with your usual command.
5. Start or refresh the React frontend with your usual command. The Sidebar should show **Threat Timeline**.
6. Log in, select a CSV or live session, and open Threat Timeline. For live sessions, start monitoring in a separate tab if you want to watch events refresh while the session is running.

## Existing Dashboard session-storage check

The existing `Prediction.jsx` should set the current dashboard session after a successful CSV upload. Immediately after the existing `setResult(data);` line, confirm this is present; add it if missing:

```jsx
if (data.session_id) {
    sessionStorage.setItem("currentAnalysisSessionId", data.session_id);
}
sessionStorage.removeItem("liveMonitoringSessionId");
```

The successful Login handler should clear the previous user's browser-only session selection before saving the new token. Add this if it is missing:

```jsx
sessionStorage.removeItem("currentAnalysisSessionId");
sessionStorage.removeItem("liveMonitoringSessionId");
```

Do not clear `currentAnalysisSessionId` when Live Monitoring stops: the Dashboard should retain the just-completed live session until a new CSV or live session is selected.

## API additions / behavior

- `GET /analysis-sessions/` — only the signed-in user's session list.
- `GET /analysis-sessions/{session_id}` — that user's one-session report details.
- `GET /analysis-sessions/{session_id}/timeline?limit=50&offset=0` — paginated events and server-side totals.
- Optional query parameters: `severity`, `attack_type`, `ip_address`, `threats_only`.
- IP filtering is intentionally supported for live sessions only because CSV prediction rows do not currently persist source/destination IP addresses in the `predictions` table.

All session endpoints verify session ownership using the authenticated user. A session ID is not treated as authorization by itself.

## Test checklist

1. Run the backend and check `/docs` loads without import errors.
2. Run a small known-good CSV upload. Confirm it creates one CSV session, and the report details page works.
3. Open `/timeline/<that-session-id>`. Confirm CSV rows are shown with row numbers, model labels, severity and confidence. IP search should be disabled for CSV sessions.
4. Start live monitoring and generate normal traffic. Confirm Scapy logs packets and predictions only appear when each flow window reaches the configured prediction checkpoint.
5. Stop monitoring while traffic is quiet. Confirm the stop request returns and the session receives a completion timestamp.
6. Open the live timeline. Confirm source/destination IP, ports, protocol, packet count, confidence, and recommendation appear when present.
7. Filter by attack type, severity and IP. Confirm event results and aggregate totals update.
8. Sign in as a different user and try opening another user's session ID. The endpoint should return 404 rather than leaking their events.
9. Start a second live run. Confirm it starts with fresh flow state and the new session does not contain events from the previous run.

## Important limitations

- The live classifier is a supervised model trained on the features available in its training dataset. It is not proof of malicious intent and cannot promise detection of every unknown / zero-day attack.
- Live packet capture only sees traffic visible to the host/interface. Monitoring other machines requires a permitted capture point such as a mirrored switch port or gateway sensor.
- `AsyncSniffer`, Windows Npcap availability and capture permissions remain platform-dependent.
- This is a local academic/prototype application. Module-level capture state is not a multi-worker production design; a deployed production system should move capture into a dedicated worker/service and add monitoring, authorization hardening and deployment tests.
- The upgrade's Python source was syntax-compiled and the new JSX/JS files were parsed. A full Vite build could not be verified in this environment because the uploaded `node_modules` snapshot contains Windows Rolldown binaries, not the Linux native binding. Run `npm run build` on your Windows project after copying the files.
