import os
import subprocess
import logging
from app.exceptions import ApiException
from app.utils.response_util import success_response

def create_svn_repository(repo_name, repo_base_path="/srv/svn/repository", config_path="/srv/svn/common/config/svnserve.conf"):
    if not repo_name:
        raise ApiException(400, "ERROR", "리포지토리 이름이 필요합니다.")

    repo_path = os.path.join(repo_base_path, repo_name)
    conf_file = os.path.join(repo_path, 'conf', 'svnserve.conf')

    if os.path.isdir(repo_path):
        raise ApiException(400, "ERROR", f"이미 존재하는 리포지토리: {repo_path}")

    try:
        subprocess.run(['svnadmin', 'create', repo_path], check=True)

        if os.path.isfile(conf_file):
            os.remove(conf_file)

        os.symlink(config_path, conf_file)

        logging.info(f"SVN 리포지토리 생성 성공: {repo_path}")
        return success_response(message=f"SVN 리포지토리 생성 완료: {repo_path}")

    except subprocess.CalledProcessError as e:
        logging.error(f"svnadmin 실패: {e}")
        raise ApiException(500, "ERROR", "SVN 생성 실패")

def list_svn_repositories(repo_base_path="/srv/svn/repository", page_num=1, page_size=10):
    try:
        repos = sorted(
            [{"name": d} for d in os.listdir(repo_base_path) if os.path.isdir(os.path.join(repo_base_path, d))],
            key=lambda x: x["name"]
        )

        start_idx = (page_num - 1) * page_size
        end_idx = start_idx + page_size
        paged_repos = repos[start_idx:end_idx]

        return success_response(data=paged_repos)

    except FileNotFoundError:
        raise ApiException(404, "ERROR", f"경로 없음: {repo_base_path}")
    except PermissionError:
        raise ApiException(403, "ERROR", f"권한 거부됨: {repo_base_path}")
    except Exception as e:
        logging.error(f"리포지토리 목록 오류: {e}")
        raise ApiException(500, "ERROR", "서버 내부 오류")
