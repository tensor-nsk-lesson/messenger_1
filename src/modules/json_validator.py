from flask import abort
import json
import jsonschema

def json_validate(data_source, schema):
    try:
        data = json.loads(data_source)
        jsonschema.validate(data, schema)
        return data
    except (jsonschema.exceptions.ValidationError, json.decoder.JSONDecodeError) as err:
        print(err)
        return abort(400)
