from shiny import ui, App, reactive
from shiny.ui import h4
from shinywidgets import output_widget, render_widget, register_widget
# from modules.cluster import cluster_ui, cluster_server
# from modules.gsea import gsea_ui, gsea_server
# from modules.tsge import tsge_ui, tsge_server
# from modules.scge import scge_ui, scge_server
from modules.crispr import crispr_ui, crispr_server



app_ui = ui.page_navbar(
#     ui.nav("Clustermap",
#            cluster_ui("cluster")
           
#     ),
#     ui.nav("GSEA",
#            gsea_ui("gsea")
           
#     ),
#     ui.nav("TSGE",
#            tsge_ui("tsge")
           
#     ),
#     ui.nav("SCGE",
#            scge_ui("scge")
           
#     ),
    ui.nav("CRISPR",
           crispr_ui("crispr")
           
    ),
    title = "openGene",
    window_title="openGene",
    selected="Clustermap",
    footer=ui.div(
        h4("openGene: Developed by Aditya Kondepudi of the Mitra Lab"),
    )
)

def server (input, output, session):
#     cluster_server("cluster")
#     gsea_server("gsea")
#     tsge_server("tsge")
#     scge_server("scge")
    crispr_server("crispr")

app = App(app_ui, server, debug=False)