# Joplin Api

![Joplin API](https://scrutinizer-ci.com/g/foxmask/joplin-api/badges/quality-score.png?b=master "joplin-api")

The API of [Joplin Editor](https://joplinapp.org/) in Python 3.6+

## requirements

* python 3.6+
* [httpx](https://github.com/encode/httpx)

## Installation 

```
git clone  https://github.com/foxmask/joplin-api
cd joplin-api 
pip install -e .
```

## Using Joplin API

Have a look at `tests/test_folder.py` and `test/test_ping.py` 

### basically
```python
import asyncio
from joplin_api import JoplinApi
joplin = JoplinApi(token='my token')

async def ping_me():
    await joplin.ping()

loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(ping_me())
finally:
    loop.close()

```
### create a folder
```python
import asyncio
from joplin_api import JoplinApi
joplin = JoplinApi(token='my token')

async def new_folder():
    folder = 'TEST FOLDER1'
    res = await joplin.create_folder(folder=folder)

loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(new_folder())
finally:
    loop.close()
``` 
### create a note
```python
import asyncio
from joplin_api import JoplinApi
joplin = JoplinApi(token='my token')

async def new_note(get_token):
    # 1 - create a folder
    res = await joplin.create_folder(folder='MY FOLDER')
    data = res.json()
    parent_id = data['id']
    # 2 - create a note with tag
    body = '# title 1\n ## subtitle \n ```python\npython --version\n```'
    assert type(body) is str
    kwargs = {'tags': 'tag1, tag2'}
    await joplin.create_note(title="MY NOTE", body=body,
                             parent_id=parent_id, **kwargs)

loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(new_note())
finally:
    loop.close()
```

### Python 3.7

with python 3.7 replace
```python
loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(new_note())
finally:
    loop.close()
``` 
by
```python
asyncio.run(new_note())
``` 


## Tests

install pytest by 
```
pip install -r requirements-dev.txt
```
then, before starting the Unit Test, you will need to set the Token line 10 of tests/conftest.py file

and run
```bash
pytest
``` 

