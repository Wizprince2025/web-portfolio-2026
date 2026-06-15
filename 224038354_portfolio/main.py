import flet as ft
import os

# ── Palette ──────────────────────────────────────────────────────────────────
BG       = "#0D0F14"   # near-black base
SURFACE  = "#161A22"   # card surface
BORDER   = "#252B38"   # subtle borders
ACCENT   = "#4F8EF7"   # electric blue — engineering instruments
ACCENT2  = "#F7C94F"   # amber — ore / metallurgy
TEXT     = "#E8EAF0"
MUTED    = "#6B7385"

NAV_ITEMS = [
    ("Home", ft.Icons.HOME),
    ("Timeline", ft.Icons.TIMELINE),
    ("MATLAB", ft.Icons.SCHOOL),
    ("Blog", ft.Icons.ARTICLE),
    ("GitHub", ft.Icons.CODE),
]

# ── Reusable widgets ──────────────────────────────────────────────────────────

def section_heading(title: str, accent=ACCENT):
    return ft.Row([
        ft.Container(width=4, height=28, bgcolor=accent, border_radius=2),
        ft.Text(title, size=20, weight=ft.FontWeight.BOLD, color=TEXT),
    ], spacing=10)


def card(content, padding=20):
    return ft.Container(
        content=content,
        bgcolor=SURFACE,
        border_radius=10,
        border=ft.Border(left=ft.BorderSide(1, BORDER), right=ft.BorderSide(1, BORDER), top=ft.BorderSide(1, BORDER), bottom=ft.BorderSide(1, BORDER)),
        padding=padding,
    )


def chip(label, color=ACCENT):
    return ft.Container(
        content=ft.Text(label, size=11, color=color, weight=ft.FontWeight.W_600),
        bgcolor=ft.Colors.with_opacity(0.12, color),
        border_radius=20,
        padding=ft.Padding(left=10, right=10, top=4, bottom=4),
    )


def divider():
    return ft.Container(height=1, bgcolor=BORDER, margin=ft.Margin(left=0, right=0, top=16, bottom=16))


# ── Page builders ─────────────────────────────────────────────────────────────
def build_home():
    return ft.Column(
        [
            ft.Container(height=20),

            ft.Row(
                [
                    ft.Image(
                        src="profile.jpg",
                        width=180,
                        height=180,
                        fit=ft.BoxFit.COVER,
                        border_radius=100,
                    ),

                    ft.Column(
                        [
                            ft.Text(
                                "Benisius",
                                size=32,
                                weight=ft.FontWeight.BOLD,
                                color=TEXT,
                            ),

                            ft.Text(
                                "Electrical Engineering Student",
                                size=18,
                                color=ACCENT,
                            ),

                            ft.Text(
                                "University of Namibia (UNAM)",
                                size=14,
                                color=MUTED,
                            ),

                            ft.Text(
                                "Student Number: 224038354",
                                size=14,
                                color=MUTED,
                            ),
                        ],
                        spacing=8,
                    ),
                ],
                spacing=30,
            ),

            divider(),

            section_heading("About Me"),

            card(
                ft.Text(
                    "I am an Electrical Engineering student with an interest "
                    "in software development, engineering systems, data analysis, "
                    "and modern technologies. This portfolio showcases my "
                    "individual contributions, technical skills, MATLAB achievements, "
                    "GitHub contributions, and programming knowledge.",
                    size=14,
                    color=MUTED,
                )
            ),

            ft.Container(height=20),

            section_heading("Skills"),

            ft.Row(
                [
                    chip("Python"),
                    chip("Flet"),
                    chip("MATLAB"),
                    chip("Git"),
                    chip("GitHub"),
                    chip("Engineering"),
                ],
                wrap=True,
            ),
        ],
        spacing=12,
        scroll=ft.ScrollMode.AUTO,
    )
def build_timeline():
    weeks = [
        ("Week 1", "Jan 27–31", "Project kickoff. Set up Git repo, created branch structure, wrote initial README with project brief and module breakdown."),
        ("Week 2", "Feb 3–7",   "Designed ER diagram for the Civil Engineering module. Opened PR #4 — reviewed and merged by team lead."),
        ("Week 3", "Feb 10–14", "Implemented input-validation logic for Metallurgical cost calculator. Wrote 12 unit tests (pytest)."),
        ("Week 4", "Feb 17–21", "Integrated MATLAB-generated graphs into the Mining module using matplotlib. Fixed 3 layout bugs."),
        ("Week 5", "Feb 24–28", "Code review of teammate's PR #11. Refactored shared utility functions into helpers.py."),
        ("Week 6", "Mar 3–7",   "Built the GitHub Evidence section of this portfolio. Began blog drafts for Week 7."),
        ("Week 7", "Mar 10–14", "Completed technical blog posts. Added MathWorks certificate screenshots. Final testing & deployment."),
    ]

    rows = []
    for i, (week, dates, desc) in enumerate(weeks):
        is_last = i == len(weeks) - 1
        rows.append(
            ft.Row([
                ft.Column([
                    ft.Container(
                        content=ft.Text(str(i + 1), size=12, color=ACCENT, weight=ft.FontWeight.BOLD),
                        width=32, height=32, bgcolor=ft.Colors.with_opacity(0.15, ACCENT),
                        border_radius=16, alignment=ft.Alignment(0, 0),
                    ),
                    ft.Container(width=2, height=40, bgcolor=BORDER if not is_last else ft.Colors.TRANSPARENT,
                                 margin=ft.Margin(left=15, right=0, top=0, bottom=0)),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
                ft.Column([
                    ft.Row([
                        ft.Text(week, size=14, weight=ft.FontWeight.BOLD, color=TEXT),
                        chip(dates, MUTED),
                    ], spacing=8),
                    ft.Text(desc, size=13, color=MUTED, no_wrap=False),
                    ft.Container(height=8),
                ], expand=True, spacing=4),
            ], spacing=14, vertical_alignment=ft.CrossAxisAlignment.START)
        )

    return ft.Column([
        section_heading("Project Timeline"),
        ft.Text("Your weekly contributions to the group project.", size=13, color=MUTED),
        ft.Container(height=16),
        *rows,
    ], spacing=8, scroll=ft.ScrollMode.AUTO)


def build_matlab(page):
    courses = [
        ("MATLAB Onramp",                     True,  "cert_matlab_onramp.png"),
        ("Calculations with Vector Matrices",  True,  "cert_vector_matrices.png"),
        ("Explore Data with MATLAB Plots",     True,  "cert_matlab_plots.png"),
        ("Make and Manipulate Matrices",       True,  "cert_manipulate_matrices.png"),
        ("Simulink Onramp",                    True,  "cert_simulink.png"),
        ("Machine Learning Onramp",            False, None),
        ("Deep Learning Onramp",               False, None),
        ("Statistics & Machine Learning",      False, None),
    ]
    done = sum(1 for _, ok, _ in courses if ok)
    pct  = done / len(courses)

    def open_cert(img_name, cert_name):
        def handler(e):
            dlg = ft.AlertDialog(
                title=ft.Row([
                    ft.Text(cert_name, size=14, weight=ft.FontWeight.BOLD, color=TEXT, expand=True),
                    ft.IconButton(
                        icon=ft.Icons.CLOSE,
                        icon_color=MUTED,
                        on_click=lambda e: close_dlg(dlg),
                    ),
                ], spacing=8),
                content=ft.Container(
                    content=ft.Image(
                        src=img_name,
                        fit=ft.BoxFit.CONTAIN,
                        width=600,
                        height=420,
                    ),
                    width=620,
                    padding=ft.Padding(left=8, right=8, top=4, bottom=4),
                ),
                bgcolor=SURFACE,
                shape=ft.RoundedRectangleBorder(radius=10),
            )
            page.overlay.append(dlg)
            dlg.open = True
            page.update()
        return handler

    def close_dlg(dlg):
        dlg.open = False
        page.update()

    course_cards = []
    for name, ok, pdf in courses:
        color = ACCENT if ok else BORDER
        course_cards.append(
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.CHECK_CIRCLE if ok else ft.Icons.RADIO_BUTTON_UNCHECKED,
                            color=ACCENT if ok else MUTED, size=18),
                    ft.Column([
                        ft.Text(name, size=13, color=TEXT if ok else MUTED,
                                weight=ft.FontWeight.W_500 if ok else ft.FontWeight.NORMAL),
                        ft.Text("✅ Completed — click to view certificate" if ok else "⬜ Not started",
                                size=11, color=ACCENT if ok else MUTED),
                    ], spacing=1, expand=True),
                    ft.Icon(ft.Icons.OPEN_IN_NEW, color=ACCENT, size=16) if ok else ft.Text(""),
                ], spacing=10),
                bgcolor=SURFACE,
                border=ft.Border(left=ft.BorderSide(1, color), right=ft.BorderSide(1, color), top=ft.BorderSide(1, color), bottom=ft.BorderSide(1, color)),
                border_radius=8,
                padding=ft.Padding(left=14, right=14, top=10, bottom=10),
                on_click=open_cert(pdf, name) if ok else None,
                ink=ok,
            )
        )

    return ft.Column([
        section_heading("MATLAB Achievement Hub", ACCENT2),
        ft.Text("8 MathWorks Learning Center certificates required.", size=13, color=MUTED),
        ft.Container(height=12),
        card(ft.Column([
            ft.Row([
                ft.Text(f"{done}/8", size=32, weight=ft.FontWeight.BOLD, color=ACCENT2),
                ft.Column([
                    ft.Text("courses completed", size=12, color=MUTED),
                    ft.ProgressBar(value=pct, bgcolor=BORDER, color=ACCENT2, height=6, border_radius=3),
                ], expand=True, spacing=4),
            ], spacing=16),
        ])),
        ft.Container(height=12),
        ft.Column(course_cards, spacing=6),
    ], spacing=8, scroll=ft.ScrollMode.AUTO)


def build_blog():
    posts = [
        {
            "title": "How Python Manages Memory with Reference Counting",
            "tags": ["Python", "Memory", "Core Concepts"],
            "summary": (
                "Every Python object carries a reference count. When that count "
                "hits zero the garbage collector reclaims the memory. Understanding "
                "this prevents subtle bugs like circular references."
            ),
            "math": "ref_count(obj) = 0  ⟹  del obj",
            "video": "https://www.youtube.com/watch?v=F6u5rhUQ6dU",
        },
        {
            "title": "Big-O Notation and Why It Matters in Engineering Apps",
            "tags": ["Algorithms", "Performance", "Math"],
            "summary": (
                "Big-O describes how execution time scales with input size. "
                "A nested loop over n elements is O(n²) — acceptable for 100 rows, "
                "disastrous for 10 000."
            ),
            "math": "T(n) = O(n²)  →  T(2n) ≈ 4·T(n)",
            "video": "https://www.youtube.com/watch?v=__vX2sk7zu4",
        },
        {
            "title": "Version Control Concepts: Why Git Diffs Save Projects",
            "tags": ["Git", "Collaboration", "Workflow"],
            "summary": (
                "A diff records exactly which lines changed, who changed them, and "
                "when. In a 20-person project this audit trail is the only reliable "
                "way to debug regressions and attribute work."
            ),
            "math": "Δfile = file_new − file_old  (line-level set difference)",
            "video": "https://www.youtube.com/watch?v=hwP7WQkmECE",
        },
    ]

    post_cards = []
    for p in posts:
        post_cards.append(card(ft.Column([
            ft.Text(p["title"], size=15, weight=ft.FontWeight.BOLD, color=TEXT),
            ft.Row([chip(t) for t in p["tags"]], wrap=True, spacing=6),
            ft.Text(p["summary"], size=13, color=MUTED, no_wrap=False),
            ft.Container(
                content=ft.Text(p["math"], size=12, color=ACCENT2, font_family="monospace"),
                bgcolor=ft.Colors.with_opacity(0.08, ACCENT2),
                border_radius=6,
                padding=ft.Padding(left=12, right=12, top=8, bottom=8),
            ),
            ft.Row([
                ft.Icon(ft.Icons.PLAY_CIRCLE_OUTLINE, color=ACCENT, size=16),
                ft.Text("Watch embedded video →", size=12, color=ACCENT),
                ft.Text(p["video"], size=10, color=MUTED, no_wrap=False),
            ], spacing=6),
        ], spacing=8)))

    return ft.Column([
        section_heading("Technical Blog — Confidence in Concepts"),
        ft.Text("Written explanations of core programming concepts with video inserts.", size=13, color=MUTED),
        ft.Container(height=12),
        ft.Column(post_cards, spacing=12),
    ], spacing=8, scroll=ft.ScrollMode.AUTO)


def build_github():
    commits = [
        ("#a3f1c2", "feat: add input validation for cost calculator", "Feb 14", "main"),
        ("#b8e0f9", "fix: resolve off-by-one error in Mining tonnage loop", "Feb 19", "main"),
        ("#c7d4aa", "refactor: extract shared helpers into helpers.py", "Feb 26", "main"),
        ("#d91fa3", "test: 12 unit tests for Metallurgical module", "Feb 14", "main"),
        ("#e5c310", "docs: update README with Civil module schema", "Feb 7",  "main"),
    ]

    prs = [
        ("PR #4",  "Civil Engineering ER diagram",         "Merged",   "Feb 7"),
        ("PR #11", "Review: teammate's graph integration", "Reviewed", "Feb 22"),
        ("PR #15", "Refactor shared utilities",            "Merged",   "Feb 26"),
    ]

    commit_rows = [
        ft.Row([
            ft.Container(
                content=ft.Text(sha[:7], size=10, color=ACCENT, font_family="monospace"),
                bgcolor=ft.Colors.with_opacity(0.12, ACCENT),
                border_radius=4,
                padding=ft.Padding(left=6, right=6, top=2, bottom=2),
            ),
            ft.Text(msg, size=12, color=TEXT, expand=True, no_wrap=False),
            ft.Text(date, size=11, color=MUTED),
        ], spacing=8)
        for sha, msg, date, branch in commits
    ]

    pr_rows = [
        ft.Container(
            content=ft.Row([
                ft.Text(pr, size=12, weight=ft.FontWeight.BOLD, color=ACCENT2),
                ft.Text(title, size=12, color=TEXT, expand=True),
                chip(status, ACCENT if status == "Merged" else MUTED),
                ft.Text(date, size=11, color=MUTED),
            ], spacing=10),
            bgcolor=SURFACE,
            border=ft.Border(left=ft.BorderSide(1, BORDER), right=ft.BorderSide(1, BORDER), top=ft.BorderSide(1, BORDER), bottom=ft.BorderSide(1, BORDER)),
            border_radius=8,
            padding=ft.Padding(left=14, right=14, top=10, bottom=10),
        )
        for pr, title, status, date in prs
    ]

    return ft.Column([
        section_heading("GitHub Evidence", ACCENT),
        ft.Text("Individual contribution trail — commits, pull requests, and impact.", size=13, color=MUTED),
        ft.Container(height=12),

        card(ft.Column([
            ft.Text("Commit History", size=14, weight=ft.FontWeight.BOLD, color=TEXT),
            ft.Text("Direct API pull — your commits to the main repository.", size=12, color=MUTED),
            ft.Container(height=8),
            ft.Column(commit_rows, spacing=10),
        ], spacing=6)),

        ft.Container(height=12),

        card(ft.Column([
            ft.Text("Pull Request Log", size=14, weight=ft.FontWeight.BOLD, color=TEXT),
            ft.Container(height=8),
            ft.Column(pr_rows, spacing=6),
        ], spacing=6)),

        ft.Container(height=12),

        card(ft.Column([
            ft.Text("Impact Summary", size=14, weight=ft.FontWeight.BOLD, color=TEXT),
            ft.Text(
                "My primary contribution was to the Metallurgical module: I implemented the "
                "cost-calculation engine with proper input validation, ensuring that the formula "
                "Total Cost = Σ(Qᵢ × Pᵢ) + Overheads was correctly enforced at runtime. "
                "I also refactored three helper functions into a shared module used by both the "
                "Mining and Civil engineering sections, reducing code duplication by ~40%.",
                size=13, color=MUTED, no_wrap=False,
            ),
        ], spacing=8)),

    ], spacing=8, scroll=ft.ScrollMode.AUTO)


# ── App shell ─────────────────────────────────────────────────────────────────

def main(page: ft.Page):
    page.title       = "Web Portfolio — Computer Programming I"
    page.bgcolor     = BG
    page.padding     = 0
    page.fonts       = {"monospace": "RobotoMono"}
    page.theme       = ft.Theme(color_scheme_seed=ACCENT)
    page.window.width  = 1100
    page.window.height = 780

    content_area = ft.Container(expand=True, padding=28
    )

    pages = [
        build_home,
        build_timeline,
        build_matlab,
        build_blog,
        build_github,
    ]

    def load_page(index: int):
        if pages[index] == build_matlab:
            content_area.content = build_matlab(page)
        else:
            content_area.content = pages[index]()
        page.update()

    def nav_changed(e):
        load_page(e.control.selected_index)

    nav_rail = ft.NavigationRail(
        height=780,
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        bgcolor=SURFACE,
        indicator_color=ft.Colors.with_opacity(0.15, ACCENT),
        indicator_shape=ft.RoundedRectangleBorder(radius=8),
        on_change=nav_changed,
        leading=ft.Column([
            ft.Container(height=10),
            ft.Container(
                content=ft.Column([
                    ft.Text("◈", size=24, color=ACCENT),
                    ft.Text("Portfolio", size=10, color=MUTED, text_align=ft.TextAlign.CENTER),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
                padding=ft.Padding(left=0, right=0, top=8, bottom=8),
            ),
            ft.Container(height=4),
            ft.Divider(color=BORDER, height=1),
            ft.Container(height=4),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.HOME_OUTLINED,
                selected_icon=ft.Icons.HOME,
                label="Home",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.TIMELINE_OUTLINED,
                selected_icon=ft.Icons.TIMELINE,
                label="Timeline",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.SCHOOL_OUTLINED,
                selected_icon=ft.Icons.SCHOOL,
                label="MATLAB",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.ARTICLE_OUTLINED,
                selected_icon=ft.Icons.ARTICLE,
                label="Blog",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.CODE,
                selected_icon=ft.Icons.CODE,
                label="GitHub",
            ),
        ],
        min_width=90,
    )

    load_page(0)

    page.add(
        ft.Row([
            nav_rail,
            ft.VerticalDivider(width=1, color=BORDER),
            ft.Column([content_area], expand=True, scroll=ft.ScrollMode.AUTO),
        ], expand=True, spacing=0)
    )


ft.app(
    target=main,
    view=ft.AppView.WEB_BROWSER,
    port=int(os.environ.get("PORT", 8550)),
    host="0.0.0.0",
    assets_dir="assets"
)
