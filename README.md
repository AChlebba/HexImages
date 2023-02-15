# HexImages

## Setup

Fastest setup with docker:

```
docker pull adam343/hexrepository:heximages
docker run --publish 8000:8000 adam343/hexrepository:heximages
```

Setup from git repo:
```
git clone https://github.com/AChlebba/HexImages.git
cd HexImages
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
python manage.py runserver
```

App is listening on http://127.0.0.1:8000/ address
