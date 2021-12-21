def Sync(store_id):
    """Standalone syncer DB<>source"""
    # 1. load all entry[store_id] into dict[uid: (id, body)]
    # 2. load all from connections into [uid: (path, body)]
    # 3. Compare
    ...
