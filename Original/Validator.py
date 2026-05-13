import json

class Validator:
    def validateFormat(self, data) -> bool:
        print("V: Validating format")

        required_fields = ["title", "author", "date", "group", "supervisor", "abstract", "keyword"]
        allowed_groups = ["CIRG", "SSFM", "CSEDAR", "DSFSI", "NICOG", "DIGIFORS"]

        # Rule 1 - Must be valid JSON format
        try:
            output = json.loads(data)
        except json.JSONDecodeError:
            return False
        
        if not isinstance(output, dict):
            return False
        
        # Rule 2 - All fields must be present and have non-empty values
        for field in required_fields:
            if field not in output:
                return False
            
            value = output[field]

            if value is None or str(value).strip == "":
                return False
            
        # Rule 3 - Research group must be valid
        if output["group"] not in allowed_groups:
            return False
        
        return True