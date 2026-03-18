"""
AI or Not? – Decision Lab
A self-paced interactive game for business leaders to learn when to use
rule-based automation, AI Assist (LLM/RAG), or Agentic AI.
"""

import random
import streamlit as st

# ──────────────────────────────────────────────
# SCENARIO DATA
# 12 scenarios across 3 levels (4 per level)
# correct_answer: "rule" | "ai" | "agent"
# expected_reason: reasoning tags the player should identify
# outcomes: real-world consequence per choice (Outcome Simulator)
# ──────────────────────────────────────────────
SCENARIOS = [
    # ── Level 1: Automation vs AI ──
    {
        "id": 1,
        "level": 1,
        "title": "Structured Invoice Extraction",
        "description": (
            "Invoice numbers are extracted from structured PDFs with a fixed, "
            "consistent format. Every invoice follows the exact same template."
        ),
        "correct_answer": "rule",
        "expected_reason": ["structured", "deterministic", "repetitive"],
        "explanation": "Structured and predictable → rule-based automation is sufficient. No AI needed.",
        "difficulty": "easy",
        "outcomes": {
            "rule":  "✅ Fast, accurate extraction with near-zero errors. Done in milliseconds, every time.",
            "ai":    "⚠️ Unnecessary cost and latency introduced. AI adds no value on perfectly fixed templates.",
            "agent": "❌ Severe over-engineering. Agent overhead slows a trivially simple, repetitive task.",
        },
    },
    {
        "id": 2,
        "level": 1,
        "title": "Multi-format Invoice Processing",
        "description": (
            "Invoices arrive from 50 different vendors, each with unique layouts, "
            "fonts, and field placements. No two invoices look the same."
        ),
        "correct_answer": "ai",
        "expected_reason": ["unstructured"],
        "explanation": "Unstructured variation across vendors → AI handles format diversity well.",
        "difficulty": "easy",
        "outcomes": {
            "rule":  "❌ Rule-based logic breaks on every new vendor layout. Requires constant manual updates.",
            "ai":    "✅ AI handles format diversity well. Extraction accuracy improves as more vendors are seen.",
            "agent": "⚠️ Agentic complexity adds overhead where extraction alone requires no autonomous actions.",
        },
    },
    {
        "id": 3,
        "level": 1,
        "title": "Daily Sales Report",
        "description": (
            "Generate a daily sales summary report by pulling data from a clean, "
            "structured database with fixed columns and known aggregation rules."
        ),
        "correct_answer": "rule",
        "expected_reason": ["structured", "deterministic", "repetitive"],
        "explanation": "Deterministic reporting from structured data does not require AI.",
        "difficulty": "easy",
        "outcomes": {
            "rule":  "✅ Report generated reliably every morning in seconds. Zero maintenance once configured.",
            "ai":    "⚠️ AI introduces unpredictability into a fully deterministic reporting task. Overkill.",
            "agent": "❌ Agents are built for multi-step decisions, not structured database queries.",
        },
    },
    {
        "id": 4,
        "level": 1,
        "title": "Email Classification",
        "description": (
            "Classify thousands of incoming customer emails into complaint categories "
            "such as billing, delivery, and product issues, based on free-form text."
        ),
        "correct_answer": "ai",
        "expected_reason": ["unstructured", "decision"],
        "explanation": "Unstructured text with semantic meaning → AI classification works well.",
        "difficulty": "easy",
        "outcomes": {
            "rule":  "❌ Keyword rules miss nuance. Emails get misclassified, frustrating agents and customers.",
            "ai":    "✅ AI classifies with high accuracy across free-form text. Easy to retrain as categories evolve.",
            "agent": "⚠️ Classification requires no system actions. Agentic overhead without meaningful benefit.",
        },
    },
    # ── Level 2: AI vs Agentic AI ──
    {
        "id": 5,
        "level": 2,
        "title": "Policy Q&A",
        "description": (
            'An employee asks the HR chatbot: "What is our leave policy?" '
            "The system should find and present the relevant policy text."
        ),
        "correct_answer": "ai",
        "expected_reason": ["unstructured", "decision"],
        "explanation": "Retrieval + generation (RAG) is all that's needed. No action or system change required.",
        "difficulty": "medium",
        "outcomes": {
            "rule":  "❌ Hard-coded FAQs miss nuanced questions. Employees get no useful answers.",
            "ai":    "✅ RAG retrieves and presents accurate policy text. Employees get instant, reliable answers.",
            "agent": "⚠️ No action is needed here — just retrieval and generation. Agent adds unnecessary complexity.",
        },
    },
    {
        "id": 6,
        "level": 2,
        "title": "Leave Application",
        "description": (
            'An employee tells the HR bot: "Apply leave for next Monday." '
            "The system needs to process and record the request."
        ),
        "correct_answer": "agent",
        "expected_reason": ["action", "decision"],
        "explanation": "Requires an action (creating a leave record) + integration with the HR system → agentic.",
        "difficulty": "medium",
        "outcomes": {
            "rule":  "❌ Rule-based systems can't interpret natural-language requests or write to HR systems.",
            "ai":    "⚠️ AI understands the request but cannot create the leave record without agentic execution.",
            "agent": "✅ Agent interprets the request, checks policy, and writes to the HR system seamlessly.",
        },
    },
    {
        "id": 7,
        "level": 2,
        "title": "FAQ Chatbot Hallucination",
        "description": (
            "Your FAQ chatbot occasionally gives incorrect or fabricated answers "
            "about company products. Customers are complaining about wrong information."
        ),
        "correct_answer": "ai",
        "expected_reason": ["unstructured", "decision"],
        "explanation": "The fix is grounding the model with RAG (retrieval from verified docs), not agentic workflows.",
        "difficulty": "medium",
        "outcomes": {
            "rule":  "❌ Rules can't fix hallucination. The model still generates without grounding.",
            "ai":    "✅ RAG grounds the model on verified product docs. Hallucination drops dramatically.",
            "agent": "⚠️ Agentic workflows don't address the root cause — the model's lack of factual grounding.",
        },
    },
    {
        "id": 8,
        "level": 2,
        "title": "Data Entry Automation",
        "description": (
            "Structured form data (name, address, tax ID) needs to be entered "
            "into the ERP system from a standardized CSV file every morning."
        ),
        "correct_answer": "rule",
        "expected_reason": ["structured", "deterministic", "repetitive"],
        "explanation": "No reasoning required. Structured input → deterministic ERP entry → simple automation.",
        "difficulty": "medium",
        "outcomes": {
            "rule":  "✅ Structured CSV → ERP entry runs without errors, every morning, on schedule.",
            "ai":    "⚠️ AI is unnecessary for a fixed-format, fully deterministic data pipeline.",
            "agent": "❌ Agents are built for multi-step decisions. This is a single-step deterministic task.",
        },
    },
    # ── Level 3: Complex Real-World Scenarios ──
    {
        "id": 9,
        "level": 3,
        "title": "Vendor Onboarding Workflow",
        "description": (
            "Onboarding a new vendor involves validating documents, scoring risk "
            "based on financials, routing for manager approval, and notifying legal."
        ),
        "correct_answer": "agent",
        "expected_reason": ["action", "decision"],
        "explanation": "Multi-step decisions + actions across systems → agentic workflow is the right fit.",
        "difficulty": "hard",
        "outcomes": {
            "rule":  "❌ The multi-step routing and conditional logic quickly overwhelm static rule systems.",
            "ai":    "⚠️ AI can score risk but cannot trigger approvals or notify legal without agentic execution.",
            "agent": "✅ Agent orchestrates validation, scoring, approval routing, and legal notification end-to-end.",
        },
    },
    {
        "id": 10,
        "level": 3,
        "title": "Sentiment Analysis Dashboard",
        "description": (
            "Analyze thousands of customer feedback responses, extract themes, "
            "identify sentiment trends, and generate an executive insights report."
        ),
        "correct_answer": "ai",
        "expected_reason": ["unstructured", "decision"],
        "explanation": "AI excels at insight extraction from unstructured data. No actions needed.",
        "difficulty": "hard",
        "outcomes": {
            "rule":  "❌ Keyword rules can't capture sentiment nuance or reliably extract emerging themes.",
            "ai":    "✅ AI surfaces themes and sentiment trends across thousands of responses in minutes.",
            "agent": "⚠️ No actions are required — this is pure insight extraction from unstructured data.",
        },
    },
    {
        "id": 11,
        "level": 3,
        "title": "Customer Complaint Resolution",
        "description": (
            "When a complaint arrives: classify it, fetch the relevant refund policy, "
            "draft a response, and automatically trigger a refund if criteria are met."
        ),
        "correct_answer": "agent",
        "expected_reason": ["action", "decision"],
        "explanation": "End-to-end workflow with reasoning + actions (refund trigger) → agentic system.",
        "difficulty": "hard",
        "outcomes": {
            "rule":  "❌ Rules can't classify free-text complaints or decide refund eligibility dynamically.",
            "ai":    "⚠️ AI can classify and draft a reply, but cannot trigger the refund without agentic execution.",
            "agent": "✅ Agent classifies, retrieves policy, drafts the response, and triggers the refund autonomously.",
        },
    },
    {
        "id": 12,
        "level": 3,
        "title": "KPI Dashboard Generation",
        "description": (
            "Every morning, pull structured sales, ops, and finance data from the "
            "data warehouse and display pre-defined KPIs on an executive dashboard."
        ),
        "correct_answer": "rule",
        "expected_reason": ["structured", "deterministic", "repetitive"],
        "explanation": "Deterministic queries on structured data → rule-based pipeline. No AI required.",
        "difficulty": "hard",
        "outcomes": {
            "rule":  "✅ Pre-defined KPIs are queried and displayed reliably every morning. Zero variance.",
            "ai":    "⚠️ AI adds latency and cost to a fully deterministic, structured reporting pipeline.",
            "agent": "❌ Agentic overhead for a single-step query pipeline is completely unjustified.",
        },
    },
]

# ──────────────────────────────────────────────
# REASONING OPTIONS
# Used in the "Explain Your Thinking" multiselect
# ──────────────────────────────────────────────
REASON_OPTIONS = {
    "structured":    "Data is structured and predictable",
    "unstructured":  "Data is unstructured / variable",
    "decision":      "Requires decision making",
    "action":        "Requires system action / integration",
    "repetitive":    "Task is repetitive",
    "deterministic": "Outcome is rule-based and fixed",
}

# One-liner clues shown on the home screen before the game starts
OPTION_CLUES = {
    "rule":  ("⚙️  Rule-based Automation", "If a robot could follow a recipe blindfolded, this is your tool."),
    "ai":    ("🤖  AI Assist (LLM / RAG)",  "When the data is messy and meaning matters — let the model read between the lines."),
    "agent": ("🦾  Agentic AI",              "It doesn't just think — it acts. Multi-step, multi-system, no hand-holding needed."),
}

# Answer labels shown in the UI
ANSWER_OPTIONS = {
    "rule":  "⚙️  Rule-based Automation",
    "ai":    "🤖  AI Assist (LLM / RAG)",
    "agent": "🦾  Agentic AI",
}

ANSWER_KEYS   = list(ANSWER_OPTIONS.keys())    # ["rule", "ai", "agent"]
ANSWER_LABELS = list(ANSWER_OPTIONS.values())

LEVEL_TITLES = {
    1: "Level 1 — Automation vs AI",
    2: "Level 2 — AI vs Agentic AI",
    3: "Level 3 — Complex Real-World Scenarios",
}

LEVEL_ICONS = {1: "⚡", 2: "🧠", 3: "🌐"}

TOTAL_QUESTIONS = len(SCENARIOS)  # 12


# ──────────────────────────────────────────────
# SCORING LOGIC
# ──────────────────────────────────────────────
def calculate_reasoning_score(selected: list, expected: list) -> int:
    """
    Reasoning Layer scoring.
    Returns +5 if at least one selected tag overlaps with expected_reason, else 0.
    Only applied when the answer is correct.
    """
    return 5 if set(selected) & set(expected) else 0


def calculate_score_correct(confidence: int, reasoning_score: int) -> int:
    """
    Score for a correct answer.
      Base:       +10
      Confidence: +5  if confidence >= 4
      Reasoning:  +5  if reasoning overlapped (pre-calculated)
    """
    delta = 10
    if confidence >= 4:
        delta += 5
    return delta + reasoning_score


def calculate_score_wrong_final(correct_answer: str, chosen: str, confidence: int) -> int:
    """
    Penalty applied when a wrong answer is final (no retries remain).
    Preserves existing misclassification + overconfidence penalties.
      Overconfidence (conf >= 4, wrong):     -3
      Over-engineering (chose agent, rule):  -5
      Over-engineering (chose ai,   rule):   -3
    """
    delta = 0
    if confidence >= 4:
        delta -= 3
    if correct_answer == "rule":
        if chosen == "agent":
            delta -= 5
        elif chosen == "ai":
            delta -= 3
    return delta


def get_player_title(score: int) -> tuple[str, str]:
    """Return (title, description) based on final score."""
    if score >= 90:
        return "🏆 AI Strategist", "Outstanding! You have a nuanced understanding of when each approach adds real value."
    elif score >= 60:
        return "🔍 AI Explorer", "Good work! You're on the right track. Keep building your intuition for these trade-offs."
    else:
        return "⚙️ Automation First Thinker", "You tend to favour simpler solutions. Review the explanations to sharpen your AI strategy instincts."


# ──────────────────────────────────────────────
# SESSION STATE INITIALISATION
# ──────────────────────────────────────────────
def init_state():
    """Initialise all session_state keys for a fresh game."""
    defaults = {
        "game_phase":            "home",   # home | game | feedback | results
        "player_name":           "",
        "current_index":         0,        # which scenario (0-based)
        "score":                 0,
        "num_correct":           0,
        "high_conf_mistakes":    0,
        "answers_log":           [],       # list of dicts per answered question
        "last_delta":            0,        # score change from last answer
        "last_chosen":           None,     # chosen key for feedback screen
        "last_confidence":       3,        # confidence value from last submission
        # ── Reasoning Layer ──
        "last_reasons":          [],       # reasoning tags selected by player
        "last_reasoning_score":  0,        # reasoning bonus from last answer
        # ── Second Chance ──
        "attempts":              0,        # attempts on the current question
        "retry_available":       False,    # whether retry option is shown
        # ── Outcome Simulator ──
        "last_outcome_variation": None,    # random variation for ai/agent choices
        # ── Leaderboard (persists across restarts) ──
        "leaderboard":           [],
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_game():
    """Reset game progress while keeping the leaderboard."""
    leaderboard = st.session_state.get("leaderboard", [])
    keys_to_reset = [
        "game_phase", "player_name", "current_index", "score",
        "num_correct", "high_conf_mistakes", "answers_log",
        "last_delta", "last_chosen", "last_confidence",
        "last_reasons", "last_reasoning_score",
        "attempts", "retry_available", "last_outcome_variation",
    ]
    for key in keys_to_reset:
        if key in st.session_state:
            del st.session_state[key]
    init_state()
    st.session_state.leaderboard = leaderboard


# ──────────────────────────────────────────────
# UI HELPERS
# ──────────────────────────────────────────────
def level_badge(level: int) -> str:
    icon = LEVEL_ICONS.get(level, "")
    return f"{icon} {LEVEL_TITLES[level]}"


def difficulty_badge(difficulty: str) -> str:
    colors = {"easy": "🟢", "medium": "🟡", "hard": "🔴"}
    return f"{colors.get(difficulty, '⚪')} {difficulty.capitalize()}"


def render_header():
    st.markdown(
        """
        <h1 style='text-align:center; color:#4F8BF9;'>🧪 AI or Not? – Decision Lab</h1>
        <p style='text-align:center; color:#888; font-size:1rem;'>
        Test your instincts: Rule-based Automation · AI Assist · Agentic AI
        </p>
        <hr>
        """,
        unsafe_allow_html=True,
    )


def render_score_sidebar():
    with st.sidebar:
        st.markdown("### 📊 Your Progress")
        idx      = st.session_state.current_index
        answered = idx
        st.metric("Score",    st.session_state.score)
        st.metric("Correct",  f"{st.session_state.num_correct} / {answered}")
        if answered > 0:
            acc = int(st.session_state.num_correct / answered * 100)
            st.metric("Accuracy", f"{acc}%")
        st.metric("High-Conf Mistakes", st.session_state.high_conf_mistakes)
        st.markdown("---")
        st.markdown(f"**Player:** {st.session_state.player_name}")
        if st.button("🔄 Restart", key="sidebar_restart"):
            reset_game()
            st.rerun()


# ──────────────────────────────────────────────
# PRE-GAME CLUES
# ──────────────────────────────────────────────
def render_option_clues():
    st.markdown("### 💡 Peek at your options — click to reveal!")
    cols = st.columns(3)
    for col, (key, (label, clue)) in zip(cols, OPTION_CLUES.items()):
        with col:
            with st.expander(label):
                st.markdown(f"*{clue}*")
    st.markdown("<br>", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# SCREEN: HOME
# ──────────────────────────────────────────────
def show_home():
    render_header()

    # ── Welcome card (centred narrow column) ──
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(
            """
            <div style='background:#1E1E2E; border-radius:12px; padding:2rem; border:1px solid #333;'>
            <h3 style='color:#4F8BF9;'>👋 Welcome, Decision Maker!</h3>
            <p style='color:#FFFFFF;'>
            In this game you'll face <b>12 real-world business scenarios</b> and
            decide which approach fits best:
            </p>
            <ul style='color:#FFFFFF;'>
            <li>⚙️ <b>Rule-based Automation</b> — structured, deterministic tasks</li>
            <li>🤖 <b>AI Assist</b> — unstructured data, language, generation</li>
            <li>🦾 <b>Agentic AI</b> — multi-step workflows that take actions</li>
            </ul>
            <p style='color:#FFFFFF;'>
            Rate your <b>confidence</b> for bonus (or penalty) points. Think carefully!
            </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── Option clues — full page width so 3 columns have room ──
    st.markdown("<br>", unsafe_allow_html=True)
    render_option_clues()

    # ── Name input + start (centred narrow column) ──
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        name = st.text_input("🎮 Enter your name to begin:", placeholder="e.g. Alex Johnson")

        col_a, col_b = st.columns([1, 1])
        with col_a:
            if st.button("🚀 Start Game", type="primary", use_container_width=True):
                if name.strip():
                    st.session_state.player_name = name.strip()
                    st.session_state.game_phase  = "game"
                    st.rerun()
                else:
                    st.warning("Please enter your name to start.")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            """
            <p style='color:#888; font-size:0.85rem;'>
            🏅 Scoring: +10 correct · +5 high-confidence correct · +5 good reasoning<br>
            ⚠️ Retry penalty: −2 · Over-engineering penalty applies on final wrong attempt
            </p>
            """,
            unsafe_allow_html=True,
        )

    # Show leaderboard if it exists
    if st.session_state.get("leaderboard"):
        st.markdown("---")
        show_leaderboard(compact=True)


# ──────────────────────────────────────────────
# SCREEN: GAME (question card)
# ──────────────────────────────────────────────
def show_game():
    idx      = st.session_state.current_index
    scenario = SCENARIOS[idx]

    render_header()
    render_score_sidebar()

    # Progress bar
    progress = idx / TOTAL_QUESTIONS
    st.progress(progress, text=f"Question {idx + 1} of {TOTAL_QUESTIONS}")

    # Level transition banner
    prev_level = SCENARIOS[idx - 1]["level"] if idx > 0 else None
    if prev_level != scenario["level"]:
        st.info(f"### {level_badge(scenario['level'])}", icon="📌")

    # Retry notice (shown when returning after a wrong first attempt)
    if st.session_state.attempts == 1:
        st.warning("🔄 **Second attempt** — a −2 penalty has been applied. Choose carefully!")

    st.markdown("<br>", unsafe_allow_html=True)

    # Scenario card
    with st.container():
        st.markdown(
            f"""
            <div style='background:#1E1E2E; border-radius:12px; padding:1.5rem;
                        border-left:5px solid #4F8BF9; margin-bottom:1rem;'>
            <div style='display:flex; justify-content:space-between; align-items:center;'>
                <span style='color:#888; font-size:0.85rem;'>
                    Q{idx+1} &nbsp;|&nbsp; {difficulty_badge(scenario['difficulty'])}
                </span>
            </div>
            <h3 style='color:#F0F0F0; margin-top:0.5rem;'>{scenario['title']}</h3>
            <p style='color:#CCCCCC; font-size:1rem; line-height:1.6;'>{scenario['description']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── Answer options (radio) ──
    chosen_label = st.radio(
        "**Which approach is most appropriate?**",
        options=ANSWER_LABELS,
        index=None,
        key=f"radio_{idx}",
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Confidence slider ──
    col_slider, col_hint = st.columns([3, 2])
    with col_slider:
        confidence = st.slider(
            "**How confident are you?**",
            min_value=1, max_value=5, value=3,
            key=f"conf_{idx}",
            help="≥4 gives a bonus if correct, but a penalty if wrong!",
        )
    with col_hint:
        conf_labels = {
            1: "🤔 Just guessing", 2: "😐 Uncertain", 3: "🙂 Fairly sure",
            4: "😎 Confident",     5: "💯 Very confident",
        }
        st.markdown(
            f"<br><span style='font-size:1rem;'>{conf_labels[confidence]}</span>",
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # ── Feature 1: Reasoning Layer ──
    # Player must articulate WHY before submitting.
    st.markdown("**🧠 Explain Your Thinking**")
    selected_reasons = st.multiselect(
        "Why did you choose this? (Select all that apply)",
        options=list(REASON_OPTIONS.keys()),
        format_func=lambda x: REASON_OPTIONS[x],
        key=f"reasons_{idx}",
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # Submit is enabled only when both answer + at least one reason are selected
    submit_ready = chosen_label is not None and len(selected_reasons) > 0
    if not submit_ready:
        st.caption("⬆️ Select an answer and at least one reason to enable submit.")

    if st.button(
        "✅ Submit Answer", type="primary", use_container_width=True,
        key=f"submit_{idx}", disabled=not submit_ready,
    ):
        chosen_key = ANSWER_KEYS[ANSWER_LABELS.index(chosen_label)]
        correct    = scenario["correct_answer"]

        # Increment attempts for this question
        st.session_state.attempts += 1

        # Reasoning score (only counted if answer is correct)
        reasoning_score = calculate_reasoning_score(selected_reasons, scenario["expected_reason"])

        # Outcome Simulator: compute random variation now so it doesn't re-roll on reruns
        if chosen_key in ["ai", "agent"]:
            variation = random.choice(["success", "partial", "failure"])
        else:
            variation = "success"

        # Persist data needed by the feedback screen
        st.session_state.last_chosen           = chosen_key
        st.session_state.last_confidence       = confidence
        st.session_state.last_reasons          = selected_reasons
        st.session_state.last_outcome_variation = variation

        if chosen_key == correct:
            # ── Correct answer ──
            delta = calculate_score_correct(confidence, reasoning_score)
            st.session_state.score              += delta
            st.session_state.last_delta          = delta
            st.session_state.last_reasoning_score = reasoning_score
            st.session_state.num_correct         += 1
            st.session_state.retry_available      = False
            st.session_state.attempts             = 0  # reset for next question
            st.session_state.answers_log.append({
                "question":       idx + 1,
                "title":          scenario["title"],
                "correct":        correct,
                "chosen":         chosen_key,
                "confidence":     confidence,
                "delta":          delta,
                "reasoning_score": reasoning_score,
            })

        elif st.session_state.attempts == 1:
            # ── First wrong attempt — offer retry ──
            # No score change yet; penalty is applied when the user clicks Retry.
            st.session_state.last_delta           = 0
            st.session_state.last_reasoning_score = 0
            st.session_state.retry_available       = True
            if confidence >= 4:
                st.session_state.high_conf_mistakes += 1

        else:
            # ── Second wrong attempt — final ──
            delta = calculate_score_wrong_final(correct, chosen_key, confidence)
            st.session_state.score              += delta
            st.session_state.last_delta          = delta
            st.session_state.last_reasoning_score = 0
            st.session_state.retry_available      = False
            st.session_state.attempts             = 0  # reset for next question
            st.session_state.answers_log.append({
                "question":       idx + 1,
                "title":          scenario["title"],
                "correct":        correct,
                "chosen":         chosen_key,
                "confidence":     confidence,
                "delta":          delta,
                "reasoning_score": 0,
            })

        st.session_state.game_phase = "feedback"
        st.rerun()


# ──────────────────────────────────────────────
# SCREEN: FEEDBACK (after each answer)
# ──────────────────────────────────────────────
def show_feedback():
    idx             = st.session_state.current_index
    scenario        = SCENARIOS[idx]
    chosen          = st.session_state.last_chosen
    delta           = st.session_state.last_delta
    confidence      = st.session_state.last_confidence
    reasoning_score = st.session_state.last_reasoning_score
    retry_available = st.session_state.retry_available
    variation       = st.session_state.last_outcome_variation
    is_correct      = (chosen == scenario["correct_answer"])

    render_header()
    render_score_sidebar()

    # Progress bar — don't count this question as done until retry is resolved
    progress_val = idx / TOTAL_QUESTIONS if retry_available else (idx + 1) / TOTAL_QUESTIONS
    progress_txt = (
        f"Question {idx + 1} of {TOTAL_QUESTIONS} — retry available"
        if retry_available
        else f"Question {idx + 1} of {TOTAL_QUESTIONS} — answered"
    )
    st.progress(progress_val, text=progress_txt)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Feature 3: Outcome Simulator ──
    # Always shown immediately after submission so players see consequences first.
    st.markdown("### 📊 Simulated Outcome")
    st.info(scenario["outcomes"][chosen])

    # Light randomness for ai/agent choices (adds realism without breaking the flow)
    if chosen in ["ai", "agent"]:
        if variation == "partial":
            st.warning("⚠️ Partial success: Some edge cases failed in production.")
        elif variation == "failure":
            st.error("❌ System struggled with real-world variability under load.")

    st.markdown("<br>", unsafe_allow_html=True)

    # ═══════════════════════════════════════════
    # BRANCH A — Retry available (first wrong attempt)
    # ═══════════════════════════════════════════
    if retry_available:
        chosen_label  = ANSWER_OPTIONS[chosen]
        correct_label = ANSWER_OPTIONS[scenario["correct_answer"]]
        st.markdown(
            f"""
            <div style='background:#2D1B1B; border-radius:10px; padding:1.2rem;
                        border-left:6px solid #E74C3C; margin-bottom:1rem;'>
            <h3 style='color:#E74C3C; margin:0;'>❌ Not quite — but you get one more chance!</h3>
            <p style='color:#CCCCCC; margin-top:0.5rem;'>
            You chose: <b>{chosen_label}</b>
            </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col_retry, col_skip = st.columns(2)

        with col_retry:
            # Feature 2: Retry — apply -2 penalty immediately, clear widget state, return to game
            if st.button("🔄 Retry  (−2 pts penalty)", type="primary", use_container_width=True):
                st.session_state.score -= 2
                # Clear widget state so the player can pick a fresh answer
                for key in [f"radio_{idx}", f"reasons_{idx}"]:
                    if key in st.session_state:
                        del st.session_state[key]
                st.session_state.game_phase = "game"
                st.rerun()

        with col_skip:
            # Skip retry: apply final wrong penalty and show full feedback
            if st.button("⏭️ Skip & See Answer", use_container_width=True):
                delta = calculate_score_wrong_final(scenario["correct_answer"], chosen, confidence)
                st.session_state.score              += delta
                st.session_state.last_delta          = delta
                st.session_state.retry_available     = False
                st.session_state.attempts            = 0
                st.session_state.answers_log.append({
                    "question":        idx + 1,
                    "title":           scenario["title"],
                    "correct":         scenario["correct_answer"],
                    "chosen":          chosen,
                    "confidence":      confidence,
                    "delta":           delta,
                    "reasoning_score": 0,
                })
                st.rerun()

    # ═══════════════════════════════════════════
    # BRANCH B — Final feedback (correct OR second wrong)
    # ═══════════════════════════════════════════
    else:
        # Result banner
        if is_correct:
            st.markdown(
                """
                <div style='background:#1B4332; border-radius:10px; padding:1.2rem;
                            border-left:6px solid #2ECC71; margin-bottom:1rem;'>
                <h3 style='color:#2ECC71; margin:0;'>✅ Correct!</h3>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            correct_label = ANSWER_OPTIONS[scenario["correct_answer"]]
            chosen_label  = ANSWER_OPTIONS[chosen]
            st.markdown(
                f"""
                <div style='background:#2D1B1B; border-radius:10px; padding:1.2rem;
                            border-left:6px solid #E74C3C; margin-bottom:1rem;'>
                <h3 style='color:#E74C3C; margin:0;'>❌ Not quite.</h3>
                <p style='color:#CCCCCC; margin-top:0.5rem;'>
                You chose: <b>{chosen_label}</b><br>
                Correct answer: <b>{correct_label}</b>
                </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Explanation
        st.info(f"💡 **Why?** {scenario['explanation']}")

        # ── Feature 1: Reasoning feedback (only shown when correct) ──
        if is_correct:
            st.markdown("**🧠 Reasoning Check**")
            if reasoning_score > 0:
                st.success("✅ Good reasoning! Your thinking aligns with the key signals.")
            else:
                st.warning("⚠️ Your reasoning could be improved.")
            expected_labels = [REASON_OPTIONS[r] for r in scenario["expected_reason"]]
            st.markdown(f"**Expected thinking:** {' · '.join(expected_labels)}")

        st.markdown("<br>", unsafe_allow_html=True)

        # Score change summary
        score_color = "#2ECC71" if delta >= 0 else "#E74C3C"
        sign        = "+" if delta >= 0 else ""

        # Build breakdown string for score card
        breakdown_parts = []
        if is_correct:
            breakdown_parts.append("+10 correct")
            if confidence >= 4:
                breakdown_parts.append("+5 confidence")
            if reasoning_score > 0:
                breakdown_parts.append("+5 reasoning")
        if st.session_state.get("_retry_penalty_applied"):
            breakdown_parts.append("−2 retry")
        breakdown = "  ·  ".join(breakdown_parts) if breakdown_parts else "No points awarded"

        st.markdown(
            f"""
            <div style='background:#1E1E2E; border-radius:8px; padding:1rem;
                        border:1px solid #333; display:flex; gap:2rem; margin-top:0.5rem;'>
            <div>
                <span style='color:#888; font-size:0.85rem;'>Score change</span><br>
                <span style='color:{score_color}; font-size:1.5rem; font-weight:bold;'>{sign}{delta}</span><br>
                <span style='color:#666; font-size:0.78rem;'>{breakdown}</span>
            </div>
            <div>
                <span style='color:#888; font-size:0.85rem;'>Total score</span><br>
                <span style='color:#F0F0F0; font-size:1.5rem; font-weight:bold;'>{st.session_state.score}</span>
            </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # Next question / results button
        is_last    = (idx == TOTAL_QUESTIONS - 1)
        next_label = "🏁 See Results" if is_last else "Next Question ➡️"

        if st.button(next_label, type="primary", use_container_width=True):
            st.session_state.current_index += 1
            if is_last:
                st.session_state.leaderboard.append({
                    "name":    st.session_state.player_name,
                    "score":   st.session_state.score,
                    "correct": st.session_state.num_correct,
                })
                st.session_state.leaderboard.sort(key=lambda x: x["score"], reverse=True)
                st.session_state.game_phase = "results"
            else:
                st.session_state.game_phase = "game"
            st.rerun()


# ──────────────────────────────────────────────
# SCREEN: RESULTS
# ──────────────────────────────────────────────
def show_results():
    render_header()

    score       = st.session_state.score
    num_correct = st.session_state.num_correct
    hcm         = st.session_state.high_conf_mistakes
    accuracy    = int(num_correct / TOTAL_QUESTIONS * 100)
    title, description = get_player_title(score)

    st.markdown(
        f"<h2 style='text-align:center;'>Results for <b>{st.session_state.player_name}</b></h2>",
        unsafe_allow_html=True,
    )

    # Metrics row
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🏅 Final Score",          score)
    c2.metric("✅ Correct",              f"{num_correct} / {TOTAL_QUESTIONS}")
    c3.metric("🎯 Accuracy",             f"{accuracy}%")
    c4.metric("⚠️ Overconfident Mistakes", hcm)

    st.markdown("<br>", unsafe_allow_html=True)

    # Title badge
    st.markdown(
        f"""
        <div style='background:#1E1E2E; border-radius:12px; padding:2rem;
                    border:2px solid #4F8BF9; text-align:center; margin-bottom:1.5rem;'>
        <h2 style='color:#4F8BF9; margin:0;'>{title}</h2>
        <p style='color:#CCCCCC; margin-top:0.8rem;'>{description}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Answer breakdown
    with st.expander("📋 Review your answers"):
        for log in st.session_state.answers_log:
            correct_icon = "✅" if log["chosen"] == log["correct"] else "❌"
            delta_str    = f"+{log['delta']}" if log["delta"] >= 0 else str(log["delta"])
            r_score      = log.get("reasoning_score", 0)
            r_str        = f" · Reasoning: +{r_score}" if r_score else ""
            st.markdown(
                f"**Q{log['question']}: {log['title']}** {correct_icon}  "
                f"| You: `{ANSWER_OPTIONS[log['chosen']]}` "
                f"| Correct: `{ANSWER_OPTIONS[log['correct']]}` "
                f"| Confidence: {log['confidence']} "
                f"| Score: `{delta_str}`{r_str}"
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # Leaderboard
    show_leaderboard(compact=False)

    st.markdown("<br>", unsafe_allow_html=True)

    col_r, col_h = st.columns(2)
    with col_r:
        if st.button("🔄 Play Again", type="primary", use_container_width=True):
            reset_game()
            st.rerun()


# ──────────────────────────────────────────────
# LEADERBOARD (session-based)
# ──────────────────────────────────────────────
def show_leaderboard(compact: bool = False):
    board = st.session_state.get("leaderboard", [])
    if not board:
        return

    st.markdown("### 🏆 Leaderboard")

    if compact:
        st.markdown("*Top scores this session:*")
        top = board[:5]
    else:
        top = board[:10]

    medals = ["🥇", "🥈", "🥉"] + ["🏅"] * 7

    for i, entry in enumerate(top):
        medal = medals[i] if i < len(medals) else "  "
        col_a, col_b, col_c = st.columns([1, 4, 2])
        col_a.markdown(f"**{medal}**")
        col_b.markdown(f"**{entry['name']}**")
        col_c.markdown(f"`{entry['score']} pts` | {entry['correct']}/{TOTAL_QUESTIONS} correct")


# ──────────────────────────────────────────────
# MAIN ROUTER
# ──────────────────────────────────────────────
def main():
    st.set_page_config(
        page_title="AI or Not? – Decision Lab",
        page_icon="🧪",
        layout="centered",
        initial_sidebar_state="auto",
    )

    st.markdown(
        """
        <style>
        .block-container { padding-top: 2rem; padding-bottom: 2rem; }
        div[data-testid="stRadio"] label { font-size: 1rem !important; }
        div[data-testid="stMetricValue"] { color: #4F8BF9 !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    init_state()

    phase = st.session_state.game_phase

    if phase == "home":
        show_home()
    elif phase == "game":
        show_game()
    elif phase == "feedback":
        show_feedback()
    elif phase == "results":
        show_results()
    else:
        st.error(f"Unknown game phase: {phase}")


if __name__ == "__main__":
    main()
