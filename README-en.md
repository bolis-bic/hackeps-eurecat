<p align="right"><a href="./README.md">Català</a> | <a href="./README-es.md">Español</a> | <a href="./README-en.md">English</a> | <a href="./README-cn.md">中文</a></p>

# HACKEPS EURECAT's CHALLENGE -  <a href="https://github.com/Applied-Artificial-Intelligence-Eurecat/hackeps/" id="top"><small>challenge</small></a>
---

<img src="./media/infrastructure.png"></img>

## 1. Dependencies

Generally, the only needed dependency will be ```Docker``` to execute the containers with their corresponding problem dependencies and code. 

## 2. GitHub Actions

To follow good programming habits to easily understand, maintain and improve the code's quality, we have implemented an automated system in GitHub's platform that will let us define customized workflows to automate code linting and formatting.    

We have created a _YAML_ in _.github/workflows_ which will allow us to automatically format the _Python_ code using the _autoyapf_. 

The steps the worflow has are:

1. Checkout to the corresponding branch.
2. Verify if there are any modified files after executing _autoyapf_.
3. If there are any, automatically format the code.
4. Do a new commit with the corresponding message and push it to the repository using the given access token in _secrets.GITHUB_TOKEN_.

Having done this, now for each pull request, we will have our linter and formatter executed automatically to have the code follow the standard guidelines of _PEP8_.


## 3. Missions

We have tried acomplishing most missions using ```Docker``` to minimize the needed manually installed libraries by the client, also simplifying the execute process.

<img src="./media/planta.png"></img>

### 🌼 Margarida

To execute the code
```
./margarida # docker-compose up --build
```

_Margarida_ was the first mission we did, having experience using the MQTT protocol it was not too much of a problem generating a code that, with the given credentials, could access the needed data. 
  
### <p id="sec-tulipa">🌷 Tulipa</p>

To execute the code
- Upload the program to the _ESP_ by putting the configuration variables of the network access point. For example, we loaded it with the _platform.io_ extension from _Visual Studio Code_.
- Once the program has been loaded into the _ESP_, the only thing left is to connect it to the electricity. The program should automatically connect, and reconnect, to the _MQTT broker_ using the specified network settings.

It wasn't our first time working with an _ESP_, but it was our first time using it with a plant. We discovered the potential, and the difficulties, of monitoring a plant.

In addition, to place a distance sensor we 3D printed a support customized to our needs. <img src="./media/suport.png"></img>

### 🎋 Bambu

To run the code:
```
./bamboo # docker-compose up --build
```

Once the container has been opened we will have a _Jupyter Notebook_ server on port _8888_, to access it we open our trusted browser and go to the address ```http://localhost:8888``` where we should have a directory with the notebook with the procedures carried out.

It wasn't the first time we preprocessed data with _Python_ libraries, although we had some problems detecting _outliers_.

### 🥑 Alvocat

To run the code (same as <a href="#sec-tulipa">Tulipa</a>):
- Upload the program to the _ESP_ by putting the configuration variables of the network access point. For example, we loaded it with the _platform.io_ extension from _Visual Studio Code_.
- Once the program has been loaded into the _ESP_, the only thing left is to connect it to the mains. The program should automatically connect, and reconnect, to the _MQTT broker_ using the specified network settings.

This challenge, in addition to sending data to the _MQTT broker_, added the reading of a signal to activate or deactivate a water pump to water the plant.

### 🍑 Prèssec

To run the code:
- Execute the steps of <a href="#sec-tulipa">Tulipa</a> (to have data to read).
- ```./pressec # docker-compose up --build```

This container takes the data sent by the sensors (in this case only from _Tulipa_) and saves it in a _time-series database_ (_influxDB_) because it is optimized to compress data of this type and is faster than a database _SQL_. Then, we take this data to represent it in real time with _Grafana_, which we can see once the container is opened at the URL: ```http://localhost:3000```. 

---
<div align="center">
This project is under license from MIT. For more details, see the <a href="./LICENSE.md">LICENSE file</a>.

Made with ❤️ by <a href="https://github.com/bolis-bic/" target="_blank">bolis-bic</a>

<a href="#top">Back to top</a>
</div>