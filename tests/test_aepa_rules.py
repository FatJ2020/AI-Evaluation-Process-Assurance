import unittest
from src.aepa_rules import detect_flags, severity_band, recommend, evaluate_session


class AepaRulesTests(unittest.TestCase):
    def test_clean_session_accept(self):
        session = {
            "session_id": "T1",
            "task_family": "tts_elo",
            "format": "pairwise",
            "n_pairs": 2,
            "preferred_side": "A",
            "position_swap_done": True,
            "length_controlled": True,
            "preference_correlated_with_length": False,
            "longer_always_preferred": False,
            "hard_fault_present": False,
            "hard_fault_tagged": True,
            "uses_gate": False,
            "gate_fpr_fnr_reviewed": True,
            "spec_version_clear": True,
            "spec_versions_seen": ["v1"],
            "subjective_dimensions": True,
            "agreement_measured": True,
            "gold_check_present": True,
            "artifact_verified": True,
        }
        result = evaluate_session(session)
        self.assertEqual(result["severity"], "L")
        self.assertEqual(result["recommendation"], "ACCEPT")
        self.assertEqual(result["flags"], "none")

    def test_gate_unstable_hold_or_review(self):
        session = {
            "session_id": "T2",
            "task_family": "diar_gate",
            "format": "gate",
            "uses_gate": True,
            "gate_fpr_fnr_reviewed": False,
            "spec_version_clear": True,
            "spec_versions_seen": ["v4"],
            "hard_fault_present": False,
            "hard_fault_tagged": True,
            "subjective_dimensions": False,
            "agreement_measured": True,
            "gold_check_present": True,
            "artifact_verified": True,
            "position_swap_done": True,
            "length_controlled": True,
        }
        flags = detect_flags(session)
        self.assertIn("gate_threshold_unstable", flags)
        self.assertEqual(severity_band(flags), "H")
        self.assertEqual(recommend(flags, "H"), "HOLD_BATCH")

    def test_artifact_not_verified_high(self):
        session = {
            "session_id": "T3",
            "task_family": "agent",
            "format": "pairwise",
            "artifact_verified": False,
            "position_swap_done": True,
            "n_pairs": 1,
            "length_controlled": True,
            "hard_fault_present": False,
            "hard_fault_tagged": True,
            "uses_gate": False,
            "gate_fpr_fnr_reviewed": True,
            "spec_version_clear": True,
            "spec_versions_seen": ["v1"],
            "subjective_dimensions": False,
            "agreement_measured": True,
            "gold_check_present": True,
        }
        flags = detect_flags(session)
        self.assertIn("artifact_not_verified", flags)
        self.assertEqual(severity_band(flags), "H")


if __name__ == "__main__":
    unittest.main()
