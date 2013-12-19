./manage.py migrate --db-dry-run --verbosity=2 | perl -ne 'print if s/^\s*=\s(.*)\[\]$/$1/'
