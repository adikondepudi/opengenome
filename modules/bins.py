# import matplotlib.pyplot as plt
# import numpy as np
# from shiny import *


# @module.ui
# def bins_ui():
#     return ui.tags.div(
#         ui.panel_title("Simulate a normal distribution"),
#         ui.layout_sidebar(
#             ui.panel_sidebar(
#                 ui.input_slider("n", "Sample size", 0, 1000, 250),
#                 ui.input_numeric("mean", "Mean", 0),
#                 ui.input_numeric("std_dev", "Standard deviation", 1),
#                 ui.input_slider("n_bins", "Number of bins", 0, 100, 20),
#             ),

#             ui.panel_main(
#                 ui.output_plot("plot")
#             )
#         )
#     )

# @module.server
# def bins_server(input, output, session):
#     @output
#     @render.plot
#     def plot():
#         x = np.random.normal(input.mean(), input.std_dev(), input.n())
#         fig, ax = plt.subplots()
#         ax.hist(x, input.n_bins(), density=True)
#         return fig

# """
# from shiny import *
# import numpy as np
# import matplotlib.pyplot as plt

# app_ui = ui.page_fluid(
#     ui.input_action_button("minus", "-1"),
#     " ",
#     ui.input_action_button("plus", "+1"),
#     ui.br(),
#     ui.output_plot("plot"),
# )


# def server(input: Inputs, output: Outputs, session: Session):
#     val = reactive.Value(0)

#     @reactive.Effect
#     @reactive.event(input.minus)
#     def _():
#         newVal = val.get() - 1
#         val.set(newVal)

#     @reactive.Effect
#     @reactive.event(input.plus)
#     def _():
#         newVal = val.get() + 1
#         val.set(newVal)

#     @output
#     @render.plot
#     def plot():
#         x = np.random.normal(int(val.get()), 1, 1000)  # Generating 1000 random numbers
#         fig, ax = plt.subplots()
#         n_bins = 10  # Number of bins for the histogram
#         ax.hist(x, bins=n_bins, density=True)  # Using 'bins' instead of 'input.n_bins()'
#         return fig

# app = App(app_ui, server)

# https://shiny.posit.co/py/api/reactive.Value.html
# https://shiny.rstudio.com/py/docs/ui-dynamic.html
# """