# B6.4.4 WP ausgew. Themen WI - Spezielle Programmierung Duc Anh Pham - Matrikelnummer: 598979 
# Projekt: Wasty - Müllklassifikation in Deutschland
## 1. Executive Summary – Kurze Zusammenfassung des Projekts.
    Wasty ist ein Ki-gestützter Müllklassifikator, der Gegenstände analysiert und autamotisch in die richtige Müllkategorie einordnet.
    Es kombiniert lokal erzeugte Embeddings von lokalen Daten, die gespeichert werdenin Qdrant, und einer Anbindung einer OpenAI API zur Klassifiezierung.
    Nutzer erhalten so verlässliche Emfehlenungen wohin der Gegenstand entwsorgt werden soll.
    Bei Unsicherheiten gibt die AI bewusst „Ich weiß leider nicht wohin das gehört.“ aus, um Fehlklassifizierungen zu vermeiden.
    Außerdem gibt es Sicherheitsmechanismen, die manche Anfragen blockieren, für die Sicherheit des Systems.
    Dazu gibt es noch einen API-Service, welcher lokal oder auch in Kubernetes aktiv sein kann.
    Die Nutzung erfolgt über eine REST-API, wo Nutzer mithilfe eines POST-Requests eine Klassifizierung anfragen können.
    Außerdem gibt es eine CLI-Anwendung, die interaktiv genutzt werden kann.
## 2. Ziele des Projekts – Welche Ziele verfolgt Ihr Projekt, welches Problem wird gelöst?  
    Das Hauptziel von Wasty ist die Verbesserung der Mülltrennung in Deutschland durch die Unterstützung einer KI.
    Viele Menschen sind unsicher, wie sie bestimmte Gegenstände richtig entsorgen sollen und was in welche Tonne gehört.
    Durch die Nutzung von Wasty soll genau das Problem lösen.
    Durch die Emfelungen von Wasty können Nutzer sicherstellen, dass sie ihren Müll korrekt trennen und entsorgen.
    Dies trägt zur Reduzierung von Umweltverschmutzung und zur Förderung von Recyclingkreislaufs bei.
    Außerdem soll Wasty dabei helfen, das Wissen der Nutzer über Mülltrennung zu verbessern, indem verschiedene Gegenstände ausprobiert und vom System bewertet werden können.
    Wasty schafft somit sowohl direkte Unterstützung im Alltag als auch einen langfristigen Lern- und Aufklärungseffekt.
## 3. Anwendung und Nutzung – Wie wird die Lösung verwendet, wer sind die Hauptnutzer:innen?
    Die Lösung wird über eine REST-API bereitgestellt, die es Nutzer ermöglicht, Gegenstände zur Müllklassifikation einzureichen.
    Nutzer können einen POST-Request an den Endpunkt /analyze senden, wobei sie den Namen des Gegenstands im JSON-Format übermitteln.
    Genutzt werden kann dafür curl oder Postman.
    Alternativ gibt es eine interaktive CLI-Anwendung die gestartet werden kann, um direkt im Terminal Gegenstände einzugeben und die Klassifikation zu erhalten.
    Die Commands, die der Nutzer zu dem nutzen kann, werden dabei am start kurz ausgegeben. (:switch und :exit)
    Standardmäßig nutzt Wasty die OpenAI API für die Klassifikation, kann aber auch im lokalen Modus betrieben werden, wenn keine API-Schlüssel vorhanden sind.
    Hauptnutzer sind dabei eher Privatpersonen, die Unterstützung bei der Mülltrennung suchen.
    Der Pitch dazu ist hier in diesem GitHub Repository zu finden: pitch.mp3
## 4. Entwicklungsstand – Idee, Proof of Concept, Prototyp oder Einsatzbereit?
    Derzeit ist Wasty als funktionstüchtiger Prototyp verfügbar.
    Die Grundfunktionen zur Müllklassifikation sind implementiert und können sowohl über die REST-API als auch über die CLI-Anwendung genutzt werden.
    Der Prototyp nutzt eine Kombination aus lokal gespeicherten Embeddings in Qdrant und der OpenAI API, um eine zuverlässige Klassifikation zu gewährleisten.
    Sicherheitsmechanismensind ebenfalls integriert, um unsichere Anfragen zu blockieren. 
    Zum Beispiel wenn die Anfrage wörter wie password enthält.
    Auch die Containiserung mit Docker und docker-compose ist umgesetzt, sodass der Prototyp einfach lokal in Docker gebaut und gestartet werden kann.
    Außerdem sind Kubernetes-Manifeste vorhanden, um den Prototyp in einer Kubernetes-Umgebung zu laufen zu bringen.
    So ist Wasty laufbereit und kann von Nutzer getestet und verwendet werden.
## 5. Projektdetails – Welche Kernfunktionen oder Besonderheiten bietet Ihr Projekt?
    Wastys Kernfunktion ist die KI-gestützte Müllklassifikation in 6 Müllkategorien.
    Dazu gehören Gelbe Tonne, Glascontainer, Biotonne, Restmülltonne, Papiertonne und Sperrmüll mit einem Fallback für unsichere Klassifikationen.
    Wasty ist dabei ein hybrides System, das sowohl lokal gespeicherte Embeddings in Qdrant nutzt als auch die OpenAI API für die Klassifikation.
    Dadurch kann Wasty auch im Offline-Modus betrieben werden, wenn kein API-Schlüssel vorhanden.
    Top-K Treffer aus der Vektor-Datenbank werden auch berücksichtigt, um die Genauigkeit zu erhöhen wenn lokale Embeddings genutzt werden.
    Die API kann einfach über HTTP-Requests angesprochen werden, was eine einfache Integration in andere Systeme ermöglicht.
    Zusätzlich gibt es eine interaktive CLI-Anwendung, die es Nutzer ermöglicht, direkt im Terminal Gegenstände einzugeben und die Klassifikation zu erhalten.
    Sicherheitsmechanismen sind ebenfalls integriert,
    Die lokalen Daten können auch erweitert werden, indem die data.csv und die configmap-waste-data.yaml erweitert wird.
## 6. Innovation – Was ist neu und besonders innovativ?  
    Das besondere an Wasty ist die Kombination aus lokal gespeicherten/erstellten Embeddings und der Nutzung der OpenAI API für die Müllklassifikation.
    Diese hybride Herangehensweise ermöglicht es Wasty, auch ohne einen OPEN AI API-Schlüssel zu funktonieren.
    Das automatische Fallback auf die Lokalen Embeddings in Qdrant ist innovativ, da es die Abhängigkeit von der OpenAI API reduziert und die Verfügbarkeit des Systems erhöht.
    Auch die bewusste Ausgabe von „Ich weiß nicht“ bei unsicheren Klassifikationen ist eine innovative Funktion, die dazu beiträgt,
    Fehlklassifizierungen zu vermeiden und die Zuverlässigkeit des Systems zu erhöhen.
    Die Integration von Sicherheitsmechanismen, die bestimmte Anfragen blockieren, ist ebenfalls ein innovativer Ansatz, um die Sicherheit des Systems zu gewährleisten.
    Insgesamt bietet Wasty eine neuartige Lösung für das Problem der Mülltrennung, die sowohl technisch als auch funktional innovativ ist.
## 7. Wirkung (Impact) – Welchen konkreten Nutzen bringt Ihr Projekt? 
    Wasty bringt einen direkten Nutzen, indem es Privatpersonen zuverlässig dabei unterstützt, ihren Müll korrekt zu trennen und zu entsorgen.
    Durch präzise Klassifikationen können Nutzer sicherstellen, dass sie ihren Beitrag zur Reduzierung von Umweltverschmutzung und zur Förderung funktionierender Recyclingkreisläufe leisten.
    Eine korrekte Mülltrennung erhöht die Effizienz von Recyclingprozessen erheblich und verringert die Menge an Abfällen, die in der Verbrennung oder auf Deponien landen.
    Auch wirtschaftlich kann Wasty einen bedeutenden Beitrag leisten, da eine sauberere Mülltrennung die Kosten für die Abfallwirtschaft reduziert.
    Weniger Fehlwürfe führen zu geringerem Sortieraufwand und reduzieren den Anteil kontaminierter Wertstoffe, was die Weiterverarbeitung erleichtert.
    Darüber hinaus fördert Wasty das Umweltbewusstsein im Alltag und unterstützt Menschen dabei, nachhaltige Entscheidungen intuitiver zu treffen.
    Insgesamt trägt das Projekt nicht nur zur Verbesserung individueller Entsorgungspraktiken bei, sondern auch langfristig zur Optimierung der gesamten Abfallwirtschaft.
## 8. Technische Exzellenz – Welche Technologien, Daten oder Algorithmen werden genutzt?  
    Für die Wasty wird Python als Hauptprogrammiersprache verwendet.
    Außerdem wird für die Bereitstellung der REST-API das FastAPI-Framework genutzt.
    Lokale Embeddings für die Lokale Müllklassifikation werden mit `sentence-transformers/all-MiniLM-L6-v2` erzeugt. 
    Diese Embeddings werden in einer Qdrant Vektor-Datenbank gespeichert und für die Ähnlichkeitssuche genutzt.
    Mit MIN_SCORE und TOP_K können die Suchergebnisse konfiguriert werden und die Genauigkeit der lokalen Klassifikation beeinflusst werden.
    Für die OpenAI Klassifizierung wird die Offizielle OpenAI API verwendet welche mithilfe unseres Promptes eine Klassifikation in die 6 Müllkategorien durchführt.
    Die Containerisierung erfolgt mit Docker um die Images lokal bauen zu können.
    Kubernetes Manifeste sind ebenfalls vorhanden, um die Anwendung in einer Kubernetes-Umgebung zu deployen.
## 9. Ethik, Transparenz und Inklusion – Wie stellen Sie Fairness, Transparenz und Sicherheit sicher?  
    Wasty legt großen Wert auf Ethik, Transparenz und Inklusion.
    Durch den Einsatz lokaler Embeddings ist das System datensparsam und benötigt keine persönlichen Informationen, wodurch ein hohes Maß an Datenschutz gewährleistet ist.
    Wenn externe KI-Modelle wie OpenAI genutzt werden, geschieht dies nur optional und mit klaren Hinweisen, sodass die Nutzer volle Kontrolle über ihren Datenfluss behalten.
    Wasty enthält außerdem Sicherheitsmechanismen, die falsche oder unsichere Eingaben erkennen und sicher abweisen.
    Wasty ist auch sehr simpel gehalten um es leicht verständlich zu machen, damit möglichst jeder es verstehen und nutzen kann.
    Durch die Möglichkeit, ohne API-Key vollständig lokal zu funktionieren, wird niemand ausgeschlossen, der keine externen Dienste nutzen möchte oder kann.
    Insgesamt fördert Wasty eine faire und inklusive Nutzung, indem es allen Nutzer ermöglicht, das System zu verwenden und ihre Daten sicher zu verarbeiten.
## 10. Zukunftsvision – Wie könnte das Projekt in 5–10 Jahren aussehen?  
    In den nächsten 5–10 Jahren könnte Wasty zu einer umfassenden Plattform für Mülltrennung und Recycling werden.
    Wasty könnte um eine mobile App mit Kameraerkennung erweitert werden, die es Nutzer ermöglicht, Gegenstände einfach zu fotografieren und automatisch klassifizieren zu lassen.
    Das macht die Nutzung noch einfacher für den Alltag.
    Außerdem durch kontinulierliche Weiterentwicklung, Erweiterung des Lokal gespeicherten Daten und Feedback von Nutzer könnte die Genauigkeit der Klassifikationen weiter verbessert werden.
    So könnte Wasty zu einem unverzichtbaren Werkzeug für Haushalte werden, das nicht mehr wegzudenken ist.
    Auch könnte man über Partnerschaften nachdenken, die Nutzer belohnt wenn sie Wasty nutzen, um ihren Müll korrekt zu trennen.
    So könnte man auch noch mehr Nutzer gewinnen und den Recyclinggedanken weiter verbreiten.
    Insgesamt könnte Wasty also in 5–10 Jahren eine zentrale Rolle in der Mülltrennung spielen und einen bedeutenden Beitrag zu einer nachhaltigeren Gesellschaft leisten.

### Datenquelle für die lokale Müllklassifikation(Mülldaten für Qdrant)
- https://www.awv-gg.de/wp-content/uploads/2023/04/awv_abfall_a_z.pdf

