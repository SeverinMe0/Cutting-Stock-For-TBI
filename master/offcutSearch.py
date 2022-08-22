""" This program performs an offcut search: It takes into input the demand for coils, 
the stock of offcuts, and returns 2 dataframes: the width to be cut from the stock of mother coils, 
and the width to be taken from the stock of existing offcuts."""

import pandas as pd
from append import append_value


def offcutSearch(stock_slit_coil_df, demand_df):

    # dictionnaries that will contain the width and data of coil to be cut from new coils
    #  and to be taken from the existing stock of offcuts
    w_to_cut = {}
    w_to_take = {}

    # we join the df of demand and the df of offcuts stock on the parameter width
    merged_df = pd.merge(
        demand_df, stock_slit_coil_df, left_on="Width (mm)", right_on="Width (mm)"
    )

    # we complete the dictionnaries according to weight available and demand.
    for index, row in merged_df.iterrows():

        width = row["Width (mm)"]
        grade_of_material = row["Grade"]
        mass_available_in_stock = row[grade_of_material]
        mass_requested = row["Weight (kg)"]

        # if stock is available and sufficient to fulfill the entire order,
        # we add to w_to_take the width of coil, its grade,
        # the mass requested and the mass available in stock
        if mass_available_in_stock >= mass_requested:
            append_value(w_to_take, "Width (mm)", width)
            append_value(w_to_take, "Grade", grade_of_material)
            append_value(w_to_take, "Mass Requested", mass_requested)
            append_value(w_to_take, "Mass in Stock", mass_available_in_stock)

        # else if stock is available but not sufficient to fulfill the order,
        # we add to w_to_take the width of coil, its grade, the mass requested,
        # the mass available in stock,
        # and we add to w_to_cut the difference of mass requested and available
        elif mass_available_in_stock > 0 and mass_available_in_stock < mass_requested:
            append_value(w_to_take, "Width (mm)", width)
            append_value(w_to_take, "Grade", grade_of_material)
            append_value(w_to_take, "Mass Requested", mass_requested)
            append_value(w_to_take, "Mass in Stock", mass_available_in_stock)

            append_value(w_to_cut, "Width (mm)", width)
            append_value(w_to_cut, "Grade", grade_of_material)
            append_value(w_to_cut, "Mass", mass_requested - mass_available_in_stock)

        # else if no stock is available
        else:
            append_value(w_to_cut, "Width (mm)", width)
            append_value(w_to_cut, "Grade", grade_of_material)
            append_value(w_to_cut, "Mass", mass_requested)

    # we convert the dictionnaries into dataframes and return them
    to_cut_df = pd.DataFrame.from_dict(w_to_cut)
    to_take_from_stock_df = pd.DataFrame.from_dict(w_to_take)
    return to_cut_df, to_take_from_stock_df
