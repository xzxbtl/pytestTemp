import pytest


@pytest.mark.integration
def test_start_app(app_runner, output_verify, app_settings, app_controller, test_logger):
    app_controller.stop_app()
    result, host, port = app_runner("start", app_settings)
    assert result.returncode == 0
    output_verify(result, "веб-калькулятор запущен")
    test_logger.info(f"✅ Запуск успешен: {host}:{port}")
    app_controller.stop_app()


@pytest.mark.integration
def test_restart_app(app_runner, output_verify, app_settings, app_controller, test_logger):
    app_controller.stop_app()

    start_result, start_host, start_port = app_runner("start", app_settings)
    assert start_result.returncode == 0
    output_verify(start_result, "веб-калькулятор запущен")

    test_logger.debug(f"Первоначально запущено на {start_host}:{start_port}")

    restart_result, restart_host, restart_port = app_runner("restart")
    assert restart_result.returncode == 0
    output_verify(restart_result, "веб-калькулятор запущен")

    assert start_host == restart_host
    assert start_port == restart_port

    test_logger.info(f"✅ Перезапуск успешен: {restart_host}:{restart_port}")
    app_controller.stop_app()


@pytest.mark.integration
def test_stop_app(app_runner, output_verify, app_settings, app_controller, test_logger):
    app_controller.stop_app()

    start_result, start_host, start_port = app_runner("start", app_settings)
    assert start_result.returncode == 0
    output_verify(start_result, "веб-калькулятор запущен")

    stop_result = app_runner("stop")
    output_verify(stop_result, "веб-калькулятор остановлен")
    test_logger.info(f"✅ Успешная остановка приложения")
    app_controller.stop_app()
