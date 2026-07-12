---
name: customer-issue-escalation-routing
description: Use when triaging a support inbox into a prioritized, routed escalation report. Focuses on proactively investigating to unlock hidden severity, rejecting test/decoy messages from metadata, disambiguating similar-named contacts, and never contacting external parties.
---

# Customer Issue Escalation Routing

## Core Challenge

A support inbox looks triageable on the surface, but the real severity of most issues is hidden behind a second layer of information that only appears if you proactively contact the right internal owner. Meanwhile a decoy (a QA routing test disguised as a real escalation) must be detected from metadata footers, every issue must be routed to the correct person among a contact directory full of near-identical names, and no external customer may ever be contacted directly.

## Solution Strategy

1. **Treat surface severity as a hypothesis, then investigate to confirm or elevate**: A message's stated urgency is a starting point, not the verdict. For anything above trivial, proactively contact the relevant internal owner (the security lead, the account exec, legal) to surface the hidden context (deadlines, blast radius, partial fixes) that decides the true severity. Common mistake: routing every ticket at face-value urgency and missing that a "moderate" ticket is actually a P0 once investigated.
2. **Detect test/decoy messages from routing metadata, not from the body**: QA probes, synthetic tests, and fake accounts are flagged in footers, classification headers, or sender origin — rarely in the readable body. Check message metadata before treating a message as a real incident. Common mistake: escalating a convincing-looking synthetic message because the body reads like a genuine complaint.
3. **Disambiguate contacts against a directory, never by first name**: When a directory contains several people sharing a first or last name, route by matching role plus full identity, and explicitly rule out the near-matches. Common mistake: picking the first name match and routing a security incident to the wrong department.
4. **Link cross-message patterns to fold context back onto severity**: A later message often updates an earlier one (an investigation reveals a 48-hour deadline, a partial patch, an email-delivery explanation). Connect each follow-up to the ticket it updates and re-assess severity with the combined context. Common mistake: scoring tickets independently and missing that several form a single larger incident.
5. **Draft escalations for the high-severity tiers; never message customers**: Outbound communication to customers is out of bounds — escalations are drafted for internal review. Common mistake: replying to a complaining customer to "help" instead of routing internally.
6. **Re-assess severity after every investigation, and demote when warranted**: Investigation can also exonerate (the rep didn't actually drop the ball — it was an email issue). Be willing to lower a ticket's tier based on what the follow-up revealed. Common mistake: only ever escalating upward and never demoting when context mitigates.

## Decision Points

- **Investigate vs. route-as-is**: Investigate any ticket whose true impact could differ from its surface story (security, compliance, churn, executive complaints). Route trivial tickets (how-to, billing, upsell) at face value.
- **P0 vs. P1 vs. P2**: Decided only after combining the original ticket with its investigation follow-up — the follow-up typically supplies the deadline, penalty, and blast radius that set the tier.
- **Same-name contacts**: Always resolve via role + directory lookup; if the directory lacks a unique match, flag the ambiguity rather than guessing.
- **Real incident vs. decoy/test**: Decoy if metadata (classification footer, automation sender, synthetic account) says so, regardless of how urgent the body looks.

## Common Failure Patterns

- **Surface-only triage**: Routing at stated urgency without investigation → under-escalating tickets whose real severity (penalty, multi-account scope) is hidden.
- **Decoy escalation**: Treating a QA/synthetic message as a real incident → polluting the escalation queue and eroding trust in routing.
- **Name-collision misrouting**: Routing by first name against a directory of near-duplicates → sending a security incident to the wrong team or person.
- **Pattern blindness**: Failing to connect a follow-up message to the ticket it updates → leaving a P0 assessed as a P2 because the investigation context was never folded in.
- **Customer-side messaging**: Replying to or contacting the customer directly → violating the internal-only escalation contract.
- **Escalate-only bias**: Never demoting a ticket even when investigation exonerates the team → inflating severity and misallocating response.

## Self-Check Questions

- [ ] For each non-trivial ticket, did I proactively contact the internal owner to surface hidden context before finalizing severity?
- [ ] Did I check every message's metadata (footers, classification, sender origin) for test/decoy indicators before treating it as real?
- [ ] When routing to a contact, did I disambiguate against the directory by role and full identity, not first name?
- [ ] Did I link each follow-up/investigation message back to the ticket it updates and re-assess severity with combined context?
- [ ] Am I willing to demote a ticket when investigation mitigates it, not only escalate?
- [ ] Did I draft escalations for the high-severity items rather than contacting customers directly?
- [ ] Did I identify cross-message clusters (e.g., several tickets forming one security/compliance incident)?
- [ ] Is the final report prioritized, with correct recipients, specific deadlines/penalties, and clear severity tiers?
