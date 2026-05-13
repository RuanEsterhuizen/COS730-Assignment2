import json

class Validator:
    def validateFormat(self, data:str) -> tuple[bool, str, dict]:
        print("V: Validating format")

        required_fields = ["title", "author", "date", "group", "supervisor", "abstract", "keyword"]
        allowed_groups = ["CIRG", "SSFM", "CSEDAR", "DSfSI", "NICOG", "DigiForS"]

        # Rule 1 - Must be valid JSON format
        try:
            output = json.loads(data)
        except json.JSONDecodeError:
            return False, "Invalid JSON", None
        
        if not isinstance(output, dict):
            return False, "Invalid JSON", None
        
        # Rule 2 - All fields must be present and have non-empty values
        for field in required_fields:
            if field not in output:
                return False, "Missing Attributes"
            
            value = output[field]

            if value is None or str(value).strip == "":
                return False, "Missing Attributes", None
            
        # Rule 3 - Research group must be valid
        if output["group"] not in allowed_groups:
            return False, "Invalid Attribute: 'group'", None
        
        return True, "Valid Format", output