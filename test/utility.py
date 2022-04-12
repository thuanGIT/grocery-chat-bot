
class ConvertUtilities:
    # Utility method to convert result set into string
    @staticmethod
    def query_result_to_str(cursor):
        result = []
        for row in cursor:
            row_data = []
            for attr in row:
                row_data.append(str(attr))
            result.append(",".join(row_data))

        return "\n".join(result)


    # Utility method to convert a single record (dict) into string
    @staticmethod
    def record_to_str(record: dict):
        if record:
            result = []
            for _, v in record.items():
                result.append(str(v))

            return ",".join(result)
        else:
            return ""

    # Utility method to convert a set of metadata to string
    @staticmethod
    def metadata_to_str(schema):
        buffer = [] # A string buffer
        for table in schema:
            inner_buffer = []
            for metadata in table:
                inner_buffer.append(str(metadata))
            buffer.append(",".join(inner_buffer))
        return "\n".join(buffer)