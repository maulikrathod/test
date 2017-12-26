# 1] Install Python-3.6.0
    https://www.python.org/downloads/

# 2] Install virtualenv
    # For Linux
        $ [sudo] pip install virtualenv
    # Windows
        PS C:\> pip install virtualenv

# 3] Create a virtualenv to isolate our package dependencies locally
    virtualenv env
    source env/bin/activate  # On Windows use `env\Scripts\activate.bat`

# 4] Install required modules
    pip install -r requirement.txt

# 5] run main script "sendEmailMain.py"
    python3 sendEmailMain.py
