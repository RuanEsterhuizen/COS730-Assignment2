import json

class Validator:
    def validateFormat(self, data) -> bool:
        #the data is already in json format

        print("V: Validating format")
        valid = True
        # do a bunch of rules stuff here

        # 1. Must be valid JSON
        # 2. All keys must be present and have non-zero values
        return valid