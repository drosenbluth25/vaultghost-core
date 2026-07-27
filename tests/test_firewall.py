import unittest
import json
from datetime import datetime, timedelta
from orchestrator import AgentFirewallOrchestrator
from schema_gate import validate_sanitized_payload_schema

class TestAgentFirewall(unittest.TestCase):
    def setUp(self):
        self.orchestrator = AgentFirewallOrchestrator()
        self.valid_envelope = {
            "agent_id": "agent-007",
            "run_id": "run-123",
            "timestamp": datetime.now().isoformat(),
            "input_data": {"query": "Hello"},
            "output_data": {"response": "Hi there"},
            "source_ref": "a" * 40,
            "source_type": "github_commit",
            "artifact_hash": "hash123"
        }

    def test_valid_run(self):
        result = self.orchestrator.process_agent_run(self.valid_envelope)
        self.assertTrue(result["is_valid"])
        self.assertEqual(len([m for m in result["messages"] if m["type"] == "error"]), 0)

    def test_schema_rejection(self):
        invalid_envelope = self.valid_envelope.copy()
        del invalid_envelope["agent_id"]
        result = self.orchestrator.process_agent_run(invalid_envelope)
        self.assertFalse(result["is_valid"])
        self.assertTrue(any("agent_id" in m["text"] for m in result["messages"]))

    def test_policy_violation(self):
        violation_envelope = self.valid_envelope.copy()
        violation_envelope["output_data"] = {"error": "UNAUTHORIZED_ACCESS detected"}
        result = self.orchestrator.process_agent_run(violation_envelope)
        self.assertFalse(result["is_valid"])
        self.assertTrue(any("POLICY_VIOLATION_UNAUTHORIZED" == m.get("code") for m in result["messages"]))

    def test_missing_source_ref(self):
        invalid_envelope = self.valid_envelope.copy()
        del invalid_envelope["source_ref"]
        # Schema validation might catch this if it's required, 
        # but our cross_ref_integrity validator definitely should.
        result = self.orchestrator.process_agent_run(invalid_envelope)
        self.assertFalse(result["is_valid"])
        self.assertTrue(any("MISSING_SOURCE_REF" == m.get("code") for m in result["messages"]))

    def test_source_type_ref_kind_mismatch(self):
        invalid_envelope = self.valid_envelope.copy()
        invalid_envelope["source_type"] = "github_commit"
        invalid_envelope["source_ref"] = "short-sha"
        result = self.orchestrator.process_agent_run(invalid_envelope)
        self.assertFalse(result["is_valid"])
        self.assertTrue(any("INVALID_COMMIT_SHA" == m.get("code") for m in result["messages"]))

    def test_artifact_hash_missing(self):
        invalid_envelope = self.valid_envelope.copy()
        del invalid_envelope["artifact_hash"]
        result = self.orchestrator.process_agent_run(invalid_envelope)
        self.assertFalse(result["is_valid"])
        self.assertTrue(any("MISSING_ARTIFACT_HASH" == m.get("code") for m in result["messages"]))

    def test_legal_escalation(self):
        legal_envelope = self.valid_envelope.copy()
        legal_envelope["output_data"] = {"LEGAL_REVIEW_REQUIRED": True}
        result = self.orchestrator.process_agent_run(legal_envelope)
        self.assertTrue(result["sanitized_payload"]["legal_escalation_required"])

    def test_sanitized_payload_validation(self):
        result = self.orchestrator.process_agent_run(self.valid_envelope)
        sanitized_payload = result["sanitized_payload"]
        # Validate the generated payload against its schema
        schema_res = validate_sanitized_payload_schema(sanitized_payload)
        self.assertTrue(schema_res["is_valid"], f"Sanitized payload schema invalid: {schema_res['messages']}")

if __name__ == '__main__':
    unittest.main()
