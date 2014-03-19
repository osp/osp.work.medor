# Install the dependencies

    sudo apt-get update && sudo apt-get install python-dev libxml2-dev libxslt1-dev

    virtualenv --no-site-packages venv
    source venv/bin/activate
    pip install -r requirements.txt

# Make some modifications to the template

    vim templates/longform.html

# Geneate the page

    python generate.py
    python generate.py -c
    python generate.py -h

    python generate.py >| output.html
