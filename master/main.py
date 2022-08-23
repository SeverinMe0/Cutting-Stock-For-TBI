"""Main program to run complete process given input"""

# import necessary modules and side functions
import pandas as pd
from packages.inputFile import importInputFile
from packages.inputControl import demandControl, stockControl
from packages.offcutSearch import offcutSearch
from packages.prepareCutting import prepareCutting
from packages.cutting import cutting
from packages.outputGeneration import slitPlanGeneration
from packages.updateStock import updateSlitStock, updateMotherStock


def main():
    # parameters
    u_bound = 600.0
    l_bound = 8.0
    grade_list = [
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
    density = 7.65

    # we begin with importing the input files
    (
        stock_mother_coil_df,
        stock_slit_coil_df,
        demand_df,
        thick_df,
        trim_df,
    ) = importInputFile()

    # quick Check on the inputs
    demandControl(demand_df)
    stockControl(stock_mother_coil_df)
    stockControl(stock_slit_coil_df)

    # we then perform the search for existing offcuts in stock that could help satisfy the demand
    to_cut_df, to_take_from_stock_df = offcutSearch(stock_slit_coil_df, demand_df)
    print(
        "List of requested items to take from the existing stock of offcuts: \n {}".format(
            to_take_from_stock_df
        )
    )

    # we can now compute the cutting patterns using df 'to_cut_df' and stock_mother_coil_df
    # we will proceed grade of material per grade of material
    for grade in grade_list:
        stock_width_l, to_cut_grade_df = prepareCutting(
            grade, stock_mother_coil_df, to_cut_df
        )
        if to_cut_grade_df.dropna().empty == False:
            trim_value = trim_df.loc[trim_df["Grade"] == grade]["Trim (mm)"].to_list()[
                0
            ]
            thickness_value = thick_df.loc[thick_df["Grade"] == grade][
                "Thick"
            ].to_list()[0]
            model = cutting(
                [x - trim_value for x in stock_width_l],
                to_cut_grade_df,
                upper_bound=u_bound,
                lower_bound=l_bound,
            )
            print(
                "List of mother coil widths available in stock for grade {}: \n {}".format(
                    grade, stock_width_l
                )
            )
            print(
                "Trim width for grade of material {}: \n {} mm".format(
                    grade, trim_df.loc[trim_df["Grade"] == grade]
                )
            )
            print(
                "List of different width to cut for grade {}: \n {}".format(
                    grade, to_cut_grade_df
                )
            )
            slit_plan = slitPlanGeneration(
                model,
                stock_width_l,
                to_cut_grade_df,
                grade,
                stock_mother_coil_df,
                trim_value,
                thickness_value,
                density,
            )
            print(slit_plan)

            slit_plan.to_excel("./output/slit_plan_" + grade + ".xlsx")

            updateSlitStock(stock_slit_coil_df, to_take_from_stock_df, slit_plan)
            updateMotherStock(stock_mother_coil_df, slit_plan)

            print(stock_mother_coil_df)
        else:
            print("No demand for grade {}".format(grade))


if __name__ == main():
    main()
