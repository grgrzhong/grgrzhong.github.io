"""
BWA-MEM – Step-by-Step Algorithm (BWT / FM-index)
==================================================
Render with:
    manim -pqh bwamem_stepbystep.py BwamemStepByStep

Shows:
1. Burrows-Wheeler Transform (BWT) on the string "BANANA$"
2. FM-index backward search for a query pattern "ANA"
3. Suffix Array lookup to retrieve genome positions
4. MEM extension on both sides to form the maximal match
"""

from manim import *

BWT_COLOR = BLUE_C
QUERY_COLOR = YELLOW
MATCH_COLOR = GREEN
SA_COLOR = TEAL
POINTER_COLOR = RED


class BwamemStepByStep(Scene):
    def construct(self):
        self.camera.background_color = "#1e1e2e"

        # ──────────────────────────────────────────────
        # SECTION 1: Burrows-Wheeler Transform
        # ──────────────────────────────────────────────
        self._section_header(
            "Step 1 of 4 – Burrows-Wheeler Transform (BWT)", BWT_COLOR
        )
        self.wait(0.3)

        original = "BANANA$"
        orig_label = Text(
            f'Input string:  "{original}"', font_size=24, color=WHITE
        )
        orig_label.move_to([0, 1.6, 0])
        self.play(Write(orig_label))
        self.wait(0.3)

        # Rotations
        rotations = [original[i:] + original[:i] for i in range(len(original))]
        rot_group = (
            VGroup(
                *[
                    Text(r, font_size=19, color=GREY_A, font="Courier")
                    for r in rotations
                ]
            )
            .arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            .move_to([-2.5, -0.1, 0])
        )
        rot_title = Text("All rotations", font_size=18, color=GREY_B).next_to(
            rot_group, UP, buff=0.15
        )
        self.play(
            FadeIn(rot_title),
            LaggedStart(*[FadeIn(r) for r in rot_group], lag_ratio=0.08),
        )
        self.wait(0.4)

        # Sorted rotations + BWT column
        sorted_rots = sorted(rotations)
        bwt_chars = [r[-1] for r in sorted_rots]
        bwt_string = "".join(bwt_chars)

        sorted_group = (
            VGroup(
                *[
                    Text(r, font_size=19, color=WHITE, font="Courier")
                    for r in sorted_rots
                ]
            )
            .arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            .move_to([1.5, -0.1, 0])
        )
        sort_title = Text(
            "Sorted → BWT last column", font_size=18, color=GREY_B
        ).next_to(sorted_group, UP, buff=0.15)
        bwt_highlight = VGroup(
            *[
                Text(
                    r[-1], font_size=19, color=MATCH_COLOR, font="Courier"
                ).move_to(sorted_group[i].get_right() + RIGHT * 0.15)
                for i, r in enumerate(sorted_rots)
            ]
        )

        self.play(Transform(rot_group.copy(), sorted_group), FadeIn(sort_title))
        self.play(FadeIn(sorted_group))
        self.play(
            LaggedStart(*[FadeIn(b) for b in bwt_highlight], lag_ratio=0.08)
        )

        bwt_result = Text(
            f'BWT(BANANA$) = "{bwt_string}"', font_size=22, color=MATCH_COLOR
        )
        bwt_result.to_edge(DOWN, buff=0.5)
        self.play(Write(bwt_result))
        self.wait(1)
        self.play(
            *[
                FadeOut(m)
                for m in [
                    orig_label,
                    rot_group,
                    rot_title,
                    sorted_group,
                    sort_title,
                    *bwt_highlight,
                    bwt_result,
                ]
            ]
        )

        # ──────────────────────────────────────────────
        # SECTION 2: FM-index Backward Search
        # ──────────────────────────────────────────────
        self._section_header(
            "Step 2 of 4 – FM-index Backward Search", QUERY_COLOR
        )
        self.wait(0.3)

        query = "ANA"
        q_label = Text(
            f'Query: "{query}"  (search right → left)',
            font_size=22,
            color=QUERY_COLOR,
        )
        q_label.move_to([0, 1.5, 0])
        self.play(Write(q_label))

        # Simplified SA/BWT rows
        bwt_display = [
            "BWT: A",
            "      N",
            "      N",
            "      B",
            "      A",
            "      A",
            "      $",
        ]
        bwt_col = (
            VGroup(
                *[
                    Text(line, font_size=17, color=WHITE, font="Courier")
                    for line in bwt_display
                ]
            )
            .arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            .move_to([-1.5, -0.2, 0])
        )
        self.play(LaggedStart(*[FadeIn(r) for r in bwt_col], lag_ratio=0.08))

        # Highlight rows matching "A" (first char of backward search = last char of ANA)
        highlight_rows = [0, 4, 5]
        highlights = VGroup(
            *[
                SurroundingRectangle(bwt_col[i], color=QUERY_COLOR, buff=0.05)
                for i in highlight_rows
            ]
        )
        step_lbl = Text(
            "1. Match 'A' → rows 0,4,5", font_size=17, color=QUERY_COLOR
        )
        step_lbl.move_to([3.2, 0.8, 0])
        self.play(Create(highlights), Write(step_lbl))
        self.wait(0.5)

        step_lbl2 = Text(
            "2. Match 'N' within range", font_size=17, color=MATCH_COLOR
        )
        step_lbl2.move_to([3.2, 0.3, 0])
        self.play(Write(step_lbl2))
        self.wait(0.5)

        step_lbl3 = Text(
            "3. Match 'A' → final range", font_size=17, color=GREEN
        )
        step_lbl3.move_to([3.2, -0.2, 0])
        self.play(Write(step_lbl3))
        self.wait(0.8)
        self.play(
            *[
                FadeOut(m)
                for m in [
                    q_label,
                    bwt_col,
                    highlights,
                    step_lbl,
                    step_lbl2,
                    step_lbl3,
                ]
            ]
        )

        # ──────────────────────────────────────────────
        # SECTION 3: Suffix Array → Genome Position
        # ──────────────────────────────────────────────
        self._section_header(
            "Step 3 of 4 – Suffix Array: Positions in Genome", SA_COLOR
        )
        self.wait(0.3)

        sa_data = [
            ("Row 0", "SA[0] = 6", "pos 6 → $"),
            ("Row 1", "SA[1] = 5", "pos 5 → A$"),
            ("Row 2", "SA[2] = 3", "pos 3 → ANA$   ← match"),
            ("Row 3", "SA[3] = 1", "pos 1 → ANANA$  ← match"),
            ("Row 4", "SA[4] = 0", "pos 0 → BANANA$"),
        ]
        sa_rows = (
            VGroup(
                *[
                    VGroup(
                        Text(r[0], font_size=16, color=GREY_A),
                        Text(r[1], font_size=16, color=SA_COLOR),
                        Text(
                            r[2],
                            font_size=16,
                            color=WHITE if "match" not in r[2] else MATCH_COLOR,
                        ),
                    ).arrange(RIGHT, buff=0.4)
                    for r in sa_data
                ]
            )
            .arrange(DOWN, aligned_edge=LEFT, buff=0.18)
            .move_to([0, 0.1, 0])
        )

        self.play(
            LaggedStart(*[FadeIn(row) for row in sa_rows], lag_ratio=0.15)
        )
        note = Text(
            "Genome positions 1 and 3 → MEM seed locations",
            font_size=18,
            color=MATCH_COLOR,
        ).to_edge(DOWN, buff=0.6)
        self.play(Write(note))
        self.wait(1)
        self.play(*[FadeOut(m) for m in [*sa_rows, note]])

        # ──────────────────────────────────────────────
        # SECTION 4: MEM Extension
        # ──────────────────────────────────────────────
        self._section_header(
            "Step 4 of 4 – MEM Extension (Grow Left & Right)", WHITE
        )
        self.wait(0.3)

        genome_str = "C A T A N A N A G T"
        gen_chars = genome_str.split()
        gen_row = self._char_row(
            gen_chars, 0.65, start_x=-3.0, y=1.2, colors=[WHITE] * 10
        )
        gen_lbl = Text("Genome", font_size=18, color=GREY_A).next_to(
            gen_row[0], LEFT, buff=0.2
        )
        self.play(FadeIn(gen_lbl), *[FadeIn(c) for c in gen_row])

        # Seed = positions 3-5 (ANA)
        seed_rect = SurroundingRectangle(
            VGroup(*gen_row[3:6]), color=QUERY_COLOR, buff=0.1
        )
        seed_lbl = Text("Seed (ANA)", font_size=15, color=QUERY_COLOR).next_to(
            seed_rect, UP, buff=0.1
        )
        self.play(Create(seed_rect), Write(seed_lbl))
        self.wait(0.4)

        # Extend left
        ext_left = SurroundingRectangle(
            VGroup(*gen_row[2:6]), color=MATCH_COLOR, buff=0.1
        )
        self.play(Transform(seed_rect, ext_left))
        lbl_ext = Text("Extend left…", font_size=15, color=MATCH_COLOR).next_to(
            ext_left, DOWN, buff=0.1
        )
        self.play(Write(lbl_ext))
        self.wait(0.4)

        # Extend right → mismatch at pos 6 (G)
        lbl_stop = Text(
            "Extend right… mismatch → STOP → MEM found",
            font_size=16,
            color=ORANGE,
        ).move_to([0, -0.4, 0])
        self.play(Write(lbl_stop))
        self.wait(1)

        summary = Text(
            "Repeat for all seeds → full set of MEMs → chain → extend",
            font_size=18,
            color=WHITE,
        ).to_edge(DOWN, buff=0.5)
        self.play(Write(summary))
        self.wait(2)

    # ── Helpers ───────────────────────────────────────────────────────────

    def _section_header(self, text: str, color=WHITE):
        hdr = Text(text, font_size=26, color=color)
        self.play(Write(hdr))
        self.wait(0.4)
        self.play(hdr.animate.scale(0.65).to_edge(UP, buff=0.25))

    def _char_row(self, chars, box_size, start_x, y, colors):
        mobs = []
        for i, (ch, col) in enumerate(zip(chars, colors)):
            x = start_x + i * (box_size + 0.08)
            box = Square(
                side_length=box_size,
                color=BLUE_D,
                fill_color=BLUE_D,
                fill_opacity=0.45,
            ).move_to([x, y, 0])
            lbl = Text(ch, font_size=int(box_size * 26), color=col).move_to(
                [x, y, 0]
            )
            mobs.append(VGroup(box, lbl))
        return mobs
