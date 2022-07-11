# imports
import os
import requests
from flask import Flask
from flask_restful import Api, request
import time

from app.api import Schools, ExtractGrades, GetGradesOptions

app = Flask(__name__)
api = Api(app)


@app.route('/new_release', methods=['POST'])
def json_example():
    try:
        s_time = time.time()

        url, apk_name = "", ""
        request_json = request.get_json()

        if request_json["action"] == "published":

            for i in request_json["release"]["assets"]:
                if i["content_type"] == "application/vnd.android.package-archive":
                    url = i["browser_download_url"]
                    apk_name = i["name"]

            download_apk = requests.get(url, stream=True)

            with open(apk_name, "wb") as fb:
                for chunk in download_apk.iter_content(chunk_size=1024):
                    fb.write(chunk)

            release_notes = f'<b>Доступна новая версия приложения: </b><i>{request_json["release"]["tag_name"]}</i>\n\n{request_json["release"]["body"]}\n\n<a href="{url}">Скачать</a>'

            with open(apk_name, "rb") as f:
                request.post(
                    "https://api.telegram.org/bot1950280557:AAFr-Zp_6q3KKu8pUfsD491sEcuKgNtA5HE/sendDocument", 
                    files={'document': (apk_name, f)}, 
                    data={"chat_id": 401311369, "caption": release_notes, "parse_mode": "HTML"}
                )
            os.remove(apk_name)

        return str(time.time() - s_time)
    except BaseException as e:
        return str(e)


# sync route and class
api.add_resource(Schools, '/schools')
api.add_resource(ExtractGrades, "/extract_grades")
api.add_resource(GetGradesOptions, "/grades_options")

if __name__ == '__main__':
    app.run()
