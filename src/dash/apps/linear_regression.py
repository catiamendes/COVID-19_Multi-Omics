
import dash
import dash_table
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import datetime
import pandas as pd

from data import get_omics_data, get_biomolecule_names, get_combined_data, get_p_values, get_volcano_data
from plot import correlation_scatter

# importing app through index page
from app import app
from apps import differential_expression

print()
print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print("Loading data for linear regression...")
print()

# load metabolomics data matrix
print("Loading metabolomics data...")
#metabolomics_df, metabolomics_quant_range = get_omics_data(dataset='metabolomics', with_metadata=True)
metabolomics_df, metabolomics_quant_range = differential_expression.metabolomics_df, differential_expression.metabolomics_quant_range
print("Metabolomics data shape: {}".format(metabolomics_df.shape))
print("Loading lipidomics data...")
#lipidomics_df, lipidomics_quant_range = get_omics_data(dataset='lipidomics', with_metadata=True)
lipidomics_df, lipidomics_quant_range = differential_expression.lipidomics_df, differential_expression.lipidomics_quant_range
print("Lipidomics data shape: {}".format(lipidomics_df.shape))
print("Loading proteomics data...")
#proteomics_df, proteomics_quant_range = get_omics_data(dataset='proteomics', with_metadata=True)
proteomics_df, proteomics_quant_range = differential_expression.proteomics_df, differential_expression.proteomics_quant_range
print("Proteomics data shape: {}".format(proteomics_df.shape))

# make biomolecule_name_dict
metabolomics_biomolecule_names_dict = get_biomolecule_names(dataset='metabolomics')
lipidomics_biomolecule_names_dict = get_biomolecule_names(dataset='lipidomics')
proteomics_biomolecule_names_dict = get_biomolecule_names(dataset='proteomics')
transcriptomics_biomolecule_names_dict = get_biomolecule_names(dataset='transcriptomics')

# define dataset dictionaries
dataset_dict = {
        "Proteins":"proteomics",
        "Lipids":"lipidomics",
        "Metabolites":"metabolomics",
        "Transcripts":"transcriptomics",
        "Combined":"combined"
    }

df_dict = {
    "proteomics":proteomics_df,
    "lipidomics":lipidomics_df,
    "metabolomics":metabolomics_df,
}

quant_value_range_dict = {
    "proteomics":proteomics_quant_range,
    "lipidomics":lipidomics_quant_range,
    "metabolomics":metabolomics_quant_range,
}

global_names_dict = {
    "proteomics":proteomics_biomolecule_names_dict,
    "lipidomics":lipidomics_biomolecule_names_dict,
    "metabolomics":metabolomics_biomolecule_names_dict,
    "combined":{**proteomics_biomolecule_names_dict,
                **lipidomics_biomolecule_names_dict,
                **metabolomics_biomolecule_names_dict,
                **transcriptomics_biomolecule_names_dict}
}

# get combined omics df and quant value range
print("Creating combined omics df...")
# get combined data with transcriptomics
df_dict, quant_value_range_dict = get_combined_data(df_dict,
    quant_value_range_dict, with_transcripts=True)

# start with proteomics data
sorted_biomolecule_names_dict = {k: v for k, v in sorted(global_names_dict['combined'].items(), key=lambda item: item[1])}
#available_biomolecules = proteomics_biomolecule_names_dict.values()
#available_biomolecules = proteomics_df.columns[:proteomics_quant_range].sort_values().tolist()
default_biomolecule = list(sorted_biomolecule_names_dict.keys())[0]

plotly_config = {"toImageButtonOptions":{'format':'svg',
                'filename': 'dash_plot'},
                "displaylogo": False}

# # NOTE: Need to add transcriptomics data here
dataset = 'combined'
combined_omics_df = df_dict[dataset]
quant_value_range = quant_value_range_dict[dataset]

available_datasets = ['Combined']
# start at COVID status
clinical_metadata_options = combined_omics_df.columns[quant_value_range+4:].sort_values().tolist()
clinical_metadata_options.remove("DM")
clinical_metadata_options.append('COVID')
biomolecule_options = [{'label': value, 'value': key} for key, value in sorted_biomolecule_names_dict.items() if key in combined_omics_df.columns.to_list()]

control_panel = dbc.Card(
    [
        dbc.CardHeader("CONTROL PANEL",
                            style={"background-color":"#5bc0de",
                                        "font-weight":"bold",
                                        "font-size":"large"}),
        dbc.CardBody(
            [html.P("Select Clinical Measurement", className="card-title", style={"font-weight":"bold"}),
            dcc.Dropdown(
                id='clinical_measurement-lr',
                options=[{'label': i, 'value': i} for i in clinical_metadata_options],
                # only passing in quant value columns
                value=clinical_metadata_options[0]),
            html.Hr(),
            html.P("Select Groups", className="card-title", style={"font-weight":"bold"}),
            dcc.Checklist(
                id='group-checklist-lr',
                options=[
                    {'label': ' COVID ICU', 'value': 'COVID_ICU'},
                    {'label': ' COVID NONICU', 'value': 'COVID_NONICU'},
                    {'label': ' NONCOVID ICU', 'value': 'NONCOVID_ICU'},
                    {'label': ' NONCOVID NONICU', 'value': 'NONCOVID_NONICU'}
                ],
                value=['COVID_ICU', 'COVID_NONICU', 'NONCOVID_ICU', 'NONCOVID_NONICU'],
                labelStyle={'display': 'inline-block'}
            ),
            html.Hr(),
            html.P("Select Biomolecule", className="card-title", style={"font-weight":"bold"}),

            # NOTE: This is dcc object not dbc
            dcc.Dropdown(
                id='biomolecule_id-lr',
                # label maps to biomolecule name, value to biomolecule_id
                options=biomolecule_options,
                # only passing in quant value columns
                value=default_biomolecule,
                className="dropdown-item p-0"),

                ])
    ])

first_card = dbc.Card(
    [
        dbc.CardHeader("BIOMOLECULE SCATTER PLOT",
                            style={"background-color":"#5bc0de",
                                        "font-weight":"bold",
                                        "font-size":"large"}),
        dbc.CardBody(dcc.Graph(id='scatter-lr',
        config=plotly_config))
    ])


COONLAB_LOGO="https://coonlabs.com/wp-content/uploads/2016/07/coon-logo-white.png"
navbar = dbc.NavbarSimple(

        [

        dbc.NavItem(dbc.NavLink(html.Span(
                "About",
                id="tooltip-about",
                style={"cursor": "pointer"},
            ))),

        dbc.Tooltip(
        "Link to Preprint",
        target="tooltip-about"
        ),

        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Meet the Team", header=True),
                dbc.DropdownMenuItem("UW–Madison", href="https://coonlabs.com/"),
                dbc.DropdownMenuItem("Albany Medical Center", href="https://www.amc.edu/Profiles/jaitova.cfm"),
                dbc.DropdownMenuItem("Morgridge Institute for Research", href="https://morgridge.org/research/regenerative-biology/bioinformatics/")
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),

        dbc.NavItem(html.Div(html.A(html.Img(src=COONLAB_LOGO,
                style={"height":"40px"}),
                href="https://coonlabs.com/"),
                className="d-none d-lg-block ml-4"))

        ],
    brand="NIH NATIONAL CENTER FOR QUANTITATIVE BIOLOGY OF COMPLEX SYSTEMS",
    brand_style={"font-size":"xx-large", "font-style":"italic"},
    brand_href="https://www.ncqbcs.com/",
    color="#5bc0de",
    dark=True,
    className="mt-1",
    fluid=True
)

#app.layout = dbc.Container([
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

        dbc.NavItem(dbc.NavLink(html.Span("PCA"),
            disabled=False,
            href="pca",
            style={"color":"grey"})),



        dbc.NavItem(dbc.NavLink("Linear Regression", active=True, href="linear_regression", style={"background-color":"grey"})),

        dbc.NavItem(dbc.NavLink(

            html.Span(
                    "Differential Expression",
                    id="tooltip-lr",
                    style={"cursor": "pointer", "color":"grey"},
                ),disabled=False, href="differential_expression")),

        dbc.NavItem(dbc.NavLink(
            html.Span(
                    "Pathway Analysis",
                    id="tooltip-pa",
                    style={"cursor":"pointer", "color":"grey"},
                ),disabled=False, href="#")),


        # tooltip for pathway analysis
        dbc.Tooltip(
        "Coming Soon!",
        target="tooltip-pa"
        ),

        html.Hr(),
        control_panel
    ],
    vertical="md",
    pills=True
        ), md=2, className="mb-3"),

        dbc.Col(first_card, md=7),
        ],

        className="mb-3"),


], fluid=True, style={"height": "100vh"})


@app.callback(
    Output('scatter-lr', 'figure'),
    [Input('biomolecule_id-lr', 'value'),
    Input('group-checklist-lr','value'),
    Input('clinical_measurement-lr', 'value')])
def update_biomolecule_scatter(biomolecule_id, groups, clinical_measurement):

    biomolecule_name = global_names_dict["combined"][biomolecule_id]
    fig = correlation_scatter(combined_omics_df, biomolecule_id, groups,
        biomolecule_name, clinical_measurement)

    return fig
