import conf

def get():
    stype = conf.storage_type
    if stype == 'prefetch':
        from storage_prefetch import StoragePrefetch
        return StoragePrefetch()
    if stype == 'ml':
        from storage_ml import StorageML
        return StorageML()
    else:
        from storage_default import StorageDefault
        return StorageDefault()
