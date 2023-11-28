<p align="right"><a href="./README.md">Català</a> | <a href="./README-es.md">Español</a> | <a href="./README-en.md">English</a> | <a href="./README-cn.md">中文</a></p>

# HACKEPS REPTE EURECAT -  <a href="https://github.com/Applied-Artificial-Intelligence-Eurecat/hackeps/" id="top"><small>repte</small></a>
---

<img src="./media/infrastructure.png"></img>

## 1. Dependències

En general, la única dependència que necessitarem és ```Docker``` per executar els contenidors amb les dependències i el codi corresponents a cada missió.

## 2. GitHub Actions

Per la importància de seguir unes bones pràctiques de programació per entendre fàcilment, mantenir i millorar la qualitat del codi, hem implementat un sistema d'automatització integrat en la plataforma de GitHub que ens permetrà definir fluxos de treball (workflows) personalitzats per automatitzar proves de _linting_ i el formateig del codi.

S'ha creat un arxiu _YAML_ en _.github/workflows_ que ens servirà per formatejar automàticament el codi _Python_ utilitzant l'eina _autoyapf_.

Els passos que segueix són:

1. Es realitza un checkout a la branca.
2. Es verifica si hi han arxius modificats després d'executar _autoyapf_.
3. Si hi ha arxius modificats, es formatejarà automàticament el codi.
4. Es duu a terme un _commit_ amb el missatge indicat i després s'envia al repositori emprant un token d'accés proporcionat per _secrets.GITHUB_TOKEN_.

De manera que ara, per a cada pull request que fem, es passarà automàticament el test i es faràn els canvis pertinents seguint l'estàndard de guies estils _PEP8_ de _Python_.

## 3. Missions

Hem intentat fer la majoria de missions utilitzant ```Docker``` per a minimitzar les llibreries y paquets a instal·lar manualment per part del client, a més de simplificar el procés d'execució.

<img src="./media/planta.png"></img>

### 🌼 Margarida

Per executar el codi:
```
./margarida # docker-compose up --build
```

Margarida va ser la primera missió que vam fer, com tenim experiència utilitzant el protocol <i>MQTT</i> no vas ser massa problema generar un codi que, amb les credencials donades, llegeixi del tòpic demanat.
  
### <p id="sec-tulipa">🌷 Tulipa</p>

Per executar el codi:
- Carregar el programa a la _ESP_ possant-hi les variables de configuració del punt d'accés a la xarxa. Per exemple, nosaltres el vam carregar amb l'extensió _platform.io_ del _Visual Studio Code_.
- A partir d'haver carregat el programa a la _ESP_, l'únic que falta és connectar-la a la xarxa elèctrica. El programa s'hauria de connectar, i reconnectar, automàticament al _MQTT broker_ utilitzant la configuració de xarxa especificada. 

No era el nostre primer cop treballant amb una _ESP_, però sí que va ser el primer cop utilitzant-la amb una planta. Vam descobrir el potencial, i les dificultats, de monitoritzar una planta. 

A més a més, per a col·locar un sensor de distància vam imprimir en 3D un suport customitzat al es nostres necessitats. <img src="./media/suport.png"></img>

### 🎋 Bambú 

Per executar el codi:
```
./bambu # docker-compose up --build
```

Un cop s'ha obert el contenidor tindrem un servidor de _Jupyter Notebook_ al port _8888_, per accedir-hi obrim el nostre navegador de confiança i anem a la direcció ```http://localhost:8888``` on hauriem de tenir un directori amb el notebook amb els procediments realitzats.

No era el primer cop que preprocessàvem dades amb llibreries de _Python_, tot i que se'ns va complicar una mica la detecció d'_outliers_.

### 🥑 Alvocat

Per executar el codi (igual que <a href="#sec-tulipa">Tulipa</a>):
- Carregar el programa a la _ESP_ possant-hi les variables de configuració del punt d'accés a la xarxa. Per exemple, nosaltres el vam carregar amb l'extensió _platform.io_ del _Visual Studio Code_.
- A partir d'haver carregat el programa a la _ESP_, l'únic que falta és connectar-la a la xarxa elèctrica. El programa s'hauria de connectar, i reconnectar, automàticament al _MQTT broker_ utilitzant la configuració de xarxa especificada. 

Aquest repte, a més a més d'enviar dades al _MQTT broker_, afegia la lectura d'una senyal per a activar o desactivar una bomba d'aigua per regar la planta. 

### 🍑 Préssec

Per executar el codi:
- Executar els passos de <a href="#sec-tulipa">Tulipa</a> (per tenir dades a llegir).
- ```./pressec # docker-compose up --build```

Aquest contenidor agafa les dades que envien els sensors (en aquest cas solament de _Tulipa_) i les guarda en una _time-series database_ (_influxDB_) perquè està optimitzada per a comprimir les dades d'aquest tipus i és més ràpida que una base de dades _SQL_. Desprès, agafem aquestes dades per representar-les a temps real amb _Grafana_, les quals podem veure un cop obert el contenidor a la URL: ```http://localhost:3000```. 

---
<div align="center">
<p>
This project is under license from MIT. For more details, see the <a href="./LICENSE.md">LICENSE file</a>.

Made with ❤️ by <a href="https://github.com/bolis-bic/" target="_blank">bolis-bic</a>

<a href="#top">Back to top</a></p>
</div>