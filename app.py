from flask import Flask, request, jsonify
import os
import subprocess
import sys

app = Flask(__name__)

def create_svn_repository(repo_name, repo_base_path, config_path):
    # 리포지토리 경로 설정
    repo_path = os.path.join(repo_base_path, repo_name)
    conf_file = os.path.join(repo_path, 'conf', 'svnserve.conf')

    # 리포지토리 이름과 경로가 유효한지 확인
    if not repo_name:
        return {"error": "리포지토리 이름이 필요합니다."}, 400

    if os.path.isdir(repo_path):
        return {"error": f"이미 존재하는 리포지토리: {repo_path}"}, 400

    try:
        # SVN 리포지토리 생성
        subprocess.run(['svnadmin', 'create', repo_path], check=True)

        # 기존 svnserve.conf 제거 및 심볼릭 링크 생성
        if os.path.isfile(conf_file):
            os.remove(conf_file)

        os.symlink(config_path, conf_file)
        return {"message": f"SVN 리포지토리 생성 완료: {repo_path}"}, 200

    except subprocess.CalledProcessError as e:
        return {"error": f"오류 발생: {e}"}, 500


@app.route('/create_repo', methods=['POST'])
def create_repo():
    data = request.get_json()

    if 'repo_name' not in data:
        return jsonify({"error": "리포지토리 이름이 필요합니다."}), 400

    repo_name = data['repo_name']
    repo_base_path = "/srv/svn/repository"
    config_path = "/srv/svn/common/config/svnserve.conf"

    return jsonify(create_svn_repository(repo_name, repo_base_path, config_path))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
