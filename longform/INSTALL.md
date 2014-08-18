# Install the dependencies

    sudo apt-get update && sudo apt-get install python-dev libxml2-dev libxslt1-dev

    virtualenv --no-site-packages venv
    source venv/bin/activate
    pip install -r requirements.txt

# Make some modifications to the template

    vim templates/longform.html

# Generate the page

    python generate.py
    python generate.py -c
    python generate.py -h

    python generate.py >| output.html

# Run the server

    python -m SimpleHTTPServer

and go to your web browser at <http://localhost:8000/output.html>


# Tip: generate the code to include the content from the wiki

Go visit the wiki page, open the javascript console and type:

    $('h2 span.mw-headline').each(function() {
        console.log('{% mwinclude "Titre de la page en question" "' + $(this).attr('id') + '" %}')
    });

It will output the code to include in the template
