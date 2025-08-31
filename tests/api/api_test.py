import pytest

URL_BASE = "/api/"
pytest_plugins = [
    "tests.fixtures"
]


# ПОЗИТИВНЫЕ ТЕСТЫ + ПРОВЕРКА НА ПРАВИЛЬНЫЙ РЕЗУЛЬТАТ
@pytest.mark.asyncio
@pytest.mark.positive
async def test_state(api_client, api_base_url, test_logger):
    try:
        response = await api_client.get(f"{api_base_url}state", timeout=5)
        confirm_response = {'statusCode': 0, 'state': 'OК'}
        assert response.json() == confirm_response
        assert response.status_code == 200

    except AssertionError as e:
        test_logger.error(f"❌ AssertionError: {e}")
        test_logger.exception("Подробности ошибки:")
        raise

    except Exception as e:
        test_logger.error(f"❌ Ошибка в тесте: {e}")
        test_logger.exception("Подробности ошибки:")


@pytest.mark.asyncio
@pytest.mark.positive
async def test_addition_with_positive_random_numbers(api_client, api_base_url, get_random_numbers_to_request,
                                                     test_logger):
    try:
        response = await api_client.post(f"{api_base_url}addition", json=get_random_numbers_to_request, timeout=5)
        expected_result = int((x := get_random_numbers_to_request.get("x")) +
                              (y := get_random_numbers_to_request.get("y")))
        confirm_response = {"statusCode": 0, "result": expected_result}

        test_logger.info("🎯 Начало теста сложения")
        test_logger.debug(f"📊 Входные данные: x={x}, y={y}")
        test_logger.debug(f"🧮 Ожидаемый результат: {expected_result}")

        assert response.json() == confirm_response
        assert response.status_code == 200
        test_logger.info(f"✅ Результат корректен: {x} + {y} = {expected_result}")

    except AssertionError as e:
        test_logger.error(f"❌ AssertionError: {e}")
        test_logger.exception("Подробности ошибки:")
        raise

    except Exception as e:
        test_logger.error(f"❌ Ошибка в тесте: {e}")
        test_logger.exception("Подробности ошибки:")


@pytest.mark.asyncio
@pytest.mark.positive
async def test_multiplication_positive_random_numbers(api_client, api_base_url, get_random_numbers_to_request,
                                                      test_logger):
    try:
        response = await api_client.post(f"{api_base_url}multiplication", json=get_random_numbers_to_request, timeout=5)
        expected_result = int((x := get_random_numbers_to_request.get("x")) *
                              (y := get_random_numbers_to_request.get("y")))
        confirm_response = {"statusCode": 0, "result": expected_result}

        test_logger.info("🎯 Начало теста умножения")
        test_logger.debug(f"📊 Входные данные: x={x}, y={y}")
        test_logger.debug(f"🧮 Ожидаемый результат: {expected_result}")

        assert response.json() == confirm_response
        assert response.status_code == 200

        test_logger.info(f"✅ Результат корректен: {x} * {y} = {expected_result}")

    except AssertionError as e:
        test_logger.error(f"❌ AssertionError: {e}")
        test_logger.exception("Подробности ошибки:")
        raise

    except Exception as e:
        test_logger.error(f"❌ Ошибка в тесте: {e}")
        test_logger.exception("Подробности ошибки:")


@pytest.mark.asyncio
@pytest.mark.positive
async def test_division_positive_random_numbers(api_client, api_base_url, get_random_numbers_to_request,
                                                test_logger):
    try:
        response = await api_client.post(f"{api_base_url}division", json=get_random_numbers_to_request, timeout=5)
        expected_result = int((x := get_random_numbers_to_request.get("x")) //
                              (y := get_random_numbers_to_request.get("y")))
        confirm_response = {"statusCode": 0, "result": expected_result}

        test_logger.info("🎯 Начало теста деления без остатка")
        test_logger.debug(f"📊 Входные данные: x={x}, y={y}")
        test_logger.debug(f"🧮 Ожидаемый результат: {expected_result}")

        assert response.json() == confirm_response
        assert response.status_code == 200
        test_logger.info(f"✅ Результат корректен: {x} // {y} = {expected_result}")

    except AssertionError as e:
        test_logger.error(f"❌ AssertionError: {e}")
        test_logger.exception("Подробности ошибки:")
        raise

    except Exception as e:
        test_logger.error(f"❌ Ошибка в тесте: {e}")
        test_logger.exception("Подробности ошибки:")


@pytest.mark.asyncio
@pytest.mark.positive
async def test_remainder_positive_random_numbers(api_client, api_base_url, get_random_numbers_to_request,
                                                 test_logger):
    try:
        response = await api_client.post(f"{api_base_url}remainder", json=get_random_numbers_to_request, timeout=5)
        expected_result = int((x := get_random_numbers_to_request.get("x")) %
                              (y := get_random_numbers_to_request.get("y")))
        confirm_response = {"statusCode": 0, "result": expected_result}

        test_logger.info("🎯 Начало деления с остатком")
        test_logger.debug(f"📊 Входные данные: x={x}, y={y}")
        test_logger.debug(f"🧮 Ожидаемый результат: {expected_result}")

        assert response.json() == confirm_response
        assert response.status_code == 200
        test_logger.info(f"✅ Результат корректен: {x} % {y} = {expected_result}")

    except AssertionError as e:
        test_logger.error(f"❌ AssertionError: {e}")
        test_logger.exception("Подробности ошибки:")
        raise

    except Exception as e:
        test_logger.error(f"❌ Ошибка в тесте: {e}")
        test_logger.exception("Подробности ошибки:")


@pytest.mark.asyncio
@pytest.mark.positive
@pytest.mark.parametrize("operation", ["addition", "multiplication", "division", "remainder"])
async def test_with_negative_values(api_client, api_base_url, operation, get_negative_numbers,
                                    test_logger):
    try:
        response = await api_client.post(
            f"{api_base_url}{operation}",
            json=get_negative_numbers,
            timeout=5
        )
        expected_status = 0
        response_data = response.json()

        assert response_data.get("statusCode") == expected_status  # ОЖИДАЕТСЯ СТАТУС 1

    except AssertionError as e:
        test_logger.error(f"❌ AssertionError: {e}")
        test_logger.exception("Подробности ошибки:")
        raise

    except Exception as e:
        test_logger.error(f"❌ Ошибка в тесте: {e}")
        test_logger.exception("Подробности ошибки:")


# НЕГАТИВНЫЕ ТЕСТЫ

@pytest.mark.asyncio
@pytest.mark.negative
@pytest.mark.parametrize("operation", ["addition", "multiplication", "division", "remainder"])
async def test_negative_keys(api_client, api_base_url, operation, get_incorrect_keys,
                             test_logger):
    try:
        response = await api_client.post(
            f"{api_base_url}{operation}",
            json=get_incorrect_keys,
            timeout=5
        )

        expected_status = 0
        response_data = response.json()

        assert response_data.get("statusCode") == expected_status  # ОЖИДАЕТСЯ СТАТУС 2

    except AssertionError as e:
        test_logger.error(f"❌ AssertionError: {e}")
        test_logger.exception("Подробности ошибки:")
        raise

    except Exception as e:
        test_logger.error(f"❌ Ошибка в тесте: {e}")
        test_logger.exception("Подробности ошибки:")


@pytest.mark.asyncio
@pytest.mark.negative
@pytest.mark.parametrize("urls", ["states", "additions", "multiplications", "divisions", "remainders"])
async def test_negative_urls(api_client, api_base_url, urls, test_logger):
    try:
        response = await api_client.get(f"{api_base_url}{urls}", timeout=5)
        expected_status = 0
        response_data = response.json()

        assert response_data.get("statusCode") == expected_status  # ОЖИДАЕТСЯ СТАТУС 5

    except AssertionError as e:
        test_logger.error(f"❌ AssertionError: {e}")
        test_logger.exception("Подробности ошибки:")
        raise

    except Exception as e:
        test_logger.error(f"❌ Ошибка в тесте: {e}")
        test_logger.exception("Подробности ошибки:")


@pytest.mark.asyncio
@pytest.mark.negative
@pytest.mark.parametrize("operation", ["addition", "multiplication", "division", "remainder"])
async def test_negative_largest_numbers(api_client, api_base_url, operation, get_largest_numbers,
                                        test_logger):
    try:
        response = await api_client.post(
            f"{api_base_url}{operation}",
            json=get_largest_numbers,
            timeout=5
        )
        expected_status = 0
        response_data = response.json()

        assert response_data.get("statusCode") == expected_status  # ОЖИДАЕТСЯ СТАТУС 4

    except AssertionError as e:
        test_logger.error(f"❌ AssertionError: {e}")
        test_logger.exception("Подробности ошибки:")
        raise

    except Exception as e:
        test_logger.error(f"❌ Ошибка в тесте: {e}")
        test_logger.exception("Подробности ошибки:")


@pytest.mark.asyncio
@pytest.mark.negative
@pytest.mark.parametrize("operation", ["addition", "multiplication", "division", "remainder"])
@pytest.mark.parametrize(
    "incorrect_number", [1.1, "gfdgfd", (12, 13), [12, 14]]
)
async def test_with_incorrect_numbers(api_client, api_base_url, operation,
                                      get_random_numbers_to_request, incorrect_number,
                                      test_logger):
    test_data = get_random_numbers_to_request.copy()
    test_data["x"] = incorrect_number

    try:
        response = await api_client.post(
            f"{api_base_url}{operation}",
            json=test_data,
            timeout=5
        )
        expected_status = 0
        response_data = response.json()

        assert response_data.get("statusCode") == expected_status  # ОЖИДАЕТСЯ СТАТУС 3

    except AssertionError as e:
        test_logger.error(f"❌ AssertionError: {e}")
        test_logger.exception("Подробности ошибки:")
        raise

    except Exception as e:
        test_logger.error(f"❌ Ошибка в тесте: {e}")
        test_logger.exception("Подробности ошибки:")


@pytest.mark.asyncio
@pytest.mark.negative
async def test_division_on_zero_value(api_client, api_base_url, get_zero_to_division,
                                      test_logger):
    try:
        response = await api_client.post(f"{api_base_url}division", json=get_zero_to_division, timeout=5)
        expected_status = 0
        response_data = response.json()

        assert response_data.get("statusCode") == expected_status  # ОЖИДАЕТСЯ СТАТУС 1

    except AssertionError as e:
        test_logger.error(f"❌ AssertionError: {e}")
        test_logger.exception("Подробности ошибки:")
        raise

    except Exception as e:
        test_logger.error(f"❌ Ошибка в тесте: {e}")
        test_logger.exception("Подробности ошибки:")
