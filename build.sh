#!/url/bin/env bash
set -o errexit

pop install -r requirements.txt

python mnage.py collectstatic --no-input
python manage.py migrate
