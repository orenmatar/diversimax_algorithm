import pandas as pd
import os

from diversimax.models import Dimensions, CategoryRanges


def read_categories_file(file_path: str) -> Dimensions:
    """
    Reads a categories file (CSV or Excel) and returns a DataFrame.
    """
    _, file_extension = os.path.splitext(file_path)
    if file_extension.lower() == ".csv":
        categories_df = pd.read_csv(file_path)
    elif file_extension.lower() in [".xls", ".xlsx"]:
        categories_df = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format. Please provide a CSV or Excel file.")

    categories = Dimensions()

    for _, row in categories_df.iterrows():
        item = CategoryRanges(
            name=row["name"].strip(),
            min=row["min"],
            max=row["max"],
        )
        categories.add_category_range(row["category"], item)

    return categories


def read_pool_members_file(file_path: str) -> pd.DataFrame:
    """
    Reads a pool members CSV file (CSV or Excel) and returns a DataFrame.
    """
    _, file_extension = os.path.splitext(file_path)
    if file_extension.lower() == ".csv":
        return pd.read_csv(file_path)
    elif file_extension.lower() in [".xls", ".xlsx"]:
        return pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format. Please provide a CSV or Excel file.")


def verify_data(pool_members_df: pd.DataFrame, dimensions: Dimensions, participating_col: str, panel_size: int) -> None:
    """
    Verifies that the pool_members DataFrame and dimensions DataFrame meet the required conditions.
    1. For each category, all the values in the pool_members DataFrame must be present in the categories DataFrame.
    2. For each category, the min and max values must be non-negative integers, and min must be less than or equal to max.
    3. For each category, the sum of min values must not exceed the panel size.
    4. For each category, all the values in the categories DataFrame must be present in the pool_members DataFrame (not mandatory but recommended).
    5. The participating_col must exist in the pool_members DataFrame.
    6. The values in the participating_col must be either 'yes', 'no' or '?'
    7. No duplicated index values in pool_members DataFrame.
    """
    for dimension_name in dimensions.dimension_names:
        dimension = dimensions.get_dimension(dimension_name)

        # Check that all values in pool_members are in categories, and vice versa
        pool_member_values = set(pool_members_df[dimension_name].unique())
        category_values = set(item.name for item in dimension.get_ranges())
        missing_in_categories = pool_member_values - category_values
        missing_in_pool_members = category_values - pool_member_values
        if missing_in_categories:
            raise ValueError(
                f"Values {missing_in_categories} in pool_members for category '{dimension_name}' are missing in categories."
            )
        if missing_in_pool_members:
            raise ValueError(
                f"Warning: Values {missing_in_pool_members} in categories for category '{dimension_name}' are missing in pool_members."
            )

        # Check min and max values
        for item in dimension.get_ranges():
            if not (isinstance(item.min, int) and isinstance(item.max, int)):
                raise ValueError(
                    f"Min and Max values for '{item.name}' in category '{dimension_name}' must be integers."
                )
            if item.min < 0 or item.max < 0:
                raise ValueError(
                    f"Min and Max values for '{item.name}' in category '{dimension_name}' must be non-negative."
                )
            if item.min > item.max:
                raise ValueError(
                    f"Min value for '{item.name}' in category '{dimension_name}' cannot be greater than Max value."
                )

        # Check sum of min values
        total_min = sum(item.min for item in dimension.get_ranges())
        if total_min > panel_size:
            raise ValueError(f"Sum of Min values for category '{dimension_name}' exceeds panel size of {panel_size}.")

    # Check participating_col
    if participating_col not in pool_members_df.columns:
        raise ValueError(f"Participating column '{participating_col}' does not exist in pool_members DataFrame.")

    valid_participating_values = {"yes", "no", "?"}
    invalid_values = set(pool_members_df[participating_col].unique()) - valid_participating_values
    if invalid_values:
        raise ValueError(
            f"Invalid values {invalid_values} found in participating column '{participating_col}'. Allowed values are 'yes', 'no', '?'."
        )

    # Check for duplicated index values
    if pool_members_df.index.duplicated().any():
        duplicated_indices = pool_members_df.index[pool_members_df.index.duplicated()].unique()
        raise ValueError(f"Duplicated index values found in pool_members DataFrame: {duplicated_indices.tolist()}.")
