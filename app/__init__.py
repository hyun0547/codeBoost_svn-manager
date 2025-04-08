import logging

from flask import Flask, jsonify
from app.routes import svnManager
from app.exceptions import ApiException


def create_app():
    app = Flask(__name__)

    app.register_blueprint(svnManager.bp)

    @app.errorhandler(ApiException)
    def handle_api_exception(e):
        return jsonify({
            "code": e.code,
            "status": e.status,
            "message": e.message
        }), e.code

    @app.errorhandler(Exception)
    def handle_unexpected_exception(e):
        logging.error(f"Unhandled Exception: {e}")
        return jsonify({
            "code": 500,
            "status": "ERROR",
            "message": "서버 내부 오류가 발생했습니다."
        }), 500

    return app

