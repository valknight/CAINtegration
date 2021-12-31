# -*- mode: python ; coding: utf-8 -*-
"""
Determine versioning using dulwich (pure python git implementation)
Fork of: https://gist.github.com/mikofski/e923750b415e4e4961b65a8eb42999e8
"""
# Generate version file

import datetime
import re
import sys
import time

from dulwich.repo import Repo

# CONSTANTS
PROJDIR = '.'
PATTERN = r'[ a-zA-Z_\-]*([\d\.]+[\-\w\.]*)'


def get_recent_tags(projdir=PROJDIR):
    """Get list of tags in order from newest to oldest and their datetimes.

    :param projdir: path to ``.git``
    :returns: list of tags sorted by commit time from newest to oldest

    Each tag in the list contains the tag name, commit time, commit id, author
    and any tag meta. If a tag isn't annotated, then its tag meta is ``None``.
    Otherwise the tag meta is a tuple containing the tag time, tag id and tag
    name. Time is in UTC.
    """
    with Repo(projdir) as project:  # dulwich repository object
        refs = project.get_refs()  # dictionary of refs and their SHA-1 values
        tags = {}  # empty dictionary to hold tags, commits and datetimes
        # iterate over refs in repository
        for key, value in refs.items():
            key = key.decode('utf-8')  # compatible with Python-3
            obj = project.get_object(value)  # dulwich object from SHA-1
            # don't just check if object is "tag" b/c it could be a "commit"
            # instead check if "tags" is in the ref-name
            if u'tags' not in key:
                # skip ref if not a tag
                continue
            # strip the leading text from refs to get "tag name"
            _, tag = key.rsplit(u'/', 1)
            # check if tag object is "commit" or "tag" pointing to a "commit"
            try:
                commit = obj.object  # a tuple (commit class, commit id)
            except AttributeError:
                commit = obj
                tag_meta = None
            else:
                tag_meta = (
                    datetime.datetime(*time.gmtime(obj.tag_time)[:6]),
                    obj.id.decode('utf-8'),
                    obj.name.decode('utf-8')
                )  # compatible with Python-3
                commit = project.get_object(commit[1])  # commit object
            # get tag commit datetime, but dulwich returns seconds since
            # beginning of epoch, so use Python time module to convert it to
            # timetuple then convert to datetime
            tags[tag] = commit.id.decode('utf-8')

    # return list of tags sorted by their datetimes from newest to oldest
    return sorted(tags.items(), key=lambda tag: tag[1][0], reverse=True)


def get_current_version(projdir=PROJDIR, pattern=PATTERN, logger=None):
    """Return the most recent tag, using an options regular expression pattern.

    The default pattern will strip any characters preceding the first semantic
    version. *EG*: "Release-0.2.1-rc.1" will be come "0.2.1-rc.1". If no match
    is found, then the most recent tag is return without modification.

    :param projdir: path to ``.git``
    :param pattern: regular expression pattern with group that matches version
    :param logger: a Python logging instance to capture exception
    :returns: tag matching first group in regular expression pattern
    """
    tags = get_recent_tags(projdir)
    r = Repo(projdir)
    current = r[r.head()]
    current = current.id.decode('utf-8')
    try:
        print(tags[0])
        latest_tag_hash = tags[0][1]
        latest_tag = tags[0][0]
    except IndexError:
        return current
    print(latest_tag)
    if latest_tag == current:
        matches = re.match(pattern, latest_tag)
        try:
            current_version = matches.group(1)
        except (IndexError, AttributeError) as err:
            if logger:
                logger.exception(err)
            return latest_tag
        return current_version
    else:
        return "git-{}".format(current)


version = get_current_version()
with open('VERSION', 'w') as f:
    f.write(version)

print("Version: {}".format(version))

# Begin build script
block_cipher = None
a = Analysis(['main.py'],
             pathex=[],
             binaries=[],
             datas=[('web', 'web'), ('config.example.json', '.'), ('../README.md', '.'), ('../VERSION', '.')],
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

os.remove('VERSION')