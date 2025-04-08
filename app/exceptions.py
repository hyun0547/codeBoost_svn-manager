class ApiException(Exception):
    def __init__(self, code=500, status="ERROR", message="서버 오류"):
        self.code = code
        self.status = status
        self.message = message