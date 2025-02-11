import pandas as pd

def txt_to_excel(txt_file, excel_file):
    try:
        with open(txt_file, "r", encoding="utf-8") as file:
            lines = file.readlines()

        # Split each line by a space or other delimiter and remove extra spaces
        # You can change the delimiter if needed (e.g., space, comma, tab)
        lines = [line.strip().split() for line in lines if line.strip()]

        # Create a DataFrame with multiple columns based on the split data
        df = pd.DataFrame(lines, columns=["Time", "Data"])  # Adjust column names as needed

        # Save the DataFrame to an Excel file
        df.to_excel(excel_file, index=False, engine="openpyxl")

        print(f"Conversion successful! Saved as {excel_file}")
    except Exception as e:
        print(f"Error: {e}")

# Example usage
txt_to_excel("time_output_server.txt", "times_server.xlsx")
