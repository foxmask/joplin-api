import pytest
from joplin_api import JoplinApi


@pytest.mark.asyncio
async def test_create_tag(get_token):
    """
    Create and delete a new tag
    :param get_token:
    :return:
    """
    
    joplin = JoplinApi(token=get_token)

    title = 'TEST TAG1'

    res = await joplin.create_tag(title=title)
    assert type(res.text) is str
    assert res.status_code == 200
    
    res = await joplin.delete_tag(res.json()['id'])
    assert res.status_code == 200



@pytest.mark.asyncio
async def test_add_tag(get_token):
    """
    Add tag to a note and remove it
    :param get_token:
    :return:
    """
    
    joplin = JoplinApi(token=get_token)

    # 1 - create a folder
    res = await joplin.create_folder(folder='MY FOLDER')
    assert res.status_code == 200
    data = res.json()
    parent_id = data['id']

    # 2 - create a note
    body = '# title 1\n ## subtitle \n ```python\npython --version\n```'
    res = await joplin.create_note(title="NOTE TEST", body=body,
                                   parent_id=parent_id)
    assert res.status_code == 200
    note_id = res.json()['id']

    # 3 - create a tag
    title = 'TEST TAG2'
    res = await joplin.create_tag(title=title)
    assert res.status_code == 200
    tag_id = res.json()['id']

    # 4 - add tag to Note
    res = await joplin.create_tags_notes(note_id=note_id, tag=tag_id)
    assert res.status_code == 200


    # drop the testing data
    # delete tag
    await joplin.delete_tag(tag_id)
    # delete note
    await joplin.delete_note(note_id)
    # delete folder
    await joplin.delete_folder(parent_id)
    
