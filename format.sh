find ./app -name '*.py' -exec autopep8 --in-place --aggressive --aggressive '{}' \;
find ./tests -name '*.py' -exec autopep8 --in-place --aggressive --aggressive '{}' \;
