import pandas as pd

from incident_types.column_merge import ColumnMerger
from incident_types.mapper import IncTypeMapper
from preprocessor import Preprocessor


class IncidentTypesProcessor(Preprocessor):
    """Normalize, apply corrections to, and merge the incident type columns."""

    def process(self, report_data: pd.DataFrame) -> pd.DataFrame:
        return ColumnMerger().process(IncTypeMapper().process(report_data))
