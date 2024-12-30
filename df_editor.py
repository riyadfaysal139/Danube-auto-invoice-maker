import pandas as pd

def add_product(df, sku, description, unit_price, quantity):
    new_row = {
        "SKU": sku,
        "Description": description,
        "Unit Price": unit_price,
        "Quantity": quantity,
        "Price": unit_price * quantity,
        "Vat": (unit_price * quantity) * 0.15,
        "Amount": (unit_price * quantity) * 1.15
    }
    df = df.append(new_row, ignore_index=True)
    return df

def modify_product(df, sku, description=None, unit_price=None, quantity=None):
    index = df[df['SKU'] == sku].index
    if not index.empty:
        if description is not None:
            df.at[index[0], 'Description'] = description
        if unit_price is not None:
            df.at[index[0], 'Unit Price'] = unit_price
            df.at[index[0], 'Price'] = unit_price * df.at[index[0], 'Quantity']
            df.at[index[0], 'Vat'] = df.at[index[0], 'Price'] * 0.15
            df.at[index[0], 'Amount'] = df.at[index[0], 'Price'] * 1.15
        if quantity is not None:
            df.at[index[0], 'Quantity'] = quantity
            df.at[index[0], 'Price'] = df.at[index[0], 'Unit Price'] * quantity
            df.at[index[0], 'Vat'] = df.at[index[0], 'Price'] * 0.15
            df.at[index[0], 'Amount'] = df.at[index[0], 'Price'] * 1.15
    return df

def delete_product(df, sku):
    df = df[df['SKU'] != sku]
    return df

def handle_dataframe(df, action, sku, description=None, unit_price=None, quantity=None):
    if action == 'add':
        df = add_product(df, sku, description, unit_price, quantity)
    elif action == 'modify':
        df = modify_product(df, sku, description, unit_price, quantity)
    elif action == 'delete':
        df = delete_product(df, sku)
    return df

def edit_dataframe(df):
    # Example edits, replace with actual logic as needed
    df = handle_dataframe(df, "add", "123456", "New Product", 10.0, 5)
    df = handle_dataframe(df, "modify", "123456", quantity=10)
    df = handle_dataframe(df, "delete", "123456")
    return df
