import json
from bson import json_util


class BsonSerializer:
    @staticmethod
    def serialize_search_results(results):

        data = []

        for result in results:
            result_obj = json.loads(json_util.dumps(result))

            if '_id' in result_obj:
                result_obj['_id'] = result_obj['_id']['$oid']

            data.append(result_obj)

        return data
