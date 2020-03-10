# import requests
from pathlib import Path

import pytest
import json
from joplin_api import JoplinApi


@pytest.mark.asyncio
async def test_get_resources(get_token):

    joplin = JoplinApi(token=get_token)

    res = await joplin.get_resources()
    assert res.status_code == 200


@pytest.mark.asyncio
async def test_create_get_update_delete_download_resource(get_token):

    joplin = JoplinApi(token=get_token)
    properties = {'title': 'test resource'}

    assert 'title' in properties

    here = Path(__file__).parent

    file_name = here / 'cactus.png'
    res = await joplin.create_resource(file_name, **properties)
    resource_id = json.loads(res.text)['id']

    assert res.status_code == 200

    res = await joplin.get_resource(resource_id)
    assert res.status_code == 200

    properties = {'title': 'test update resource'}
    file_name = here / 'update_cactus.png'
    res = await joplin.update_resources(resource_id, **properties)
    assert res.status_code == 200

    res = await joplin.download_resources(resource_id)
    assert res.status_code == 200

    res = await joplin.delete_resources(resource_id)
    assert res.status_code == 200
