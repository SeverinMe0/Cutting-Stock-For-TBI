# __Cutting Stock Problem with Reusable Offcuts - Waste Reduction for TBI Plant__

For any information on this program, please ask Severin Meo (SESA657712, @SeverinMe0 on GitHub)

## **Acknowledgement**

I would like to thank TBI team for their support, as both sides were cooperative during this project. TBI team was open and responsive during the process of development. I would like to thank Alihan Kucukyilmaz and Jerome Guesnon for their help managing this project and the relation with TBI team. Finally I would like to thank Tristan Rigaut for his help when creating the optimization model.

## __Business Problem__

The manufacture of Transformers requires costly material, among which ferromagnetic metal sheets that make up its core. These sheets are winded into __metal coils of different grade,__ indicating the quality and the supplier of the material. As a transformer manufacture, TBI plant has a specific process where coils of ferromagnetic material are __cut into coils of different width.__ This process is process is called __slitting__. Process of slitting is described below:
- Firstly, manufacturers receive a "__design request__", formulating a demand of coils of certain mass and width. This document specifies following parameters:
    - __Width__ (mm) of coil requested.
    - __Weigth__ (kg) of coil requested.
    - __Length__ (mm) of coil requested.
    - __Grade__ of material of the coil.
- Given the design request, manufacturers __check in their stock if former cuts of material__, that haven't been used and saved for later, can be used to fulfill element of the design request. Such items will be named "__offcuts__" in the following.
- If there is still requests after this step, manufacturers have to cut new coils, called __mother coils__. In order to minimize the cost of production, __if the entire mother coil should be used, there shall be no waste in this process.__ Therefore, when a mother coil is cut but not the entire width of the mother coil is needed, __the offcut is stored in the plant, and saved for a future design request.__ To be noted that design request will ask for coil of standard width: the acceptable width lies in a range from $[80mm;\ 500mm]\ modulo\ 10$, meaning that width are multiple of $10$, and between $80$ or $500$ millimeters.
- Therefore, when creating a __slitting pattern__, i.e. decide how to fit the requested width into the stock of mother coils to perform the most efficient cut, engineers have browse through several Excel files, fill them manually and choose an optimal cutting pattern by themselves. This process is __time consuming__, ends up to __errors__, and can be __sub-optimal__, leading to overuse mother coils or excessive stock.

The following software aims to tackle this problematic.

## __Front-End__
This software has following structure: the __master folder__ contains the folders "data", "output", and "packages", and also the files "hook-mip.py", "main.py". It contains all the Python code needed for computing slit plans automatically. To do so, if you have a Python Interpreter, you just have to run the program "main".

### __How to generate slit plans?__

To generate sit plans with this program, there is two easy steps to follow. Firstly fill the data folder with your data (see section below), then run main.py.

#### __How the data folder should be handled?___

The main program browses the folder “data” to generate the slitting plan. All the input you can find there can be modified, provided that the name of each file stays the same and that the structure of each file is preserved. Here how each input should be handled:
-	the data folder is organized as follow:

<figure>
<img src=img/Data_Folder_Content.png>
<figcaption><b>Figure 1 - Data Folder Content</b></figcaption>
</figure>

-	To be firstly noted that, for the program to run without error, all the data files should have the names displayed in Fig.1. They should also have the same structure.
-	The file “design.xlsx” contains the request for slitting. It follows below structure:

<figure>
<img src=img/Example_of_design.xlsx_input_file.png>
<figcaption><b>Figure 2 - Example of "design.xlsx" input file</b></figcaption>
</figure>

    - Name of columns shouldn’t be modified otherwise the program will return an error.
    - In this file, you should add the Width in mm requested, the weight in kg, the length in m and the grade of material to be cut.
-	The file “stock_mother_coil.xlsx” contains the stock of mother coil. Once again, its name shouldn’t change, and its structure should be respected to run the program. 

<figure>
<img src=img/Example_of_stock_mother_coil.xlsx_input_file.png>
<figcaption ><b>Figure 3 - Example of "stock_mother_coil.xlsx" input file</b></figcaption>
</figure>

    - Name of columns shouldn’t be modified otherwise the program will return an error.
    - The “stock_mother_coil.xlsx” file contains, for each width of mother coil, the mass in stock for each grade of material.

-	The file “stock_slit_coil.xlsx” follow the same structure as “stock_mother_coil.xlsx”. It contains the stock of slit coils that haven’t been used before. The program will check it, take it account when generating slit plans.

<figure>
<img src=img/Example_of_stock_slit_coil.xlsx_input_file.png>
<figcaption ><b>Figure 3 - Example of "stock_slit_coil.xlsx" input file</b></figcaption>
</figure>

    - Name of columns shouldn’t be modified otherwise the program will return an error.
    - The “stock_slit_coil.xlsx” file contains, for each width of mother coil, the mass in stock for each grade of material.


-	The file “thick.xlsx” contains the thickness for each grade of material. The program takes it into account for computing mass generated when slitting mother coils.

<figure>
<img src=img/Example_of_thickness_file.png>
<figcaption ><b>Figure 5 - Example of thickness file</b></figcaption>
</figure>

    - Name of columns shouldn’t be modified otherwise the program will return an error.
- The file “trim.xlsx” contains the trim in mm on each side needed for each grade. 

<figure>
<img src=img/Example_of_trim_file.png>
<figcaption ><b>Figure 5 - Example of trim file</b></figcaption>
</figure>

    - Name of columns shouldn’t be modified otherwise the program will return an error.

#### __How the output will be generated?__

Once you’ve entered and your input in data file, and executed $\textsf{main.py} $ after a few seconds, in the “output” folder, several files will appear:

<figure>
<img src=img/Example_of_output_generated_by_the_executable.png>
<figcaption ><b>Figure 7 - Example of output generated by the executable</b></figcaption>
</figure>

-	For each grade of material, we will find an excel file name “slit_plan_<grade>.xlsx”. It contains the slit plan for each mother coil. Below is an example of such file:

<figure>
<img src=img/Example_of_generated_slit_plan_for_grade_M75_BAO_1.png>
<img src=img/Example_of_generated_slit_plan_for_grade_M75_BAO_2.png>
<figcaption ><b>Figure 8 - Example of generated slit plan for grade M75_BAO</b></figcaption>
</figure>

-	A folder named “updatedStock” contains the stock files if all the slit plans are in reality followed and that mother coils or slit coils are processed.

<figure>
<img src=img/Content_of_updatedStock_folder.png>
<figcaption ><b>Figure 9 - Content of "updatedStock" folder</b></figcaption>
</figure>

    - The above files follow the same structure as “stock_mother_coil.xlsx” and can be used as input stock files in data folder.
-	The file “coils_requested_to_take_from_stock.xlsx”, as its name indicates, contains the data of the coils requested that can be fulfilled with previous offcuts. 

<figure>
<img src=img/Example_of_coil_request_to_take_from_stock.xlsx.png>
<figcaption ><b>Figure 10 - Example of "coil_request_to_take_from_stock.xlsx"</b></figcaption>
</figure>


## __Back-End__

### __Required Libraries__
This software has been programmed under:
- Python 3.9.4 \
with following libraries:
    - pandas 1.4.1
    - mip 1.14.0
    - Pyinstaller 4.8

under the platform Windows-10-10.0.19043-SP0 64bits.

### $\textsf{main.py}$ - __Main Algorithm__

This program mimics the complete process followed by manufacturers when they create a slit plan. This process is detailed in the following pseudo-algorithm.

<figure>
<img src=img/Algo_main.PNG>
<figcaption ><b>Figure 11 - Pseudo-algorithm implemented in main.py to create slit plans."</b></figcaption>
</figure>

The program $\textsf{main.py}$ implement this pseudo-code. To match as close as possible this structure, external functions have been developed and stored in the folder "packages". As we can see, most of the steps consist only in input reading and processing. Each functions contains comments that should make it easy to understand.
Here is a quick overview of the function of each functions in package:

- $\textsf{inputFile.py}$: This file extracts the files necessary to the slitting process: the stock of mother coils, the stock of offcuts, the customer request.
- $\textsf{inputControl.py}$: These functions checks the input given and raise error accordingly.
- $\textsf{offcutSearch.py}$: This program performs an offcut search: It takes into input the demand for coils,
the stock of offcuts, and returns 2 dataframes: the width to be cut from the stock of mother coils, and the width to be taken from the stock of existing offcuts.
- $\textsf{prepareCutting.py}$: This file takes into input the grade of material, the stock of mother coils and the list of items to cut. It returns the list of item to cut and given stock for the particular grade of material. This program adapts the input for the optimization algorithm $\textsf{cutting.py}$.
- $\textsf{cutting.py}$: This is an adaptation of Cutting Stock Problem (CSP) 'naive' model with multiple bars in stock of different length and constrained slack variable to generate offcut of standard width. See next section for more info.
- $\textsf{outputGeneration.py}$: This file take into input the result of the algorithm cutting.py and generate a cutting plan on excel.
- $\textsf{updateStock.py}$: This program takes into input the results of cutting order & the width to take from stock to update the stock of existing offcuts & the stock of mother coils.
- $\textsf{append.py}$: This function appends a couple key/value to a dictionary.

The only difficulty here consists in developing a program minimizing the number of new mother coils to be used, i.e. __step 6__. We will present it in the following.

### $\textsf{cutting.py}$ - __MIP Problem Solver__

The following Mixed-Integer-Programming (MIP) Problem has been implemented in the program $\textsf{cutting.py}$. This is an adaptation of Cutting Stock problem (CSP) 'naive' model, to consider multiple coils in stock of different width and constrained slack variable to generate offcuts of standard width. Please check [1], section 9.6, for more infos (search for Cutting Stock Problem).

#### **Inputs**

- __stock_width_l__: a list containing the coil widths of new mother coils in stock.
- __to_cut_grade_df__: a pd.Dataframe containing width and number requested of coils requested.
- __upper_bound__ & __lower_bound__ for slack variables: indeed the generated offcuts have a width contained in $[80mm;\ 500mm]$.

Using these inputs, we build the following variables.

#### **Variables**
Here $n = len(stock\_width\_l)$, i.e. $n$ is the number of coils in stock, and $ m = len(to\_cut\_grade\_df.index)$, i.e. $m$ is the number of different width required. These variables are key to build the MIP variables of our model:
- $\forall\; j\in [1;m],\; \forall\; i\in [1;n],\;$ $x_{i,j}$, an integer variable: number of coil of width i cut from mother coil j.
- $\forall\; i\in [1;n],\;$ $y_{j}$, a boolean variable: indicator variables, $y_{j} = 1$ if and only if standard coil j is used.
- $\forall\; i\in [1;n],\;$ $s_{j}$, an integer variable: Slack variables used to generate reusable offcuts.
- $\forall\; i\in [1;n],\;$ $t_{j}$, a boolean variable: Boolean variables to constraint the range of our slack variable.

#### **Problem Statement**
We adapt here the "Naive" model usually used for modelling the cutting stock problem, see _H. Paul Williams_ [1]:

$$ Minimize\; f(y_{1},...,y_{n}) = \sum_{i=1}^{n}{y_{i}} \\$$

$
Subject\;to:\\
(1)\; \forall\; j\in [1;m],\; \sum_{i=1}^{n}{x_{i,j}} = b_{i} \\
(2)\; \forall\; j\in [1;m],\; \sum_{i=1}^{n}{w_{i}*x_{i,j} + 10*s_{j}} = L_{j}*y_{j}\\
$

#### **Model Explanation**
The objective function $f$ represents the total number of coils used, which should be minimized.\
Constraint $(1)$ impose that demand must be met.\
Constraint $(2)$ impose that the cutting pattern must use the entirety of used coil (if ${s_j}=0$), or generate an offcut of standard width (if $s_{j} \neq 0$). 
We have used in this last constraint the fact that requested widths, and therefore offcuts widths, must all be multiple of 10. Therefore ${s_j}$ are integer variables in the interval $[8;\ 50]$.
#### **Adding Constraints**
This naive model has the default to have symmetrical solutions. We therefore add the following constraint to reduce symmetry:
$$ (3)\; \forall\;j\in [1;m],\; y_{j-1}\geq y_{j}$$
**This constraint will give priority to the first elements in stock. This rule might be change in the future to suit better industrial needs.**\
We then try to add a constraint specifying the range of possible values for the slack variables to generate standard cutting patterns :
$$(4)\; \forall j, \; (lower\_bound \le s_{j} \le upper\_bound)\;
OR\;
 (s_{j}=0)$$
This is a specific constraint on integer variable, that look hard to implement on the first hand. It could be reformulated into a non-linear constraint:
$$\forall\;j,\; s_{j}*(s_{j}-8.0) \geq 0 $$
How to deal with this constraint?\
We could impose $s_{j}$ as a sum of boolean variable, $s_{j} = \sum_{i=1}^{B}{i*{\delta}_{i}}$ where ${\delta}_{i}=1$ if and only if $s_{j}=i$, develop the product and set boolean constraints. But it would lead to an explosion of the number of variables, problem that can be tackle if we reduce the range of acceptable slack variables...\
__To deal smartly with this issue,__ we introduce new binary variables, $(t_{j})_{j \in [1;n]}$, and set the following constraints:
$$\forall j, \; s_{j}\geq 8.0*t_{j}$$
$$\forall j, \; s_{j}\le 50.0*t_{j}$$
We therefore have, if $t_{j}=0$, $s_{j}=0$, and if $t_{j}=1$, $s_{j} \in [8,50]$ while introducing 'only' $n$ new binary variable. **Coupled with constraint $\bold{(2)}$, every cutting pattern will either use the entirety of a coil to meet the demand, or generate an offcut of width multiple of $ \bold{10}$, and of width between $\bold{80 mm}$ and $\bold{500 mm}$.**

#### __Output__
The program $\textsf{cutting.py}$ implements this model and optimizes it using $\textsf{mip.Model.optimize()}$ function. See the documentation of $\textsf{python-mip}$ library [here](https://python-mip.readthedocs.io/en/latest/).
The output of this function will be ingested by the program $\textsf{outputGeneration.py}$ to then create the slit plan.

## __Creating an executable__
- If you don't have it already, install pyinstaller using pip: 
```
pip install pyinstaller --upgrade --user
```
- Using your command prompt, go to the location of $\textsf{main.py}$, and type:
```bash
pyinstaller --noconfirm --onefile --console --name "SlitPlanGenerator" --add-data "<your_location>/Cutting-Stock-For-TBI/master/data;data/" --hidden-import "mip" --additional-hooks-dir "<your_location>/Cutting-Stock-For-TBI/master"  "<your_location>Cutting-Stock-For-TBI/master/main.py" --clean --windowed
```
Of course, type your location of your folder "Cutting-Stock-For-TBI" instead of "<your_location>".
- This will take a few minutes. A folder "build" and "dist" should appear, as well as a file "SlitPlanGenerator.spec".
- The file $\textsf{hook-mip.py}$ is very important and allows a proper import of the library $\textsf{python-mip}$ when generating the .exe with pyinstaller.
- In the folder "dist", you'll find the executable "SlitPlanGenerator.exe". This is the program to run in order to generate slit plans if you can't run python files.
- __To share the slit plan generator to someone that hasn't got a Python interpreter__, create a zip folder with
    - data folder
    - output folder
    - SlitPlanGenerator.exe
    - readme.docx
-  and share it with your colleague. The file readme.docx contains useful information on how to run the program when you don't have a Python environment.

## Conclusion
This document comes now to an end. I hope this documentation is clear. If you have any questions or suggestion, please feel free to reach via GitHub or my email adress: severin.meo@student-cs.fr. Obviously, there is still a lot of work to be completed. The very minimal user interface can be improved with Tkinter, or we can imagine a web interface. To do so, Quartz Design System Team, via François Delpech de Frayssinet, can be reached.

## **References**

[1]: H. Paul Williams, "Model Building in Mathematical Programming, 5th Edition", March 2013, ISBN: 978-1-118-44333-0.

