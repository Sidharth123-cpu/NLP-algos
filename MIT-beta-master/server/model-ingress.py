from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer, CrossEncoder 
import requests
import json
import time 
from waitress import serve




app = Flask(__name__)

model_cross = CrossEncoder('cross_encoder/ms-marco-electra-base', max_length=512)

def payload1(query, size = 400):
      payload = {
      "_source": [
          "title",
          "id_", 
          "content"

      ],
      "size": size,
      "from": 0,
      "query": {
          "bool": {
              "must": [
                  {
                      "multi_match": {
                          "query": query[0],
                          "fields": [
                              "title",
                              "content"
                          ]
                      }
                  }
              ],

          }
      },
  }
      headers = {
    'Content-Type': 'application/json'
}
      r = requests.post("https://search-legal-research-z46e7wzfvak5aamgahdp6uknjy.us-west-2.es.amazonaws.com/courts_pre/_search", data= json.dumps(payload), headers=headers)
      data = r.json()
      print(query)
      ids = []
      for i in range(len(data['hits']['hits'])):
            ids.append((data['hits']['hits'][i]['_source']['title'], data['hits']['hits'][i]["_source"]['content'], data['hits']['hits'][i]['_id'][:32]))

      return ids

@app.route("/query",methods=[ 'POST'])
def hello():

    try:
        q =  request.get_json()["query"]
    except:
        return "Error: QUERY not included in REQUEST"

    query = [q.strip()]
    size = 400
    emb_return_size = 50
    ids = payload1(query, size)

    inputs = []
    secondary = []
    for i in range(0, 200):
  # source = data['hits']['hits'][i]['_source']
      inputs.append(( query[0], ids[i][1]))
      secondary.append((ids[i][0], ids[i][2]))
        
    scores = model_cross.predict(inputs[:100])

    final = []
    for i in range(0, len(scores)): 
      final.append((inputs[i][1], scores[i], secondary[i][0], secondary[i][1]))
    final.sort(key = lambda x : x[1], reverse = True)
    print(query[0])

    re = []
    lis = []
    for i in final: 
      if i[2] not in re:
          lis.append({"Title" : i[2], "ID" : i[3], "Text" : i[0], "Score" : str(i[1])})

    return jsonify(lis[:10])



if __name__ == "__main__":
    serve(app, port=80)
