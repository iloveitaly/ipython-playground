from ipython_playground.extras import get_default_module_imports


def test_get_default_module_imports_includes_typing_and_pydantic():
    imports = get_default_module_imports()

    # Check typing
    typing_import = next((i for i in imports if i["module"] == "typing"), None)
    assert typing_import is not None
    assert typing_import["alias"] == "t"
    assert any(ei["import"] == "List" for ei in typing_import["extra_imports"])
    assert any(ei["import"] == "Any" for ei in typing_import["extra_imports"])
    assert any(ei["import"] == "Optional" for ei in typing_import["extra_imports"])
    assert any(ei["import"] == "Dict" for ei in typing_import["extra_imports"])
    assert any(ei["import"] == "Union" for ei in typing_import["extra_imports"])
    assert any(ei["import"] == "TypeVar" for ei in typing_import["extra_imports"])

    # Check pydantic
    pydantic_import = next((i for i in imports if i["module"] == "pydantic"), None)
    assert pydantic_import is not None
    assert any(ei["import"] == "TypeAdapter" for ei in pydantic_import["extra_imports"])
