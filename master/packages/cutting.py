""" IMPORTANT: This program uses 'naive' Mixed Integer Programming (MIP) Model for Cutting Stock Problem (see readMe.md)
and not Column Generation Technique! Do not give into input large files!
This is an adaptation CSP 'naive' model with multiple bars in stock of different length 
and constrained slack variable to generate offcut of standard width.

Input: 
    - stock_width_l: coil width of coils in stock
    - to_cut_grade_df: coil width and number requested
    - upper_bound & lower bounds for slack variables.
    
Output: 
    - Object mip.Model containing results of optimization of the MIP Model."""

from mip import Model, xsum, BINARY, INTEGER


def cutting(stock_width_l, to_cut_grade_df, upper_bound, lower_bound):

    n = len(stock_width_l)  # number of coils in stock
    m = len(to_cut_grade_df.index)  # number of different width required

    # creating the model (see readMe.md)
    model = Model()
    x = {
        (i, j): model.add_var(obj=0, var_type=INTEGER, name="x[%d,%d]" % (i, j))
        for i in range(m)
        for j in range(n)
    }  # number of coil of length i cut from mother coil j numbering the standard stocked coil 1, 2, 3...
    y = {
        j: model.add_var(obj=1, var_type=BINARY, name="y[%d]" % j) for j in range(n)
    }  # indicator variable, y[j] = 1 if and only if mother coil j is used
    s = {
        j: model.add_var(obj=0, var_type=INTEGER, name="s[%d]" % j) for j in range(n)
    }  # slack variable used to generate reusable offcuts
    t = {
        j: model.add_var(obj=0, var_type=BINARY, name="t[%d]" % j) for j in range(n)
    }  # binary variables used to constrain slack variables

    # constraints (see readMe.md)
    for i in range(m):
        model.add_constr(
            xsum(x[i, j] for j in range(n)) == to_cut_grade_df["Number"][i]
        )  # orders must be satisfied
    for j in range(n):
        model.add_constr(
            xsum(to_cut_grade_df["Width (mm)"][i] * x[i, j] for i in range(m))
            + 10 * s[j]
            == stock_width_l[j] * y[j]
        )  # cutting pattern must use the entire coil or generate reusable offcut
    """TO DO : add a parameter for those ranges for the slack variable"""
    for j in range(n):
        model.add_constr(s[j] >= lower_bound * t[j])
        model.add_constr(
            s[j] <= upper_bound * t[j]
        )  # slack constraints to generate reusable offcuts of standard width (ie between 80mm and 6000mm)
    for j in range(1, n):
        model.add_constr(y[j - 1] >= y[j])  # additional constraints to reduce symmetry

    # optimizing the model
    model.verbose = 0
    model.optimize()

    return model
