---
bibliography: references.bib
link-citations: true
---

# Cutting Stock with Reusable Offcuts - Naive Model

For any information on this program, please ask Severin Meo (SESA657712, @SeverinMe0 on GitHub)
## **Acknowledgement**
I would like to thank TBI team, especially Sachin Singh, for their support, as both sides were cooperative during this project. TBI team was open and responsive during the process of development. I would like to thank Alihan Kucukyilmaz and Jerome Guesnon for their help managing this project and the relation with TBI team. Finally I would like to thank Tristan Rigaut for his help when creating the optimization model.

## Business Problem

The manufacture of Transformers requires costly material, among which ferromagnetic metal sheets that make up its core. These sheets are winded into coils of different grade, indicating the quality and the supplier of the material. As a transformer manufacture, TBI plant has a specific process where coils of ferromagnetic material are cut into coils of different width.

## 

### **Inputs**
A list $(L_{i})_{i\in[1;n]}$ containing all coils width (in mm) of the mother coils in stock.\
A list $(w_{i})_{i\in[1;m]}$ containing all coils width (in mm) requested by the customer.\
A list $(b_{i})_{i\in[1;m]}$ containing the demand associated with each requested width.

### **Variables**
$\forall\; j\in [1;m],\; \forall\; i\in [1;n],\;$ $x_{i,j}$, an integer variable: number of coil of width i cut from mother coil j.\
$\forall\; i\in [1;n],\;$ $y_{j}$, a boolean variable: indicator variables, $y_{j} = 1$ if and only if standard coil j is used.\
$\forall\; i\in [1;n],\;$ $s_{j}$, an integer variable: Slack variables used to generate reusable offcuts.\
$\forall\; i\in [1;n],\;$ $t_{j}$, a boolean variable: Boolean variables to constraint the range of our slack variable.

### **Problem Statement**
We adapt here the "Naive" model usually used for modelling the cutting stock problem, see _H. Paul Williams_ [1]:

$$ Minimize\; f(y_{1},...,y_{n}) = \sum_{i=1}^{n}{y_{i}} \\$$

$
Subject\;to:\\
(1)\; \forall\; j\in [1;m],\; \sum_{i=1}^{n}{x_{i,j}} = b_{i} \\
(2)\; \forall\; j\in [1;m],\; \sum_{i=1}^{n}{w_{i}*x_{i,j} + 10*s_{j}} = L_{j}*y_{j}\\
$

### **Model Explanation**
The objective function $f$ represents the total number of coils used, which should be minimized.\
Constraint $(1)$ impose that demand must be met.\
Constraint $(2)$ impose that the cutting pattern must use the entirety of used coil (if ${s_j}=0$), or generate an offcut of standard width (if $s_{j} \neq 0$). 
We have used in this last constraint the fact that requested widths, and therefore offcuts' widths, must all be multiple of 10.

### **Adding Constraints**
This naive model has the default to have symmetrical solutions. We therefore add the constraint to reduce symmetry:
$$ (3)\; \forall\;j\in [1;m],\; y_{j-1}\geq y_{j}$$
**This constraint will give priority to the first elements in stock. This rule might be change in the future to suit better industrial needs.**\
We then try to add a constraint specifying the range of possible values for the slack variables to generate standard cutting patterns :
$$(4)\; \forall j, \; (8.0 \le s_{j} \le 600.0)\;
OR\;
 (s_{j}=0)$$
This is a specific constraint on integer variable, that look hard to implement on the first hand. It could be reformulated into a non-linear constraint:
$$\forall\;j,\; s_{j}*(s_{j}-8.0) \geq 0 $$
How to deal with this constraint?\
We could impose $s_{j}$ as a sum of boolean variable, $s_{j} = \sum_{i=1}^{B}{i*{\delta}_{i}}$ where ${\delta}_{i}=1$ if and only if $s_{j}=i$, develop the product and set boolean constraints. But it would lead to an explosion of the number of variables, problem that can be tackle if we reduce the range of acceptable slack variables...\
To deal smartly with this issue, we introduce new binary variables, $(t_{j})_{j \in [1;n]}$, and set the following constraints:
$$\forall j, \; s_{j}\geq 8.0*t_{j}$$
$$\forall j, \; s_{j}\le 600.0*t_{j}$$
We therefore have, if $t_{j}=0$, $s_{j}=0$, and if $t_{j}=1$, $s_{j} \in [8,600]$ while introducing 'only' $n$ new binary variable. **Coupled with constraint $\bold{(2)}$, every cutting pattern will either use the entirety of a coil to meet the demand, or generate an offcut of width multiple of $ \bold{10}$, and of width between $\bold{80 mm}$ and $\bold{6000 mm}$.**

## Create an executable
- install pyinstaller using pip
- type in your command promt at the location of main.py:
pyinstaller --noconfirm --onefile --console --icon "C:/Users/sever/Downloads/Custom-Icon-Design-Office-Calculator.ico" --name "SlitPlanGenerator" --add-data "C:/Users/sever/OneDrive/Bureau/Cutting-Stock-For-TBI/master/data;data/" --hidden-import "mip" --additional-hooks-dir "C:/Users/sever/OneDrive/Bureau/Cutting-Stock-For-TBI/master"  "C:/Users/sever/OneDrive/Bureau/Cutting-Stock-For-TBI/master/main.py" --clean --windowed





## **References**

[1]: H. Paul Williams, "Model Building in Mathematical Programming, 5th Edition", March 2013, ISBN: 978-1-118-44333-0.

