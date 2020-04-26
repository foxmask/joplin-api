import pytest
import re
from joplin_api import JoplinApi


@pytest.mark.asyncio
async def test_create_folder(get_token):
    joplin = JoplinApi(token=get_token)

    folder = 'TEST FOLDER1'
    assert type(folder) is str

    res = await joplin.create_folder(folder=folder)
    assert type(res.text) is str
    assert res.status_code == 200

    res = await joplin.delete_folder(res.json()['id'])
    assert res.status_code == 200


@pytest.mark.asyncio
async def test_delete_folder(get_token):
    joplin = JoplinApi(token=get_token)

    folder = 'TEST FOLDER1'
    assert type(folder) == str

    res = await joplin.create_folder(folder=folder)
    assert res.status_code == 200

    res = await joplin.delete_folder(res.json()['id'])
    assert res.status_code == 200


@pytest.mark.asyncio
async def test_get_folders(get_token):
    joplin = JoplinApi(token=get_token)

    res = await joplin.get_folders()
    print(res.json())
    assert type(res.json()) is list
    assert res.status_code == 200


@pytest.mark.asyncio
async def test_get_folder(get_token):
    joplin = JoplinApi(token=get_token)

    res = await joplin.create_folder(folder='MY FOLDER2')
    res = await joplin.get_folder(res.json()['id'])
    assert type(res.json()) is dict
    assert res.status_code == 200
    res = await joplin.delete_folder(res.json()['id'])
    assert res.status_code == 200


@pytest.mark.asyncio
async def test_create_note(get_token):
    joplin = JoplinApi(token=get_token)
    # 1 - create a folder
    res = await joplin.create_folder(folder='MY FOLDER3')
    data = res.json()
    parent_id = data['id']
    assert type(parent_id) is str
    # 2 - create a note with tag
    body = '# title 1\n ## subtitle \n ```python\npython --version\n```'
    assert type(body) is str
    kwargs = {'tags': 'tag1, tag2', 'id': '00a87474082744c1a8515da6aa5792d2'}
    assert 'id' in kwargs
    assert re.match('[a-z0-9]{32}', kwargs['id'])
    # let's set a user created time
    timestamp = 1545730073
    kwargs['user_created_time'] = timestamp
    res = await joplin.create_note(title="NOTE TEST", body=body,
                                   parent_id=parent_id, **kwargs)
    assert res.status_code == 200
    note_id = res.json()['id']

    note_user_created_time = res.json()['user_created_time']
    assert note_user_created_time == timestamp

    """
    # 3 - update a note with tag
    body = '# title 1\n ## subtitle \n ```python\npython --version\n```'
    assert type(body) is str
    # BUG : joplin does not update TAG yet
    # @TOFIX once fixed by Joplin
    kwargs = {'tags': 'tag1, tag2, tag11'}
    res = await joplin.update_note(note_id=note_id,
                                   body=body,
                                   title="NOTE TEST",
                                   parent_id=parent_id,
                                   **kwargs)
    assert res.status_code == 200
    """
    # drop the testing data
    # 4 - get the tag of that note
    tags_to_delete = await joplin.get_notes_tags(note_id)
    # 5 - delete the tags
    for line in tags_to_delete.json():
        await joplin.delete_tags_notes(line['id'], note_id)

    # delete note
    await joplin.delete_note(note_id)
    # delete folder
    await joplin.delete_folder(parent_id)


@pytest.mark.asyncio
async def test_create_note_no_body(get_token):
    joplin = JoplinApi(token=get_token)
    # 1 - create a folder
    res = await joplin.create_folder(folder='MY FOLDER3')
    data = res.json()
    parent_id = data['id']
    assert type(parent_id) is str
    # 2 - create a note with tag
    body = ''
    assert type(body) is str
    kwargs = {'tags': 'tag1, tag2', 'id': '00a87474082744c1a8515da6aa5792d2'}
    assert 'id' in kwargs
    assert re.match('[a-z0-9]{32}', kwargs['id'])
    # let's set a user created time
    timestamp = 1545730073
    kwargs['user_created_time'] = timestamp
    res = await joplin.create_note(title="NOTE TEST", body='',
                                   parent_id=parent_id, **kwargs)
    assert res.status_code == 200
    note_id = res.json()['id']

    note_user_created_time = res.json()['user_created_time']
    assert note_user_created_time == timestamp

    # drop the testing data
    # 4 - get the tag of that note
    tags_to_delete = await joplin.get_notes_tags(note_id)
    # 5 - delete the tags
    for line in tags_to_delete.json():
        await joplin.delete_tags_notes(line['id'], note_id)

    # delete note
    await joplin.delete_note(note_id)
    # delete folder
    await joplin.delete_folder(parent_id)


@pytest.mark.asyncio
async def test_get_notes(get_token):
    joplin = JoplinApi(token=get_token)

    res = await joplin.get_notes()
    assert type(res.json()) is list
    assert res.status_code == 200


@pytest.mark.asyncio
async def test_get_note(get_token):
    joplin = JoplinApi(token=get_token)
    res = await joplin.create_folder(folder='MY FOLDER4')
    data = res.json()
    parent_id = data['id']

    body = '# title 1\n ## subtitle \n ```python\npython --version\n```'
    res = await joplin.create_note(title="NOTE TEST2", body=body,
                                   parent_id=parent_id)
    data = res.json()
    note_id = data['id']

    assert type(note_id) is str
    res = await joplin.get_note(note_id)

    assert type(res.json()) is dict
    assert res.status_code == 200

    # drop the testing data
    await joplin.delete_note(note_id)
    await joplin.delete_folder(parent_id)


@pytest.mark.asyncio
async def test_get_tags(get_token):
    joplin = JoplinApi(token=get_token)

    res = await joplin.get_tags()

    assert type(res.json()) is list
    assert res.status_code == 200
