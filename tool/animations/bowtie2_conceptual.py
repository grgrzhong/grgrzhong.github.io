"""
Bowtie2 – Conceptual Overview Animation
=========================================
Render with:
    manim -pqh bowtie2_conceptual.py Bowtie2Conceptual

Shows:
1. Two reads: one clean, one with a soft-clipped adapter tail
2. End-to-end mode: full read must align, clean read succeeds
3. Local mode: soft-clipping trims bad end, read aligns
4. Alignment score comparison for each preset
"""

from manim import *

REF_COLOR = BLUE_D
READ_COLOR = YELLOW
CLIP_COLOR = RED_B
ALIGN_COLOR = GREEN
SCORE_COLOR = TEAL


class Bowtie2Conceptual(Scene):
    def construct(self):
        self.camera.background_color = "#1e1e2e"

        title = Text(
            "Bowtie2: End-to-End vs Local Alignment – Conceptual Overview",
            font_size=28,
            color=WHITE,
        ).to_edge(UP, buff=0.35)
        self.play(Write(title))
        self.wait(0.4)

        # ── Reference ──────────────────────────────────────────────────────
        ref = Rectangle(
            width=11.0,
            height=0.55,
            color=REF_COLOR,
            fill_color=REF_COLOR,
            fill_opacity=0.4,
        ).move_to([0, 2.0, 0])
        ref_lbl = Text("Reference genome", font_size=19, color=GREY_A).next_to(
            ref, LEFT, buff=0.2
        )
        self.play(FadeIn(ref_lbl), FadeIn(ref))
        self.wait(0.3)

        # ── Read with adapter tail ─────────────────────────────────────────
        read_good = Rectangle(
            width=3.8,
            height=0.5,
            color=READ_COLOR,
            fill_color=READ_COLOR,
            fill_opacity=0.65,
        ).move_to([-2.4, 0.6, 0])
        read_adapter = Rectangle(
            width=1.2,
            height=0.5,
            color=CLIP_COLOR,
            fill_color=CLIP_COLOR,
            fill_opacity=0.75,
        ).move_to([0.5, 0.6, 0])
        read_lbl = Text(
            "Read with adapter tail", font_size=18, color=GREY_A
        ).move_to([-5.2, 0.6, 0])
        good_lbl = Text("Genomic", font_size=13, color=BLACK).move_to(read_good)
        adapt_lbl = Text("Adapter", font_size=13, color=WHITE).move_to(
            read_adapter
        )
        self.play(
            FadeIn(read_lbl),
            FadeIn(read_good),
            FadeIn(good_lbl),
            FadeIn(read_adapter),
            FadeIn(adapt_lbl),
        )
        self.wait(0.5)

        # ─────────────────────────────────────────────
        # Side A: End-to-end mode (left half)
        # ─────────────────────────────────────────────
        e2e_title = Text("End-to-End Mode", font_size=21, color=YELLOW).move_to(
            [-3.3, -0.5, 0]
        )
        self.play(Write(e2e_title))

        # Full read copy, moves toward ref
        full_read = VGroup(
            Rectangle(
                width=3.8,
                height=0.5,
                color=READ_COLOR,
                fill_color=READ_COLOR,
                fill_opacity=0.65,
            ),
            Rectangle(
                width=1.2,
                height=0.5,
                color=CLIP_COLOR,
                fill_color=CLIP_COLOR,
                fill_opacity=0.75,
            ).shift(RIGHT * 2.5),
        ).move_to([-2.4, -1.0, 0])
        self.play(FadeIn(full_read))

        # Attempt to align → red X (adapter blocks alignment)
        fail_arrow = Arrow(
            [-2.4, -0.75, 0], [-2.4, 1.75, 0], color=RED, stroke_width=2
        )
        fail_x = Text(
            "✗ UNALIGNED\n(adapter mismatch)", font_size=17, color=RED
        ).move_to([-2.4, -1.9, 0])
        self.play(Create(fail_arrow), Write(fail_x))
        self.wait(0.6)

        note_e2e = Text(
            "→ Reads MUST be adapter-trimmed first!", font_size=16, color=RED_B
        )
        note_e2e.move_to([-3.3, -2.7, 0])
        self.play(Write(note_e2e))
        self.wait(0.5)

        # ─────────────────────────────────────────────
        # Side B: Local mode (right half)
        # ─────────────────────────────────────────────
        local_title = Text(
            "Local Mode  (--local)", font_size=21, color=TEAL
        ).move_to([3.3, -0.5, 0])
        self.play(Write(local_title))

        # Copy of read, adapter gets soft-clipped
        local_good = Rectangle(
            width=3.8,
            height=0.5,
            color=READ_COLOR,
            fill_color=READ_COLOR,
            fill_opacity=0.65,
        ).move_to([3.2, -1.0, 0])
        local_clip = Rectangle(
            width=1.2,
            height=0.5,
            color=GREY_D,
            fill_color=GREY_D,
            fill_opacity=0.45,
        ).move_to([5.3, -1.0, 0])
        soft_lbl = Text("soft-clipped", font_size=12, color=GREY_B).next_to(
            local_clip, DOWN, buff=0.08
        )
        clip_brace = Brace(local_clip, direction=UP, color=GREY_B)
        self.play(
            FadeIn(local_good),
            FadeIn(local_clip),
            FadeIn(soft_lbl),
            FadeIn(clip_brace),
        )

        success_arrow = Arrow(
            [3.2, -0.75, 0], [3.2, 1.75, 0], color=GREEN, stroke_width=2
        )
        success_lbl = Text(
            "✓ ALIGNED\n(adapter soft-clipped)", font_size=17, color=GREEN
        )
        success_lbl.move_to([3.3, -1.9, 0])
        self.play(Create(success_arrow), Write(success_lbl))
        self.wait(0.6)

        note_local = Text(
            "→ Adapter trimming optional with --local",
            font_size=16,
            color=GREEN_B,
        )
        note_local.move_to([3.3, -2.7, 0])
        self.play(Write(note_local))
        self.wait(0.8)

        # ── Preset comparison bar ─────────────────────────────────────────
        preset_note = Text(
            "Presets: --very-fast  ←—(speed)—→  --very-sensitive-local",
            font_size=17,
            color=GREY_A,
        ).to_edge(DOWN, buff=0.3)
        self.play(Write(preset_note))
        self.wait(2)
