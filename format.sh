find ./app -name '*.py' -exec autopep8 --in-place '{}' \;
find ./tests -name '*.py' -exec autopep8 --in-place '{}' \;
