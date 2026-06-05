# AmazonPeptide Assistant — UX Design Doc

**Designer:** Senior UX Designer
**Status:** Draft v0.1
**Last updated:** June 5, 2026

---

## 1. The design bet

We are betting that the retro early-2000s AmazonPeptide aesthetic will evoke immediate nostalgia and brand alignment. Rather than a modern, sterile SaaS bubble, the widget will look like an authentic part of the original site's vintage UI. By prioritizing a single-column retro chat widget layout that expands from a floating tab, we spend 80% of our design effort matching the physical assets, color blocks, and retro spacing of the parent site.

## 2. The defining interaction

The user types a question into the text box and presses the classic green "Go!" button. The input field turns disabled and greyed-out, the "Go!" button displays a small press-down state, and a retro "Checking COA & Database..." loading indicator with a simple marquee dot-animation pulses at the bottom. Once the response is ready, it is printed with a typewriter effect, bubble-by-bubble, appearing as if it were fetched from a legacy server database. The input field clears and re-focuses.

## 3. Screen inventory

Since this is an embeddable widget, it resides on the host page as:
- **Collapsed Tab State (Launcher)** — A small, sticky retro tab in the bottom right corner.
- **Expanded Widget State (Chat Panel)** — A floating vertical panel (380px wide) containing the chat history and input.

## 4. Screen-by-screen specs

### Collapsed Tab State (Launcher)

**Purpose:** Provide a clean, non-intrusive entry point to the assistant that integrates with the site's layout.

**Layout (top to bottom):**
1. **Chat Tab** — A dark green tab (`#1C6F3B`) containing the text "Help & FAQ / Chat" in white Arial, with a small yellow arrow pointing up.

**Key interactions:**
- **Click/Tap Tab** → Expands the Chat Panel and hides the collapsed tab.

**States:**
- **Default:** Sticky tab sits at the bottom-right corner of the viewport.

---

### Expanded Widget State (Chat Panel)

**Purpose:** The main interface where back-and-forth chat occurs.

**Layout (top to bottom):**
1. **Header Bar** — Dark green background (`#1C6F3B`) containing the "AmazonPeptide" logo (white/green/yellow arrow) on the left, a pulsing yellow "COA Verify" badge in the center, and a white "X" close button on the right.
2. **Warning Banner** — A cream-colored (`#FFF8E7`) thin banner at the top of the chat area displaying: "Research Use Only. All responses are theoretical and anecdotal."
3. **Chat Feed** — A vertical scrolling area with a light cream-beige background (`#F7F5EC`).
   - **Assistant Messages:** Standard retro text boxes with a border and white background (`#FFFFFF`).
   - **User Messages:** Light green background (`#E8F5E9`) with a dark green border.
4. **Input Area** — A white box containing:
   - A single-line text input field (`<input type="text">`) styled with a thin, classic border.
   - A classic green rectangular button with the text "Go!" styled to match the site's retro search buttons.
5. **Session Progress** — A small text indicator ("Session: 1/5 messages") in the bottom-left corner of the input area.

**Key interactions:**
- **Click Close (X)** → Collapses the Chat Panel back into the Collapsed Tab.
- **Type text & click "Go!" (or press Enter)** → Sends the message, disables inputs, and triggers the loading state.
- **Click "Reset Chat" (when limit reached)** → Wipes chat history and starts a fresh session.

**States:**
- **Default (Empty / First-time):** Shows a welcome message from the assistant: "Welcome to the AmazonPeptide Research Database. Ask me any theoretical question about peptide therapeutics."
- **Loading:** Shows "Searching database..." with a simple retro scrolling dots animation.
- **Error:** Shows "Database timeout. Please verify connection and click Go! again." in red Georgia font.
- **Session Limit Reached:** Input is locked. A notice says "5/5 messages used. Chat history cleared on reset." and the "Go!" button changes to a yellow "Reset Chat" button.

## 5. The user journey

The user lands on the AmazonPeptide website. In the bottom-right corner, they see a sticky green tab labeled "Help & FAQ / Chat". They click the tab; it slides up into the expanded Chat Panel. 

The user sees the warning banner reminding them that all info is theoretical, and a welcome message. They type "What is the mechanism of BPC-157?" and click "Go!". The interface goes into a loading state for 2 seconds. The assistant's response types out, outlining the growth-factor expression pathway and angiogenesis properties, carefully framing the effects in cellular theory.

The user asks a second question: "Can I inject 5mg for joint pain?" 
The chatbot instantly responds, declining to give dosing or administration instructions, redirecting them to theoretical models and reinforcing that human effects are purely anecdotal. 
After 5 turns, the input locks, showing a "Session complete" state with a "Reset Chat" button. The user clicks "Reset Chat", the feed clears, and they can start a new query.

## 6. Component & visual notes

- **Typography:** Display headings in Times New Roman/Georgia (serif); body messages and inputs in Arial/Helvetica (sans-serif).
- **Color:** Forest green (`#1C6F3B`), vintage cream (`#F7F5EC`), warning yellow/orange (`#FF9900`), and dark text (`#111111`).
- **Motion:** Instant transitions for opening/closing. Fade-in for new messages. Simple marquee text animation for loading. No modern fluid bounces.
- **Signature Visual:** The custom "AmazonPeptide" logo inside the header bar, complete with the retro orange curved arrow under it.
- **Microcopy Voice:** Academic, objective, and vintage database-like. Uses terms like "Query received...", "Searching database...", "Theoretical Research Only."

## 7. Accessibility & inclusion

- **Screen Readers:** All inputs have descriptive labels. The message feed uses `aria-live="polite"` so new messages are read as they stream in.
- **Keyboard Navigation:** Users can open, close, type, and submit using Tab, Enter, and Esc.
- **Contrast:** High-contrast text on cream/white backgrounds (passes WCAG AA).

## 8. What we are NOT designing

- **No customization / themes** — The widget only exists in the AmazonPeptide retro style.
- **No drag-and-drop file upload** — The input is strictly text-based.
- **No feedback/rating system** — No "thumbs up/down" buttons for chatbot responses.

## 9. Open design questions

- [ ] Should the warning banner be dismissible, or should it remain sticky at the top of the widget?
- [ ] Should the widget automatically expand on the first page load, or always remain collapsed?

## 10. Handoff to engineering

The visual borders and buttons must match the original AmazonPeptide HTML button classes (`.Go` button styling) exactly. The typewriter animation speed should be fast (~20ms per character) so it doesn't cause fatigue.
