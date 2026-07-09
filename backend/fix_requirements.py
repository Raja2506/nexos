from pathlib import Path
import subprocess
base = Path(__file__).resolve().parent
venv_pip = base / 'venv' / 'Scripts' / 'pip.exe'
req_file = base / 'requirements.txt'
if not venv_pip.exists():
    raise FileNotFoundError(f'pip executable not found at {venv_pip}')
print('Using', venv_pip)
with req_file.open('wb') as f:
    subprocess.run([str(venv_pip), 'freeze'], stdout=f, check=True)
print('Wrote', req_file)
text = req_file.read_text('utf-8')
print('HEAD 200 chars:', repr(text[:200]))
