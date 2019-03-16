# -*- mode: python -*-

block_cipher = None

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

added_files = [('C:\\Users\\marij\\Dropbox\\Wageningen\\ACT\\Toolkit_Work\\v2\\Logo.png', '.'), ('C:\\Users\\marij\\Dropbox\\Wageningen\\ACT\\Toolkit_Work\\v2\\watermark.png', '.'), ('C:\\Users\\marij\\Dropbox\\Wageningen\\ACT\\Toolkit_Work\\v2\\Manual.pdf', '.'),]

a = Analysis(['GUI.py', 'reportlab_report.py', 'updated_function.py'],
             pathex=['C:\\Users\\marij\\Dropbox\\Wageningen\\ACT\\Toolkit_Work\\v2'],
             binaries=[],
             datas = added_files, 
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

def get_pandas_path():
    import pandas
    pandas_path = pandas.__path__[0]
    return pandas_path             
             
dict_tree = Tree(get_pandas_path(), prefix='pandas', excludes=["*.pyc"])
a.datas += dict_tree
a.binaries = filter(lambda x: 'pandas' not in x[0], a.binaries)

def get_reportlab_path():
    import reportlab
    reportlab_path = reportlab.__path__[0]
    return reportlab_path             
             
dict_tree = Tree(get_reportlab_path(), prefix='reportlab', excludes=["*.pyc"])
a.datas += dict_tree
a.binaries = filter(lambda x: 'reportlab' not in x[0], a.binaries)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='SATAlytics',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False , 
          icon='LogoIco.ico')