from shiny import ui, module, reactive, render
from shinywidgets import output_widget, render_widget
import plotly.express as px
import pandas as pd
import seaborn as sns

from data import crispr_df, extract_clustered_table

global ordered

@module.ui
def crispr_ui():
    return ui.tags.div(
        ui.tags.style(
            """
            .app-col {
                border: 1px solid black;
                border-radius: 5px;
                background-color: #eee;
                padding: 8px;
                margin-top: 5px;
                margin-bottom: 5px;
            }
            """
        ),
        ui.row(
            ui.column(
                3,
                ui.div(
                    {"class": "app-col"},
                        ui.input_selectize(
                            "Gene",
                            label="Choose gene",
                            choices= crispr_df.index.tolist() + ["All"],
                            multiple=True,
                        ),
                ),
                ui.div(
                    {"class": "app-col"},
                        ui.input_selectize(
                            "cellline",
                            label="Choose cell lines",
                            choices= crispr_df.columns.tolist() + ["All"],
                            multiple=True,
                        ),
                ),

            ),
        ),
        ui.row(
            ui.column(
                12,
                ui.div(
                    {"class": "app-col"},
                        ui.input_checkbox_group(
                            "x", "Cluster", {"g": "Genes", "t": "Cell Lines"}, inline=True,
                        ),
                        ui.input_action_button("button", "Generate Heatmap"),
                ),
            )
        ),
        ui.row(
            ui.column(
                12,
                ui.div(
                    {"class": "app-col"},
                        output_widget("plot_widget"),
                ),
            ),
        ),
        ui.row(
            ui.column(
                12,
                ui.div(
                    {"class": "app-col"},
                        ui.input_selectize(
                            "firstgene",
                            label="First gene:",
                            choices= crispr_df.index.tolist(),
                            multiple=True,
                        ),
                        ui.input_selectize(
                            "secondgene",
                            label="Last gene:",
                            choices= crispr_df.index.tolist(),
                            multiple=True,
                        ),
                        ui.input_action_button("list_button", "Get List"),
                        # ui.download_button("downloadData", "Download"),
                ),
            ),
        ),
    )


@module.server
def crispr_server(input, output, session):
    @output
    @render_widget
    @reactive.event(input.button, ignore_none=True)
    def plot_widget():
        print("Reached 1")
        genes = []
        if str(input.Gene()) == "('All',)":
            print("Reached All")
            crispr_df_filter = crispr_df
        else:
            print("Reached not all")
            crispr_df_filter = crispr_df.loc[crispr_df.index.isin(list(input.Gene()))]

        if str(input.cellline()) != "('All',)":
            crispr_df_filter = crispr_df_filter[list(input.cellline())]
        
        print("Reached 1")
        
        if (str(input.x()) == "('g', 't')"):
            print("Reached 2")
            clustermap = sns.clustermap(crispr_df_filter, cmap="YlGnBu")

        if (str(input.x()) == "('g',)"):
            print("Reached 2")
            clustermap = sns.clustermap(crispr_df_filter, cmap="YlGnBu", col_cluster=False)

        if (str(input.x()) == "('t',)"):
            print("Reached 3")
            clustermap = sns.clustermap(crispr_df_filter, cmap="YlGnBu", row_cluster=False)

        if (str(input.x()) == "()"):
            print("Reached 4")
            print(crispr_df_filter.shape)
            ordered = crispr_df_filter
            plot = px.imshow(crispr_df_filter, aspect='auto', color_continuous_scale='YlGnBu')
            return plot


        print("Reached 5")
        ordered = extract_clustered_table(clustermap, crispr_df_filter)

        print("Reached 6")
        fig = px.imshow(ordered, aspect='auto', color_continuous_scale='YlGnBu')

        print("Reached 7")
        return fig
        
    @output
    @render.text
    @reactive.event(input.list_button, ignore_none=True)
    def get_list():
        list = list(ordered.index)
        # get subset of list from first term to next term
        first_string = str(input.firstgene)
        second_string = str(input.secondgene)
        first_string = first_string[2:]
        first_string = first_string[:-3]
        second_string = second_string[2:]
        second_string = second_string[:-3]
        first = list.index(first_string)
        second = list.index(second_string)
        subset_list = list[first:second]
        list_df = pd.DataFrame(subset_list)
        list_df.to_csv('list.csv', index=False)
        return "Saved!" 

