import pytest
from joplin_api import JoplinApi


@pytest.mark.asyncio
async def test_search(get_token):
    """
    grab receipt in all note
    :param get_token:
    :return:
    """
    joplin = JoplinApi(token=get_token)
    query = "recette"
    search = await joplin.search(query)
    assert type(search.text) is str
    assert search.status_code == 200


@pytest.mark.asyncio
async def test_search_folder(get_token):
    """
    checkout a folder named 'database'
    :param get_token:
    :return:
    """
    joplin = JoplinApi(token=get_token)
    query = "database"
    item_type = 'folder'
    search = await joplin.search(query, item_type)
    assert type(search.text) is str
    assert search.status_code == 200


@pytest.mark.asyncio
async def test_search_tag(get_token):
    """
    checkout a tag named 'git*'
    :param get_token:
    :return:
    """
    joplin = JoplinApi(token=get_token)
    query = "git*"
    item_type = 'tag'
    search = await joplin.search(query, item_type)
    assert type(search.text) is str
    assert search.status_code == 200


@pytest.mark.asyncio
async def test_search_limited_returned_field(get_token):
    """
    grab receipt in all note
    :param get_token:
    :return:
    """
    joplin = JoplinApi(token=get_token)
    query = "recette"
    search = await joplin.search(query, item_type='note', field_restrictions='title')
    assert type(search.text) is str
    assert search.status_code == 200
