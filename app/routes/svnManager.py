from flask import Blueprint, request, jsonify, make_response
from app.services.svnManager_service import create_svn_repository, list_svn_repositories

bp = Blueprint('svn', __name__)

@bp.route('/repo_create', methods=['POST'])
def create_repo():
    data = request.get_json()
    repo_name = data.get('repoName')
    return create_svn_repository(repo_name)

@bp.route('/repo_list', methods=['POST'])
def list_repo():
    data = request.get_json()
    return list_svn_repositories(data.get("pageNum", 1), data.get("pageSize", 10))