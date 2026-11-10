import os
import sys
import subprocess

def create_desktop_shortcut():
    desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
    shortcut_path = os.path.join(desktop, 'Alpha_Doc Suite.lnk')
    python_dir = os.path.dirname(sys.executable)
    pythonw = os.path.join(python_dir, 'pythonw.exe')
    if not os.path.exists(pythonw):
        pythonw = sys.executable

    main_py = os.path.abspath(os.path.join(os.path.dirname(__file__), 'main.py'))
    work_dir = os.path.dirname(main_py)
    icon_path = os.path.abspath(os.path.join(work_dir, 'assets', 'app_icon.ico'))

    vbs_content = f'''Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = "{shortcut_path}"
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = "{pythonw}"
oLink.Arguments = """{main_py}"""
oLink.WorkingDirectory = "{work_dir}"
oLink.IconLocation = "{icon_path},0"
oLink.Description = "Alpha_Doc Suite"
oLink.Save
'''
    vbs_path = os.path.join(work_dir, '_temp_shortcut.vbs')
    with open(vbs_path, 'w', encoding='utf-8') as f:
        f.write(vbs_content)

    try:
        subprocess.run(['cscript.exe', '//Nologo', vbs_path], check=True)
        print(f"Shortcut successfully created at: {shortcut_path}")
    finally:
        if os.path.exists(vbs_path):
            os.remove(vbs_path)

if __name__ == "__main__":
    create_desktop_shortcut()

