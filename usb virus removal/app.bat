@echo off
setlocal EnableExtensions
color 0A
title USB Virus Removal Tool - Owner: GENERATIVE AI

echo =======================================================
echo     USB VIRUS REMOVAL TOOL
echo ___ Owner: GENERATIVE AI
echo =======================================================
echo.

:: Request USB drive letter
set /p drive=Enter USB Drive Letter (Example: E):
set "drive=%drive::=%"

:: Validate drive
if not exist "%drive%:\" (
    echo ERROR: Drive not found!
    pause
    exit /b
)

echo.
echo Target USB Drive: %drive%:
echo.

:: Confirm before making changes
set /p confirm=Continue with cleanup? (Y/N):
if /i not "%confirm%"=="Y" exit /b

echo.
echo Removing shortcut files...
del /a /f /q "%drive%:\*.lnk"

echo.
echo Removing autorun.inf...
attrib -h -r -s "%drive%:\autorun.inf" 2>nul
del /f /q "%drive%:\autorun.inf" 2>nul

echo.
echo Restoring hidden files...
attrib -h -r -s "%drive%:\*.*" /s /d

echo.
echo Cleanup completed.
echo.

:: Microsoft Defender scan
echo Starting Microsoft Defender scan...
powershell -NoProfile -Command ^
    "Start-MpScan -ScanType CustomScan -ScanPath '%drive%:\'"

echo.
echo USB cleanup and scan completed.
echo Check your files and scan results.
pause
```[cite: 1]