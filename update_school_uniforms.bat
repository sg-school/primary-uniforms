@echo off
chcp 65001 > nul

:: 新加坡小学校服图片更新脚本
:: 此批处理文件用于运行校服图片更新工具

:: 检查Python是否已安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
echo 错误: 未找到Python。请先安装Python并添加到系统环境变量中。
pause
exit /b 1
)

:: 检查pip是否可用
pip --version >nul 2>&1
if %errorlevel% neq 0 (
echo 错误: 未找到pip。请安装pip或更新Python。
pause
exit /b 1
)

:: 安装必要的Python库
echo 正在安装必要的Python库...
pip install -r requirements.txt --upgrade

if %errorlevel% neq 0 (
echo 警告: 某些库可能安装失败，程序可能无法正常运行。
)

cls

:: 显示菜单
:MENU
echo ==================================================
echo          新加坡小学校服图片更新工具
echo ==================================================
echo 1. 验证当前学校资料与图片完整性
echo 2. 打开 schools.json 进行手动更新
echo 3. 退出
echo ==================================================

echo 请选择要执行的操作 (1-3):
set /p choice=

if %choice%==1 (
echo 正在验证当前学校资料与图片...
python -c "import json,os,sys; d=json.load(open('schools.json',encoding='utf-8')); missing=[s.get('uniformImage','') for s in d if not os.path.exists(s.get('uniformImage',''))]; print('学校总数:',len(d)); print('缺失图片:',len(missing)); [print(' -',m) for m in missing[:20]]; sys.exit(1 if missing else 0)"
if %errorlevel% neq 0 (
echo 校验未通过，请检查 schools.json 或图片目录。
pause
) else (
echo 校验通过：资料与图片路径完整。
)
pause
cls
goto MENU
)

if %choice%==2 (
echo 即将打开 schools.json，请手动更新资料后重新执行选项 1 进行校验...
start "" notepad schools.json
pause
cls
goto MENU
)

if %choice%==3 (
echo 感谢使用新加坡小学校服图片更新工具，再见！
pause
exit /b 0
)

:: 无效选择
echo 无效的选择，请重新输入。
pause
cls
goto MENU
