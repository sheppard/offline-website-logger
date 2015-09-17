set -e
if [ "$LINT" ]; then
    flake8 owl tests --exclude migrations
    flake8 owl/migrations --ignore E501
else
    python setup.py test
fi
