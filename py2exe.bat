if exist dist (del /f /s /q dist)
:: 需安装 pyinstaller: pip install -U pyinstaller
pyinstaller -F -c --distpath .\dist\TencentMeetingHelper -n TencentMeetingHelper main.py
copy config.example.yaml .\dist\TencentMeetingHelper\config.yaml
mkdir .\dist\TencentMeetingHelper\pic
copy pic .\dist\TencentMeetingHelper\pic
:: 需安装 7-Zip 并将其路径添加到环境变量 Path
7z a .\dist\TencentMeetingHelper.7z .\dist\TencentMeetingHelper