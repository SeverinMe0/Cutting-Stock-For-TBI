"""This function the files necessary to the slitting process:
the stock of mother coils, the stock of offcuts, the customer request."""

"""TO DO: location of the file might change. Adding in argument the location can be sufficient"""

import pandas as pd


def importInputFile():
    # stock of mother coils
    stock_mother_coil_df = pd.read_excel("./master/data/stock_mother_coil.xlsx")
    stock_mother_coil_df.fillna(0, inplace=True)
    # stock of offcuts of standard width
    stock_slit_coil_df = pd.read_excel("./master/data/stock_slit_coil.xlsx")
    stock_slit_coil_df.fillna(0, inplace=True)
    # customer request
    demand_df = pd.read_excel("./master/data/design.xlsx")

    # thickness of different coils (depends on the grade of material)
    thick_df = pd.read_excel("./master/data/thick.xlsx")

    # trim loss required (depends on the grade of material)
    trim_df = pd.read_excel("./master/data/trim.xlsx")

    return stock_mother_coil_df, stock_slit_coil_df, demand_df, thick_df, trim_df
