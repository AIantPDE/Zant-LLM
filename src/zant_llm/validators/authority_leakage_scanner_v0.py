from zant_llm.governance import forbidden_fields_in_output
AUTHORITY = {"runtime_authority", "runtime_authority_granted", "provider_dispatch", "worker_trigger", "writeback_execution", "route_decision", "fetch_decision", "new_decision"}

def validate_authority_leakage(explanation: dict) -> dict:
    leaked = sorted(set(forbidden_fields_in_output(explanation)) & AUTHORITY)
    return {"validator":"AuthorityLeakageScannerV0", "passed": not leaked, "leaked_fields": leaked}
