import numpy as np
import json

file_name = "all_apps.json"


def get_random_names(num_apps):
    all_apps = get_all_apps()
    titles = []
    for i in range(num_apps):
        index = np.random.randint(len(all_apps))
        app = all_apps[index]
        titles.append(app["title"])
    return titles


def get_all_apps():
    f = open(file_name, 'r')
    return json.loads(f.read())


if __name__ == "__main__":
    np.random.seed(10)
    num_apps = 100
    app_names = get_random_names(num_apps)
    print(app_names)
