"""
BWA-MEM – Conceptual Overview Animation
========================================
Render with:
    manim -pqh bwamem_conceptual.py BwamemConceptual

Shows:
1. A read is shown as a string of bases
2. Maximal Exact Matches (MEMs) are found on the reference
3. MEMs are chained into a colinear chain
4. Gaps between MEMs are filled via Smith-Waterman extension
5. Final alignment in SAM format with CIGAR string
"""

from manim import *

REF_COLOR = BLUE_D
READ_COLOR = YELLOW
MEM_COLOR = GREEN
CHAIN_COLOR = ORANGE
GAP_COLOR = RED_B


class BwamemConceptual(Scene):
    def construct(self):
        self.camera.background_color = "#1e1e2e"

        title = Text(
            "BWA-MEM: Alignment – Conceptual Overview",
            font_size=34,
            color=WHITE,
        ).to_edge(UP, buff=0.4)
        self.play(Write(title))
        self.wait(0.4)

        # ── Reference track ───────────────────────────────────────────────
        ref_label = Text("Reference", font_size=20, color=GREY_A).move_to(
            [-5.5, 1.5, 0]
        )
        ref_bar = Rectangle(
            width=10.5,
            height=0.5,
            color=REF_COLOR,
            fill_color=REF_COLOR,
            fill_opacity=0.4,
        ).move_to([0.2, 1.5, 0])
        self.play(FadeIn(ref_label), FadeIn(ref_bar))

        # Position ticks
        ticks = VGroup(
            *[
                VGroup(
                    Line([x, 1.25, 0], [x, 1.75, 0], color=GREY_B),
                    Text(str(i * 50), font_size=11, color=GREY_B).move_to(
                        [x, 1.05, 0]
                    ),
                )
                for i, x in enumerate([-4.8, -2.3, 0.2, 2.7, 5.2])
            ]
        )
        self.play(LaggedStart(*[FadeIn(t) for t in ticks], lag_ratio=0.1))

        # ── Read bar ──────────────────────────────────────────────────────
        read_label = Text("Read (150 bp)", font_size=20, color=GREY_A).move_to(
            [-5.5, -0.2, 0]
        )
        read_bar = Rectangle(
            width=5.5,
            height=0.5,
            color=READ_COLOR,
            fill_color=READ_COLOR,
            fill_opacity=0.55,
        ).move_to([-1.0, -0.2, 0])
        self.play(FadeIn(read_label), FadeIn(read_bar))
        self.wait(0.4)

        # ── Step 1: MEM discovery ─────────────────────────────────────────
        step = self._step_label(
            "Step 1: Find Maximal Exact Matches (MEMs) in the FM-index"
        )
        self.play(Write(step))

        mem1 = Rectangle(
            width=1.8,
            height=0.5,
            color=MEM_COLOR,
            fill_color=MEM_COLOR,
            fill_opacity=0.85,
        ).move_to([-3.1, 1.5, 0])
        mem2 = Rectangle(
            width=1.6,
            height=0.5,
            color=MEM_COLOR,
            fill_color=MEM_COLOR,
            fill_opacity=0.85,
        ).move_to([0.5, 1.5, 0])
        mem3 = Rectangle(
            width=1.2,
            height=0.5,
            color=MEM_COLOR,
            fill_color=MEM_COLOR,
            fill_opacity=0.85,
        ).move_to([3.3, 1.5, 0])
        mem_lbl1 = Text("MEM 1", font_size=13, color=BLACK).move_to(mem1)
        mem_lbl2 = Text("MEM 2", font_size=13, color=BLACK).move_to(mem2)
        mem_lbl3 = Text("MEM 3", font_size=13, color=BLACK).move_to(mem3)

        self.play(
            LaggedStart(
                FadeIn(mem1),
                FadeIn(mem_lbl1),
                FadeIn(mem2),
                FadeIn(mem_lbl2),
                FadeIn(mem3),
                FadeIn(mem_lbl3),
                lag_ratio=0.25,
            )
        )
        self.wait(0.6)

        # ── Step 2: Chaining ──────────────────────────────────────────────
        step2 = self._step_label(
            "Step 2: Chain colinear MEMs (same strand, consistent positions)"
        )
        self.play(Transform(step, step2))

        chain_arrow = Arrow(
            [-4.0, 1.85, 0], [3.9, 1.85, 0], color=CHAIN_COLOR, stroke_width=3
        )
        chain_label = Text("Colinear chain", font_size=16, color=CHAIN_COLOR)
        chain_label.next_to(chain_arrow, UP, buff=0.1)
        self.play(Create(chain_arrow), Write(chain_label))
        self.wait(0.6)

        # ── Step 3: Gap extension ─────────────────────────────────────────
        step3 = self._step_label(
            "Step 3: Fill gaps between MEMs using Smith-Waterman extension"
        )
        self.play(Transform(step, step3))

        gap1 = Rectangle(
            width=0.9,
            height=0.5,
            color=GAP_COLOR,
            fill_color=GAP_COLOR,
            fill_opacity=0.6,
        ).move_to([-1.65, 1.5, 0])
        gap2 = Rectangle(
            width=0.9,
            height=0.5,
            color=GAP_COLOR,
            fill_color=GAP_COLOR,
            fill_opacity=0.6,
        ).move_to([2.15, 1.5, 0])
        gap_lbl1 = Text("SW", font_size=13, color=WHITE).move_to(gap1)
        gap_lbl2 = Text("SW", font_size=13, color=WHITE).move_to(gap2)
        self.play(
            FadeIn(gap1), FadeIn(gap_lbl1), FadeIn(gap2), FadeIn(gap_lbl2)
        )
        self.wait(0.8)

        # ── Step 4: SAM output ────────────────────────────────────────────
        step4 = self._step_label("Step 4: Emit SAM record with CIGAR string")
        self.play(Transform(step, step4))

        cigar_text = Text(
            "read1   0   chr1   1001   60   30M5I40M3D75M   *   0   0",
            font_size=15,
            color=WHITE,
            font="Courier",
        ).move_to([0.5, -1.5, 0])
        cigar_box = SurroundingRectangle(cigar_text, color=GREY_B, buff=0.15)
        sam_label = Text("SAM output", font_size=16, color=GREY_A).next_to(
            cigar_box, LEFT, buff=0.2
        )
        self.play(FadeIn(cigar_box), Write(cigar_text), FadeIn(sam_label))
        self.wait(2)

    def _step_label(self, text: str):
        return Text(text, font_size=19, color=YELLOW).to_edge(DOWN, buff=1.0)
