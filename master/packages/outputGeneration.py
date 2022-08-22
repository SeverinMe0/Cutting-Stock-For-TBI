"""This file take into input the result of the algorithm and generate a cutting plan on excel"""

import pandas as pd


def slitPlanGeneration(
    model,
    stock_width_l,
    to_cut_grade_df,
    grade,
    stock_mother_coil_df,
    trim_value,
    thickness,
    density,
):
    # printing the model variables
    """print('')
    print('Objective value: {model.objective_value:.3}'.format(**locals()))
    print('Solution: ', end='')
    for v in model.vars:
        if v.x > 1e-5:
            print('{v.name} = {v.x}'.format(**locals()))
            print('          ', end='')"""

    slit_plan = {}
    n = len(stock_width_l)
    m = len(to_cut_grade_df.index)

    for j in range(n):
        name_y = "y[%d]" % j
        name_s = "s[%d]" % j
        if model.vars[name_y].x != 0:
            pattern = {}
            cuts_count = 0

            for i in range(m):
                name_x = "x[%d,%d]" % (i, j)
                if model.vars[name_x].x != 0:
                    for k in range(int(model.vars[name_x].x)):
                        cuts_count += 1
                        col = "Width-%d (mm)" % cuts_count
                        pattern[col] = to_cut_grade_df.loc[i]["Width (mm)"]

            extra_width = 10 * model.vars[name_s].x
            pattern["Extra Width Generated (mm)"] = extra_width
            pattern["Trim (mm)"] = trim_value
            mother_coil_width = stock_width_l[j]
            pattern["Mother Coil Width (mm)"] = mother_coil_width
            pattern["Grade"] = grade
            mother_coil_weight = stock_mother_coil_df.loc[
                stock_mother_coil_df["Width (mm)"] == stock_width_l[j]
            ][grade].to_list()[0]
            pattern["Mother Coil Weight (kg)"] = mother_coil_weight
            mother_coil_length = (
                1000 * mother_coil_weight / density / thickness / mother_coil_width
            )
            pattern["Mother Coil Length (m)"] = mother_coil_length

            cuts_count = 0
            for i in range(m):
                name_x = "x[%d,%d]" % (i, j)
                if model.vars[name_x].x != 0:
                    for k in range(int(model.vars[name_x].x)):
                        cuts_count += 1
                        col = "Weight-%d (kg)" % cuts_count
                        weight_job = (
                            to_cut_grade_df.loc[i]["Width (mm)"]
                            * mother_coil_length
                            * thickness
                            * density
                            / 1000
                        )
                        pattern[col] = weight_job

            pattern["Extra Weight (kg)"] = (
                extra_width * mother_coil_length * thickness * density / 1000
            )

            slit_plan[j] = pattern
    slit_plan = pd.DataFrame.from_dict(slit_plan, orient="index")
    slit_plan.fillna(0.0, inplace=True)
    return slit_plan
