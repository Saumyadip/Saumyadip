"""
AI or Not? – Decision Lab
A self-paced interactive game for business leaders to learn when to use
rule-based automation, AI Assist (LLM/RAG), or Agentic AI.
"""

import streamlit as st

# ──────────────────────────────────────────────
# SCENARIO DATA
# 12 scenarios across 3 levels (4 per level)
# correct_answer: "rule" | "ai" | "agent"
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
        "explanation": "Structured and predictable → rule-based automation is sufficient. No AI needed.",
        "difficulty": "easy",
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
        "explanation": "Unstructured variation across vendors → AI handles format diversity well.",
        "difficulty": "easy",
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
        "explanation": "Deterministic reporting from structured data does not require AI.",
        "difficulty": "easy",
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
        "explanation": "Unstructured text with semantic meaning → AI classification works well.",
        "difficulty": "easy",
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
        "explanation": "Retrieval + generation (RAG) is all that's needed. No action or system change required.",
        "difficulty": "medium",
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
        "explanation": "Requires an action (creating a leave record) + integration with the HR system → agentic.",
        "difficulty": "medium",
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
        "explanation": "The fix is grounding the model with RAG (retrieval from verified docs), not agentic workflows.",
        "difficulty": "medium",
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
        "explanation": "No reasoning required. Structured input → deterministic ERP entry → simple automation.",
        "difficulty": "medium",
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
        "explanation": "Multi-step decisions + actions across systems → agentic workflow is the right fit.",
        "difficulty": "hard",
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
        "explanation": "AI excels at insight extraction from unstructured data. No actions needed.",
        "difficulty": "hard",
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
        "explanation": "End-to-end workflow with reasoning + actions (refund trigger) → agentic system.",
        "difficulty": "hard",
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
        "explanation": "Deterministic queries on structured data → rule-based pipeline. No AI required.",
        "difficulty": "hard",
    },
]

# One-liner clues shown on the home screen before the game starts
OPTION_CLUES = {
    "rule":  ("⚙️  Rule-based Automation", "If a robot could follow a recipe blindfolded, this is your tool."),
    "ai":    ("🤖  AI Assist (LLM / RAG)",  "When the data is messy and meaning matters — let the model read between the lines."),
    "agent": ("🦾  Agentic AI",              "It doesn't just think — it acts. Multi-step, multi-system, no hand-holding needed."),
}

# Answer labels shown in the UI
ANSWER_OPTIONS = {
    "rule": "⚙️  Rule-based Automation",
    "ai": "🤖  AI Assist (LLM / RAG)",
    "agent": "🦾  Agentic AI",
}

ANSWER_KEYS = list(ANSWER_OPTIONS.keys())   # ["rule", "ai", "agent"]
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
def calculate_score_delta(correct_answer: str, chosen: str, confidence: int) -> int:
    """
    Returns the score change for a single answer.

    Base scoring:
      Correct → +10
      Incorrect → 0

    Bonus:
      Confidence >= 4 and correct → +5
      Confidence >= 4 and wrong  → -3

    Extra penalty for severe misclassification:
      Chose "agent" when correct is "rule" → -5
      Chose "ai"    when correct is "rule" → -3
    """
    delta = 0
    if chosen == correct_answer:
        delta += 10
        if confidence >= 4:
            delta += 5
    else:
        if confidence >= 4:
            delta -= 3
        # Extra penalty for over-engineering simple tasks
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
        "game_phase": "home",       # home | game | feedback | results
        "player_name": "",
        "current_index": 0,         # which scenario (0-based)
        "score": 0,
        "num_correct": 0,
        "high_conf_mistakes": 0,
        "answers_log": [],          # list of dicts per answered question
        "last_delta": 0,            # score change from last answer
        "last_chosen": None,        # chosen key for feedback screen
        "leaderboard": [],          # persists across restarts (session only)
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
        "last_delta", "last_chosen",
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
        idx = st.session_state.current_index
        answered = idx  # questions answered so far
        st.metric("Score", st.session_state.score)
        st.metric("Correct", f"{st.session_state.num_correct} / {answered}")
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
                    st.session_state.game_phase = "game"
                    st.rerun()
                else:
                    st.warning("Please enter your name to start.")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            """
            <p style='color:#888; font-size:0.85rem;'>
            🏅 Scoring: +10 correct · +5 high-confidence correct · -3 overconfident wrong<br>
            ⚠️ Extra penalty for over-engineering simple tasks!
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
    idx = st.session_state.current_index
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

    # Answer options (radio)
    chosen_label = st.radio(
        "**Which approach is most appropriate?**",
        options=ANSWER_LABELS,
        index=None,
        key=f"radio_{idx}",
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # Confidence slider
    col_slider, col_hint = st.columns([3, 2])
    with col_slider:
        confidence = st.slider(
            "**How confident are you?**",
            min_value=1,
            max_value=5,
            value=3,
            key=f"conf_{idx}",
            help="≥4 gives a bonus if correct, but a penalty if wrong!",
        )
    with col_hint:
        conf_labels = {1: "🤔 Just guessing", 2: "😐 Uncertain", 3: "🙂 Fairly sure", 4: "😎 Confident", 5: "💯 Very confident"}
        st.markdown(f"<br><span style='font-size:1rem;'>{conf_labels[confidence]}</span>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("✅ Submit Answer", type="primary", use_container_width=True, key=f"submit_{idx}"):
        if chosen_label is None:
            st.warning("Please select an answer before submitting.")
        else:
            # Map label back to key
            chosen_key = ANSWER_KEYS[ANSWER_LABELS.index(chosen_label)]
            correct = scenario["correct_answer"]
            delta = calculate_score_delta(correct, chosen_key, confidence)

            # Update state
            st.session_state.score += delta
            st.session_state.last_delta = delta
            st.session_state.last_chosen = chosen_key

            if chosen_key == correct:
                st.session_state.num_correct += 1
            elif confidence >= 4:
                st.session_state.high_conf_mistakes += 1

            st.session_state.answers_log.append({
                "question": idx + 1,
                "title": scenario["title"],
                "correct": correct,
                "chosen": chosen_key,
                "confidence": confidence,
                "delta": delta,
            })

            st.session_state.game_phase = "feedback"
            st.rerun()


# ──────────────────────────────────────────────
# SCREEN: FEEDBACK (after each answer)
# ──────────────────────────────────────────────
def show_feedback():
    idx = st.session_state.current_index
    scenario = SCENARIOS[idx]
    chosen = st.session_state.last_chosen
    delta = st.session_state.last_delta
    is_correct = chosen == scenario["correct_answer"]

    render_header()
    render_score_sidebar()

    # Progress bar (same position as game screen)
    st.progress((idx + 1) / TOTAL_QUESTIONS, text=f"Question {idx + 1} of {TOTAL_QUESTIONS} — answered")

    st.markdown("<br>", unsafe_allow_html=True)

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
        chosen_label = ANSWER_OPTIONS[chosen]
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

    # Score change
    score_color = "#2ECC71" if delta >= 0 else "#E74C3C"
    sign = "+" if delta >= 0 else ""
    st.markdown(
        f"""
        <div style='background:#1E1E2E; border-radius:8px; padding:1rem;
                    border:1px solid #333; display:flex; gap:2rem; margin-top:0.5rem;'>
        <div>
            <span style='color:#888; font-size:0.85rem;'>Score change</span><br>
            <span style='color:{score_color}; font-size:1.5rem; font-weight:bold;'>{sign}{delta}</span>
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

    # Next button
    is_last = (idx == TOTAL_QUESTIONS - 1)
    next_label = "🏁 See Results" if is_last else "Next Question ➡️"

    if st.button(next_label, type="primary", use_container_width=True):
        st.session_state.current_index += 1
        if is_last:
            # Add to leaderboard
            st.session_state.leaderboard.append({
                "name": st.session_state.player_name,
                "score": st.session_state.score,
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

    score = st.session_state.score
    num_correct = st.session_state.num_correct
    hcm = st.session_state.high_conf_mistakes
    accuracy = int(num_correct / TOTAL_QUESTIONS * 100)
    title, description = get_player_title(score)

    st.markdown(f"<h2 style='text-align:center;'>Results for <b>{st.session_state.player_name}</b></h2>", unsafe_allow_html=True)

    # Metrics row
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🏅 Final Score", score)
    c2.metric("✅ Correct", f"{num_correct} / {TOTAL_QUESTIONS}")
    c3.metric("🎯 Accuracy", f"{accuracy}%")
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
            delta_str = f"+{log['delta']}" if log['delta'] >= 0 else str(log['delta'])
            st.markdown(
                f"**Q{log['question']}: {log['title']}** {correct_icon}  "
                f"| You: `{ANSWER_OPTIONS[log['chosen']]}` "
                f"| Correct: `{ANSWER_OPTIONS[log['correct']]}` "
                f"| Confidence: {log['confidence']} "
                f"| Score: `{delta_str}`"
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

    # Custom CSS for dark card feel and clean typography
    st.markdown(
        """
        <style>
        /* Slightly tighten default padding */
        .block-container { padding-top: 2rem; padding-bottom: 2rem; }
        /* Make radio options larger */
        div[data-testid="stRadio"] label { font-size: 1rem !important; }
        /* Metric value colour */
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
