# Individual Report: Lab 3 - Chatbot vs ReAct Agent

- **Student Name**: Khong Manh Tuan
- **Student ID**: 2A202600086
- **Date**: 2026-04-06

---

## I. Technical Contribution (15 Points)

I focused on building a reproducible evaluation pipeline to compare a one-shot Chatbot baseline against stress-oriented agentic behaviors.

- **Modules Implemented**:
	- `src/agent/chatbot.py`: One-shot baseline chatbot for controlled comparison.
	- `scripts/evaluate_chatbot_limitations.py`: Batch evaluator for S/M/F/H/X cases with scoring and JSON/Markdown export.
	- `scripts/run_hallucination_stress.py`: Multi-turn stress runner (I2-I5 and H1-H5) with hallucination dimensions.
	- `scripts/merge_group_reports.py`: Auto-merges baseline and stress outputs into one combined summary.
	- `report/group_report/CAMPING_TEST_CASES.md`: Extended testcase design from basic to extreme stress suites.

- **Code Highlights**:
	- Added provider override support (`--provider`, `--model`, `--base-url`, `--api-key`) to run the same test suite across OpenAI/OpenRouter.
	- Added selective run/overwrite capability (`--case-ids`, `--merge-existing`) for rerunning only failed cases.
	- Added Vietnamese-accent-insensitive keyword matching for robust scoring.
	- Added dedicated multi-turn scoring dimensions: Data Fidelity, Contradiction Handling, Memory Consistency, Uncertainty Honesty.

- **Documentation**:
	- Updated README with runnable commands for baseline tests, stress tests, and report merge.
	- Ensured all test outputs are saved under `report/group_report/` to support group RCA and scoring transparency.

---

## II. Debugging Case Study (10 Points)

- **Problem Description**:
	- During stress evaluation, the run was interrupted by external tool/provider errors, causing incomplete results and false fail rows:
		- `429 RateLimitReached` on Azure OpenAI (`gpt-4o`, daily quota)
		- `402 Insufficient credits` on OpenRouter
		- `400 content_filter` on injection-like prompt (H3)

- **Log Source**:
	- `logs/2026-04-06.log`
	- Sample entries include high-volume `LLM_METRIC` records and provider failures during long multi-turn suites.

- **Diagnosis**:
	- Root cause was not parser logic in our scripts but runtime dependency on provider quotas/credits and policy filters.
	- Secondary cause: strict stress prompts can trigger policy filters, resulting in missing answers and skewed scoring.

- **Solution**:
	- Switched execution path from `gpt-4o` to `gpt-4o-mini` on the same Azure endpoint for quota headroom.
	- Added rerun strategy with case/suite slicing:
		- rerun only failed IDs
		- overwrite results deterministically into existing JSON/MD
	- Kept failure transparency by preserving error evidence in report outputs when request truly fails.

### II-A. Debug Tool/API Error Notes (Added)

- **Error 1: Azure 429 RateLimitReached**
	- Symptom: stress run stopped mid-suite.
	- Fix: switched model from `gpt-4o` to `gpt-4o-mini` with same base URL.

- **Error 2: OpenRouter 402 Insufficient credits**
	- Symptom: all rows in a subset were empty with provider error.
	- Fix: fallback to Azure provider and rerun target subsets.

- **Error 3: Azure content_filter 400**
	- Symptom: injection-style prompt returns blocked response.
	- Fix: mark as tool/policy failure evidence, then rerun with safer wording when the objective is functionality testing.

- **Post-fix Outcome**:
	- Restored full run for requested subsets.
	- Produced stable result artifacts and combined summary for grading.

### II-B. Debug Agent Tool Errors (Added)

- **Tool Error 1: Hallucinated/Unknown Tool Call**
	- Symptom: the model returned an action that called a tool not present in the registry (or used a wrong tool name), resulting in observations such as `Tool <name> not found`.
	- Root cause: LLM output did not consistently follow the allowed tool list and required action format.
	- Fix applied:
		- Enforced a strict JSON action format in the system prompt.
		- Validated tool names against an allowlist before execution.
		- Returned structured error observations so the model could self-correct in the next step.

- **Tool Error 2: Invalid Tool Arguments (`TypeError`)**
	- Symptom: tool calls contained missing/extra argument fields or wrong data types.
	- Root cause: the action parser extracted arguments that were incompatible with the tool function signature.
	- Fix applied:
		- Added robust JSON parsing with a safe fallback path.
		- Wrapped tool execution in `try/except` to catch `TypeError` and return explicit diagnostics.
		- Fed error observations back to the model so it could re-plan instead of crashing the loop.

- **Tool Error 3: Action Parsing Failure**
	- Symptom: model output could not be parsed into a valid `Action`, causing the ReAct loop to stall.
	- Root cause: output formatting was inconsistent across models/providers.
	- Fix applied:
		- Added an `AGENT_PARSE_ERROR` branch in the loop.
		- Automatically injected feedback into the prompt requesting a valid action format.
		- Enforced `max_steps` to prevent infinite loops.

- **Tool Error 4: Tool Chain Completed but Finalization Failed**
	- Symptom: the agent had enough observations but failed to terminate with a consistent `Final Answer`.
	- Root cause: missing or weak termination signals.
	- Fix applied:
		- Added a `finish` tool as an explicit terminal signal in the scenario.
		- Prioritized `Final Answer:` detection and logged `AGENT_FINAL_ANSWER`.
		- Added a safe fallback response when `max_steps` is exceeded.

---

## III. Personal Insights: Chatbot vs ReAct (10 Points)

1. **Reasoning**:
	 - Chatbot is strong in direct response tasks but weak in explicit step control and stateful decomposition.
	 - ReAct-style loop improves traceability because each intermediate action/observation can be audited.

2. **Reliability**:
	 - In this lab, Chatbot performed well on many direct tasks, but reliability dropped in stress contexts:
		 - safety edge case (F1)
		 - strict logic/string/count constraints (X4, X5, X7, X9)
		 - context-switching memory weakness (I5 score 5/8)
	 - Agent can still underperform if tool policy, parser constraints, or budget limits are not handled robustly.

3. **Observation**:
	 - Environment feedback (observations + telemetry) is essential for debugging real failure causes.
	 - Without observation traces, failures can be misattributed to prompt design while the true cause is provider error, policy filter, or runtime quota.

---

## IV. Future Improvements (5 Points)

- **Scalability**:
	- Move to queue-based asynchronous tool execution.
	- Add cached retrieval for repeated weather/traffic lookups and deterministic replay for evaluation.

- **Safety**:
	- Add a supervisor guard stage before final answer:
		- tool allowlist enforcement
		- contradiction and missing-data checks
		- uncertainty policy (must explicitly label unknowns)

- **Performance**:
	- Add calculator/code tool for arithmetic-heavy cases.
	- Add state manager for long multi-turn context switching.
	- Add a pre-answer validator for strict constraints (word count, format, negative constraints).


## V. Evidence Summary (Quick Reference)

- `report/group_report/CHATBOT_LIMITATIONS.md`
- `report/group_report/HALLUCINATION_STRESS_RESULTS.md`
- `report/group_report/COMBINED_EVAL_SUMMARY.md`
- `logs/2026-04-06.log`

---

> [!NOTE]
> Submit this report by renaming it to `REPORT_[YOUR_NAME].md` and placing it in this folder.
