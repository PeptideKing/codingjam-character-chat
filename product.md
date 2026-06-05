# AmazonPeptide Assistant — Product Design Doc

**Author:** PM
**Status:** Draft v0.1
**Last updated:** June 5, 2026
**One-liner:** A retro-styled embeddable chat widget that provides instant, theoretical, and encyclopedic knowledge about peptide therapeutics without offering human usage or dosing advice.

---

## 1. The user & the moment

Who is this for, and what are they doing/feeling **right before** they open the app?

- **Who:** A laboratory researcher, biohacking enthusiast, or prospective buyer visiting the AmazonPeptide website to understand the mechanism, structure, or research applications of specific peptides (e.g., Semaglutide, BPC-157).
- **When:** They are looking at a product listing, feeling curious but cautious, and wanting quick, detailed, encyclopedic information to verify scientific properties, research literature, or chemical structures before ordering.
- **Why now:** Existing chatbots either refuse to discuss peptides due to strict safety guardrails, or offer dangerous, unverified human dosing instructions. There is no middle-ground assistant that acts as a safe, highly-specialized, theoretical research encyclopedia.

## 2. The contract (I/O)

The most important section. What does the user give, and what do they get back?

- **Input:** A text input field in a floating chat widget where the user types a question about peptide therapeutics or a specific product (e.g., "How does BPC-157 promote tissue repair?").
- **Output:** A structured, back-and-forth chat conversation providing detailed scientific and theoretical explanations, explicitly framed as research-only/anecdotal, with zero dosing advice and a polite refusal for non-peptide topics.
- **The loop:** User types question → Chatbot responds instantly with theoretical/encyclopedic answers → User asks follow-up or next question → Maximum 5-turn session on a given topic to keep interactions concise and safe. If the user asks about anything related to human dosing, politely tell them the peptides are only used to research and are not for human or animal consumption. State the FDA regulations in place which make this the policy. If they continue to ask about dosing or anything related to dosing, tell them you will have to start the conversation over and then close the chat window after one more time.

## 3. The magical moment

The single sentence the user would say to a friend after using this for the first time. Write it in their voice.

> "I asked about the cellular mechanism of Semaglutide, and it explained the GLP-1 pathway perfectly in seconds, while keeping me safely in the realm of lab research."

## 4. Scope: what we ARE building (v1)

- A floating, expandable chat widget that can be embedded on any webpage.
- A retro early-2000s AmazonPeptide aesthetic theme matching the header, green/orange tabs, and cream-colored boxes of the website.
- A backend API endpoint (`POST /api/chat`) that interfaces with Gemini using a system prompt that enforces strict topic locks and safety compliance.
- In-memory conversation state tracking up to a 5-message limit per session.
- Automatic safety filters that refuse to output human dosing recommendations or medical advice, redirecting to theoretical scientific context.

## 5. Scope: what we are NOT building

- **No user accounts or authentication** — Sessions are transient and anonymous.
- **No chat history persistence** — Conversations are wiped on page reload to maintain privacy and keep the system lightweight.
- **No voice output or avatar generation** — The interface is text-only.
- **No general-purpose web search** — The assistant relies on its built-in knowledge of peptide therapeutics and doesn't answer off-topic queries (e.g., weather, coding, generic advice).
- **No e-commerce checkout integration** — The widget does not add items to the cart or handle payments.

## 6. The signature detail

The widget features an animated, pulsing yellow-green "AmazonPeptide COA Verify" emblem in the widget header. The visual layout mimics the classic 2000s Amazon sidebar: serif typography (Times New Roman), forest green headers (`#1C6F3B`), and cream background blocks (`#F7F5EC`), making it look like a seamless, native extension of the vintage site rather than a modern generic SaaS bubble.

## 7. Success: how we know it worked

Pick ONE primary signal. Not 5 metrics. ONE.

- **Primary:** 95% of questions containing "how to dose", "how to take", or "human usage" are successfully redirected to theoretical/anecdotal research explanations without triggering safety failures or giving dosing numbers.
- **Secondary (optional, max 2):**
  - Average response latency remains under 2.5 seconds.
  - ≥50% of users who expand the widget complete at least a 3-turn conversation.
- **What we're NOT measuring:** Total daily active users or click-through rate to product checkout.

## 8. Open questions

- [ ] What is the exact message/text fallback to show when a user repeatedly asks for dosing guidelines?
- [ ] How should the widget handle the 5-message session limit UI-wise (e.g., show a "Session Limit Reached" alert and a "Reset Chat" button)?

## 9. Handoff

- **For UX:** The chat widget must feel cohesive when floating over the busy, retro layout of the parent page; its collapsed launcher button should look like a retro "Help & FAQ / Chat" tab.
- **For Eng:** Designing a system prompt that reliably blocks dosing questions while still answering the theoretical mechanism of the same peptide is the main prompt-engineering challenge.
