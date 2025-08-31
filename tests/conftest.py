import pytest
from main import AppControl
from tests.logs.logger_settings import logger


@pytest.fixture(scope="session")
def app_controller():
    controller = AppControl()
    try:
        yield controller

    finally:
        controller.stop_app()


@pytest.fixture(
    params=[
        {"host": "localhost", "port": 5843},  # С параметрами хоста и порта
        {}  # с значениями по умолчанию, то есть host="127.0.0.1", port=17678
    ],
    scope="session"
)
def app_settings(request):
    return request.param


@pytest.fixture(scope="session")
def running_app(app_controller, app_settings):
    host = app_settings.get("host", "127.0.0.1")
    port = app_settings.get("port", 17678)

    host_actual, port_actual = app_controller.take_host_part(host, port)

    yield host_actual, port_actual

    app_controller.stop_app()


@pytest.fixture(scope="session")
def app_runner(app_controller, test_logger):
    def _run_app(operation, app_settings=None):

        OPERATION_WITH_PARAMS = ["start"]
        OPERATION_WITHOUT_PARAMS = ["restart", "stop", "show_log"]

        if operation in OPERATION_WITHOUT_PARAMS:
            test_logger.debug(f"{operation.capitalize()} приложения")
            result = app_controller.run_app(operation)
            if operation == "stop":
                return result
            host, port = app_controller.parse_port_host(result.stdout)
        elif operation in OPERATION_WITH_PARAMS:
            if len(app_settings) == 0:
                test_logger.debug(f"{operation.capitalize()} без параметров")
                result = app_controller.run_app(operation)
                host, port = app_controller.parse_port_host(result.stdout)
            else:
                test_logger.debug(f"{operation.capitalize()} с параметрами")
                host = app_settings.get("host", "127.0.0.1")
                port = app_settings.get("port", 17678)
                result = app_controller.run_app(operation, host, port)
        else:
            raise Exception(f"Ошибка при операции {operation}")

        return result, host, port
    return _run_app


@pytest.fixture(scope="session")
def output_verify(test_logger):
    def _verify_output(result, expected_operation="веб-калькулятор запущен"):
        excepted_result = list(filter(lambda x: x != "", result.stdout.lower().split("\n")))[-1]
        if excepted_result.startswith(expected_operation):
            return True
        pytest.fail(f"Не найдена строка о : {expected_operation}")
    return _verify_output



@pytest.fixture(scope="session")
def test_logger():
    return logger
