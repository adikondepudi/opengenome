# from shiny import ui, module, reactive, render
# from shinywidgets import output_widget, register_widget, render_widget
# import plotly.graph_objects as go
# import plotly.express as px

# from data import df

# @module.ui
# def tsge_ui():
#     return ui.tags.div(
#         ui.tags.div(
#             ui.input_selectize(
#                 "Gene",
#                 label="Choose gene",
#                 choices= df.index.tolist() + ["All"],
#                 multiple=False,
#             ),
#             # id="div-navbar-tabs",
#             # class_="main-sidebar card-style",
#         ),
#         ui.tags.div(
#             output_widget("bar_widget"),
#             # class_="main-main card-style"
#         ),
#         # class_="main-layout",
#     )


# @module.server
# def tsge_server(input, output, session):
#     @output
#     @render_widget
#     def bar_widget():
#         row_data = df.loc[str(input.Gene())]
#         # fig = go.Figure(data=[
#         #     go.Bar(x=row_data.index,
#         #            y=row_data.values,
#         #     )
#         # ])
#         # fig.update_layout(
#         #     title="Bar Graph from Pivot Table",
#         #     xaxis_title="Categories",
#         #     yaxis_title="Values",
#         #     xaxis={'categoryorder':'total descending'},
#         # )
#         fig = px.bar(row_data,
#                      x=row_data.values,
#                      y=row_data.index,
#                      orientation='h',
#                      height=1000,
#         )
#         fig.update_layout(yaxis={'categoryorder':'total ascending'})

#         return fig

