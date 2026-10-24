"""Regression contracts for the generated GitHub profile.

The profile is mostly generated SVG and HTML, so these tests protect the facts
and geometry that are easy to break while changing the visual system.
"""

from __future__ import annotations

import json
import re
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import phosphor as ph  # noqa: E402
import render_hacklog as hacklog  # noqa: E402
import render_hero as hero  # noqa: E402


class HeroContracts(unittest.TestCase):
    def test_win_meter_is_full_width_and_percentage_based(self) -> None:
        svg = hero.hackathon_meter(
            x=16,
            y=207,
            cell=5,
            gap=2,
            height=11,
            segments=58,
            motion=hero.Motion(False),
            attach=0,
        )
        all_cells = svg.count("h5v11h-5z")
        unlit = re.search(r'<path class="tr" d="([^"]*)"', svg)
        self.assertIsNotNone(unlit)
        unlit_cells = unlit.group(1).count("h5v11h-5z")  # type: ignore[union-attr]

        self.assertEqual(all_cells, 58)
        self.assertEqual(all_cells - unlit_cells, round(58 * ph.WON / ph.ENTERED))
        self.assertEqual(round(100 * ph.WON / ph.ENTERED), 62)

    def test_desktop_name_and_cursor_stay_inside_left_pane(self) -> None:
        x0 = 16
        pixel_pitch = 6
        second_word_x = x0 + (6 * 6 - 1 + 3) * pixel_pitch
        cursor_x = second_word_x + 5 * 6 * pixel_pitch
        cursor_right = cursor_x + 5 * pixel_pitch

        self.assertLessEqual(cursor_right, hero.XS)
        self.assertGreaterEqual(hero.XS - cursor_right, 10)


class WinLedgerContracts(unittest.TestCase):
    def test_all_eight_verified_wins_render(self) -> None:
        lines = (ROOT / "var/log/hackathons.log").read_text(encoding="utf-8").splitlines()
        ships = hacklog.newest(hacklog.parse_log(lines), count=8)
        records = json.loads((ROOT / "var/lib/ships.json").read_text(encoding="utf-8"))
        hacklog.attach_records(ships, records)

        self.assertEqual(len(ships), 8)
        self.assertTrue(all(ship.tag == "WIN" for ship in ships))
        self.assertTrue(all(ship.repo for ship in ships))

        rendered = hacklog.render(ships)
        self.assertEqual(len(rendered), 24)
        self.assertFalse(any(re.search(r"\b\d+ (?:stars?|forks?)\b", svg) for svg in rendered.values()))


class ReadmeContracts(unittest.TestCase):
    def test_every_local_image_reference_exists(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        refs = re.findall(r'(?:src|srcset)="([^"?#]+)', readme)
        local = [ref for ref in refs if not ref.startswith(("http://", "https://"))]

        self.assertGreater(len(local), 0)
        missing = sorted({ref for ref in local if not (ROOT / ref).is_file()})
        self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()
