import asyncio
import re
import subprocess
import sys

APP_PATH = r"webcalculator.exe"


class AppControl:
    def __init__(self):
        self.appPath = APP_PATH

    def run_app(self, *args):
        "Запуск приложения с произвольным хостом и портом"
        params = [str(arg) for arg in args]
        res = subprocess.run(
            [self.appPath] + params,
            capture_output=True,
            text=True,
            timeout=30
        )
        return res

    def parse_port_host(self, output):
        "Парсим хост и порт из ответа"
        pattern = r'(\S+):(\d+)'
        match = re.search(pattern, output)
        if match:
            return match.group(1), int(match.group(2))
        return None, None

    def take_host_part(self, host, port):
        "Запуск приложения + перезапуск если запущен для получения порта и хоста"
        result = self.run_app("start", host, port)

        if result and "сервер уже запущен" in result.stdout.lower():
            result = self.restart_app()

        host, port = self.parse_port_host(result.stdout)
        return host, port

    def stop_app(self):
        result = self.run_app("stop")
        return list(filter(lambda x: x != "", result.stdout.lower().split("\n")))[-1]

    def restart_app(self):
        result = self.run_app("restart")
        return list(filter(lambda x: x != "", result.stdout.lower().split("\n")))[-1]


async def run_tests():
    print("🚀 Тесты начаты")

    process = await asyncio.create_subprocess_exec(
        "pytest", "-v",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    async def read_stream(stream, stream_type):
        while True:
            line = await stream.readline()
            if not line:
                break
            if stream_type == "stdout":
                print(line.decode().rstrip())
            else:
                print("STDERR:", line.decode().rstrip(), file=sys.stderr)

    await asyncio.gather(
        read_stream(process.stdout, "stdout"),
        read_stream(process.stderr, "stderr")
    )

    return_code = await process.wait()
    print(f"✅ Тесты завершены с кодом: {return_code}")
    return return_code


if __name__ == '__main__':
    exit_code = asyncio.run(run_tests())
    sys.exit(exit_code)
