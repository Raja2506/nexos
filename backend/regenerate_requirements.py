from pathlib import Path
from subprocess import run, PIPE
base = Path(__file__).resolve().parent
pip_exe = base / 'venv' / 'Scripts' / 'pip.exe'
req_file = base / 'requirements.txt'
if not pip_exe.exists():
    raise FileNotFoundError(f'pip executable not found at {pip_exe}')
print('using pip at', pip_exe)
result = run([str(pip_exe), 'freeze'], stdout=PIPE, stderr=PIPE, text=True)
if result.returncode != 0:
    print('ERROR', result.stderr)
    raise SystemExit(result.returncode)
req_file.write_text(result.stdout, encoding='utf-8')
print('wrote', req_file)
print('preview:', repr(result.stdout[:400]))
