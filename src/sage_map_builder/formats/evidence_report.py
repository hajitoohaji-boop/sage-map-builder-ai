"""Text report for cross-sample evidence."""
from __future__ import annotations

from .evidence_matrix import EvidenceCell


def render_matrix(cells: tuple[EvidenceCell, ...]) -> str:
    lines = ['identity | left | right | comparable | score']
    for cell in cells:
        lines.append(
            f'{cell.identity.label} v{cell.identity.version} | '
            f'{cell.left_count} | {cell.right_count} | '
            f'{cell.comparable} | {cell.score}'
        )
    return '\n'.join(lines) + '\n'
