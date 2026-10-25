"""Lightweight unit tests for live-flow cleanup behavior."""
import unittest
from datetime import datetime, timedelta

from app.services.flow_tracker import FlowTracker


class FlowTrackerLifecycleTests(unittest.TestCase):
    def test_idle_flow_expires_and_fresh_flow_remains(self):
        tracker = FlowTracker()
        now = datetime(2026, 1, 1, 12, 0, 0)

        tracker.flows["idle-flow"] = {
            "start_time": now - timedelta(seconds=120),
            "last_time": now - timedelta(seconds=45),
        }
        tracker.flows["fresh-flow"] = {
            "start_time": now - timedelta(seconds=10),
            "last_time": now - timedelta(seconds=2),
        }

        expired = tracker.expire_stale_flows(
            now=now,
            idle_timeout_seconds=30,
            max_age_seconds=300,
        )

        self.assertEqual(expired, ["idle-flow"])
        self.assertNotIn("idle-flow", tracker.flows)
        self.assertIn("fresh-flow", tracker.flows)

    def test_maximum_age_expires_active_flow(self):
        tracker = FlowTracker()
        now = datetime(2026, 1, 1, 12, 0, 0)

        tracker.flows["old-flow"] = {
            "start_time": now - timedelta(seconds=301),
            "last_time": now - timedelta(seconds=1),
        }

        expired = tracker.expire_stale_flows(
            now=now,
            idle_timeout_seconds=60,
            max_age_seconds=300,
        )

        self.assertEqual(expired, ["old-flow"])
        self.assertEqual(len(tracker.flows), 0)

    def test_clear_removes_all_flows(self):
        tracker = FlowTracker()
        tracker.flows["one"] = {"start_time": None, "last_time": None}
        tracker.flows["two"] = {"start_time": None, "last_time": None}

        tracker.clear()

        self.assertEqual(len(tracker.flows), 0)


if __name__ == "__main__":
    unittest.main()
