"""Convert reader evidence into the neutral MapDocument model."""
from __future__ import annotations

from ..map.reader import MapReaderResult
from .map_document import MapDocument, MapRegion


def document_from_reader(result: MapReaderResult) -> MapDocument:
    regions = [MapRegion(r.start, r.end, r.source) for r in result.regions]
    return MapDocument(
        file_name=result.file_name,
        raw_size=len(result.data),
        regions=regions,
        opaque_sections=list(regions),
    )
