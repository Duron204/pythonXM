@echo off
cd /d "%~dp0"
git reset --soft cd21184
git rm --cached "病虫害/homeobjects-3K.zip"
git add -A
git commit -m "first commit"
git push -u origin main
echo Done!
pause
