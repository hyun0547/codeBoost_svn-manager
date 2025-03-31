from flask import Flask, request, jsonify
import os
import subprocess

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


def list_svn_repositories(repo_base_path="/srv/svn/repository", page_num=1, page_size=10):
    try:
        repos = [{"name": d} for d in os.listdir(repo_base_path)
                 if os.path.isdir(os.path.join(repo_base_path, d))]

        start_idx = (page_num - 1) * page_size
        end_idx = start_idx + page_size
        paged_repos = repos[start_idx:end_idx]

        return paged_repos, 200
    except FileNotFoundError:
        return {"error": f"경로 없음: {repo_base_path}"}, 404
    except PermissionError:
        return {"error": f"권한 거부됨: {repo_base_path}"}, 403

@app.route('/create_repo', methods=['POST'])
def create_repo():
    data = request.get_json()

    if 'repo_name' not in data:
        return jsonify({"error": "리포지토리 이름이 필요합니다."}), 400

    repo_name = data['repo_name']
    repo_base_path = "/srv/svn/repository"
    config_path = "/srv/svn/common/config/svnserve.conf"

    return jsonify(create_svn_repository(repo_name, repo_base_path, config_path))


@app.route('/repo_list', methods=['POST'])
def list_repos():
    data = request.get_json()
    page_num = data.get("pageNum", 1)
    page_size = data.get("pageSize", 10)
    repo_base_path = "/srv/svn/repository"  # 실제 경로를 지정

    return jsonify(list_svn_repositories(repo_base_path, page_num, page_size)[0])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
