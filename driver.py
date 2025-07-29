import pyodbc

# List all ODBC drivers installed on the system
drivers = [driver for driver in pyodbc.drivers()]
print("ODBC Drivers available:")
for driver in drivers:
    print(driver)