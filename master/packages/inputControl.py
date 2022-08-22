"""These functions checks the input given and raise error accordingly"""


def demandControl(df):
    demand_columns = ["No", "Width (mm)", "Weight (kg)", "Length (m)", "Grade"]
    for col in demand_columns:
        try:
            col in df.columns
        except KeyError:
            print("Try another input file, column {} is missing".format(col))
    print("Demand Input file has passed demandControl!")


def stockControl(df):
    stock_columns = [
        "No",
        "Width (mm)",
        "M4_NOMAL",
        "M4_BAO",
        "HODR_NIPON",
        "HODR_BAO",
        "HODR_TKES",
        "MOH_NIPON",
        "MOH_BAO",
        "M75_NIPON",
        "M75_BAO",
    ]
    for col in stock_columns:
        try:
            col in df.columns
        except KeyError:
            print("Try another input file, column {} is missing".format(col))
    print("Stock Input file has passed stockControl!")
