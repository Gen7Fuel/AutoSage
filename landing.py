# Third-party library imports
import streamlit.components.v1 as components


def main():
    html_code = "<!DOCTYPE html>"
    html_code += "<html>"
    html_code += "<header>"
    # html_code += get_text_content_from_file("styles.html")
    html_code += "</header>"
    html_code += "<body>"
    # html_code += get_text_content_from_file("welcome_body.html")
    # html_code += get_text_content_from_file("app_introduction.html")
    # html_code += get_text_content_from_file("what_we_do.html")
    html_code += "</body>"
    html_code += "</html>"

    components.html(html_code, height=4000)


def get_text_content_from_file(file_name):
    path = f"assets/html/{file_name}"
    file = open(path, "r", encoding="utf-8")
    file_content = file.read()

    return file_content