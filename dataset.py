import csv

# Create a list of dictionaries containing currency data
currency_data = [
    {"Currency_Code": "AED", "Currency_Name": "United Arab Emirates Dirham", "Exchange_Rate": 3.880669},
    {"Currency_Code": "AFN", "Currency_Name": "Afghan Afghani", "Exchange_Rate": 80.043644},
    {"Currency_Code": "ALL", "Currency_Name": "Albanian Lek", "Exchange_Rate": 105.849142},
    {"Currency_Code": "AMD", "Currency_Name": "Armenian Dram", "Exchange_Rate": 426.944097},
    {"Currency_Code": "ANG", "Currency_Name": "Netherlands Antillean Guilder", "Exchange_Rate": 1.903318},
    {"Currency_Code": "AOA", "Currency_Name": "Angolan Kwanza", "Exchange_Rate": 872.484564},
    {"Currency_Code": "ARS", "Currency_Name": "Argentine Peso", "Exchange_Rate": 369.804877},
    {"Currency_Code": "AUD", "Currency_Name": "Australian Dollar", "Exchange_Rate":  1.649393},
    {"Currency_Code": "AWG", "Currency_Name": "Aruban Florin", "Exchange_Rate":  1.901763},
    {"Currency_Code": "AZN", "Currency_Name": "Azerbaijani Manat", "Exchange_Rate":  1.789778},
    {"Currency_Code": "BAM", "Currency_Name": " Bosnia-Herzegovina Convertible Mark", "Exchange_Rate": 1.962263},
    {"Currency_Code": "BBD", "Currency_Name": " Barbadian Dollar", "Exchange_Rate": 2.132725},
    {"Currency_Code": "BDT", "Currency_Name": "  Bangladeshi Taka", "Exchange_Rate":116.454675},
    


    # Add more data here
]

# Specify the CSV file name
csv_filename = "exchange_rates.csv"

# Define the CSV fieldnames (column names)
fieldnames = ["Currency_Code", "Currency_Name", "Exchange_Rate"]

# Write the data to a CSV file
with open(csv_filename, mode="w", newline="") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    # Write the header row
    writer.writeheader()

    # Write the data rows
    writer.writerows(currency_data)

print(f"Data has been written to {csv_filename}")
