"""
Bowtie2 – Step-by-Step Algorithm Animation
===========================================
Render with:
    manim -pqh bowtie2_stepbystep.py Bowtie2StepByStep

Shows:
1. FM-index backward search (same BWT principle as BWA, but Bowtie2-flavored)
2. Dynamic programming alignment scoring matrix (simplified 5×5)
3. Traceback path → CIGAR string
4. Preset comparison table (very-fast → very-sensitive-local)
"""

from manim import *

FM_COLOR = BLUE_C
DP_COLOR = TEAL
TRACE_COLOR = ORANGE
PRESET_BAR_COLORS = [RED, ORANGE, YELLOW, GREEN_B, GREEN_D]


class Bowtie2StepByStep(Scene):
    def construct(self):
        self.camera.background_color = "#1e1e2e"

        # ──────────────────────────────────────────────
        # SECTION 1: FM-Index Lookup
        # ──────────────────────────────────────────────
        self._section_header(
            "Step 1 of 4 – FM-index Seed Lookup (same as BWA)", FM_COLOR
        )
        self.wait(0.3)

        note = Text(
            "Bowtie2 uses an FM-index built on the BWT of the reference.\n"
            "Seeds (substrings of the read) are looked up in O(seed length) time.",
            font_size=19,
            color=WHITE,
            line_spacing=1.4,
        ).move_to([0, 0.6, 0])
        self.play(Write(note))

        bwt_note = Text(
            "Key difference from BWA-MEM:\nBowtie2 uses fixed-length seeds + DP scoring\n"
            "BWA-MEM uses variable-length MEMs + SW extension",
            font_size=18,
            color=YELLOW,
            line_spacing=1.4,
        ).move_to([0, -1.0, 0])
        self.play(Write(bwt_note))
        self.wait(1.2)
        self.play(FadeOut(note), FadeOut(bwt_note))

        # ──────────────────────────────────────────────
        # SECTION 2: DP Scoring Matrix
        # ──────────────────────────────────────────────
        self._section_header(
            "Step 2 of 4 – Dynamic Programming Scoring Matrix", DP_COLOR
        )
        self.wait(0.3)

        ref_chars = ["-", "A", "T", "G", "C", "A"]
        read_chars = ["-", "A", "T", "G", "C"]

        # Score values (manual, simple match=+2 mismatch=-2 gap=-3)
        scores = [
            [0, -3, -6, -9, -12, -15],
            [-3, 2, -1, -4, -7, -10],
            [-6, -1, 4, 1, -2, -5],
            [-9, -4, 1, 6, 3, 0],
            [-12, -7, -2, 3, 8, 5],
        ]

        cell_size = 0.68
        start_x, start_y = -2.0, 1.5

        # Header row (ref)
        ref_row = VGroup(
            *[
                Text(ch, font_size=20, color=BLUE_B if i > 0 else GREY).move_to(
                    [start_x + i * cell_size, start_y + cell_size, 0]
                )
                for i, ch in enumerate(ref_chars)
            ]
        )
        # Header col (read)
        read_col = VGroup(
            *[
                Text(ch, font_size=20, color=TEAL if i > 0 else GREY).move_to(
                    [start_x - cell_size, start_y - i * cell_size, 0]
                )
                for i, ch in enumerate(read_chars)
            ]
        )

        self.play(FadeIn(ref_row), FadeIn(read_col))

        # Draw cells
        cells = []
        score_texts = []
        for r in range(5):
            for c in range(6):
                x = start_x + c * cell_size
                y = start_y - r * cell_size
                cell = Square(
                    side_length=cell_size,
                    color=GREY_C,
                    fill_color=DARK_GREY,
                    fill_opacity=0.5,
                ).move_to([x, y, 0])
                score = scores[r][c]
                col = GREEN_B if score > 0 else (RED_B if score < 0 else WHITE)
                txt = Text(str(score), font_size=16, color=col).move_to(
                    [x, y, 0]
                )
                cells.append(cell)
                score_texts.append(txt)

        self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.04))
        self.play(
            LaggedStart(*[FadeIn(t) for t in score_texts], lag_ratio=0.04)
        )
        self.wait(0.5)

        # ── Best score highlight ──────────────────────────────────────────
        best_cell_idx = 4 * 6 + 4  # row=4, col=4 → score=8
        best_cell = cells[best_cell_idx]
        best_highlight = SurroundingRectangle(
            best_cell, color=ORANGE, buff=0.04, stroke_width=3
        )
        self.play(Create(best_highlight))
        best_lbl = Text("Best score = 8", font_size=17, color=ORANGE).move_to(
            [3.5, 0.2, 0]
        )
        self.play(Write(best_lbl))
        self.wait(0.6)
        self.play(
            *[
                FadeOut(m)
                for m in [
                    *cells,
                    *score_texts,
                    ref_row,
                    read_col,
                    best_highlight,
                    best_lbl,
                ]
            ]
        )

        # ──────────────────────────────────────────────
        # SECTION 3: Traceback → CIGAR
        # ──────────────────────────────────────────────
        self._section_header(
            "Step 3 of 4 – Traceback → CIGAR String", TRACE_COLOR
        )
        self.wait(0.3)

        traceback_text = (
            VGroup(
                Text(
                    "Traceback path (diagonal = match/mismatch, up = deletion, left = insertion)",
                    font_size=17,
                    color=WHITE,
                ),
                Text(
                    "Example: diagonal → diagonal → diagonal → diagonal",
                    font_size=17,
                    color=GREY_A,
                ),
                Text("→  CIGAR: 4M", font_size=22, color=TRACE_COLOR),
            )
            .arrange(DOWN, buff=0.25, aligned_edge=LEFT)
            .move_to([0, 0.4, 0])
        )
        self.play(
            LaggedStart(*[Write(t) for t in traceback_text], lag_ratio=0.4)
        )

        cigar_box_txt = Text(
            "CIGAR codes:  M=match/mismatch   I=insertion   D=deletion   S=soft-clip",
            font_size=16,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.8)
        self.play(FadeIn(cigar_box_txt))
        self.wait(0.8)
        self.play(*[FadeOut(m) for m in [*traceback_text, cigar_box_txt]])

        # ──────────────────────────────────────────────
        # SECTION 4: Preset Speed/Sensitivity Table
        # ──────────────────────────────────────────────
        self._section_header(
            "Step 4 of 4 – Presets: Speed vs Sensitivity Trade-off", WHITE
        )
        self.wait(0.3)

        presets = [
            ("--very-fast(-local)", "fastest", "lowest", 1.0),
            ("--fast(-local)", "fast", "moderate", 2.5),
            ("--sensitive(-local)", "moderate", "good", 4.0),
            ("--very-sensitive(-local)", "slow", "highest", 6.0),
        ]
        preset_col_color = [RED, ORANGE, YELLOW, GREEN_D]

        rows = (
            VGroup(
                *[
                    VGroup(
                        Text(
                            p[0],
                            font_size=16,
                            color=preset_col_color[i],
                            font="Courier",
                        ),
                        Text(f"Speed: {p[1]}", font_size=15, color=GREY_A),
                        Text(
                            f"Sensitivity: {p[2]}", font_size=15, color=GREY_A
                        ),
                        Rectangle(
                            width=p[3],
                            height=0.3,
                            color=preset_col_color[i],
                            fill_color=preset_col_color[i],
                            fill_opacity=0.7,
                        ),
                    ).arrange(RIGHT, buff=0.3)
                    for i, p in enumerate(presets)
                ]
            )
            .arrange(DOWN, aligned_edge=LEFT, buff=0.25)
            .move_to([0, 0.1, 0])
        )

        self.play(LaggedStart(*[FadeIn(row) for row in rows], lag_ratio=0.2))
        tip = Text(
            "Tip: --very-sensitive-local is best for ATAC-seq / ChIP-seq",
            font_size=17,
            color=TEAL,
        ).to_edge(DOWN, buff=0.5)
        self.play(Write(tip))
        self.wait(2)

    def _section_header(self, text: str, color=WHITE):
        hdr = Text(text, font_size=24, color=color)
        self.play(Write(hdr))
        self.wait(0.4)
        self.play(hdr.animate.scale(0.65).to_edge(UP, buff=0.25))
