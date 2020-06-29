from flask import Flask, request
from flask_restful import Api, Resource
import secrets
from Summarizer import SummarizeTexts
from FetchData import get_data_from_url

lsa_app = Flask(__name__)
api = Api(lsa_app)
ids_results = {}


class SubmitText(Resource):
    @classmethod
    def post(cls, type_: str):
        posted_data = request.get_json()
        if posted_data is None:
            return {"error": "request body is empty."}, 400
        type_ = type_.lower()
        if type_ not in ['text', 'link']:
            return {"error": f"The received type={type_} is invalid."}, 400
        elif type_ == "text" and posted_data.get("text") is None:
            return {"error": "For submit type text, text field must be valid."}, 400
        elif type_ == "link" and posted_data.get("url") is None:
            return {"error": "For submit type link, url field must be valid."}, 400

        id_ = secrets.token_hex(6)
        req = posted_data
        req['id'] = id_
        if type_ == "link":
            _, title, text = get_data_from_url(req.get("url"))
            if text is None:
                return {"error": "For submit url could not find any text."}, 400
            req['text'] = text
            req['title'] = title
        summerizer.register_new_request(req)
        ids_results[id_] = {"message": "request is accepted and is being processed",
                            "id": id_,
                            "status": "busy"}
        return ids_results[id_], 200


class GetSummary(Resource):
    @classmethod
    def get(cls, id_: str):
        if id_ is None or len(id_) == 0 or id_ not in ids_results.keys():
            return {"message": "id is invalid"}, 404
        results = summerizer.status
        for res in results:
            _id = res.get("id")
            ids_results[_id] = res

        res = ids_results.get(id_)
        if res is not None and res.get('status', 'busy') != 'busy':
            del ids_results[id_]
        return res, 200


api.add_resource(SubmitText, "/submit/<string:type_>")
api.add_resource(GetSummary, "/summary/<string:id_>")

if __name__ == "__main__":
    summerizer = SummarizeTexts()
    lsa_app.run(port=5000, debug=True)
