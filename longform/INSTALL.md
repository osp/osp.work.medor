# Install the dependencies

    virtualenv2 --no-site-packages venv
    source venv/bin/activate
    pip install -r requirements.txt

# Make some modifications to the template

    vim templates/longform.html

# Geneate the page

    python generate.py
    python generate.py -c
    python generate.py -h

    python generate.py >| output.html
