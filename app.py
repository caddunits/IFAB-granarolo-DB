from shiny import App, render, ui, reactive
from shinywidgets import output_widget, render_widget
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from query import *
from rdkit import Chem
from rdkit.Chem.Draw import rdMolDraw2D
from pathlib import Path


custom_css = ui.tags.style("""
/* ---- TOP NAVBAR (page_navbar) ---- */

/* default (inactive) navbar links */
.navbar .nav-link {
    color: var(--bs-gray-600) !important; /* muted */
}

/* active navbar link */
.navbar .nav-link.active {
    color: var(--bs-primary) !important;
    font-weight: 600;
}

/* ---- INNER TABS (navset_tab) ---- */

/* inactive tab links */
.nav-tabs .nav-link {
    color: var(--bs-gray-600) !important; 
}

/* active tab link */
.nav-tabs .nav-link.active {
    color: var(--bs-primary) !important;
    font-weight: 600;
    border-bottom: 3px solid var(--bs-primary); /* optional: underline */
}

/* hover effect */
.nav-tabs .nav-link:hover {
    color: var(--bs-primary) !important;
}
""")

home = ui.page_fillable(
    ui.layout_columns(
        ui.card(
            ui.card_header("Get Started"),
            ui.markdown(
                """
                ### What is this app?

                This web application provides access to a curated database of
                **polymer properties**, **computational workflows**, and **predictive models** developed within 
                the project **PISA**-Harnessing H**P**C: Granarolo's Bio-Driven Revolut**I**on for **S**ustainable P**A**ckaging

                ### What can you do?
                - Explore material properties across polymers

                ### How to use the app
                Navigate using the top menu, each section focuses on a specific
                type of analysis
                """
            ),
        ),
        ui.card(
            ui.card_header("Data Overview"),
            ui.markdown(
                """
                ### Database content
                - Polymers
                - Properties (mechanical, thermal, chemical,...)
                - Computational workflows
                - Molecular simulations

                ### Data source
                - Multiscale simulations
                """
            ),
        ),
        col_widths=(6, 6)
    ),
    ui.card(
        ui.markdown("""
                      **List of partners**: CNR-NANO-Modena, CNR-ICCOM-Pisa, UniTN (Università di Trento), UniTS (Università di Trieste), UniPI (Università di Pisa), ENEA, IFAB and Granarolo Group SpA
                    
                     **Involved Spokes**: Spoke 7 - Materials & Molecular Sciences
                     """
        )

    )
)

plots = ui.page_fillable(
              ui.navset_card_tab(

        ui.nav_panel(
            "Barplot",
            ui.layout_sidebar(
                ui.sidebar(
                    ui.input_selectize("select1", "Select a Polymer : ",
                                       df_polymers['Name'].tolist()),
                    ui.input_selectize("select2", "Available properties : ",
                                       choices=[]),
                ),
                output_widget("barplot"),
                ui.output_ui('workflow_details', placeholder=True),
                ui.output_data_frame('workflow_table')
            )
        ),

        ui.nav_panel(
            "Violinplot",
            ui.layout_sidebar(
                ui.sidebar(
                    ui.input_selectize("select3", "Select a Property : ",
                                       df_properties['Name'].tolist()),
                    ui.input_selectize("select4", "Available Polymers : ",
                                       choices=[], multiple=True),
                ),
                output_widget("violinplot"),
            )
        )
            )
        )


#models = ui.page_fillable(
#            ui.panel_title(ui.h4('Toxicity Models for Small Molecules of Interest')),
#            ui.br(),
#            ui.output_data_frame('models_df'),
#            ui.br(),
#            ui.layout_column_wrap(
#                ui.input_selectize('toxicology', 'Molecules associated with polymer :', choices=df_polymers['Name'].tolist()),
#                ui.card(
#                    ui.layout_column_wrap(
#                        ui.input_text('molecule', 'Enter a valid IUPAC name to display the chemical structure'),
#                        ui.output_ui('mol_image')
#                    ),
#                    style="height: 200px; overflow-y: auto;"
#                )
#            )
#        )


www_dir = Path(__file__).parent / 'www'

#animations = ui.page_fillable(
#                ui.navset_pill_list(
#                    ui.nav_menu(
#                       'Filling Dynamics',
#                       ui.nav_panel('Case1_CoffeeBrick_Case0_Part_GasVelSlice', ui.tags.video(ui.tags.source(src='Case1_CoffeeBrick_Case0_Part_GasVelSlice.mp4', type='video/mp4'), controls=True, autoplay=False, loop=False, style='width:800px')),
#                       ui.nav_panel('Case2_CGf=2_rho=827_u=1', ui.tags.video(ui.tags.source(src='Case2_CGf=2_rho=827_u=1.mp4', type='video/mp4'), controls=True, autoplay=False, loop=False, style='width:800px')),
#                       ui.nav_panel('Case3_CoffeeBrick_2View_PartCG2_Fwall_JKR', ui.tags.video(ui.tags.source(src='Case3_CoffeeBrick_2View_PartCG2_Fwall_JKR.mp4', type='video/mp4'), controls=True, autoplay=False, loop=False, style='width:800px')),
#                       ui.nav_panel('Case4_CoffeeBrick_2View_PartCG2_Fwall_shk_v2', ui.tags.video(ui.tags.source(src='Case4_CoffeeBrick_2View_PartCG2_Fwall_shk_v2.mp4', type='video/mp4'), controls=True, autoplay=False, loop=False, style='width:800px'))
#                    )
#                )
#             )
            
         
app_ui = ui.page_fillable(
    custom_css,
        ui.page_navbar(
            ui.nav_spacer(),
            ui.nav_panel('Home', home),
            ui.nav_panel('Plots', plots),
            #ui.nav_panel('Models', models),
            #ui.nav_panel('Animations', animations),
            title=ui.h1('GRANAROLO DATABASE APP', class_='bg-bold text-primary')
        )
    )

  
def server(input, output, session):

    selected_workflow = reactive.value()


    @reactive.effect
    def text1():
        polymer = input.select1()
        sql = f"""SELECT pr.Name AS Name
                  FROM Properties pr
                  JOIN Polymer_Property pp ON pp.Property_ID=pr.ID
                  JOIN Polymers p ON p.ID=pp.Polymer_ID
                  WHERE p.Name='{polymer}'
               """
        df = query_db(sql)
        properties = df['Name'].tolist()

        ui.update_select('select2', choices=properties, selected=None)


    @output
    @render_widget
    def barplot():
        prop = input.select2()

        sql = f"""SELECT pr.Value AS Value,
                         w.Workflow AS Workflow
                  FROM Predictions pr
                  JOIN Properties p ON p.ID=pr.Property_ID
                  JOIN Workflows w ON w.Prediction_ID=pr.ID
                  WHERE p.Name='{prop}';"""
        
        df = query_db(sql).reset_index()

        fig = px.bar(df, x=df.index, y='Value', color_discrete_sequence=['#0d6efd'])
        fig.update_layout(xaxis=dict(tickvals=[], showticklabels=False),
                          xaxis_title = prop,
                          height=700, 
                          margin=dict(l=10, r=10, t=10, b=10),
                          autosize=True)
       
        fig.update_traces(
        hovertemplate="<b>Workflow:</b> %{customdata[0]}<br>"
                      "<b>Value:</b> %{y}<extra></extra>",
        customdata=df[["Workflow"]]
        )

        w = go.FigureWidget(fig)

        def on_bar_click(trace, points, state):
            if points.point_inds:
                i= points.point_inds[0]
                wf = df.iloc[i]['Workflow']
                selected_workflow.set(wf)

        if w.data:
            w.data[0].on_click(on_bar_click)

        return w
    

    @output
    @render.ui
    def workflow_details():
        wf = selected_workflow.get()
        if wf is None:
            return ui.div('Click a bar to see wotkflow details')
        return ui.h5(f'Workflow:  {wf}')
    

    @output
    @render.data_frame
    def workflow_table():
        wf = selected_workflow.get()

        if wf is None:
           return None
        
        sql =  f"""SELECT we.StepNumber AS Step,
                          cc.Class AS Class,
                          cm.Model AS Model,
                          c.System AS System,
                          n1.Node AS Input, 
                          n2.Node AS Output,
                          s.Name AS Software 
                    FROM Edges e 
                    JOIN Nodes n1 ON e.Input_ID=n1.ID 
                    JOIN Nodes n2 ON n2.ID=e.Output_ID 
                    JOIN Workflow_Edges we ON we.Edge_ID=e.ID 
                    JOIN Workflows w ON w.ID=we.Workflow_ID
                    JOIN Calculations c ON e.ID=c.Edge_ID
                    JOIN CalculationClasses cc ON c.Class_ID=cc.ID
                    JOIN CalculationModels cm ON c.Model_ID=cm.ID
                    JOIN Software s ON c.Software_ID=s.ID
                    WHERE w.Workflow='{wf}' 
                    ORDER BY we.StepNumber;"""
        
        df = query_db(sql)

        df = (df.groupby(['Class', 'Model', 'System', 'Input', 'Output'], as_index=False)
              .agg(Step=('Step', 'min'),Software=('Software', lambda x: ' + '.join(dict.fromkeys(x))))
              .sort_values('Step')
              )

        return render.DataTable(df[['Step', 'Input', 'Output', 'System', 'Software', 'Class', 'Model']], summary=False, selection_mode='row')
    

    @reactive.effect
    def text2():
        property = input.select3()
        sql = f"""SELECT p.Name AS Name
                  FROM Polymers p
                  JOIN Polymer_Property pp ON pp.Polymer_ID=p.ID
                  JOIN Properties pr ON pr.ID=pp.Property_ID
                  WHERE pr.Name='{property}'
               """
        df = query_db(sql)
        properties = df['Name'].tolist()

        ui.update_select('select4', choices=properties, selected=None)

    
    @output
    @render_widget
    def violinplot():
        
        prop = input.select3()
        polymers = input.select4()

        if not polymers:
            return None
        
        polymer_list = ", ".join(f"'{p}'" for p in polymers)
        
        sql = f"""SELECT pd.Value AS Value,
                         pd.Unit AS Unit,
                         p.Name AS Polymer
                  FROM Predictions pd
                  JOIN Properties pr ON pr.ID=pd.Property_ID
                  JOIN Polymer_Property pp ON pp.Property_ID=pr.ID
                  JOIN Polymers p ON p.ID=pp.Polymer_ID
                  WHERE p.Name IN ({polymer_list}) AND pr.Name='{prop}';"""
        
        df = query_db(sql)

        unit = df['Unit'].iloc[0]

        fig = go.Figure()

        colors = [
                   "#0d6efd",  # blue
                   "#ff7f0e",  # orange
                   "#2ca02c",  # green
                   "#d62728",  # red
                   "#9467bd",  # purple
                 ]

        for i, p in enumerate(polymers):
                 fig.add_trace(
                               go.Violin(
                                         y=df.loc[df["Polymer"] == p, "Value"],
                                         name=p,
                                         box_visible=True,
                                         meanline_visible=True,
                                         points="all",
                                         line_color=colors[i % len(colors)],  
                                         fillcolor=colors[i % len(colors)],    
                                         opacity=0.6
                                        )
                              )

        
        fig.update_layout(violinmode='group',
                          yaxis_title=f"Value ({unit})",
                          title=f'{prop} distribution across polymers',
                          template="plotly_white",
                          font=dict(size=14),
                          margin=dict(l=60, r=30, t=80, b=60),
                          showlegend=True
                         )
        
        fig.update_traces(hovertemplate=
                           "<b>Polymer:</b> %{fullData.name}<br>" +
                           "<b>Value:</b> %{y:.3f}<br>" +
                           "<extra></extra>"
                         )

        w = go.FigureWidget(fig)
        
        return w 
    

    @output
    @render.data_frame
    def models_df():
        pl = input.toxicology()
        sql = f"""SELECT sm.IUPACName AS IUPACName,
                         m.Model AS Model,
                         pm.Classification AS Classification, 
                         pm.Value AS Value 
                  FROM Polymers p 
                  JOIN Mol_to_Polymer mp ON mp.Polymer_ID=p.ID 
                  JOIN SmallMolecules sm ON sm.ID=mp.SmallMolecule_ID 
                  JOIN Mol_predicted_by_Model pm ON pm.SmallMolecule_ID=sm.ID 
                  JOIN Models m ON m.ID=pm.Model_ID 
                  WHERE p.Name='{pl}';"""
        df = query_db(sql)

        if df.empty:
           empty_df = pd.DataFrame({'Message': [f'No Available Data for {pl}']}) 
           return render.DataGrid(empty_df)

        def pack_values(row):
            if pd.notnull(row['Classification']) and pd.notnull(row['Value']):
               return f"{row['Classification']}({int(row['Value'])})"
            elif pd.notnull(row['Classification']):
               return f"{row['Classification']}"
            else:
               return ''

        df['Variable'] = df.apply(pack_values, axis=1)
        df = df.pivot(index='IUPACName', columns='Model', values='Variable').reset_index()

        #styles = [{'class' : 'text-center',}, {'cols': [0], 'style': {'background-color': '#0d95fd', 'color': '#e6f0fe'}},]

        return render.DataTable(df, filters=True, summary=True, styles = [{'class' : 'text-center',}])
    

    @output
    @render.ui
    def mol_image():

        name = input.molecule()

        sql = f"""SELECT sm.SMILES AS SMILES, p.Name AS Name
                  FROM SmallMolecules sm
                  JOIN Mol_to_Polymer mp ON mp.SmallMolecule_ID=sm.ID
                  JOIN Polymers p ON p.ID=mp.Polymer_ID
                  WHERE sm.IUPACName='{name}';"""
        
        df = query_db(sql)

        if df.empty:
            return ui.div('No data available')
        
        polymers = str.join(',', df['Name'].tolist())
        
        smiles = str(df.iloc[0,0]).strip()

        if not smiles or smiles.lower() == 'nan':
            return ui.div('Molecule not found')

        mol = Chem.MolFromSmiles(smiles)
        if not mol:
            return ui.div('Molecule not convertible')
        
        drawer = rdMolDraw2D.MolDraw2DSVG(200,200)
        drawer.DrawMolecule(mol)
        drawer.FinishDrawing()

        svg = drawer.GetDrawingText()
        
        return ui.div(
                      ui.HTML(svg),
                      ui.p(f'Linked to polymers: {polymers}', style='margin:0; font-size:16px;'),
                      style='text-align:center;'
                     )


app=App(app_ui, server, static_assets=www_dir) #shiny run --launch-browser script/shiny_app/app.py

