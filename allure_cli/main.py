import sys

from cli import CLIService

if __name__ == "__main__":
    app = CLIService()
    arguments = app.get_parser_data(sys.argv[1:])
    app.upload_in_allure(arguments.project)
    app.do_build_report(arguments.project, arguments.type, arguments.build_name, arguments.build_url)
