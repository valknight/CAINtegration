# -*- mode: python ; coding: utf-8 -*-
import subprocess
import os

block_cipher = None

# TODO: Put versioning here
p = subprocess.run(['git', 'describe', '--exact-match', 'HEAD'], capture_output=True)
print("status code:", p.returncode)
if p.returncode == 0:
    version = p.stdout.decode('utf-8')
else:
    p = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True)
    version = p.stdout.decode('utf-8')
    version = "git-{}".format(version)
version = version.replace("\n", "")
print("Version: {}".format(version))
with open('version', 'w') as f:
    f.write(version)
a = Analysis(['main.py'],
             pathex=[],
             binaries=[],
             datas=[('web', 'web'), ('config.example.json', '.'), ('../README.md', '.'), ('../version', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts, 
          [],
          exclude_binaries=True,
          name='CustomAudioIntegration',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='CustomAudioIntegration')

os.remove('version')