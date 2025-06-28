from configparser import ConfigParser

URL_VAC = "https://api.hh.ru/vacancies"
URL_EMP = "https://api.hh.ru/employers"
HEADERS = {"User-Agent": "HH-User-Agent"}
PARAMS_VAC = {"page": 0, "per_page": 100, "employer_id": ""}
PARAMS_EMP = {"page": 0, "per_page": 100}
EMPLOYER_ID_KEY = "employer_id"
DATA_KEY = "items"
PAGE_KEY = "page"
NAME_KEY = "name"
LINK_KEY = "alternate_url"



SALARY_KEY = "salary"
FROM_SALARY_KEY = "from"
SNIPPET_KEY = "snippet"
REQUIREMENT_KEY = "requirement"
RESPONSIBILITY_KEY = "responsibility"
ID_KEY = "id"


def config(filename="database.ini", section="postgresql"):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section, filename))
    return db