#!/usr/bin/env python3
"""Render the definitive T Krobot sticker pack.

The renderer keeps the mascot construction deterministic so the pack does not
drift on the details that are hard to enforce with image prompts: no mouth, no
limb marks, and exactly three fingers plus one thumb on every visible hand.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Literal

from PIL import Image, ImageDraw


SIZE = 1024
BLACK = (11, 11, 14, 255)
BLACK_2 = (26, 26, 30, 255)
OUTLINE = (2, 2, 3, 255)
LIMB = (225, 225, 225, 255)
WHITE = (255, 255, 255, 255)
RED = (248, 24, 35, 255)
ORANGE = (255, 154, 22, 255)
YELLOW = (255, 209, 36, 255)
GREEN = (0, 255, 0, 255)
SHINE = (190, 190, 190, 255)


HandKind = Literal["open", "point_right", "point_left", "thumbsup", "ok", "clasp", "down"]
EyeKind = Literal["blank", "happy", "x", "glare", "lightning", "dizzy"]


@dataclass(frozen=True)
class Arm:
    points: tuple[tuple[int, int], ...]
    hand: tuple[int, int]
    angle: float
    kind: HandKind = "open"
    scale: float = 1.0
    mirror: bool = False


@dataclass(frozen=True)
class Leg:
    points: tuple[tuple[int, int], ...]
    foot: tuple[int, int]
    angle: float


@dataclass(frozen=True)
class StickerSpec:
    slug: str
    eyes: EyeKind = "blank"
    arms: tuple[Arm, ...] = ()
    legs: tuple[Leg, ...] = ()
    body_shift: tuple[int, int] = (0, 0)
    head_shift: tuple[int, int] = (0, 0)
    rotate: float = 0
    marks: tuple[tuple[str, int, int, float], ...] = ()
    heart: bool = False
    cross: bool = False
    sleep: bool = False


def lerp(a: int, b: int, t: float) -> int:
    return int(a + (b - a) * t)


def draw_gradient_poly(draw_image: Image.Image, points: list[tuple[int, int]], top: tuple[int, int, int, int], bottom: tuple[int, int, int, int]) -> None:
    mask = Image.new("L", draw_image.size, 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.polygon(points, fill=255)

    gradient = Image.new("RGBA", draw_image.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(gradient)
    min_y = min(y for _, y in points)
    max_y = max(y for _, y in points)
    for y in range(min_y, max_y + 1):
        t = (y - min_y) / max(1, max_y - min_y)
        gd.line(
            [(0, y), (draw_image.width, y)],
            fill=(
                lerp(top[0], bottom[0], t),
                lerp(top[1], bottom[1], t),
                lerp(top[2], bottom[2], t),
                255,
            ),
        )
    draw_image.alpha_composite(Image.composite(gradient, Image.new("RGBA", draw_image.size, (0, 0, 0, 0)), mask))


def draw_tube(draw: ImageDraw.ImageDraw, points: Iterable[tuple[int, int]], width: int = 34) -> None:
    pts = list(points)
    draw.line(pts, fill=OUTLINE, width=width + 14, joint="curve")
    draw.line(pts, fill=LIMB, width=width, joint="curve")


def draw_rotated_rounded_rect(layer: Image.Image, cx: int, cy: int, w: int, h: int, angle: float, fill: tuple[int, int, int, int], radius: int = 8, outline_width: int = 5) -> None:
    pad = 28
    patch = Image.new("RGBA", (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(patch)
    d.rounded_rectangle([pad - outline_width, pad - outline_width, pad + w + outline_width, pad + h + outline_width], radius=radius + outline_width, fill=OUTLINE)
    d.rounded_rectangle([pad, pad, pad + w, pad + h], radius=radius, fill=fill)
    rotated = patch.rotate(angle, resample=Image.Resampling.BICUBIC, expand=True)
    layer.alpha_composite(rotated, (int(cx - rotated.width / 2), int(cy - rotated.height / 2)))


def draw_hand(base: Image.Image, cx: int, cy: int, angle: float, kind: HandKind = "open", scale: float = 1.0, mirror: bool = False) -> None:
    hand = Image.new("RGBA", (220, 220), (0, 0, 0, 0))
    d = ImageDraw.Draw(hand)

    def rect(x: int, y: int, w: int, h: int, a: float = 0, fill=LIMB) -> None:
        if mirror:
            x = 220 - x - w
            a = -a
        draw_rotated_rounded_rect(hand, x + w // 2, y + h // 2, w, h, a, fill)

    # Exactly three fingers plus one thumb in every hand construction.
    if kind in {"open", "down"}:
        rect(72, 28, 24, 72, -8)
        rect(98, 20, 24, 78, 0)
        rect(124, 30, 24, 68, 8)
        rect(42, 74, 24, 62, -48)
        d.ellipse([54, 82, 164, 184], fill=OUTLINE)
        d.ellipse([61, 89, 157, 177], fill=BLACK)
    elif kind == "thumbsup":
        rect(78, 90, 24, 54, -86)
        rect(96, 92, 24, 58, -86)
        rect(114, 96, 24, 50, -86)
        rect(130, 35, 30, 82, 4)
        d.ellipse([54, 82, 156, 180], fill=OUTLINE)
        d.ellipse([61, 89, 149, 173], fill=BLACK)
    elif kind in {"point_right", "point_left"}:
        flip = kind == "point_left"
        local_mirror = mirror ^ flip
        saved = mirror
        mirror = local_mirror  # noqa: F841 - kept readable by local helper replacement below.
        def rect2(x: int, y: int, w: int, h: int, a: float = 0) -> None:
            xx, aa = (220 - x - w, -a) if local_mirror else (x, a)
            draw_rotated_rounded_rect(hand, xx + w // 2, y + h // 2, w, h, aa, LIMB)
        rect2(118, 72, 76, 25, 2)
        rect2(86, 100, 45, 22, 6)
        rect2(86, 124, 39, 22, 8)
        rect2(94, 48, 25, 46, -42)
        d.ellipse([54, 76, 138, 162], fill=OUTLINE)
        d.ellipse([61, 83, 131, 155], fill=BLACK)
    elif kind == "ok":
        rect(102, 28, 23, 68, 3)
        rect(128, 36, 23, 62, 12)
        rect(74, 41, 23, 60, -14)
        rect(43, 78, 24, 58, -40)
        d.ellipse([58, 86, 158, 180], fill=OUTLINE)
        d.ellipse([65, 93, 151, 173], fill=BLACK)
        d.ellipse([79, 62, 121, 104], outline=OUTLINE, width=8)
        d.ellipse([85, 68, 115, 98], outline=LIMB, width=7)
    elif kind == "clasp":
        rect(76, 36, 22, 72, -8)
        rect(100, 30, 22, 78, 0)
        rect(124, 38, 22, 70, 8)
        rect(46, 88, 22, 56, -50)
        d.ellipse([58, 92, 158, 184], fill=OUTLINE)
        d.ellipse([65, 99, 151, 177], fill=BLACK)

    if kind == "down":
        hand = hand.rotate(180, resample=Image.Resampling.BICUBIC, expand=False)

    if scale != 1:
        hand = hand.resize((int(hand.width * scale), int(hand.height * scale)), Image.Resampling.LANCZOS)
    rotated = hand.rotate(angle, resample=Image.Resampling.BICUBIC, expand=True)
    base.alpha_composite(rotated, (int(cx - rotated.width / 2), int(cy - rotated.height / 2)))


def draw_glasses(draw: ImageDraw.ImageDraw, eyes: EyeKind, hx: int, hy: int) -> None:
    left = (hx - 112, hy - 44, hx - 8, hy + 60)
    right = (hx + 8, hy - 44, hx + 112, hy + 60)
    for box in (left, right):
        draw.ellipse([box[0] - 9, box[1] - 9, box[2] + 9, box[3] + 9], fill=OUTLINE)
        draw.ellipse([box[0] - 4, box[1] - 4, box[2] + 4, box[3] + 4], fill=(40, 40, 45, 255))
        draw.ellipse(box, fill=WHITE)
    draw.rounded_rectangle([hx - 14, hy + 4, hx + 14, hy + 18], radius=7, fill=OUTLINE)
    draw.rounded_rectangle([hx - 10, hy + 7, hx + 10, hy + 15], radius=5, fill=SHINE)

    if eyes == "happy":
        for cx in (hx - 60, hx + 60):
            draw.arc([cx - 30, hy + 5, cx + 30, hy + 58], start=200, end=340, fill=OUTLINE, width=9)
    elif eyes == "x":
        for cx in (hx - 60, hx + 60):
            draw.line([(cx - 24, hy - 4), (cx + 24, hy + 42)], fill=OUTLINE, width=9)
            draw.line([(cx + 24, hy - 4), (cx - 24, hy + 42)], fill=OUTLINE, width=9)
    elif eyes == "glare":
        draw.line([(hx - 92, hy + 16), (hx - 28, hy - 6)], fill=OUTLINE, width=10)
        draw.line([(hx + 28, hy - 6), (hx + 92, hy + 16)], fill=OUTLINE, width=10)
    elif eyes == "lightning":
        for cx in (hx - 60, hx + 60):
            pts = [(cx - 12, hy - 12), (cx + 10, hy + 15), (cx - 4, hy + 15), (cx + 16, hy + 48), (cx - 20, hy + 8), (cx - 4, hy + 8)]
            draw.polygon(pts, fill=YELLOW)
            draw.line(pts + [pts[0]], fill=OUTLINE, width=4, joint="curve")
    elif eyes == "dizzy":
        for cx in (hx - 60, hx + 60):
            draw.arc([cx - 24, hy - 6, cx + 24, hy + 42], 20, 320, fill=OUTLINE, width=8)


def draw_robot(spec: StickerSpec, background: tuple[int, int, int, int] | None = None) -> Image.Image:
    image = Image.new("RGBA", (SIZE, SIZE), background or (0, 0, 0, 0))
    layer = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    bx, by = spec.body_shift
    hx, hy = 512 + spec.head_shift[0] + bx, 300 + spec.head_shift[1] + by

    for mark, x, y, angle in spec.marks:
        draw_mark(draw, mark, x + bx, y + by, angle)

    for arm in spec.arms:
        draw_tube(draw, arm.points)
    for leg in spec.legs:
        draw_tube(draw, leg.points, width=36)

    body = [(392 + bx, 390 + by), (632 + bx, 390 + by), (682 + bx, 706 + by), (612 + bx, 766 + by), (412 + bx, 766 + by), (342 + bx, 706 + by)]
    draw.line(body + [body[0]], fill=OUTLINE, width=18, joint="curve")
    draw_gradient_poly(layer, body, BLACK_2, BLACK)
    draw.line(body + [body[0]], fill=OUTLINE, width=10, joint="curve")

    head = [(390 + hx - 512, 198 + hy - 300), (634 + hx - 512, 198 + hy - 300), (668 + hx - 512, 360 + hy - 300), (618 + hx - 512, 414 + hy - 300), (406 + hx - 512, 414 + hy - 300), (356 + hx - 512, 360 + hy - 300)]
    draw.line(head + [head[0]], fill=OUTLINE, width=18, joint="curve")
    draw_gradient_poly(layer, head, BLACK_2, BLACK)
    draw.line(head + [head[0]], fill=OUTLINE, width=10, joint="curve")
    draw.arc([392 + hx - 512, 371 + hy - 300, 632 + hx - 512, 440 + hy - 300], 12, 168, fill=SHINE, width=5)

    draw_glasses(draw, spec.eyes, hx, hy)
    draw_diamond(draw, 512 + bx, 558 + by)

    if spec.heart:
        draw_heart(draw, 512 + bx, 542 + by)
    if spec.cross:
        draw.line([(424 + bx, 244 + by), (600 + bx, 392 + by)], fill=(230, 20, 32, 255), width=24)
        draw.line([(600 + bx, 244 + by), (424 + bx, 392 + by)], fill=(230, 20, 32, 255), width=24)
    if spec.sleep:
        for i, size in enumerate((32, 26, 20)):
            draw.text((710 + i * 42 + bx, 240 - i * 36 + by), "Z", fill=(150, 150, 155, 255), anchor="mm")

    for leg in spec.legs:
        draw_foot(layer, *leg.foot, leg.angle)
    for arm in spec.arms:
        draw_hand(layer, *arm.hand, arm.angle, arm.kind, arm.scale, arm.mirror)

    if spec.rotate:
        layer = layer.rotate(spec.rotate, resample=Image.Resampling.BICUBIC, expand=False, center=(512, 512))
    image.alpha_composite(layer)
    return image


def draw_diamond(draw: ImageDraw.ImageDraw, cx: int, cy: int) -> None:
    pts = [(cx, cy - 72), (cx + 44, cy), (cx, cy + 72), (cx - 44, cy)]
    draw.polygon(pts, fill=OUTLINE)
    inner = [(cx, cy - 60), (cx + 35, cy), (cx, cy + 60), (cx - 35, cy)]
    draw.polygon(inner, fill=RED)


def draw_heart(draw: ImageDraw.ImageDraw, cx: int, cy: int) -> None:
    draw.ellipse([cx - 70, cy - 70, cx - 5, cy - 5], fill=OUTLINE)
    draw.ellipse([cx + 5, cy - 70, cx + 70, cy - 5], fill=OUTLINE)
    draw.polygon([(cx - 78, cy - 33), (cx + 78, cy - 33), (cx, cy + 78)], fill=OUTLINE)
    draw.ellipse([cx - 58, cy - 58, cx - 8, cy - 8], fill=(238, 38, 62, 255))
    draw.ellipse([cx + 8, cy - 58, cx + 58, cy - 8], fill=(238, 38, 62, 255))
    draw.polygon([(cx - 62, cy - 26), (cx + 62, cy - 26), (cx, cy + 60)], fill=(238, 38, 62, 255))


def draw_foot(layer: Image.Image, cx: int, cy: int, angle: float) -> None:
    patch = Image.new("RGBA", (190, 112), (0, 0, 0, 0))
    d = ImageDraw.Draw(patch)
    d.ellipse([8, 12, 182, 100], fill=OUTLINE)
    d.ellipse([18, 20, 172, 92], fill=BLACK)
    rotated = patch.rotate(angle, resample=Image.Resampling.BICUBIC, expand=True)
    layer.alpha_composite(rotated, (int(cx - rotated.width / 2), int(cy - rotated.height / 2)))


def draw_mark(draw: ImageDraw.ImageDraw, kind: str, x: int, y: int, angle: float) -> None:
    if kind == "burst":
        for i in range(3):
            a = math.radians(angle - 28 + i * 28)
            p1 = (x + int(math.cos(a) * 16), y + int(math.sin(a) * 16))
            p2 = (x + int(math.cos(a) * 72), y + int(math.sin(a) * 72))
            draw.line([p1, p2], fill=ORANGE, width=16)
            draw.line([p1, p2], fill=YELLOW, width=9)
    elif kind == "spark":
        pts = [(x, y - 36), (x + 10, y - 10), (x + 36, y), (x + 10, y + 10), (x, y + 36), (x - 10, y + 10), (x - 36, y), (x - 10, y - 10)]
        draw.polygon(pts, fill=YELLOW)
        draw.line(pts + [pts[0]], fill=OUTLINE, width=4)
    elif kind == "wrong":
        draw.line([(x - 50, y - 50), (x + 50, y + 50)], fill=(240, 24, 32, 255), width=18)
        draw.line([(x + 50, y - 50), (x - 50, y + 50)], fill=(240, 24, 32, 255), width=18)


def specs() -> list[StickerSpec]:
    base_legs = (
        Leg(((464, 740), (452, 874)), (416, 912), -12),
        Leg(((560, 740), (572, 874)), (608, 912), 12),
    )
    down_arms = (
        Arm(((365, 430), (300, 560), (292, 690)), (292, 724), -12, "down", 0.9),
        Arm(((659, 430), (724, 560), (732, 690)), (732, 724), 12, "down", 0.9, True),
    )
    return [
        StickerSpec("greetings", arms=(Arm(((366, 440), (270, 340), (222, 250)), (214, 216), -28, "open", 0.95), Arm(((658, 440), (716, 560), (718, 688)), (718, 716), 10, "down", 0.85, True)), legs=base_legs, marks=(("burst", 224, 158, 250),)),
        StickerSpec("gasp", arms=(Arm(((382, 438), (330, 458), (300, 372)), (302, 342), -18, "open", 0.88), Arm(((642, 438), (694, 458), (724, 372)), (722, 342), 18, "open", 0.88, True)), legs=base_legs, marks=(("burst", 330, 160, 250), ("burst", 690, 160, 290))),
        StickerSpec("handraise", arms=(Arm(((366, 438), (286, 326), (260, 188)), (262, 154), -12, "open", 0.95), Arm(((660, 440), (728, 558), (728, 676)), (728, 710), 8, "down", 0.85, True)), legs=base_legs, marks=(("burst", 258, 102, 255),)),
        StickerSpec("shrug", arms=(Arm(((368, 436), (272, 420), (210, 350)), (194, 326), -62, "open", 0.9), Arm(((656, 436), (752, 420), (814, 350)), (830, 326), 62, "open", 0.9, True)), legs=base_legs, marks=(("spark", 210, 260, 0), ("spark", 816, 260, 0))),
        StickerSpec("yay", eyes="happy", arms=(Arm(((370, 430), (284, 286), (226, 160)), (218, 126), -20, "open", 0.95), Arm(((654, 430), (740, 286), (798, 160)), (806, 126), 20, "open", 0.95, True)), legs=base_legs, marks=(("burst", 270, 90, 250), ("burst", 754, 90, 290))),
        StickerSpec("wrong", arms=(Arm(((368, 440), (290, 520), (225, 512)), (198, 500), -75, "open", 0.9), Arm(((656, 440), (734, 520), (799, 512)), (826, 500), 75, "open", 0.9, True)), legs=base_legs, marks=(("wrong", 512, 150, 0),)),
        StickerSpec("thumbsup", arms=(Arm(((366, 438), (286, 350), (238, 232)), (232, 196), -8, "thumbsup", 0.95), Arm(((658, 438), (718, 560), (714, 692)), (714, 724), 12, "down", 0.85, True)), legs=base_legs, marks=(("spark", 226, 120, 0),)),
        StickerSpec("snooze", eyes="lightning", arms=down_arms, legs=(Leg(((455, 740), (405, 826), (338, 838)), (322, 856), 16), Leg(((558, 740), (635, 820), (704, 810)), (724, 828), -20)), body_shift=(-20, 50), head_shift=(0, 8), rotate=-8, sleep=True),
        StickerSpec("shock", arms=(Arm(((376, 438), (316, 358), (278, 270)), (268, 232), -24, "open", 0.9), Arm(((648, 438), (708, 358), (746, 270)), (756, 232), 24, "open", 0.9, True)), legs=base_legs, marks=(("burst", 280, 146, 250), ("burst", 744, 146, 290))),
        StickerSpec("salute", arms=(Arm(((366, 438), (296, 330), (356, 260)), (382, 238), -58, "open", 0.82), Arm(((658, 438), (716, 552), (714, 680)), (714, 708), 12, "down", 0.85, True)), legs=base_legs, marks=(("burst", 344, 170, 235),)),
        StickerSpec("right", arms=(Arm(((366, 438), (304, 560), (296, 686)), (296, 718), -12, "down", 0.85), Arm(((654, 430), (760, 392), (858, 392)), (888, 392), 86, "point_right", 0.9)), legs=base_legs, marks=(("burst", 906, 338, 280),)),
        StickerSpec("pls", arms=(Arm(((392, 444), (452, 510), (488, 566)), (488, 548), 10, "clasp", 0.8), Arm(((632, 444), (572, 510), (536, 566)), (536, 548), -10, "clasp", 0.8, True)), legs=base_legs, marks=(("spark", 512, 206, 0),)),
        StickerSpec("ok", arms=(Arm(((366, 438), (276, 346), (228, 240)), (218, 206), -18, "ok", 0.92), Arm(((658, 438), (720, 556), (718, 682)), (718, 712), 12, "down", 0.85, True)), legs=base_legs, marks=(("spark", 220, 128, 0),)),
        StickerSpec("intenseglare", eyes="glare", arms=(Arm(((366, 438), (298, 552), (296, 684)), (296, 716), -12, "down", 0.85), Arm(((658, 438), (726, 552), (728, 684)), (728, 716), 12, "down", 0.85, True)), legs=base_legs),
        StickerSpec("heart", arms=(Arm(((386, 440), (426, 510), (452, 576)), (450, 568), 16, "open", 0.72), Arm(((638, 440), (598, 510), (572, 576)), (574, 568), -16, "open", 0.72, True)), legs=base_legs, heart=True),
        StickerSpec("flailing", arms=(Arm(((370, 438), (260, 380), (184, 300)), (160, 270), -56, "open", 0.9), Arm(((654, 438), (764, 380), (840, 300)), (864, 270), 56, "open", 0.9, True)), legs=(Leg(((456, 742), (400, 850), (344, 880)), (316, 900), -28), Leg(((562, 742), (626, 850), (690, 878)), (718, 898), 28)), marks=(("burst", 166, 212, 245), ("burst", 858, 212, 295))),
        StickerSpec("fingerguns", arms=(Arm(((370, 438), (284, 396), (204, 370)), (176, 358), -90, "point_left", 0.88), Arm(((654, 438), (740, 396), (820, 370)), (848, 358), 90, "point_right", 0.88)), legs=base_legs, marks=(("spark", 142, 330, 0), ("spark", 884, 330, 0))),
        StickerSpec("falling", arms=(Arm(((366, 438), (254, 392), (172, 300)), (148, 274), -54, "open", 0.86), Arm(((656, 438), (766, 512), (838, 600)), (858, 628), 118, "open", 0.86, True)), legs=(Leg(((454, 740), (378, 828), (310, 850)), (286, 868), -24), Leg(((560, 740), (654, 818), (730, 812)), (756, 832), -16)), rotate=18, marks=(("burst", 186, 216, 245),)),
        StickerSpec("facepalm", arms=(Arm(((368, 438), (320, 364), (410, 302)), (432, 292), 58, "open", 0.78), Arm(((658, 438), (724, 556), (724, 680)), (724, 708), 12, "down", 0.85, True)), legs=base_legs),
        StickerSpec("ded", eyes="x", arms=down_arms, legs=(Leg(((456, 740), (370, 790), (300, 768)), (272, 782), -12), Leg(((560, 740), (650, 790), (724, 764)), (752, 780), 12)), body_shift=(0, 76), head_shift=(0, 10), rotate=90),
        StickerSpec("depressed", eyes="dizzy", arms=down_arms, legs=(Leg(((454, 742), (392, 820), (342, 852)), (310, 870), -10), Leg(((560, 742), (626, 820), (688, 850)), (720, 870), 12)), body_shift=(0, 36), head_shift=(-10, 18), rotate=-5),
        StickerSpec("crashed", eyes="x", arms=(Arm(((368, 438), (294, 552), (218, 660)), (196, 690), -24, "open", 0.8), Arm(((656, 438), (746, 520), (836, 520)), (864, 518), 90, "open", 0.8, True)), legs=(Leg(((454, 740), (346, 812), (250, 792)), (222, 808), -10), Leg(((560, 740), (682, 800), (774, 758)), (804, 774), 20)), rotate=-28, marks=(("burst", 732, 190, 290),)),
    ]


def write_manifest(items: list[StickerSpec], out: Path) -> None:
    original = {
        "crashed": "crashed2.png",
        "depressed": "depressed2.png",
        "flailing": "flailing2.png",
        "handraise": "handraise4.png",
        "intenseglare": "intenseglare2.png",
        "pls": "pls5.png",
        "shrug": "shrug4.png",
    }
    payload = {
        "name": "T Krobot Sticker Library",
        "count": len(items),
        "contact_sheet": "stickers/contact-sheet.png",
        "items": [
            {
                "slug": spec.slug,
                "filename": f"{spec.slug}.png",
                "sticker_path": f"stickers/{spec.slug}.png",
                "source_path": f"archive/chroma-key-sources/{spec.slug}.png",
                "original_filename": original.get(spec.slug, f"{spec.slug}.png"),
            }
            for spec in sorted(items, key=lambda item: item.slug)
        ],
    }
    out.write_text(json.dumps(payload, indent=2) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stickers", type=Path, default=Path("stickers"))
    parser.add_argument("--sources", type=Path, default=Path("archive/chroma-key-sources"))
    parser.add_argument("--iteration", type=Path, default=Path("archive/generated-iterations/blocky-final"))
    parser.add_argument("--manifest", type=Path, default=Path("stickers/manifest.json"))
    args = parser.parse_args()

    args.stickers.mkdir(parents=True, exist_ok=True)
    args.sources.mkdir(parents=True, exist_ok=True)
    (args.iteration / "sources").mkdir(parents=True, exist_ok=True)
    (args.iteration / "stickers").mkdir(parents=True, exist_ok=True)

    all_specs = specs()
    for spec in all_specs:
        transparent = draw_robot(spec)
        source = draw_robot(spec, GREEN)
        transparent.save(args.stickers / f"{spec.slug}.png")
        source.save(args.sources / f"{spec.slug}.png")
        transparent.save(args.iteration / "stickers" / f"{spec.slug}.png")
        source.save(args.iteration / "sources" / f"{spec.slug}.png")

    write_manifest(all_specs, args.manifest)
    notes = args.iteration / "NOTES.md"
    notes.write_text(
        "# Blocky Final Render\n\n"
        "- Deterministic vector-style raster render of the definitive pack.\n"
        "- Hands are constructed from one black palm blob, exactly three light grey rectangular fingers, and one light grey thumb.\n"
        "- Limbs are smooth `#e1e1e1` tubes with no joint or segment lines.\n"
        "- Numbered final names have been canonicalised unless the number was part of the original source reference.\n"
    )


if __name__ == "__main__":
    main()
