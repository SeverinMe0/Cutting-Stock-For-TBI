"""This file takes into input the grade of material, the stock of mother coils and the list of items to cut.
It returns the list of item to cut and given stock for the particular grade of material.
This program adapts the input for the optimization algorithm 'cutting.py'

Input: 
    - stock_mother_coil_df
    - to_cut_df'
Output: 
    - stock_width_l: list that contains the width of coils in stock from the stock df
    - to_cut_grade_df: df containing width to cut + number of coil requested (and not mass requested!).
        It has Width as index, number requested as column"""

import pandas as pd


def prepareCutting(grade, stock_mother_coil_df, to_cut_df):
    stock_mother_coil_df[grade] = stock_mother_coil_df[grade].fillna(0)
    stock_width_l = stock_mother_coil_df[stock_mother_coil_df[grade] != 0][
        "Width (mm)"
    ].to_list()
    to_cut_grade_df = (
        to_cut_df[to_cut_df["Grade"] == grade].groupby("Width (mm)").count()["Mass"]
    )
    to_cut_grade_df = pd.DataFrame(to_cut_grade_df)
    to_cut_grade_df.rename(columns={"Mass": "Number"}, inplace=True)
    to_cut_grade_df.reset_index(inplace=True)
    return stock_width_l, to_cut_grade_df
