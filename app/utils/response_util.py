from flask import jsonify

def success_response(data=None, message="요청이 성공적으로 처리되었습니다."):
    return jsonify({
        "code": 200,
        "status": "OK",
        "message": message,
        "data": data
    }), 200