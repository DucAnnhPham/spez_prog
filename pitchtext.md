Viele Menschen sind unsicher, wie sie ihren Müll korrekt trennen sollen.
Falsche Mülltrennung führt dabei zu verunreinigten Recyclingstoffen, höheren Kosten für die Abfallwirtschaft und belastet unsere Umwelt.

Hier kommt dann Wasty ins Spiel: Wasty ist ein KI-gestützter Müllklassifikator, der Gegenstände automatisch in die richtige Müllkategorie einordnet.

Das System kombiniert lokal erzeugte Embeddings, die in einer Qdrant-Datenbank gespeichert sind, mit der Option, die OpenAI API für Klassifikationen zu nutzen.
Wenn kein API-Key vorhanden ist, arbeitet Wasty zuverlässig komplett lokal.
Eingaben werden in "Gelbe Tonne", "Glascontainer", "Biotonne", "Restmülltonne", "Papiertonne", oder "Sperrmüll" klassifiziert.
Unsichere Eingaben werden bewusst mit „Ich weiß leider nicht, wohin das gehört.“ beantwortet, um Fehlklassifikationen zu vermeiden, und Sicherheitsmechanismen blockieren gefährliche oder unerwünschte Anfragen.

Wasty kann über eine REST-API oder eine interaktive CLI verwendet werden.
Es richtet sich an Privatpersonen, die Unterstützung bei der Mülltrennung suchen.
Damit bietet Wasty eine praktische Unterstützung im Alltag.

Durch Wasty können Nutzer ihren Beitrag zum Umweltschutz leisten. 
Kosten für die Abfallwirtschaft werden reduziert, und Recyclingprozesse werden effizienter.

Wasty macht Mülltrennung einfach, sicher und nachhaltig.

Pitch wurde gesprochen von https://luvvoice.com/