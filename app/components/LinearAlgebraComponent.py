from typing import *

import dash_core_components as dcc
import dash_html_components as html

from components.BaseComponent import BaseComponent
from assets.data.covid_data import COVID_DATA_DF


linear_algebra_intro_text = """One topic that I come up against almost daily is Linear Algebra. When I took my first 
linear algebra course I thought it was easy. Very soon after that I realized there was much more to linear algebra than 
what I knew. To this day I find this topic fascinating but so so challenging. In this section I will explore some 
concepts that I find most interesting, most challenging or both!"""

norm_observation_text = """After making these plots and playing around with the ranges of values of p I noticed some "
"interesting and unexpected observations.\n"
"The first thing that really stuck out was that as we increase p, in other words as p approaches"
" +inf the value of the Lp norm seems to converge to a finite number. What is even more interesting,"
"as I found out, is that if you play around with the values of the components of the input vector,"
"you will see that as p -> +inf the norm converges to the scalar equal to the largest component of "
"the input vector. As I found out this even has a name, the Chebyshev norm."""

isocontours_text = """That looks so cool! I've seen such plots many times, but never quite understood how they are made."
"It actually wasn't that hard to recreate and I actually think I now better understand what the different"
"p norms 'look like' outside of their mathematical definition. """

regularization_intro_text = """While all of this is very cool to look at on its own, we don't have to limit ourselves
to just some nice plots and shapes. Norms play an important role in machine learning when it comes to obtaining models
that generalize better and don't overfit the training data. This is called regularization and it is done by adding 
a penalty term equal to the some p-norm of the weights of our parameter vector. Usually p here is 1 (Lasso regression) 
or 2 (Ridge regression). Let's explore how those two (and others) impact performance of a machine learning model. For
this exercise I will go with the COVID cases data (because that's the hot topic now) provided in the book."""

regularization_post_covid_scatter_text = """Looking at the scatter plots, we see that cases are not going up in a linear
fashion, so for this case (again, following the book) we will use polynomial feature regression to fit the apparent 
non-linear relationship. I just want to note that this is really done for the purpose of an exercise rather than to 
predict anything.\n The plot below will let you experiment with different values of the regularization parameters 
(alpha) and look at the difference between Lasso(L1) and Ridge(L2) regression."""


class LinearAlgebraComponent(BaseComponent):
    title: str = "Linear Algebra"

    @staticmethod
    def p_value_range_slider(
            id: str,
            min: int = -5,
            max: int = 20,
            value: List[int] = None,
            step: int = 1,
            marks: Dict[int, str] = None,
            tooltip: Dict = None,
            *args,
            **kwargs
    ) -> dcc.RangeSlider:
        if marks is None:
            marks = {val: f"{val}" for val in range(min, max + 1, step)}

        if value is None:
            value = [2, 10]

        if tooltip is None:
            tooltip = {
                "placement": "right"
            }

        slider = dcc.RangeSlider(
            id=id,
            min=min,
            max=max,
            value=value,
            marks=marks,
            step=step,
            tooltip=tooltip,
            *args,
            **kwargs
        )
        return slider

    def vector_input_form_group(
            self,
            id: str,
            type: str = "text",
            input_width: int = 4,
            row: bool = True,
            placeholder: str = "2D Vector goes here. Try (2,2)",
            *args,
            **kwargs
    ):
        return self.input_form_group(
            id=id,
            type=type,
            input_width=input_width,
            row=row,
            placeholder=placeholder,
            *args,
            **kwargs
        )

    def isoline_plot_p_form_group(
            self,
            id: str,
            type: str = "number",
            input_width: int = 4,
            row: bool = True,
            placeholder: str = "Enter a value of P",
            *args,
            **kwargs
    ):
        return self.input_form_group(
            id=id,
            type=type,
            input_width=input_width,
            row=row,
            placeholder=placeholder,
            *args,
            **kwargs
        )

    def covid_data_region_select(
            self,
            id: str,
            classes_to_attach: List[str] = None,
            *args,
            **kwargs
    ):
        regions = COVID_DATA_DF.columns.to_list()
        regions = [r for r in regions if r.lower() not in ['days', 'date']]
        options = [{"label": r, "value": r} for r in regions]
        return self.dropdown_select(
            id, options=options, value="Ile-de-France", classes_to_attach=classes_to_attach, *args, **kwargs
        )

    def get_regression_type_selector(
            self,
            id: str,
            classes_to_attach: List[str] = None,
            *args,
            **kwargs
    ):
        options = [{"label": r, "value": r.lower()} for r in ['Lasso regression', "Ridge regression"]]
        return self.dropdown_select(
            id,
            value="lasso",
            options=options,
            classes_to_attach=classes_to_attach,
            *args,
            **kwargs
        )

    def get_polynomial_degree_input(
            self,
            id: str,
            type: str = "number",
            input_width: int = 4,
            row: bool = True,
            placeholder: str = "Degree of Polynomial Features",
            *args,
            **kwargs
    ):
        return self.input_form_group(
            id=id,
            type=type,
            input_width=input_width,
            row=row,
            step=1,
            placeholder=placeholder,
            *args,
            **kwargs
        )

    def layout(
            self,
            make_dash_component: bool = False,
            *args,
            **kwargs
    ):
        layout = [
            *self.text_block(text=linear_algebra_intro_text),
            *self.sub_section_header("Lp Norms"),
            *self.vector_input_form_group("p-vs-norm-vector-input"),
            self.p_value_range_slider("p-vs-norm-range-slider"),
            *self.figure("p-vs-norm-plot"),
            *self.text_block(norm_observation_text),
            *self.sub_section_header("Norm Iso-contours"),
            *self.isoline_plot_p_form_group('p-isoline-input'),
            *self.figure("p-isolines-plot"),
            *self.text_block(isocontours_text),
            *self.sub_section_header("Application in Regularization"),
            *self.text_block(regularization_intro_text),
            *self.covid_data_region_select("covid-data-region-selector"),
            *self.figure("covid-data-scatter"),
            *self.text_block(regularization_post_covid_scatter_text),
            *self.get_regression_type_selector("kind-value-selector"),
            *self.get_polynomial_degree_input("poly-degree-input"),
            *self.figure("covid-poly-fit-plot")
        ]

        if make_dash_component:
            layout = html.Div(layout, className="container")

        return layout