import conf

__model = None

def load():
    global __model

    import keras.models
    __model = keras.models.load_model(conf.path_model)

def predict(accbmp):
    inputs = get_pred_inputs(accbmp)
    sv_read, sv_write = __model.predict([[inputs]])
    return sv_read[0].tolist(), sv_write[0].tolist()

def get_pred_inputs(accbmp):
    if conf.model_type == 'cnn':
        return accbmp.bitmap()

    bmp = []
    for b in accbmp.bitmap():
        bmp += b
    return bmp

