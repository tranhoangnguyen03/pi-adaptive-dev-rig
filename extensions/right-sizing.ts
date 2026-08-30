/**
 * Right-sizing extension
 *
 * Appends the frozen Stage 1 right-sizing instruction (plus the owner-approved
 * fresh-verification sentence) to the system prompt on every agent start.
 * Verbatim text: eval/stage0/systems/right-sizing-instruction.md + one sentence.
 * Spec: https://github.com/tranhoangnguyen03/pi-adaptive-dev-rig/issues/5#issuecomment-5469876702
 */

import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

const GUIDANCE = `Right-size the process to the task. Prototype/exploratory work needs only
the smallest convincing implementation plus named limitations. Ordinary
maintainable changes need targeted tests and fresh verification, not full
production ceremony. Reserve comprehensive hardening for consequential or
production-facing work. Skip heavyweight workflow phases the delivery claim
doesn't need.

Before claiming completion, run the relevant checks and cite fresh evidence.`;

export default function rightSizingExtension(pi: ExtensionAPI) {
	pi.on("before_agent_start", async (event) => {
		if (event.systemPrompt.includes(GUIDANCE)) return undefined;
		return { systemPrompt: event.systemPrompt + "\n\n" + GUIDANCE };
	});
}
