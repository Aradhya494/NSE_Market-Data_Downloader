import pandas as pd

class ValidationError(Exception):
    """Raised when downloaded market data fails validation."""

def validate_dataframe(dataframe: pd.DataFrame, dataset_name: str) -> None:
    if not isinstance(dataframe, pd.DataFrame):
        raise ValidationError("Downloaded data is not a pandas DataFrame.")

    if dataframe.empty:
        raise ValidationError("Downloaded dataset is empty.")

    if len(dataframe.columns) == 0:
        raise ValidationError("No columns were received from NSE.")

    # NSE normally uses 'symbol'. Accept 'underlying' as an alternate identifier
    # because some NSE reports use that field name.
    normalized_columns = {str(column).strip().lower() for column in dataframe.columns}
    if not ({"symbol", "underlying"} & normalized_columns):
        raise ValidationError(
            f"{dataset_name}: required identifier column 'symbol' was not found. "
            f"Received columns: {list(dataframe.columns)}"
        )

    identifier_column = next(
        column for column in dataframe.columns
        if str(column).strip().lower() in {"symbol", "underlying"}
    )
    cleaned = dataframe[identifier_column].astype(str).str.strip()
    if cleaned.eq("").all() or cleaned.str.lower().eq("nan").all():
        raise ValidationError("All stock identifiers are blank.")
