# Nettverk Oblig 2

**Studentnr:** s374907 \
**Navn:** Fabian Tangen

## Task 1
`/task1` er task 1 sin http server. Her er alle requestsene håndtert en for hver. 

`connectionSocket.sendall(httpResponse.encode())`

Jeg velger å bruke sendall i stedet for å loope og sende hver packet. Sendall gjør alt dette for oss.

Om porten er full så går vi videre til neste.

Ctrl+C for å ende serveren på linux.

![Viser http og at den kjører i chrome](/task1/http_running.png)

## Task 2
Klient som bruker argparse til å lage en CLI http klient.

Argparse lar oss copy-paste port og ip sjekken fra siste oblig.

Vi kan også lett gi hjelp til brukeren.


## Task 3
Honestly hele tasken er bare å importere low-level libraryet _thread og gjøre hver client connection til en egen thread med 
`thread.start_new_thread(handle_client, (connectionSocket,))`

## NOTE:
Task1 og Task3 sin server.py er praktisk like bare med tanke på multithreading, så det er bare multithreading kommentarer i `/task3/server.py`.