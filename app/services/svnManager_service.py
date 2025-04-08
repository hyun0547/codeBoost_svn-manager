import os
import subprocess
import logging
from flask import jsonify, make_response

def create_svn_repository(repo_name, repo_base_path="/srv/svn/repository", config_path="/srv/svn/common/config/svnserve.conf"):
    repo_path = os.path.join(repo_base_path, repo_name)
    conf_file = os.path.join(repo_path, 'conf', 'svnserve.conf')

    if not repo_name:
        logging.warning("리포지토리 이름이 필요합니다.")
        return make_response(jsonify({"code": 400, "status": "ERROR", "message": "리포지토리 이름이 필요합니다."}), 400)

    if os.path.isdir(repo_path):
        logging.warning(f"이미 존재하는 리포지토리: {repo_path}")
        return make_response(jsonify({"code": 400, "status": "ERROR", "message": f"이미 존재하는 리포지토리: {repo_path}"}), 400)

    try:
        subprocess.run(['svnadmin', 'create', repo_path], check=True)

        if os.path.isfile(conf_file):
            os.remove(conf_file)

        os.symlink(config_path, conf_file)

        logging.info(f"SVN 리포지토리 생성 성공: {repo_path}")
        return make_response(jsonify({"code": 200, "status": "OK", "message": f"SVN 리포지토리 생성 완료: {repo_path}"}), 200)

    except subprocess.CalledProcessError as e:
        logging.error(f"svnadmin 명령 실패: {e}")
        return make_response(jsonify({"code": 500, "status": "ERROR", "message": "SVN 생성 실패"}), 500)

    except Exception as e:
        logging.error(f"예외 발생: {e}")
        return make_response(jsonify({"code": 500, "status": "ERROR", "message": "서버 내부 오류"}), 500)


def list_svn_repositories(repo_base_path="/srv/svn/repository", page_num=1, page_size=10):
    try:
        repos = sorted(
            [{"name": d} for d in os.listdir(repo_base_path) if os.path.isdir(os.path.join(repo_base_path, d))],
            key=lambda x: x["name"]
        )

        start_idx = (page_num - 1) * page_size
        end_idx = start_idx + page_size
        paged_repos = repos[start_idx:end_idx]

        logging.debug(f"리포지토리 목록 조회 성공 (총 {len(repos)}개 중 {len(paged_repos)}개 반환)")
        return make_response(jsonify({"code": 200, "status": "OK", "data": paged_repos}), 200)

    except FileNotFoundError:
        logging.warning(f"경로 없음: {repo_base_path}")
        return make_response(jsonify({"code": 404, "status": "ERROR", "message": f"경로 없음: {repo_base_path}"}), 404)

    except PermissionError:
        logging.warning(f"권한 거부됨: {repo_base_path}")
        return make_response(jsonify({"code": 403, "status": "ERROR", "message": f"권한 거부됨: {repo_base_path}"}), 403)

    except Exception as e:
        logging.error(f"리포지토리 목록 조회 중 오류 발생: {e}")
        return make_response(jsonify({"code": 500, "status": "ERROR", "message": "서버 내부 오류"}), 500)
