class tylemap:
    def __init__(self, tile_size=16): #Tamaño de cada tile en pixeles, usamos 16x16
        self.tile_size = tile_size
        self.tilemap = {} #Diccionario que almacenará los tiles organizados por posición en la cuadricula (sólidos)
        self.offgrid_tiles = []  #Lista para tiles, esto es para la decoración y elementos sueltos

        for i in range(10):
            self.tilemap[str(3 + i) + ';10'] = {'type': 'grass', 'variant': 1, 'pos': (3 + i, 10)}
            self.tilemap[';10' + str(5 + i)] = {'type': 'stone', 'variant': 1, 'pos': (10 + i, 5)}
    
    
