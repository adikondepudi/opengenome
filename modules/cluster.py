from shiny import ui, module
from shinywidgets import output_widget, render_widget
import dash_bio as dashbio
import plotly.express as px

from data import df, mt_list, er_list, ga_list

@module.ui
def cluster_ui():
    return ui.tags.div(
        ui.layout_sidebar(
            ui.panel_sidebar(
                ui.input_checkbox_group(
                    "x", "Cluster", {"g": "Genes", "t": "Tissues"}
                ),
                ui.input_selectize(
                    "Gene",
                    label="Choose gene(s):",
                    choices= df.index.tolist() + ["All"] + ["Mitochondria"] + ["Golgi Apparatus"] + ["Endoplasmic Reticulum"],
                    multiple=True,
                ),
                ui.input_selectize(
                    "Tissue",
                    label="Choose cell(s):",
                    choices=df.columns.tolist() + ["All"],
                    multiple=True,
                ),
            ),
            ui.panel_main(
                output_widget("heatmap_widget")
            )
        )
    )

@module.server
def cluster_server(input, output, session):
    @output
    @render_widget
    def heatmap_widget():  
        if str(input.Gene()) == "('All',)":
            df_filter = df
        elif str(input.Gene()) == "('Endoplasmic Reticulum',)":
            df_filter = df[df.index.isin(er_list)]
        elif str(input.Gene()) == "('Mitochondria',)":
            df_filter = df[df.index.isin(mt_list)]
        elif str(input.Gene()) == "('Golgi Apparatus',)":
            df_filter = df[df.index.isin(ga_list)]
        else:
            df_filter = df.loc[df.index.isin(list(input.Gene()))]
        
        if str(input.Tissue()) != "('All',)":
            # df_filter = df.loc[df.columns.isin(list(input.Tissue()))]
            df_filter = df_filter[list(input.Tissue())]
        
        heatmap_plot = px.imshow(
            df_filter,
            aspect='auto',
            color_continuous_scale='YlGnBu',
            height=800, width=800
        )

        '''
        If organelle is selected 
        '''
    
        if (str(input.x()) == "('g', 't')"):
            heatmap_plot = dashbio.Clustergram(
                data=df_filter,
                column_labels=df_filter.columns.tolist(),
                row_labels=df_filter.index.tolist(),
                color_threshold={"row": 250, "col": 700},
                height=800, width=800,
                color_map="YlGnBu"
            )
            heatmap_plot.update_layout(
                xaxis={'automargin': True},
                yaxis={'automargin': True}
            )
        if (str(input.x()) == "('g',)"):
            heatmap_plot = dashbio.Clustergram(
                data=df_filter,
                column_labels=df_filter.columns.tolist(),
                row_labels=df_filter.index.tolist(),
                color_threshold={"row": 250, "col": 700},
                height=800, width=800,
                color_map="YlGnBu",
                cluster="row"
            )
            heatmap_plot.update_layout(
                xaxis={'automargin': True},
                yaxis={'automargin': True}
            )
        if (str(input.x()) == "('t',)"):
            heatmap_plot = dashbio.Clustergram(
                data=df_filter,
                column_labels=df_filter.columns.tolist(),
                row_labels=df_filter.index.tolist(),
                color_threshold={"row": 250, "col": 700},
                height=800, width=800,
                color_map="YlGnBu",
                cluster="column"
            )
            heatmap_plot.update_layout(
                xaxis={'automargin': True},
                yaxis={'automargin': True}
            )
        if (str(input.x()) == "()"):
            heatmap_plot = px.imshow(
                df_filter,
                aspect='auto',
                color_continuous_scale='YlGnBu',
                height=800, width=800
            )
        return heatmap_plot
