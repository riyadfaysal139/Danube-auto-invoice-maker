import pandas as pd

def modify_dataframe(df, edit_flag):
    if edit_flag.lower() == 'yes':
        history = [df.copy()]  # Initialize history with the original DataFrame
        print("DataFrame before modification:")
        print(df)
        while True:
            action = input("Choose an action: add, delete, modify, undo, or done: ").strip().lower()
            if action == 'add':
                df = add_row(df)
                history.append(df.copy())
            elif action == 'delete':
                df = delete_row(df)
                history.append(df.copy())
            elif action == 'modify':
                df = modify_row(df)
                history.append(df.copy())
            elif action == 'undo':
                if len(history) > 1:
                    history.pop()
                    df = history[-1].copy()
                    print("Undo successful. Current DataFrame:")
                    print(df)
                else:
                    print("Nothing to undo.")
            elif action == 'done':
                break
            else:
                print("Invalid action. Please choose add, delete, modify, undo, or done.")
        print("DataFrame after modification:")
        print(df)
    return df

def add_row(df):
    new_row = {}
    sku_value = input("Enter value for SKU: ").strip()
    if sku_value in df['SKU'].values:
        print("SKU already exists. Please modify the existing row instead.")
        return df
    new_row['SKU'] = sku_value
    for column in df.columns:
        if column not in ["SKU", "Price", "Vat", "Amount"]:
            value = input(f"Enter value for {column} ({df[column].dtype}): ").strip()
            if df[column].dtype == 'int64':
                new_row[column] = int(value)
            elif df[column].dtype == 'float64':
                new_row[column] = float(value)
            else:
                new_row[column] = value
    df = df.append(new_row, ignore_index=True)
    df = recalculate_totals(df)
    df['SKU'] = pd.to_numeric(df['SKU'], errors='coerce')
    df = df.sort_values(by="SKU").reset_index(drop=True)
    print("DataFrame after adding the row:")
    print(df)
    return df

def delete_row(df):
    sku_number = input("Enter the SKU number of the row to delete: ").strip()
    # Convert the input SKU number to the same type as the SKU column
    sku_number = convert_sku_type(sku_number, df['SKU'].dtype)
    row_index = df[df['SKU'] == sku_number].index
    if not row_index.empty:
        df = df.drop(row_index).reset_index(drop=True)
        df = recalculate_totals(df)
        print("DataFrame after deleting the row:")
        print(df)
    else:
        print("Invalid SKU number.")
    return df

def modify_row(df):
    sku_number = input("Enter the SKU number of the row to modify: ").strip()
    # Convert the input SKU number to the same type as the SKU column
    sku_number = convert_sku_type(sku_number, df['SKU'].dtype)
    row_index = df[df['SKU'] == sku_number].index
    if not row_index.empty:
        row_index = row_index[0]
        for column in ["Description", "Unit Price", "Quantity"]:
            new_value = input(f"Enter new value for {column} (leave blank to keep current value): ").strip()
            if new_value:
                if column == "Quantity":
                    while not new_value.isdigit():
                        new_value = input("Invalid input. Enter an integer value for Quantity: ").strip()
                    df.at[row_index, column] = int(new_value)
                elif df[column].dtype == 'int64':
                    df.at[row_index, column] = int(new_value)
                elif df[column].dtype == 'float64':
                    df.at[row_index, column] = float(new_value)
                else:
                    df.at[row_index, column] = new_value
        df = recalculate_totals(df)
        print("DataFrame after modifying the row:")
        print(df)
    else:
        print("Invalid SKU number.")
    return df

def convert_sku_type(sku_number, dtype):
    if dtype == 'int64':
        return int(sku_number)
    elif dtype == 'float64':
        return float(sku_number)
    else:
        return sku_number

def recalculate_totals(df):
    df["Unit Price"] = pd.to_numeric(df["Unit Price"], errors='coerce').round(3)
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors='coerce').fillna(0).astype(int)
    df["Price"] = (df["Unit Price"] * df["Quantity"]).round(4)
    df["Vat"] = (df["Price"] * 0.15).round(4)
    df["Amount"] = (df["Price"] + df["Vat"]).round(4)
    return df
