"""This program takes into input the results of cutting order & the width to take from stock
to update the stock of existing offcuts & the stock of mother coils"""

"""when we take a coil from stock of offcuts, and the demand is INFERIOR to mass available.
the updated stock should contain the difference between the two mass?
or the existing offcut will be used entirely?"""


def updateSlitStock(stock_slit_coil_df, to_take_from_stock_df, slit_plan):

    # we begin with updating the stock of slit coils with the coils to be taken from existing stock
    for index, row in to_take_from_stock_df.iterrows():

        initial_stock_index = stock_slit_coil_df.loc[
            stock_slit_coil_df["Width (mm)"] == row["Width (mm)"]
        ].index

        initial_stock_mass = stock_slit_coil_df.loc[
            stock_slit_coil_df["Width (mm)"] == row["Width (mm)"]
        ][row["Grade"]]

        updated_stock_mass = initial_stock_mass - row["Mass Requested"]
        stock_slit_coil_df.at[initial_stock_index[0], row["Grade"]] = updated_stock_mass
        print(initial_stock_index, initial_stock_mass, updated_stock_mass)

    # then we update the stock of slit coils with the coils generated by the cutting process
    for index, row in slit_plan.iterrows():

        initial_stock_index = stock_slit_coil_df.loc[
            stock_slit_coil_df["Width (mm)"] == row["Extra Width Generated (mm)"]
        ].index

        initial_stock_mass = stock_slit_coil_df.loc[
            stock_slit_coil_df["Width (mm)"] == row["Extra Width Generated (mm)"]
        ][row["Grade"]]

        updated_stock_mass = initial_stock_mass + row["Extra Weight (kg)"]

        stock_slit_coil_df.at[initial_stock_index[0], row["Grade"]] = updated_stock_mass


def updateMotherStock(stock_mother_coil, slit_plan):

    # mother coils taken for slit plan need to be removed from the stock of mother coils.
    for index, row in slit_plan.iterrows():
        initial_stock_index = stock_mother_coil.loc[
            stock_mother_coil["Width (mm)"] == row["Mother Coil Width (mm)"]
        ].index

        initial_stock_mass = stock_mother_coil.loc[
            stock_mother_coil["Width (mm)"] == row["Mother Coil Width (mm)"]
        ][row["Grade"]]

        updated_stock_mass = initial_stock_mass - row["Mother Coil Weight (kg)"]

        stock_mother_coil.at[initial_stock_index[0], row["Grade"]] = updated_stock_mass