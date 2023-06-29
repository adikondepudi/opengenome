from shiny import ui, module, reactive, render
from shiny.types import FileInfo
from shinywidgets import output_widget, register_widget, render_widget
import pandas as pd
import numpy as np
import gseapy as gp
from gseapy import dotplot
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from gseapy.plot import gseaplot


from ipydatagrid import DataGrid



from data import nameconversion

df = pd.DataFrame()
global pre_res

@module.ui
def gsea_ui():
    return ui.tags.div(
        ui.layout_sidebar(
            ui.panel_sidebar(
                ui.input_file("file1", "Choose CSV File", accept=[".csv"], multiple=False),
                ui.input_action_button("csv", "Read CSV"),
                ui.output_text("progress"),
                ui.input_action_button("button", "Generate choices"),
                ui.output_ui("choices_ui"),
                ui.input_action_button("computing", "Compute!"),
                ui.output_text("computed"),
                ui.input_action_button("generate", "List plot options"),
                ui.output_ui("plot_options_ui"),
            ),
            ui.panel_main(
                ui.panel_conditional(
                    "input.termplotgraph",
                    ui.output_plot("termplot"),
                ),
                ui.panel_conditional(
                    "input.dotplotgraph",
                    ui.output_plot("dotplotplot"),
                ),
                ui.panel_conditional(
                    "input.rankingstable",
                    ui.output_ui("top_table_ui"),
                    # ui.output_table("toptable"),
                    output_widget("toptable"),
                    ui.output_ui("bottom_table_ui"),
                    ui.output_table("bottomtable"),
                ),
            )
        )
    )

@module.server
def gsea_server(input, output, session):
    @output
    @render.ui
    @reactive.event(input.button, ignore_none=True)
    def choices_ui():
        global df
        if df.empty:
            return "Please upload a csv file"
        return ui.tags.div(
            ui.input_selectize(
                "name",
                label="Choose gene identifier column:",
                choices=df.columns.tolist(),
                multiple=False,
            ),
            ui.input_selectize(
                "logfc",
                label="Choose logFC column:",
                choices=df.columns.tolist(),
                multiple=False,
            ),
            ui.input_selectize(
                "pval",
                label="Choose Pval column:",
                choices=df.columns.tolist(),
                multiple=False,
            ),
            ui.input_selectize(
                "geneset",
                label="Choose gene set:",
                choices = gp.get_library_name(),
                multiple=False,
            ),
        )

    @output
    @render.ui
    @reactive.event(input.generate)
    def plot_options_ui():
        global pre_res
        return ui.tags.div(
            ui.navset_tab_card(
                ui.nav(
                    "Term Plot",
                    ui.input_checkbox("termplotgraph", "Show Term Plot", False),
                    ui.input_selectize(
                        "term_to_plot1",
                        label="Choose term:",
                        choices=pre_res.res2d["Term"].to_list(),
                        multiple=False,
                    ),
                    ui.input_action_button("termplotbuttton", "Generate plot"),
                ),
                ui.nav(
                    "Dot Plot",
                    ui.input_checkbox("dotplotgraph", "Show Dot Plot", False),
                    ui.input_selectize(
                        "term_to_plot2",
                        label="Choose term:",
                        choices=pre_res.res2d["Term"].to_list(),
                        multiple=False,
                    ),
                    ui.input_action_button("dotplotbutton", "Generate plot"),
                ),
                ui.nav(
                    "Rankings Table",
                    ui.input_checkbox("rankingstable", "Show Rankings Table", False),
                    ui.input_numeric("x", "Top and Bottom X Rankings", value=10),
                    ui.input_action_button("rankingstablebutton", "Generate table"),
                ),
            )
        )
    @output
    @render.text
    @reactive.event(input.csv)
    async def progress():
        with ui.Progress(min=1, max=15) as p:
            p.set(message="Calculation in progress", detail="This may take a while...")
            global df
            if input.file1() is None:
                return "Please upload a csv file"
            f: list[FileInfo] = input.file1()
            df = pd.read_csv(f[0]["datapath"])
        return "Uploaded!"
    
    @output
    @render.text
    @reactive.event(input.computing)
    async def computed():
        with ui.Progress(min=1, max=15) as p:
            global pre_res
            global df
            p.set(message="Calculation in progress", detail="This may take a while...")

            # df_changed = df[[input.name(), input.logfc(), input.pval()]]
            df_changed = df.rename(columns={input.name(): "Gene", input.logfc(): "logFC", input.pval(): "adjPval"}, inplace=True)
            df_changed["Rank"] = -np.log10(df_changed["adjPval"])*df_changed["logFC"]
            df_changed.sort_values(by="Rank", ascending=False).reset_index(drop=True)
            ranking = df_changed[['Gene', 'Rank']]

            gtf_df = nameconversion
            gtf_list = list(gtf_df.itertuples(index = False, name=None))
            gtf = dict(gtf_list)

            ranking.loc[:, 'Gene'] = ranking['Gene'].map(lambda x: gtf.get(x, x), na_action="ignore")
            ranking = ranking.dropna(axis=0, how='any').reset_index(drop=True)

            pre_res = gp.prerank(rnk = ranking, gene_sets = input.geneset(), seed = 6, min_size = 15, max_size = 500)
        return "Computed!"
    
    @output
    @render.plot
    @reactive.event(input.termplotbuttton)
    def termplot():
        # gseaplot(pre_res.ranking, term = input.term_to_plot(), **pre_res.results[input.term_to_plot()], ofname = "gsea_plot.png")
        # img = {"src": "gsea_plot.png", "width": "500px"}
        # return img
        fig = pre_res.plot(terms=input.term_to_plot1())
        return fig

    @output
    @render.plot
    @reactive.event(input.dotplotbutton)
    def dotplotplot():
        # gseaplot(pre_res.ranking, term = input.term_to_plot(), **pre_res.results[input.term_to_plot()], ofname = "gsea_plot.png")
        # img = {"src": "gsea_plot.png", "width": "500px"}
        # return img
        fig = pre_res.plot(terms=input.term_to_plot2())
        return fig
    
    @output
    @render_widget
    @reactive.event(input.rankingstablebutton)
    def toptable():
        global pre_res
        # df_table = pd.DataFrame()
        df_table = pre_res.res2d.sort_values("NES", ascending=False).head(input.x())
        # return df_table
        grid = DataGrid(df_table)
        return grid

    @output
    @render.table
    @reactive.event(input.rankingstablebutton)
    def bottomtable():
        global pre_res
        # df_table = pd.DataFrame()
        df_table = pre_res.res2d.sort_values("NES", ascending=False).tail(input.x())
        return df_table
    
    @output
    @render.ui
    @reactive.event(input.rankingstablebutton)
    def top_table_ui():
        return ui.tags.div(
            ui.tags.h1("Top " + str(input.x()) + " Rankings"),
        )
    
    @output
    @render.ui
    @reactive.event(input.rankingstablebutton)
    def bottom_table_ui():
        return ui.tags.div(
            ui.tags.h1("Bottom " + str(input.x()) + " Rankings"),
        )
