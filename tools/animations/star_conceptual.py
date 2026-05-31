"""
STAR Aligner – Conceptual Overview Animation
============================================
Render with:
    manim -pqh star_conceptual.py StarConceptual

Shows:
1. Pre-mRNA with exons (E1, E2, E3) and introns
2. Splicing produces mature mRNA
3. Illumina read is drawn across a splice junction (E1–E2 boundary)
4. STAR splits the read, maps each segment to the correct exon
5. Final aligned read shown on the genome with the intron "skipped"
"""

from manim import *

EXON_COLOR = BLUE_D
INTRON_COLOR = GREY
READ_COLOR = YELLOW
SPLIT_COLOR = ORANGE


class StarConceptual(Scene):
    def construct(self):
        self.camera.background_color = "#1e1e2e"

        # ── Title ──────────────────────────────────────────────────────────
        title = Text(
            "STAR: Spliced Alignment – Conceptual Overview",
            font_size=34,
            color=WHITE,
        )
        title.to_edge(UP, buff=0.4)
        self.play(Write(title))
        self.wait(0.5)

        # ── Genome track ──────────────────────────────────────────────────
        genome_label = Text("Genome", font_size=22, color=GREY_A)
        genome_label.move_to([-5.5, 1.6, 0])
        self.play(FadeIn(genome_label))

        # Exons and introns (boxes + line)
        e1 = Rectangle(
            width=1.6,
            height=0.5,
            color=EXON_COLOR,
            fill_color=EXON_COLOR,
            fill_opacity=0.8,
        ).move_to([-4.0, 1.1, 0])
        intron1 = Line(
            [-3.2, 1.35, 0], [-1.2, 1.35, 0], color=INTRON_COLOR, stroke_width=3
        )
        e2 = Rectangle(
            width=2.0,
            height=0.5,
            color=EXON_COLOR,
            fill_color=EXON_COLOR,
            fill_opacity=0.8,
        ).move_to([-0.2, 1.1, 0])
        intron2 = Line(
            [0.8, 1.35, 0], [2.8, 1.35, 0], color=INTRON_COLOR, stroke_width=3
        )
        e3 = Rectangle(
            width=1.6,
            height=0.5,
            color=EXON_COLOR,
            fill_color=EXON_COLOR,
            fill_opacity=0.8,
        ).move_to([3.6, 1.1, 0])

        e1_label = Text("Exon 1", font_size=16, color=WHITE).move_to(
            e1.get_center()
        )
        e2_label = Text("Exon 2", font_size=16, color=WHITE).move_to(
            e2.get_center()
        )
        e3_label = Text("Exon 3", font_size=16, color=WHITE).move_to(
            e3.get_center()
        )
        i1_label = Text("Intron", font_size=14, color=GREY_B).next_to(
            intron1, DOWN, buff=0.1
        )
        i2_label = Text("Intron", font_size=14, color=GREY_B).next_to(
            intron2, DOWN, buff=0.1
        )

        genome_group = VGroup(
            e1,
            intron1,
            e2,
            intron2,
            e3,
            e1_label,
            e2_label,
            e3_label,
            i1_label,
            i2_label,
        )
        self.play(
            LaggedStart(*[FadeIn(m) for m in genome_group], lag_ratio=0.15)
        )
        self.wait(0.5)

        # ── Splicing arrow to mRNA ─────────────────────────────────────────
        splice_arrow = CurvedArrow(
            start_point=[-0.2, 0.8, 0],
            end_point=[-0.2, -0.3, 0],
            angle=-PI / 3,
            color=GREEN_B,
        )
        splice_label = Text("Splicing", font_size=18, color=GREEN_B).next_to(
            splice_arrow, RIGHT, buff=0.1
        )
        self.play(Create(splice_arrow), Write(splice_label))
        self.wait(0.3)

        # mRNA bar (exons only, concatenated)
        mrna_label = Text("mRNA", font_size=22, color=GREY_A).move_to(
            [-5.5, -0.8, 0]
        )
        me1 = Rectangle(
            width=1.6,
            height=0.5,
            color=EXON_COLOR,
            fill_color=EXON_COLOR,
            fill_opacity=0.8,
        ).move_to([-3.2, -0.8, 0])
        me2 = Rectangle(
            width=2.0,
            height=0.5,
            color=EXON_COLOR,
            fill_color=EXON_COLOR,
            fill_opacity=0.8,
        ).move_to([-1.0, -0.8, 0])
        me3 = Rectangle(
            width=1.6,
            height=0.5,
            color=EXON_COLOR,
            fill_color=EXON_COLOR,
            fill_opacity=0.8,
        ).move_to([1.2, -0.8, 0])
        me1_l = Text("E1", font_size=14, color=WHITE).move_to(me1.get_center())
        me2_l = Text("E2", font_size=14, color=WHITE).move_to(me2.get_center())
        me3_l = Text("E3", font_size=14, color=WHITE).move_to(me3.get_center())
        mrna_group = VGroup(me1, me2, me3, me1_l, me2_l, me3_l)
        self.play(FadeIn(mrna_label), *[FadeIn(m) for m in mrna_group])
        self.wait(0.5)

        # ── Illumina read spanning E1–E2 junction ─────────────────────────
        step1 = Text(
            "Step 1: A read spans the Exon 1 – Exon 2 junction",
            font_size=20,
            color=YELLOW,
        ).to_edge(DOWN, buff=1.2)
        self.play(Write(step1))

        read = Rectangle(
            width=3.0,
            height=0.35,
            color=READ_COLOR,
            fill_color=READ_COLOR,
            fill_opacity=0.7,
        ).move_to([-2.2, -0.8, 0])
        read_label = Text("Read", font_size=16, color=BLACK).move_to(
            read.get_center()
        )
        self.play(FadeIn(read), FadeIn(read_label))
        self.wait(0.8)

        # ── STAR splits the read ──────────────────────────────────────────
        step2 = Text(
            "Step 2: STAR splits and maps each segment to the genome",
            font_size=20,
            color=ORANGE,
        ).to_edge(DOWN, buff=1.2)
        self.play(Transform(step1, step2))

        # Left segment of read maps to E1 on genome
        seg_left = Rectangle(
            width=1.3,
            height=0.35,
            color=SPLIT_COLOR,
            fill_color=SPLIT_COLOR,
            fill_opacity=0.85,
        ).move_to([-3.7, 1.85, 0])
        seg_right = Rectangle(
            width=1.3,
            height=0.35,
            color=SPLIT_COLOR,
            fill_color=SPLIT_COLOR,
            fill_opacity=0.85,
        ).move_to([-0.8, 1.85, 0])
        arrow_left = Arrow(
            [-2.8, -0.62, 0], [-3.7, 1.65, 0], color=SPLIT_COLOR, stroke_width=2
        )
        arrow_right = Arrow(
            [-1.6, -0.62, 0], [-0.8, 1.65, 0], color=SPLIT_COLOR, stroke_width=2
        )

        self.play(
            FadeIn(seg_left),
            FadeIn(seg_right),
            Create(arrow_left),
            Create(arrow_right),
        )
        self.wait(0.8)

        # ── Junction annotation ───────────────────────────────────────────
        step3 = Text(
            "Step 3: STAR records the splice junction (E1→E2)",
            font_size=20,
            color=GREEN,
        ).to_edge(DOWN, buff=1.2)
        self.play(Transform(step1, step3))

        junction_arc = ArcBetweenPoints(
            [-3.2, 1.35, 0],
            [-1.2, 1.35, 0],
            angle=-PI / 2.5,
            color=GREEN,
            stroke_width=3,
        )
        junction_label = Text(
            "Splice junction\n(SJ.out.tab)", font_size=14, color=GREEN
        )
        junction_label.next_to(junction_arc, UP, buff=0.1)
        self.play(Create(junction_arc), Write(junction_label))
        self.wait(1.2)

        # ── Summary box ───────────────────────────────────────────────────
        summary = Text(
            "STAR output: sorted BAM  |  SJ.out.tab  |  ReadsPerGene.out.tab",
            font_size=18,
            color=WHITE,
        ).to_edge(DOWN, buff=0.4)
        self.play(FadeOut(step1), Write(summary))
        self.wait(2)
