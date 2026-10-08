"""Run from project root: python run_dashboard.py. Uses only the local venv."""
from pathlib import Path
import argparse
import os
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description='Install into the project venv and launch Dash')
    parser.add_argument('--port', type=int, default=8050)
    parser.add_argument('--check', action='store_true', help='Check dependencies without installing or starting')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    python = root / '.venv' / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
    if not python.exists():
        if args.check:
            print('Local .venv is missing.', file=sys.stderr)
            return 1
        result = subprocess.run([sys.executable, '-m', 'venv', str(root / '.venv')], cwd=root)
        if result.returncode:
            return result.returncode
    env = dict(os.environ, PYTHONIOENCODING='utf-8')
    probe = subprocess.run([str(python), '-c',
        'import dash, plotly, pandas; import sys; assert sys.prefix != sys.base_prefix'],
        cwd=root, env=env, capture_output=True, text=True, encoding='utf-8')
    if probe.returncode:
        if args.check:
            print('Dependencies are not ready in .venv:\n' + probe.stderr, file=sys.stderr)
            return 1
        print('Installing dashboard dependencies into .venv...', flush=True)
        result = subprocess.run([str(python), '-m', 'pip', '--isolated', 'install',
            '--index-url', 'https://pypi.org/simple', '--retries', '0', '--timeout', '15',
            '--disable-pip-version-check', '-r', str(root / '5. Dashboard/requirements.txt')], cwd=root, env=env)
        if result.returncode:
            print('Installation failed; dashboard was not started. See the pip error above.', file=sys.stderr)
            return result.returncode
    if args.check:
        print('Local venv dependencies are ready.')
        return 0
    return subprocess.run([str(python), str(root / '5. Dashboard/app.py'), '--port', str(args.port)],
                          cwd=root, env=env).returncode


if __name__ == '__main__':
    raise SystemExit(main())
