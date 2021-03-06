import httplib
import os
import argparse
import json
import urllib


# ss = [{"name": "abc", "scripts": ["script.sh", "abc"], "args": ["args"]}]

service_name_task_dispatch = "task-dispatch"
service_path_task_dispatch = "/v1/endpoint/%s/tasks"
service_name_files = "files"


def args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--consul-server", type=str, required=True,
                        help="consul server ip.")
    parser.add_argument("--consul-port", type=str, required=True,
                        help="consul server port.")
    parser.add_argument("--cache-location", type=str, required=True,
                        help="cache file location.")
    parser.add_argument("--endpoint-name", type=str, required=True,
                        help="endpoint name.")
    return parser.parse_args()


args = args()
consul_server = args.consul_server
consul_port = args.consul_port
cache_location = args.cache_location
endpoint_name = args.endpoint_name


def service_url(name):
    return "/v1/catalog/service/%s" % (name)


def check_script_usable(name, script):
    path = gen_script_location(name, script)
    return os.path.exists(path) and os.path.isfile(path)


def extract_service(name):
    path = service_url(name)
    service = http_client("GET", consul_server, consul_port, path)
    obj = json.loads(service)[0]
    return obj["ServiceAddress"], obj["ServicePort"]


def http_client(method, host, port, url):
    conn = httplib.HTTPConnection(host, port, timeout=10)
    if method.upper() == "GET":
        conn.request("GET", url)
    elif method.upper() == "POST":
        headers = {"Content-type": "application/json"}
        conn.request("POST", url, headers)
    else:
        raise BaseException("method: %s no support.")
    res = conn.getresponse()
    if res.status == 200:
        data = res.read()
    conn.close()
    return data


def download_file(name, script):
    f_addr, f_port = extract_service(service_name_files)
    path = os.path.join(name, script)
    url = "http://%s:%s/files/scripts/%s" % (f_addr, f_port, path)
    location = gen_script_location(name, script)
    urllib.urlretrieve(url, location)


def gen_script_url_path(name, script):
    return os.path.join("os", name, script)


def make_dirs(dirs_path):
    if not os.path.exists(dirs_path):
        os.makedirs(dirs_path)


def gen_script_location(name, script):
    file_path = os.path.join(cache_location, name, script)
    make_dirs("/".join(file_path.split("/")[:-1][1:]))
    return file_path


def put_task_result(t_name, t_result):
    td_addr, td_port = extract_service(service_name_task_dispatch)
    http_client("POST", td_addr, td_port, t_result)
    return 1


def request_tasks():
    td_addr, td_port = extract_service(service_name_task_dispatch)
    path = service_path_task_dispatch % endpoint_name
    return http_client("GET", td_addr, td_port, path)


def main():
    tasks = request_tasks()
    for task in json.loads(tasks):
        task_name = task["task_name"]
        task_scripts = json.loads(task["task_scripts"])
        task_args = task["task_args"]
        for script in json.loads(task_scripts):
            if not check_script_usable(task_name, script):
                download_file(task_name, script)
#            result = os.system()
#            put_task_result(task_name, result)


if __name__ == "__main__":
    main()
