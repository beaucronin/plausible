import plausible as pbl

KEY = "test_key.txt"
TEXT = "The quick brown fox jumped over the lazy dog"

obj_store = pbl.resource.object_store.obj

try:
    s = obj_store.get_string(KEY)
except Exception as e:
    assert isinstance(e, pbl.ItemNotFoundException)
obj_store.put(KEY, TEXT)
s = obj_store.get_string(KEY)
assert s == TEXT
obj_store.delete(KEY)
try:
    s = obj_store.get_string(KEY)
except Exception as e:
    assert isinstance(e, pbl.ItemNotFoundException)