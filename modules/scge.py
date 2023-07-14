# from shiny import ui, module, reactive
# from shinywidgets import output_widget, render_widget
# import dash_bio as dashbio
# import plotly.express as px
# import matplotlib.pyplot as plt

# from data import df, mt_list, er_list, ga_list

# @module.ui
# def scge_ui():
#     return ui.tags.div(
#         ui.tags.style(
#             """
#             .app-col {
#                 border: 1px solid black;
#                 border-radius: 5px;
#                 background-color: #eee;
#                 padding: 8px;
#                 margin-top: 5px;
#                 margin-bottom: 5px;
#             }
#             """
#         ),
#         ui.row(
#             ui.column(
#                 6,
#                 ui.div(
#                     {"class": "app-col"},
#                         ui.input_checkbox_group(
#                             "colors",
#                             "Choose color(s):",
#                             {
#                                 "mt": ui.span("Mitochondria"),
#                                 "er": ui.span("Endoplasmic Reticulum"),
#                                 "ga": ui.span("Golgi Apparatus"),
#                                 "chosen_genes": ui.span("Choose genes"),
#                                 "upload_genes": ui.span("Uploaded genes"),
#                             },
#                             inline=True,
#                         ),
#                 ),
#             ),
#             ui.column(
#                 3,
#                 ui.div(
#                     {"class": "app-col"},
#                         ui.input_selectize(
#                             "Gene",
#                             label="Choose gene",
#                             choices= df.index.tolist(),
#                             multiple=True,
#                         ),
#                 ),
#             ),
#             ui.column(
#                 3,
#                 ui.div(
#                     {"class": "app-col"},
#                         ui.input_file("file1", "Choose CSV File", accept=[".csv"], multiple=False),
#                         ui.input_action_button("csv", "Read CSV"),
#                 ),
#             )
#         ),
#         ui.row(
#             ui.column(
#                 12,
#                 ui.div(
#                     {"class": "app-col"},
#                         ui.input_radio_buttons(
#                             "rb",
#                             "Choose one:",
#                             {
#                                 "html": "Brain",
#                                 "text": "PNS/DRG",
#                                 "text": "All cells (HPA)",
#                             },
#                             inline=True,
#                         ),
#                 ),
#             )
#         ),
#         ui.row(
#             ui.column(
#                 12,
#                 ui.div(
#                     {"class": "app-col"},
#                         ui.input_checkbox_group(
#                             "x", "Cluster", {"g": "Genes", "t": "Tissues"}, inline=True,
#                         ),
#                         ui.input_action_button("button", "Generate Heatmap"),
#                 ),
#             )
#         ),
#         ui.row(
#             ui.column(
#                 12,
#                 ui.div(
#                     {"class": "app-col"},
#                         output_widget("plot_widget"),
#                 ),
#             ),
#         ),
#         ui.row(
#             ui.column(
#                 12,
#                 ui.div(
#                     {"class": "app-col"},
#                         ui.input_selectize(
#                             "Gene",
#                             label="First gene:",
#                             choices= df.index.tolist(),
#                             multiple=True,
#                         ),
#                         ui.input_selectize(
#                             "Gene",
#                             label="Last gene:",
#                             choices= df.index.tolist(),
#                             multiple=True,
#                         ),
#                 ),
#             ),
#         ),
#     )


# @module.server
# def scge_server(input, output, session):
#     @output
#     @render_widget
#     @reactive.event(input.button, ignore_none=True)
#     def plot_widget():
#         genes = []
#         if "mt" in list(input.colors()):
#             genes.extend(mt_list)
#         if "er" in list(input.colors()):
#             genes.extend(er_list)
#         if "ga" in list(input.colors()):
#             genes.extend(ga_list)
#         if "chosen_genes" in list(input.colors()):
#             genes.extend(list(input.Gene()))
#         if "upload_genes" in list(input.colors()):
#             # genes.extend(input.file1)
#             # TODO complete csv file to gene list conversion
#             pass
#         df_filter = df.loc[df.index.isin(genes)]
#         heatmap_plot = copx.imshow(
#             df_filter,
#             aspect='auto',
#             color_continuous_scale='YlGnBu',
#             height=800, width=1200
#         )
#         return heatmap_plot
        
