@echo off
echo 正在启动论文降重工具...

:: 检查并关闭占用5678端口的进程
for /f "tokens=5" %%a in ('netstat -aon ^| find ":5678"') do (
    echo 发现端口被占用，正在释放端口...
    taskkill /f /pid %%a
)

echo 请稍候，服务器启动中...
:: 等待1秒确保端口完全释放
timeout /t 1 /nobreak > nul

:: 获取本机IP地址
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| find "IPv4"') do (
    set ip=%%a
    goto :done
)
:done

echo.
echo === 论文降重工具启动信息 ===
echo 本机访问地址: http://127.0.0.1:5678
echo 局域网访问地址: http://%ip:~1%:5678
echo 注意：请确保防火墙允许其他电脑访问5678端口
echo ===========================
echo.

start http://127.0.0.1:5678
python app.py
pause 