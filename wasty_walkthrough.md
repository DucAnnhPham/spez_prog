# Projektnutzung mit Docker und Kubernetes mit Konsolen-Ausgaben

# 1) Microservice A wasty-chat
### Docker image bauen
```bash
export OPENAI_API_KEY="<openai_api_key>"


cd wasty-chat

docker build -t wasty-chat:latest .
```

Konsolenausgabe:
```
[+] Building 14.5s (12/12) FINISHED 
...
View build details:...
```

# 2) Microservice B wasty-api

### Docker image bauen
```bash
export OPENAI_API_KEY="<openai_api_key>"


cd wasty-api

docker build -t wasty-api:latest .
```

Konsolenausgabe:
```
[+] Building 11.3s (11/11) FINISHED
...
View build details:...
```

# 3) Gemeinsamer Start mit Docker Compose
```bash
export OPENAI_API_KEY="<openai_api_key>"


docker compose up --build -d
```

Konsolenausgabe:
```
[+] Running 6/6                                                                                                                                                                      
 ✔ wasty-api:latest                 Built                                                                                                                                       0.0s 
 ✔ wasty-chat:latest                Built                                                                                                                                       0.0s 
 ✔ Network spez_prog_final_default  Created                                                                                                                                     0.0s 
 ✔ Container qdrant                 Started                                                                                                                                     0.9s 
 ✔ Container wasty-api              Started                                                                                                                                     0.8s 
 ✔ Container wasty-chat             Started  
```

### Ingest der lokalen Daten in Qdrant
```bash
export OPENAI_API_KEY="<openai_api_key>"


docker compose exec wasty-chat python classifier.py ingest /app/data/waste.csv
```

Konsolenausgabe:
```

tokenizer_config.json: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 350/350 [00:00<00:00, 1.66MB/s]
tokenizer.json: 466kB [00:00, 3.37MB/s]
special_tokens_map.json: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 112/112 [00:00<00:00, 743kB/s]
config.json: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 190/190 [00:00<00:00, 1.83MB/s]
Alte Collection gelöscht
Batch 1: 50 Punkte hochgeladen
[...]
Batch 22: 6 Punkte hochgeladen
```

### Interaktiver start der anwendung
```bash
docker compose exec wasty-chat python classifier.py
```

Konsolenausgabe:
```
OpenAI-Modus aktiv.
Starte Müll-Klassifikator. Aktueller Modus: OpenAI
Befehle: ':exit' zum Beenden, ':switch' zum Moduswechsel
Gib ein Objekt ein: 
```

Beispiel-Eingabe mit Konsolenausgabe:
```
OpenAI-Modus aktiv.
Starte Müll-Klassifikator. Aktueller Modus: OpenAI
Befehle: ':exit' zum Beenden, ':switch' zum Moduswechsel
Gib ein Objekt ein: banane
Klassifizierung mittels OpenAI: banane
Das Objekt gehört hier rein: → Biotonne
Gib ein Objekt ein: Zeitung
Klassifizierung mittels OpenAI: zeitung
Das Objekt gehört hier rein: → Papiertonne
Gib ein Objekt ein: :switch
Modus gewechselt → Lokale Embeddings aktiviert.
Gib ein Objekt ein: bananenschale
Klassifizierung mittels localEmbeddings: bananenschale
Das Objekt gehört hier rein: → Biotonne
Gib ein Objekt ein: password
Sicherheitsmeldung: Anfrage blockiert.
Gib ein Objekt ein: :exit
Beende Müll-Klassifikator.
```

### API testen
```bash
curl -s http://localhost:8080/health
curl -s -X POST "http://localhost:8080/analyze" \
     -H "Content-Type: application/json" \
     -d '{"item": "bananenschale"}' | jq
curl -s -X POST "http://localhost:8080/analyze" \
     -H "Content-Type: application/json" \
     -d '{"item": "bananenschale", "use_openai": false}' | jq
curl -s -X POST "http://localhost:8080/analyze" \
     -H "Content-Type: application/json" \
     -d '{"item": "password", "use_openai": false}' | jq
curl -s -X POST "http://localhost:8080/analyze" \
     -H "Content-Type: application/json" \
     -d '{"item": "HNVHJNWWUN", "use_openai": false}' | jq
```

Konsolenausgaben:
```
{"status":"ok"}%    
{
  "alert": "classified",
  "category": "Biotonne"
}
{
  "alert": "classified",
  "category": "Biotonne"
}
{
  "alert": "blocked",
  "reason": "Sicherheits-Schlüsselwort erkannt"
}
{
  "alert": "unknown Object",
  "category": "ich weiß nicht"
}

```

# 4) Kubernetes Deployment - kubernetes cluster ist schon am laufen
### # Secret, confifigmap und qdrant deployment anlegen
```bash
cd k8s
kubectl apply -f secret-openai.yaml -f configmap-wasty.yaml -f deployment-qdrant.yaml -f service-qdrant.yaml -f configmap-waste-data.yaml
```

- Meldung:
```
secret/secret-openai created
configmap/configmap-wasty created
deployment.apps/qdrant created
service/qdrant created
configmap/waste-data created
```


# Kubernetes Job/One-Off Pod zum Collection-Anlegen in Qdrant
```bash
kubectl run qdrant-ensure-wasty-chat --rm -i --restart=Never \
  --image=curlimages/curl:8.9.0 -- \
  sh -lc 'set -e;
  echo "Prüfe, ob Collection wasty_docs existiert...";
  if curl -sf http://qdrant:6333/collections/wasty_docs >/dev/null; then
      echo "✔ Collection existiert bereits";
  else
      echo "Collection fehlt – wird angelegt...";
      curl -s -X PUT http://qdrant:6333/collections/wasty_docs \
        -H "Content-Type: application/json" \
        -d "{\"vectors\":{\"size\":384,\"distance\":\"Cosine\"}}" \
        && echo "✔ Collection erfolgreich angelegt";
  fi'
```

Konsolenausgabe:
```
Prüfe, ob Collection wasty_docs existiert...
Collection fehlt – wird angelegt...
{"result":true,"status":"ok","time":0.040216792}✔ Collection erfolgreich angelegt
pod "qdrant-ensure-wasty-chat" deleted from default namespace
```

# Microservice A Wasty-Chat Deployment
```bash
kubectl apply -f deployment-wasty-chat.yaml

kubectl wait --for=condition=available --timeout=120s deployment/wasty-chat

POD=$(kubectl get pods -l app=wasty-chat -o jsonpath="{.items[0].metadata.name}")
echo "Wasty-chat Pod: $POD"

kubectl exec -it $POD -- bash -lc 'python classifier.py ingest /app/data/waste.csv'
```

Konsolenausgabe:
```
deployment.apps/wasty-chat created

deployment.apps/wasty-chat condition met

Wasty-chat Pod: wasty-chat-7d97749-8nhpv

Alte Collection gelöscht
Batch 1: 50 Punkte hochgeladen
[...]
Batch 22: 6 Punkte hochgeladen
```

# CLI zum interaktiven testen des wasty-chat microservice mit Beispielklassifikationen
```bash
kubectl exec -it $POD -- bash -lc 'python classifier.py'
```

Konsolenausgabe:
```
OpenAI-Modus aktiv.
Starte Müll-Klassifikator. Aktueller Modus: OpenAI
Befehle: ':exit' zum Beenden, ':switch' zum Moduswechsel
Gib ein Objekt ein: bananenschale
Klassifizierung mittels OpenAI: bananenschale
Das Objekt gehört hier rein: → Biotonne
Gib ein Objekt ein: :switch
Modus gewechselt → Lokale Embeddings aktiviert.
Gib ein Objekt ein: bananenschale
Klassifizierung mittels localEmbeddings: bananenschale
Das Objekt gehört hier rein: → Biotonne
Gib ein Objekt ein: :switch
Modus gewechselt → OpenAI aktiviert.
Gib ein Objekt ein: password
Sicherheitsmeldung: Anfrage blockiert.
Gib ein Objekt ein: lalalalala
Klassifizierung mittels OpenAI: lalalalala
Ich weiß leider nicht wohin das gehört.
Gib ein Objekt ein: :exit
Beende Müll-Klassifikator.
```

# Microservice B Wasty-API Deployment
```bash
kubectl apply -f deployment-wasty-api.yaml -f service-wasty-api.yaml

kubectl wait --for=condition=available --timeout=120s deployment/wasty-api

kubectl port-forward svc/wasty-api 18080:8080
```

Konsolenausgabe:
```
deployment.apps/wasty-api created
service/wasty-api created

deployment.apps/wasty-api condition met


Forwarding from 127.0.0.1:18080 -> 8080
Forwarding from [::1]:18080 -> 8080
```


# API testen im neuen Terminal
```bash
curl -s http://localhost:18080/health
curl -s -X POST "http://localhost:18080/analyze" \
     -H "Content-Type: application/json" \
     -d '{"item": "bananenschale"}' | jq
curl -s -X POST "http://localhost:18080/analyze" \
     -H "Content-Type: application/json" \
     -d '{"item": "bananenschale", "use_openai": false}' | jq
curl -s -X POST "http://localhost:18080/analyze" \
     -H "Content-Type: application/json" \
     -d '{"item": "password", "use_openai": false}' | jq
curl -s -X POST "http://localhost:18080/analyze" \
     -H "Content-Type: application/json" \
     -d '{"item": "HNVHJNWWUN", "use_openai": false}' | jq
```

Konsolenausgaben:
```
{"status":"ok"}%    
{
  "alert": "classified",
  "category": "Biotonne"
}
{
  "alert": "classified",
  "category": "Biotonne"
}
{
  "alert": "blocked",
  "reason": "Sicherheits-Schlüsselwort erkannt"
}
{
  "alert": "unknown Object",
  "category": "ich weiß nicht"
}
```