# Pràctica Final - Explorant els Hàbits Culturals de la Societat Catalana

A continuació es pot trobar el codi de la pràctica final de l'Assigantura de Visualització De Dades del Màster de Ciència de Dades de la UOC.

## Autora

**Marta Granero I Martí**

## Eines

- **Plotly**
- **Python**
- **Git, Github i Github-Pages**
- **Excel**
- **Flask, i Freezer**

## Estructura del repositori

El codi de les visualitzacions es troba al fitxer `app.py`. Addicionalment, a la carpeta `data` es troba el conjunt de dades emprat `dataset.xlsx` i el Qüestionari amb les diferents preguntes de l'enquesta. També, a `templates` podem visualitzar el `index.html` sobre el que es veuen les gràfiques. I a la carpeta `build` es troba l'aplicació web estàtica creada amb Flask-Freezer, que és una extensió per al microframework Flask, que permet generar la viusalització com una aplicacions web estàtiques a partir d'aplicacions web dinàmiques desenvolupades amb Flask. S'ha emprat per poder-la desplegar fàcilment en un servidor estàtic, com GitHub Pages.

## Com construir el projecte?

Per tal de fer-ho, hem d'ubicar-nos en l'entorn `venv` creat, un cop a dins, hem d'anar a la terminal i escriure la següent comanda:

```{python}
python3 app.py
```

**Notem!**

Se'ns desplegarà al nostre entorn local i al port 5000. Tot i això, per tal d'assegurar-nos que es deplagarà correctament al port 5000, hem d'anar al fixer de `app.py` i fixar-nos si la primera línia està descomenada i la segona comentada per tal que no ens faci la generació de la visualització com una web i la guardi a `build` sinó que se'ns mostri al port:

```{python}
if __name__ == '__main__':
    app.run(debug=True)
    # freezer.freeze()
```

## On es pot trobar la visualització?

La pàgina web on visualitzar el **storytelling**: https://martaw-code.github.io/Martaw-code/

## Llicència MIT

Aquestes dades s'han obtingut a partir del portal de Dades Obertes de la Generalitat de Catalunya i les dades provenen del Departament de Cultura.
Es poden trobar en el següent ellaç: [https://analisi.transparenciacatalunya.cat/Cultura-oci/Enquesta-de-participaci-cultural-de-Catalunya-2023/tdfn-n2aw/about_data](https://analisi.transparenciacatalunya.cat/Cultura-oci/Enquesta-de-participaci-cultural-de-Catalunya-2023/tdfn-n2aw/about_data)

Les dades es troben subjectes sota la llicència **[Llicència oberta d’ús d’informació - Catalunya](https://administraciodigital.gencat.cat/ca/dades/dades-obertes/informacio-practica/llicencies/)**


