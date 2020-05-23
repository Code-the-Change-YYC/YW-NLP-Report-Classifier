import pandas as pd

from report_data_d import ColName


def merge_columns(report_data: pd.DataFrame) -> pd.DataFrame:
    """Merges the old incident type columns into the new, removes the old.

    :param report_data:
    :return: The updated data.
    """
    pd.set_option('display.max_columns', None)
    # create new column and add to end of DataFrame
    report_data[ColName.INC_T1] = report_data[ColName.INC_T1_OLD].fillna(
        '') + report_data[ColName.INC_T1].fillna('')
    # preprocess, replace nan with empty string
    report_data[ColName.INC_T2] = report_data[ColName.INC_T2].fillna('')
    # for "Other" 2nd types, set to description instead of "Other"
    report_data[ColName.INC_T2] = report_data.apply(
        lambda r: (r[ColName.INC_T2_OLD] if r[ColName.INC_T2].lower() == 'other'
                   else r[ColName.INC_T2]),
        axis=1)

    # make blank if matching first incident type
    report_data[ColName.INC_T2] = report_data.apply(
        lambda r: (r[ColName.INC_T2] if r[ColName.INC_T1] != r[ColName.INC_T2] else ''),
        axis=1)

    # remove old columns
    return report_data[[col for col in report_data if col not in [ColName.INC_T1_OLD, ColName.INC_T2_OLD]]]