from flask import Flask, render_template
import plotly.express as px
from flask_frozen import Freezer
import pandas as pd
import plotly.figure_factory as ff
import numpy as np
import plotly.graph_objs as go
from plotly.graph_objs import Sankey


app = Flask(__name__)
freezer = Freezer(app)

# DATASET

dataset = pd.read_excel("data/dataset.xlsx")

# EDAT
    
age_distribution = dataset['EDAT'].value_counts().reset_index()
age_distribution.columns = ['Age Group', 'Count']

# GÈNERE

gender_distribution = dataset['SEXE'].value_counts().reset_index()
gender_distribution.columns = ['Gender', 'Count']

# REGIÓ

region_distribution = dataset['AmbitTerritorial'].value_counts().reset_index()
region_distribution.columns = ['Region', 'Count']

# Llengua
i1_labels = {
    1: "Català",
    2: "Castellà",
    0: "Cap llengua especificada"
}
i1_column_summary = dataset['I1'].value_counts()
i1_summary = i1_column_summary.rename(index=i1_labels).reset_index()
i1_summary.columns = ["Llengua", "Comptes"]

# Tipus de llar
i4_column_summary = dataset['I4'].value_counts()
i4_labels = {
    1: "Llar unipersonal",
    2: "Dues persones o més",
    3: "Parella sense fills",
    4: "Parella amb fills",
    5: "Mare o pare amb fills",
    6: "Llars amb dos nuclis o més",
    99: "NS/NC"
}
i4_summary = i4_column_summary.rename(index=i4_labels).reset_index()
i4_summary.columns = ["Tipus de llar", "Comptes"]

# Diaris
d1_summary = dataset['D1'].value_counts()
d1_labels = {
    1: "Sí",
    0: "No",
    99: "NS/NC"
}
d1_summary_df = d1_summary.rename(index=d1_labels).reset_index()
d1_summary_df.columns = ["Va llegir diaris ahir?", "Comptes"]
filtered_data = dataset[dataset['D1'] == 1]

d2_columns_updated = ['D2#1', 'D2#2', 'D2#4', 'D2#99']
d3_columns_updated = ['D3#1', 'D3#2', 'D3#3', 'D3#99']
d2_summary_updated = filtered_data[d2_columns_updated].sum()
d3_summary_updated = filtered_data[d3_columns_updated].sum()

d2_labels_updated = {
    'D2#1': "Físic (paper)",
    'D2#2': "Digital pàgina web",
    'D2#4': "Digital aplicacions mòbils",
    'D2#99': "NS/NC"
}
d2_summary_df = d2_summary_updated.rename(index=d2_labels_updated).reset_index()
d2_summary_df.columns = ["Format de lectura", "Comptes"]

d3_labels_updated = {
    'D3#1': "En català",
    'D3#2': "En castellà",
    'D3#3': "Altres idiomes",
    'D3#99': "NS/NC"
}
d3_summary_df = d3_summary_updated.rename(index=d3_labels_updated).reset_index()
d3_summary_df.columns = ["Llengua de lectura", "Comptes"]

# Edat vs diaris
age_group_reading = dataset.groupby(['EDAT', 'D1']).size().unstack(fill_value=0)
age_group_reading.columns = ["No", "Sí"]
# lectors= D1=1 per cada grup
age_group_reading['Percent Sí'] = (age_group_reading["Sí"] / 
                                    (age_group_reading["No"] + age_group_reading["Sí"])) * 100

age_group_reading['Total'] = age_group_reading['No'] + age_group_reading['Sí']
age_group_reading['Proportion No'] = age_group_reading['No'] / age_group_reading['Total']
age_group_reading['Proportion Sí'] = age_group_reading['Sí'] / age_group_reading['Total']

radar_data = age_group_reading[["No", "Sí"]].reset_index()
radar_data_long = radar_data.melt(id_vars="EDAT", value_vars=["No", "Sí"],
                                var_name="Resposta", value_name="Comptes")

# RÀDIO
r1_summary = dataset['R1'].value_counts()
r1_labels = {
    1: "Sí",
    0: "No",
    99: "NS/NC"
}
r1_summary_df = r1_summary.rename(index=r1_labels).reset_index()
r1_summary_df.columns = ["Va escoltar la ràdio ahir?", "Comptes"]

#  R1 == 1
filtered_radio_data = dataset[dataset['R1'] == 1]

r2_columns = ['R2#1', 'R2#2', 'R2#3', 'R2#4', 'R2#5', 'R2#99']
r3_columns = ['R3#1', 'R3#2', 'R3#3', 'R3#99']

r2_summary = filtered_radio_data[r2_columns].sum()
r3_summary = filtered_radio_data[r3_columns].sum()

r2_labels = {
    'R2#1': "Ràdio convencional",
    'R2#2': "Per Internet",
    'R2#3': "Pel mòbil o la tablet",
    'R2#4': "Podcasts",
    'R2#5': "Altres",
    'R2#99': "NS/NC"
}
r3_labels = {
    'R3#1': "En català",
    'R3#2': "En castellà",
    'R3#3': "Altres idiomes",
    'R3#99': "NS/NC"
}

r2_summary_df = r2_summary.rename(index=r2_labels).reset_index()
r2_summary_df.columns = ["Format d'escolta", "Comptes"]

r3_summary_df = r3_summary.rename(index=r3_labels).reset_index()
r3_summary_df.columns = ["Llengua d'escolta", "Comptes"]

# CINEMA

cn1_summary = dataset['CN1'].value_counts()
cn1_labels = {
    1: "Sí",
    0: "No",
    99: "NS/NC"
}
cn1_summary_df = cn1_summary.rename(index=cn1_labels).reset_index()
cn1_summary_df.columns = ["Ha anat al cinema?", "Comptes"]

#  CN1 == 1
filtered_cinema_data = dataset[dataset['CN1'] == 1]

cn2_columns = ['CN2#1', 'CN2#2', 'CN2#3', 'CN2#4', 'CN2#5', 'CN2#6', 'CN2#99']
cn1b_column = 'CN1B'

cn2_summary = filtered_cinema_data[cn2_columns].sum()
cn1b_summary = filtered_cinema_data[cn1b_column].value_counts()

cn2_labels = {
    'CN2#1': "Català",
    'CN2#2': "Castellà",
    'CN2#3': "Anglès",
    'CN2#4': "Francès",
    'CN2#5': "Alemany",
    'CN2#6': "Altres",
    'CN2#99': "NS/NC"
}
cn1b_labels = {
    1: "Original sense subtitular",
    2: "Doblada",
    3: "Original subtitulada",
    99: "NS/NC"
}

cn2_summary_df = cn2_summary.rename(index=cn2_labels).reset_index()
cn2_summary_df.columns = ["Llengua de la pel·lícula", "Comptes"]

cn1b_summary_df = cn1b_summary.rename(index=cn1b_labels).reset_index()
cn1b_summary_df.columns = ["Versió de la pel·lícula", "Comptes"]

# CS1 vs CN1
cs1_vs_cn1 = dataset.groupby(['CS1', 'CN1']).size().unstack(fill_value=0)

# OR2 (Lloc de naixement) vs CN1 (Anar al cinema)
or2_vs_cn1 = dataset.groupby(['OR2', 'CN1']).size().unstack(fill_value=0)

cs1_labels = {
    1: "Treballa",
    2: "Aturat",
    3: "Estudiant",
    4: "Jubilat/Incapacitat",
    5: "Treball no remunerat",
    99: "NS/NC"
}
or2_labels = {
    1: "Catalunya",
    2: "Resta de l'Estat",
    3: "Altres països",
    99: "NS/NC"
}
cn1_labels = {1: "Sí", 0: "No", 99: "NS/NC"}

cs1_vs_cn1.index = cs1_vs_cn1.index.map(cs1_labels)
cs1_vs_cn1.columns = cs1_vs_cn1.columns.map(cn1_labels)
or2_vs_cn1.index = or2_vs_cn1.index.map(or2_labels)
or2_vs_cn1.columns = or2_vs_cn1.columns.map(cn1_labels)

# Area
cs1_vs_cn1_long = cs1_vs_cn1.reset_index().melt(id_vars="CS1", var_name="Resposta", value_name="Comptes")
or2_vs_cn1_long = or2_vs_cn1.reset_index().melt(id_vars="OR2", var_name="Resposta", value_name="Comptes")


# Ingressos

i4_filter_3_to_6 = dataset[dataset['I4'].isin([3, 4, 5, 6])]
g2_summary = i4_filter_3_to_6['G2'].value_counts().sort_index()

i4_filter_1_to_2 = dataset[dataset['I4'].isin([1, 2])]
g2a_summary = i4_filter_1_to_2['G2A'].value_counts().sort_index()

g2_labels = {
    1: "Menys de 1.000 €",
    2: "1.001 - 1.500 €",
    3: "1.501 - 2.500 €",
    4: "2.501 - 3.500 €",
    5: "3.501 - 4.500 €",
    6: "4.501 - 6.000 €",
    7: "Més de 6.000 €",
    99: "NS/NC"
}
g2a_labels = {
    1: "Sense ingressos",
    2: "Menys de 1.000 €",
    3: "1.001 - 1.500 €",
    4: "1.501 - 2.500 €",
    5: "2.501 - 3.500 €",
    6: "Més de 3.500 €",
    99: "NS/NC"
}

g2_summary.index = g2_summary.index.map(g2_labels)
g2a_summary.index = g2a_summary.index.map(g2a_labels)

g2_bubble_data = g2_summary.reset_index()
g2_bubble_data.columns = ["Interval d'Ingressos", "Comptes"]
g2a_bubble_data = g2a_summary.reset_index()
g2a_bubble_data.columns = ["Interval d'Ingressos", "Comptes"]
g2_bubble_data["Categoria"] = "Llar amb nucli familiar (parella/fills)"
g2a_bubble_data["Categoria"] = "Llar amb sense nucli familiar (unipersonal/amics)"

bubble_data = pd.concat([g2_bubble_data, g2a_bubble_data])

# Índex de cultura
dataset['IndexCultural'] = (
    (dataset[['R1', 'D1', 'CN1', 'ES1', 'EX1']] == 1).sum(axis=1) >= 3
).astype(int)

# (EDAT) and IndexCultural
index_cultural_by_age = dataset.groupby('EDAT')['IndexCultural'].mean() * 100

index_cultural_df = index_cultural_by_age.reset_index()
index_cultural_df.columns = ["Grup d'Edat", "Percentatge"]

# index, edat, ambit i sexe:
cultural_index_territorial_sexe_edat = dataset.groupby(['AmbitTerritorial', 'SEXE', 'EDAT'])['IndexCultural'].mean() * 100

income_labels = {
    1: "Menys de 1.000 €",
    2: "De 1.001 a 1.500 €",
    3: "De 1.501 a 2.500 €",
    4: "De 2.501 a 3.500 €",
    5: "De 3.501 a 4.500 €",
    6: "De 4.501 a 6.000 €",
    7: "Més de 6.000 €",
    9: "NS/NC"
}
dataset['Income'] = dataset[['G2', 'G2A']].bfill(axis=1).iloc[:, 0]

cultural_index_income = dataset.groupby('Income')['IndexCultural'].mean() * 100
cultural_index_income_df = cultural_index_income.reset_index()
cultural_index_income_df.columns = ['Ingressos', 'Percentatge Index Cultural']
cultural_index_income_df['Ingressos'] = cultural_index_income_df['Ingressos'].map(income_labels)

cultural_index_territorial_sexe_edat_df = cultural_index_territorial_sexe_edat.reset_index()


@app.route('/')
def index():
    
    # Gràfic edat
    fig_age = px.bar(
        age_distribution,
        x='Age Group',
        y='Count',
        title="Distribució dels Participants per Edat",
        labels={'Age Group': 'Grup d\'Edat', 'Count': 'Nombre de Participants'},
        template='plotly_white',
        color='Age Group',
        color_discrete_sequence=px.colors.sequential.Oranges_r
    )
    plot_html_edat = fig_age.to_html(full_html=False)
    
    # Gràfic gènere
    fig_gender = px.pie(
        gender_distribution,
        names='Gender',
        values='Count',
        title="Distribució dels Participants per Sexe",
        labels={'Gender': 'Gènere', 'Count': 'Participants'},
        color='Gender',
        color_discrete_map={'H': '#ff7f0e', 'D': '#ffbb78'},  # Atronjats neutres
    )
    plot_html_gender = fig_gender.to_html(full_html=False)


    # Gràfic regió
    fig_region = px.bar(
        region_distribution,
        x='Region',
        y='Count',
        title="Distribució dels Participants per Regió",
        labels={'Region': 'Regió', 'Count': 'Participants'},
        template='plotly_white',
        color='Region',
        color_discrete_sequence=px.colors.sequential.Oranges_r
    )
    plot_html_regio = fig_region.to_html(full_html=False)
    
    # Llengua
    fig_llengua = px.bar(i1_summary, x="Llengua", y="Comptes", text="Comptes",
             title="Preferència de la Llengua per dur a terme l'Entrevista",
             labels={"Comptes": "Nombre de respostes", "Llengua": "Llengua"},
             template='plotly_white',
             color='Llengua',
             color_discrete_sequence=px.colors.sequential.Oranges_r)

    plot_html_llengua = fig_llengua.to_html(full_html=False)
    
    # Tipus de llar
    fig_tipus_llar = px.bar(i4_summary, x="Tipus de llar", y="Comptes", text="Comptes",
                    title="Distribució del Tipus de Llar dels participants",
                    labels={"Comptes": "Nombre de respostes", "Tipus de llar": "Tipus de llar"},
                    template='plotly_white',
                    color='Tipus de llar',
                    color_discrete_sequence=px.colors.sequential.Oranges_r)

    plot_html_tipus_llar = fig_tipus_llar.to_html(full_html=False)
    
    # Diaris
    fig_d1_pie = px.pie(d1_summary_df, values="Comptes", names="Va llegir diaris ahir?",
                    title="Va llegir o fullejar diaris ahir?",
                    labels={"Comptes": "Nombre de respostes"},
                    template='plotly_white',
                    color='Va llegir diaris ahir?',
                    color_discrete_sequence=px.colors.sequential.Oranges_r)
    
    plot_html_d1 = fig_d1_pie.to_html(full_html=False)
    
    
    # Plot per D2
    fig_d2 = px.bar(d2_summary_df, x="Format de lectura", y="Comptes", text="Comptes",
                    title="Formats de Lectura de Diaris",
                    labels={"Comptes": "Nombre de respostes", "Format de lectura": "Format"},
                    template='plotly_white',
                    color='Format de lectura',
                    color_discrete_sequence=px.colors.sequential.Oranges_r)
    
    plot_html_d2 = fig_d2.to_html(full_html=False)
    
    # Plot per D3
    fig_d3 = px.bar(d3_summary_df, x="Llengua de lectura", y="Comptes", text="Comptes",
                    title="Llengües de Lectura de Diaris",
                    labels={"Comptes": "Nombre de respostes", "Llengua de lectura": "Llengua"},
                    template='plotly_white',
                    color='Llengua de lectura',
                    color_discrete_sequence=px.colors.sequential.Oranges_r)

    plot_html_d3 = fig_d3.to_html(full_html=False)
    

    # Create Radar Plot
    fig_radar = px.line_polar(
        radar_data_long,
        r="Comptes",
        theta="EDAT",
        color="Resposta",
        line_close=True,
        title="Lectura de Diaris per Edat",
        color_discrete_map={"No": "red", "Sí": "yellow"}
    )
    
    plot_edat_vs_diars_radar = fig_radar.to_html(full_html=False)
    
    fig_r1_pie = px.pie(
        r1_summary_df,
        values="Comptes",
        names="Va escoltar la ràdio ahir?",
        title="Va escoltar la ràdio ahir?",
        color='Va escoltar la ràdio ahir?',
        color_discrete_sequence=px.colors.sequential.Oranges_r
    )
    fig_r1_pie.update_traces(textposition='inside', textinfo='percent+label')
    
    plot_edat_vs_radio_pie = fig_r1_pie.to_html(full_html=False)
    
    #  Polar Bar Chart per R2 (Formats d'escolta)
    fig_r2_polar = px.bar_polar(
        r2_summary_df,
        r="Comptes",
        theta="Format d'escolta",
        color="Format d'escolta",
        title="Distribució dels Formats d'Escolta de la Ràdio",
        color_discrete_sequence=px.colors.sequential.Oranges_r
    )
    plot_r2_polar = fig_r2_polar.to_html(full_html=False)

    #  Funnel Chart per R3 (Llengües d'escolta)
    fig_r3_funnel = px.funnel(
        r3_summary_df,
        x="Comptes",
        y="Llengua d'escolta",
        color="Llengua d'escolta",
        title="Distribució de les Llengües d'Escolta de la Ràdio",
        color_discrete_sequence=px.colors.sequential.Oranges_r
    )
    plot_r3_funnel = fig_r3_funnel.to_html(full_html=False)
    
    fig_parallel = px.parallel_categories(
        dataset,
        dimensions=["EDAT", "R1"],
        color="R1",
        color_continuous_scale=px.colors.sequential.Oranges_r,
        title="Relació entre Edat i l'Escolta de la Ràdio",
        labels={"EDAT": "Grup d'Edat", "R1": "Va escoltar la ràdio ahir?"}
    )

    plot_parallel_radio = fig_parallel.to_html(full_html=False)
    
    fig_cn2_treemap = px.treemap(
        cn2_summary_df,
        path=["Llengua de la pel·lícula"],
        values="Comptes",
        title="Llengües de l'Última Pel·lícula Vista",
        color="Comptes",
        color_continuous_scale=px.colors.sequential.Oranges
    )
    plot_cinema_cn2 = fig_cn2_treemap.to_html(full_html=False)

    #   Polar Area Chart per CN1b (Versió de l'última pel·lícula vista)
    fig_cn1b_polar = px.bar_polar(
        cn1b_summary_df,
        r="Comptes",
        theta="Versió de la pel·lícula",
        color="Versió de la pel·lícula",
        title="Versions de l'Última Pel·lícula Vista",
        color_discrete_sequence=px.colors.sequential.Oranges_r
    )
    plot_cinema_cn1b = fig_cn1b_polar.to_html(full_html=False)
    
    #   Waterfall Chart per CN1 (Ha anat al cinema?)
    fig_cn1_waterfall = px.bar(
        cn1_summary_df,
        x="Ha anat al cinema?",
        y="Comptes",
        color="Ha anat al cinema?",
        title="Ha anat al cinema?",
        color_discrete_sequence=px.colors.sequential.Oranges_r
    )
    plot_cinema_cn1 = fig_cn1_waterfall.to_html(full_html=False)
    
    fig_cs1_area = px.area(
        cs1_vs_cn1_long,
        x="CS1",
        y="Comptes",
        color="Resposta",
        title="Relació entre Situació Laboral i Anar al Cinema",
        labels={"CS1": "Situació Laboral", "Comptes": "Nombre de Respostes"},
        color_discrete_sequence=px.colors.sequential.Oranges_r
    )
    
    plot_situacio_laboral_vs_cinema_area = fig_cs1_area.to_html(full_html=False)

    # OR2 vs CN1 Area Plot
    fig_or2_area = px.area(
        or2_vs_cn1_long,
        x="OR2",
        y="Comptes",
        color="Resposta",
        title="Relació entre Lloc de Naixement i Anar al Cinema",
        labels={"OR2": "Lloc de Naixement", "Comptes": "Nombre de Respostes"},
        color_discrete_sequence=px.colors.sequential.Oranges_r
    )

    plot_lloc_naixement_vs_cinema_area = fig_or2_area.to_html(full_html=False)

    # Bubble Chart
    fig_bubble = px.scatter(
        bubble_data,
        x="Categoria",
        y="Interval d'Ingressos",
        size="Comptes",
        color="Categoria",
        title="Distribució d'Ingressos",
        labels={"Comptes": "Nombre de Respostes"},
        size_max=60,
        color_discrete_sequence=px.colors.sequential.Reds_r
    )
    
    plot_interval_ingressos = fig_bubble.to_html(full_html=False)
    
    categories = list(g2_summary.index) + list(g2a_summary.index)
    sources = ["Llar amb nucli familiar (parella/fills)"] * len(g2_summary) + ["Llar amb sense nucli familiar (unipersonal/amics)"] * len(g2a_summary)
    targets = list(range(len(g2_summary))) + list(range(len(g2_summary), len(categories)))
    values = g2_summary.tolist() + g2a_summary.tolist()
    nodes = sources + categories

    # Sankey Diagram
    fig_sankey_corrected = go.Figure(Sankey(
        node=dict(
            pad=40,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=[f"<b>{label}</b>" for label in nodes],
            color="Orange"
        ),
        link=dict(
            source=[nodes.index(s) for s in sources],
            target=[nodes.index(categories[t]) for t in targets],
            value=values
        )
    ))

    fig_sankey_corrected.update_layout(
        title_text="Flux d'Ingressos dels participants",
        font_size=10
    )
    
    plot_sankey = fig_sankey_corrected.to_html(full_html=False)
    
    fig_cultural_radar_percentages = px.line_polar(
        index_cultural_df,
        r="Percentatge",
        theta="Grup d'Edat",
        line_close=True,
        title="Índex de Culturalitat per Franja d'Edat",
        color_discrete_sequence=["orange"]
    )

    fig_cultural_radar_percentages.update_traces(
        fill='toself',
        mode='lines+text',
        text=index_cultural_df["Percentatge"].round(1).astype(str) + '%',
        textposition='top center'
    )
    
    plot_cultural_index_cultura = fig_cultural_radar_percentages.to_html(full_html=False)
    
    cultural_index_analysis = dataset.groupby(['AmbitTerritorial', 'SEXE'])['IndexCultural'].mean() * 100
    cultural_index_analysis_df = cultural_index_analysis.reset_index()
    cultural_index_analysis_df.columns = ['Àmbit Territorial', 'Sexe', 'Percentatge Index Cultural']

    fig_cultural_index_bar = px.bar(
        cultural_index_analysis_df,
        x='Àmbit Territorial',
        y='Percentatge Index Cultural',
        color='Sexe',
        title="Índex de Culturalitat per Àmbit Territorial i per Sexe",
        barmode='group',
        labels={'Percentatge Index Cultural': 'Percentatge', 'Àmbit Territorial': 'Àmbit Territorial', 'Sexe': 'Sexe'},
        color_discrete_sequence=px.colors.sequential.Oranges_r
    )

    plot_cultural_index_cultura_sexe_ambit = fig_cultural_index_bar.to_html(full_html=False)
    
    
    cultural_index_territorial_sexe_edat_df['IndexCultural'] = cultural_index_territorial_sexe_edat_df['IndexCultural'].replace(0, 0.01)

    fig_sunburst_corrected = px.sunburst(
        cultural_index_territorial_sexe_edat_df,
        path=['AmbitTerritorial', 'SEXE', 'EDAT'],
        values='IndexCultural',
        color='IndexCultural',
        color_continuous_scale='Oranges',
        title="Índex de Culturalitat per Àmbit Territorial, Sexe i Edat",
        labels={'IndexCultural': 'Índex Cultural (%)', 'EDAT': "Franja d'Edat", 'SEXE': 'Sexe', 'AmbitTerritorial': 'Àmbit Territorial'},
        width=1350,  # Ample més gran
        height=1000  # Alt més gran
    )
    
    plot_cultural_index_cultura_sexe_ambit_edat_sunburst = fig_sunburst_corrected.to_html(full_html=False)
    
    #index vs edat
    fig_scatter = px.scatter(
        cultural_index_income_df,
        x='Ingressos',
        y='Percentatge Index Cultural',
        size='Percentatge Index Cultural',
        color='Ingressos',
        title="Índex de Culturalitat segons els Ingressos de la Llar",
        labels={'Ingressos': "Intervals d'Ingressos", 'Percentatge Index Cultural': 'Índex Cultural (%)'},
        size_max=60,
        color_discrete_sequence=px.colors.sequential.Oranges_r
    )
    
    plot_cultural_index_cultura_ingressos = fig_scatter.to_html(full_html=False)

    return render_template('index.html', 
                           plot_edat=plot_html_edat,
                           plot_genere=plot_html_gender, 
                           plot_regio=plot_html_regio,
                           plot_llengua=plot_html_llengua,
                           plot_llar=plot_html_tipus_llar,
                           plot_diari=plot_html_d1,
                           plot_diari_d2=plot_html_d2,
                           plot_diari_d3=plot_html_d3,
                           plot_edat_vs_diars_radar=plot_edat_vs_diars_radar,
                           plot_edat_vs_radio_pie=plot_edat_vs_radio_pie,
                           plot_r2_polar=plot_r2_polar,
                           plot_r3_funnel=plot_r3_funnel,
                           plot_parallel_radio=plot_parallel_radio,
                           plot_cinema_cn1=plot_cinema_cn1,
                           plot_cinema_cn1b=plot_cinema_cn1b,
                           plot_cinema_cn2=plot_cinema_cn2,
                           plot_lloc_naixement_vs_cinema_area=plot_lloc_naixement_vs_cinema_area,
                           plot_situacio_laboral_vs_cinema_area=plot_situacio_laboral_vs_cinema_area,
                           plot_interval_ingressos=plot_interval_ingressos,
                           plot_sankey=plot_sankey,
                           plot_cultural_index_cultura=plot_cultural_index_cultura,
                           plot_cultural_index_cultura_sexe_ambit=plot_cultural_index_cultura_sexe_ambit,
                           plot_cultural_index_cultura_ingressos=plot_cultural_index_cultura_ingressos,
                           plot_cultural_index_cultura_sexe_ambit_edat_sunburst=plot_cultural_index_cultura_sexe_ambit_edat_sunburst)

if __name__ == '__main__':
    # app.run(debug=True)
    freezer.freeze()