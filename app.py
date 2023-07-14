from shiny import ui, App, reactive
from shiny.ui import h4
from shinywidgets import output_widget, render_widget, register_widget
from modules.cluster import cluster_ui, cluster_server
# from modules.gsea import gsea_ui, gsea_server
# from modules.tsge import tsge_ui, tsge_server
# from modules.bins import bins_ui, bins_server
# from modules.scge import scge_ui, scge_server


app_ui = ui.page_navbar(
    ui.nav("Clustermap",
           cluster_ui("cluster")
           
    ),
    # ui.nav("GSEA",
    #        gsea_ui("gsea")
           
    # ),
    # ui.nav("TSGE",
    #        tsge_ui("tsge")
           
    # ),
    # ui.nav("Bins",
    #        bins_ui("bins")
           
    # ),
    # ui.nav("SCGE",
    #        scge_ui("scge")
           
    # ),
    title = "openGene",
    window_title="openGene",
    selected="SCGE",
    footer=ui.div(
        h4("openGene: Developed by Aditya Kondepudi of the Mitra Lab"),
    )
)

def server (input, output, session):
    cluster_server("cluster")
    # gsea_server("gsea")
    # tsge_server("tsge")
    # bins_server("bins")
    # scge_server("scge")

app = App(app_ui, server, debug=False)