
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import datetime

from data import get_omics_data, get_biomolecule_names, get_combined_data
from plot import biomolecule_bar, boxplot, pca_scores_plot, pca_loadings_plot
from nav import navbar

external_stylesheets=[dbc.themes.BOOTSTRAP]

"""app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets)
app.title = 'COVID-19 Multi-Omics'"""

from app import app

print()
print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print("Loading data for pca...")
print()

# load metabolomics data matrix
print("Loading metabolomics data...")
from app import metabolomics_df, metabolomics_quant_range
print("Metabolomics data shape: {}".format(metabolomics_df.shape))
print("Loading lipidomics data...")
from app import lipidomics_df, lipidomics_quant_range
print("Lipidomics data shape: {}".format(lipidomics_df.shape))
print("Loading proteomics data...")
from app import proteomics_df, proteomics_quant_range
print("Proteomics data shape: {}".format(proteomics_df.shape))
print("Loading transcriptomics data...")
from app import transcriptomics_df, transcriptomics_quant_range
print("Transcriptomics data shape: {}".format(transcriptomics_df.shape))

available_datasets = ['Proteins', 'Lipids', 'Metabolites', 'Transcripts', 'Combined Biomolecules']

# define dataset dictionaries
from app import dataset_dict, df_dict, quant_value_range_dict, global_names_dict
from app import metabolomics_biomolecule_names_dict
from app import lipidomics_biomolecule_names_dict
from app import proteomics_biomolecule_names_dict
from app import transcriptomics_biomolecule_names_dict

# get combined omics df and quant value range
print("Creating combined omics df...")
df_dict, quant_value_range_dict = get_combined_data(df_dict, quant_value_range_dict)

# start with proteomics data
sorted_biomolecule_names_dict = {k: v for k, v in sorted(proteomics_biomolecule_names_dict.items(), key=lambda item: item[1])}
#available_biomolecules = proteomics_biomolecule_names_dict.values()
#available_biomolecules = proteomics_df.columns[:proteomics_quant_range].sort_values().tolist()
default_biomolecule = list(sorted_biomolecule_names_dict.keys())[0]

plotly_config = {"toImageButtonOptions":{'format':'svg',
                'filename': 'dash_plot'},
                "displaylogo": False}

first_card = dbc.Card(
    [
        dbc.CardHeader("PCA SCORES PLOT",
                            style={"background-color":"#5bc0de",
                                    "font-weight":"bold",
                                    "font-size":"large"}),
        dbc.CardBody(dcc.Graph(id='pca-scores-figure',
            config=plotly_config))

        ])

second_card = dbc.Card(
    [
        dbc.CardHeader("PCA LOADINGS PLOT",
                            style={"background-color":"#5bc0de",
                                    "font-weight":"bold",
                                    "font-size":"large"}),
        dbc.CardBody(dcc.Graph(id='pca-loadings-figure',
        config=plotly_config))
    ])

third_card = dbc.Card(
    [
        dbc.CardHeader("BIOMOLECULE BARPLOT",
                            style={"background-color":"#5bc0de",
                                        "font-weight":"bold",
                                        "font-size":"large"}),
        dbc.CardBody(dcc.Graph(id='biomolecule-barplot',
        config=plotly_config))
    ])

fourth_card = dbc.Card(
    [
        dbc.CardHeader("BIOMOLECULE BOXPLOT",
                            style={"background-color":"#5bc0de",
                                    "font-weight":"bold",
                                    "font-size":"large"}),
        dbc.CardBody(dcc.Graph(id='biomolecule-boxplot',
        config=plotly_config))
    ])

###

control_panel = dbc.Card(
    [
        dbc.CardHeader("CONTROL PANEL",
                            style={"background-color":"#5bc0de",
                                        "font-weight":"bold",
                                        "font-size":"large"}),
        dbc.CardBody(
            [html.P("Select Dataset", className="card-title", style={"font-weight":"bold"}),
            dcc.Dropdown(
                id='dataset_id',
                options=[{'label': i, 'value': i} for i in available_datasets],
                # only passing in quant value columns
                value=available_datasets[0]),
            html.Hr(),
            html.P("Select Biomolecule", className="card-title", style={"font-weight":"bold"}),

            # NOTE: This is dcc object not dbc
            dcc.Dropdown(
                id='biomolecule_id',
                # label maps to biomolecule name, value to biomolecule_id
                options=[{'label': value, 'value': key} for key, value in sorted_biomolecule_names_dict.items()],
                # only passing in quant value columns
                value=default_biomolecule,
                className="dropdown-item p-0"),

                ])
    ])

#app.layout =  dbc.Container([
layout = dbc.Container([

    navbar,

    html.Hr(),

    dbc.Row(dbc.Col(html.H1("COVID-19 Multi-Omics Data Dashboard"), width={"size": 6, "offset": 3})),

    html.Hr(),

    dbc.Row(
        [dbc.Col(
        dbc.Nav(
    [
        html.H3("TYPE OF ANALYSIS", style={"font-weight":"bold", "color":"black"}),

        dbc.NavItem(dbc.NavLink("PCA", active=True, href="pca", style={"background-color":"grey"})),

        dbc.NavItem(dbc.NavLink(

            html.Span(
                    "Linear Regression",
                    id="tooltip-lr",
                    style={"cursor": "pointer", "color":"grey"},
                ),disabled=False, href="linear_regression")),

        dbc.NavItem(dbc.NavLink(
            html.Span(
                    "Differential Expression",
                    id="tooltip-de",
                    style={"cursor": "pointer", "color":"grey"},
                ),disabled=False, href="differential_expression")),

                dbc.NavItem(dbc.NavLink(
                    html.Span(
                            "Clustergrammer",
                            id="tooltip-cg",
                            style={"cursor":"pointer", "color":"grey"},
                        ),disabled=False, href="clustergrammer")),

        html.Hr(),
        control_panel
    ],
    vertical="md",
    pills=True
        ), md=2, className="mb-3"),

        #dbc.Col(control_panel, md=6)
        dbc.Col(first_card, md=4),
        dbc.Col(second_card, md=6)
        ],

        className="mb-3"),

    dbc.Row([dbc.Col(third_card, md=7, align="center"), dbc.Col(fourth_card, md=5, align="center")], className="mb-3")

], fluid=True)


@app.callback(
    dash.dependencies.Output('biomolecule_id', 'options'),
    [Input('dataset_id', 'value')])
def update_biomolecule_options(dataset_id):

    dataset = dataset_dict[dataset_id]
    biomolecule_names_dict = global_names_dict[dataset]

    df = df_dict[dataset]
    quant_value_range = quant_value_range_dict[dataset]

    # get list of columns for dataset
    available_biomolecules = df.columns[:quant_value_range].sort_values().tolist()

    sorted_biomolecule_names_dict = {k: v for k, v in sorted(biomolecule_names_dict.items(), key=lambda item: item[1])}

    options=[{'label': value, 'value': key} for key, value in sorted_biomolecule_names_dict.items() if key in available_biomolecules]
    #print(options)
    return options

@app.callback(
    Output('biomolecule_id', 'value'),
    [Input('dataset_id', 'value')])
def update_default_biomolecule(dataset_id):

    dataset = dataset_dict[dataset_id]
    biomolecule_names_dict = global_names_dict[dataset]

    sorted_biomolecule_names_dict = {k: v for k, v in sorted(biomolecule_names_dict.items(), key=lambda item: item[1])}
    default_biomolecule=list(sorted_biomolecule_names_dict.keys())[0]

    return default_biomolecule

@app.callback(
    Output('pca-scores-figure', 'figure'),
    [Input('dataset_id', 'value')])
def update_pca_scores_plot(dataset_id):

    dataset = dataset_dict[dataset_id]
    df = df_dict[dataset]
    quant_value_range = quant_value_range_dict[dataset]

    fig = pca_scores_plot(df, quant_value_range)

    return fig

@app.callback(
    Output('pca-loadings-figure', 'figure'),
    [Input('dataset_id', 'value'),
    Input('biomolecule_id', 'value')])
def update_pca_loadings_plot(dataset_id, biomolecule_id):

    dataset = dataset_dict[dataset_id]
    df = df_dict[dataset]
    biomolecule_names_dict = global_names_dict[dataset]
    quant_value_range = quant_value_range_dict[dataset]

    # build ome type list for coloring
    if not dataset == 'combined':
        ome_type_list = [dataset] * quant_value_range

    else:
        ome_type_list = ['proteomics'] * quant_value_range_dict['proteomics']
        ome_type_list.extend(['lipidomics'] * quant_value_range_dict['lipidomics'])
        ome_type_list.extend(['metabolomics'] * quant_value_range_dict['metabolomics'])
        ome_type_list.extend(['transcriptomics'] * quant_value_range_dict['transcriptomics'])

    # get biomolecule index
    biomolecule_index = df.columns.tolist().index(biomolecule_id)
    ome_type_list[biomolecule_index] = 'selected_biomolecule'

    fig = pca_loadings_plot(df, quant_value_range, dataset_id, biomolecule_names_dict, ome_type_list)

    return fig

@app.callback(
    Output('biomolecule-barplot', 'figure'),
    [Input('biomolecule_id', 'value'),
    Input('dataset_id', 'value')])
def update_biomolecule_barplot(biomolecule_id, dataset_id):

    dataset = dataset_dict[dataset_id]
    df = df_dict[dataset]

    biomolecule_names_dict = global_names_dict[dataset]
    biomolecule_name = biomolecule_names_dict[biomolecule_id]

    fig = biomolecule_bar(df, biomolecule_id, biomolecule_names_dict)

    return fig

@app.callback(
    Output('biomolecule-boxplot', 'figure'),
    [Input('biomolecule_id', 'value'),
    Input('dataset_id', 'value')])
def update_biomolecule_boxplot(biomolecule_id, dataset_id):

    dataset = dataset_dict[dataset_id]
    df = df_dict[dataset]

    biomolecule_names_dict = global_names_dict[dataset]
    biomolecule_name = biomolecule_names_dict[biomolecule_id]

    fig = boxplot(df, biomolecule_id, biomolecule_names_dict)

    return fig

print("Starting server...")

if __name__ == '__main__':
    app.run_server(
        debug=True,
        host='0.0.0.0',
        #port='8080'
        )
