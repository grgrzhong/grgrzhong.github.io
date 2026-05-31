"""
STAR Aligner – Step-by-Step Algorithm Animation
================================================
Render with:
    manim -pqh star_stepbystep.py StarStepByStep

Shows:
1. Suffix Array index construction on a short genome snippet
2. Seed lookup: read segments hit index positions
3. Clustering seeds → candidate alignment windows
4. Two-pass strategy: pass 1 discovers novel junctions, pass 2 uses them
5. Final BAM record construction
"""

from manim import *

EXON_COLOR = BLUE_D
SEED_COLOR = YELLOW
CLUSTER_COLOR = GREEN_D
PASS1_COLOR = ORANGE
PASS2_COLOR = TEAL


class StarStepByStep(Scene):
    def construct(self):
        self.camera.background_color = "#1e1e2e"

        # ──────────────────────────────────────────────
        # SECTION 1: Genome Index (Suffix Array concept)
        # ──────────────────────────────────────────────
        self._section_header(
            "Step 1 of 4 – Genome Index (Suffix Array)", BLUE_B
        )
        self.wait(0.3)

        genome_seq = "ACGTATGCGT"
        genome_text = self._make_sequence_row(
            genome_seq, 0.55, start_x=-2.8, y=1.5, box_color=EXON_COLOR
        )
        genome_label = Text(
            "Reference (excerpt)", font_size=20, color=GREY_A
        ).next_to(genome_text[0], LEFT, buff=0.3)
        self.play(FadeIn(genome_label), *[FadeIn(b) for b in genome_text])
        self.wait(0.4)

        # Show first 4 suffixes
        suffixes = [genome_seq[i:] for i in range(len(genome_seq))][:5]
        suffix_labels = (
            VGroup(
                *[
                    Text(f"{i}: {s}", font_size=16, color=WHITE)
                    for i, s in enumerate(suffixes)
                ]
            )
            .arrange(DOWN, aligned_edge=LEFT, buff=0.15)
            .move_to([1.8, 0.4, 0])
        )
        sa_title = Text(
            "Suffixes (→ Suffix Array)", font_size=18, color=GREY_B
        ).next_to(suffix_labels, UP, buff=0.15)
        self.play(
            FadeIn(sa_title),
            LaggedStart(*[FadeIn(l) for l in suffix_labels], lag_ratio=0.12),
        )
        self.wait(0.5)

        sorted_label = Text(
            "Sorted → enables O(log N) search", font_size=16, color=GREEN
        ).next_to(suffix_labels, DOWN, buff=0.25)
        self.play(Write(sorted_label))
        self.wait(1)
        self.play(
            FadeOut(
                VGroup(
                    genome_label,
                    sa_title,
                    sorted_label,
                    suffix_labels,
                    *genome_text,
                )
            )
        )

        # ──────────────────────────────────────────────
        # SECTION 2: Seed Lookup (MMP – Maximal Mappable Prefix)
        # ──────────────────────────────────────────────
        self._section_header(
            "Step 2 of 4 – Seed Lookup (MMP Seeding)", SEED_COLOR
        )
        self.wait(0.3)

        # Read
        read_seq = "TATGCG"
        read_text = self._make_sequence_row(
            read_seq, 0.7, start_x=-1.8, y=1.5, box_color=SEED_COLOR
        )
        read_label = Text("Read", font_size=20, color=GREY_A).next_to(
            read_text[0], LEFT, buff=0.3
        )
        self.play(FadeIn(read_label), *[FadeIn(b) for b in read_text])

        # Highlight seeds (windows)
        seed1_brace = Brace(
            VGroup(*read_text[0:3]), direction=DOWN, color=ORANGE
        )
        seed1_lbl = Text("Seed 1", font_size=14, color=ORANGE).next_to(
            seed1_brace, DOWN, buff=0.05
        )
        seed2_brace = Brace(
            VGroup(*read_text[2:6]), direction=DOWN, color=GREEN
        )
        seed2_lbl = Text("Seed 2", font_size=14, color=GREEN).next_to(
            seed2_brace, DOWN, buff=0.05
        )
        self.play(Create(seed1_brace), Write(seed1_lbl))
        self.wait(0.3)
        self.play(Create(seed2_brace), Write(seed2_lbl))

        # Arrows to genome positions
        genome_pos1 = Text(
            "Genome pos 3,7", font_size=16, color=ORANGE
        ).move_to([3.0, 1.5, 0])
        genome_pos2 = Text("Genome pos 4,9", font_size=16, color=GREEN).move_to(
            [3.0, 0.8, 0]
        )
        arr1 = Arrow(
            [-0.3, 0.9, 0], [2.1, 1.5, 0], color=ORANGE, stroke_width=2
        )
        arr2 = Arrow([0.5, 0.55, 0], [2.1, 0.8, 0], color=GREEN, stroke_width=2)
        self.play(Create(arr1), FadeIn(genome_pos1))
        self.play(Create(arr2), FadeIn(genome_pos2))
        self.wait(1)
        self.play(
            FadeOut(
                VGroup(
                    read_label,
                    seed1_brace,
                    seed1_lbl,
                    seed2_brace,
                    seed2_lbl,
                    arr1,
                    arr2,
                    genome_pos1,
                    genome_pos2,
                    *read_text,
                )
            )
        )

        # ──────────────────────────────────────────────
        # SECTION 3: Seed Clustering → Alignment Window
        # ──────────────────────────────────────────────
        self._section_header(
            "Step 3 of 4 – Clustering Seeds → Alignment Windows", CLUSTER_COLOR
        )
        self.wait(0.3)

        # Simple axis line (avoid NumberLine with LaTeX labels)
        axis_line = Line(
            [-4.5, 0.8, 0], [4.5, 0.8, 0], color=GREY, stroke_width=3
        )
        axis_ticks = VGroup(
            *[
                VGroup(
                    Line(
                        [x, 0.65, 0], [x, 0.95, 0], color=GREY, stroke_width=2
                    ),
                    Text(str(n), font_size=14, color=GREY_B).move_to(
                        [x, 0.45, 0]
                    ),
                )
                for x, n in [
                    (-4.5, 0),
                    (-2.25, 5),
                    (0.0, 10),
                    (2.25, 15),
                    (4.5, 20),
                ]
            ]
        )
        axis_label = Text(
            "Genome position", font_size=16, color=GREY_A
        ).move_to([0, 0.15, 0])
        self.play(Create(axis_line), FadeIn(axis_ticks), FadeIn(axis_label))

        # Seed hit dots (manually positioned along the axis)
        # Positions 3,4.2,7.1,7.9,9 map linearly onto [-4.5,4.5] for [0,20]
        def pos_to_x(p):
            return -4.5 + (p / 20.0) * 9.0

        dot_positions = [3.0, 4.2, 7.1, 7.9, 9.0]
        dots = VGroup(
            *[
                Dot([pos_to_x(p), 0.8, 0], color=SEED_COLOR, radius=0.12)
                for p in dot_positions
            ]
        )
        dot_lbl = Text("Seed hits", font_size=16, color=SEED_COLOR).move_to(
            [0, 1.8, 0]
        )
        self.play(
            LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.15),
            FadeIn(dot_lbl),
        )
        self.wait(0.4)

        # Cluster 1 box (dots[2], dots[3], dots[4])
        cluster_box = SurroundingRectangle(
            VGroup(dots[2], dots[3], dots[4]),
            color=CLUSTER_COLOR,
            buff=0.25,
            corner_radius=0.1,
        )
        cluster_lbl = Text(
            "Best cluster\n→ Alignment window",
            font_size=16,
            color=CLUSTER_COLOR,
        )
        cluster_lbl.next_to(cluster_box, DOWN, buff=0.2)
        self.play(Create(cluster_box), Write(cluster_lbl))
        self.wait(1)
        self.play(
            FadeOut(
                VGroup(
                    axis_line,
                    axis_ticks,
                    axis_label,
                    dots,
                    dot_lbl,
                    cluster_box,
                    cluster_lbl,
                )
            )
        )

        # ──────────────────────────────────────────────
        # SECTION 4: Two-Pass Strategy
        # ──────────────────────────────────────────────
        self._section_header("Step 4 of 4 – Two-Pass Alignment Strategy", WHITE)
        self.wait(0.3)

        # Timeline
        pass1_box = RoundedRectangle(
            width=4.5,
            height=1.1,
            color=PASS1_COLOR,
            fill_color=PASS1_COLOR,
            fill_opacity=0.3,
            corner_radius=0.15,
        ).move_to([-2.5, 0.8, 0])
        pass1_txt = Text(
            "Pass 1\nAlign all reads → discover\nnovel splice junctions",
            font_size=16,
            color=PASS1_COLOR,
        ).move_to(pass1_box)

        arrow_between = Arrow([-0.2, 0.8, 0], [0.2, 0.8, 0], color=WHITE)

        pass2_box = RoundedRectangle(
            width=4.5,
            height=1.1,
            color=PASS2_COLOR,
            fill_color=PASS2_COLOR,
            fill_opacity=0.3,
            corner_radius=0.15,
        ).move_to([2.5, 0.8, 0])
        pass2_txt = Text(
            "Pass 2\nRebuild index + novel JXNs\n→ final alignment",
            font_size=16,
            color=PASS2_COLOR,
        ).move_to(pass2_box)

        self.play(FadeIn(pass1_box), Write(pass1_txt))
        self.play(Create(arrow_between))
        self.play(FadeIn(pass2_box), Write(pass2_txt))
        self.wait(0.5)

        # Output row
        output_items = [
            "sorted BAM",
            "SJ.out.tab",
            "ReadsPerGene.out.tab",
            "Log.final.out",
        ]
        output_row = (
            VGroup(
                *[
                    Text(f"• {item}", font_size=16, color=WHITE)
                    for item in output_items
                ]
            )
            .arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            .move_to([0, -1.1, 0])
        )
        out_title = Text(
            "Key output files:", font_size=18, color=GREY_A
        ).next_to(output_row, UP, buff=0.2)
        self.play(
            FadeIn(out_title),
            LaggedStart(*[FadeIn(o) for o in output_row], lag_ratio=0.15),
        )
        self.wait(2)

    # ── Helpers ───────────────────────────────────────────────────────────

    def _section_header(self, text: str, color=WHITE):
        """Flashes a section title, then shrinks it to the top."""
        hdr = Text(text, font_size=26, color=color)
        self.play(Write(hdr))
        self.wait(0.4)
        self.play(hdr.animate.scale(0.65).to_edge(UP, buff=0.25))
        self._current_header = hdr

    def _make_sequence_row(
        self,
        seq: str,
        box_size: float,
        start_x: float,
        y: float,
        box_color=BLUE_D,
    ):
        """Returns a list of Mobjects (boxes + letters) for a sequence."""
        mobs = []
        for i, ch in enumerate(seq):
            x = start_x + i * (box_size + 0.05)
            box = Square(
                side_length=box_size,
                color=box_color,
                fill_color=box_color,
                fill_opacity=0.55,
            ).move_to([x, y, 0])
            lbl = Text(ch, font_size=int(box_size * 28), color=WHITE).move_to(
                [x, y, 0]
            )
            mobs.append(VGroup(box, lbl))
        return mobs
