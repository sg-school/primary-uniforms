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
echo 1. 验证和更新现有学校数据
echo 2. 添加新学校并更新校服图片
echo 3. 退出
echo ==================================================

echo 请选择要执行的操作 (1-3):
set /p choice=

if %choice%==1 (
echo 正在验证和更新现有学校数据...
python scrape_school_uniforms.py
if %errorlevel% neq 0 (
echo 处理过程中出现错误！
)
pause
cls
goto MENU
)

if %choice%==2 (
echo 正在添加新学校并更新校服图片...
python update_uniform_images.py
if %errorlevel% neq 0 (
echo 处理过程中出现错误！
)
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