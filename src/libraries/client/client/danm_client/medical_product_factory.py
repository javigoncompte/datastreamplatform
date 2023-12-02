class MedicalProductFactory:
    @staticmethod
    def create_product(id, nombreComercial, Activo, FECHA_INSCRIPCION, noregistro, nombre_comercial, estatus, formula, principio_activo, concentracion, NOMBRE_FORMA_FARMACEUTICA, laboratorio, precio_nivel, precio_rango, precio_presentacion_min, precio_presentacion_max, precios_rango):
        return MedicalProduct(id, nombreComercial, Activo, FECHA_INSCRIPCION, noregistro, nombre_comercial, estatus, formula, principio_activo, concentracion, NOMBRE_FORMA_FARMACEUTICA, laboratorio, precio_nivel, precio_rango, precio_presentacion_min, precio_presentacion_max, precios_rango)



class MedicalProduct:
    def __init__(self, id, nombreComercial, Activo, FECHA_INSCRIPCION, noregistro, nombre_comercial, estatus, formula, principio_activo, concentracion, NOMBRE_FORMA_FARMACEUTICA, laboratorio, precio_nivel, precio_rango, precio_presentacion_min, precio_presentacion_max, precios_rango):
        self.danm_id = id
        self.commercial_name = nombreComercial
        self.active = Activo
        self.inscription_date = FECHA_INSCRIPCION
        self.registry_number = noregistro
        self.nombre_comercial_second = nombre_comercial
        self.status = estatus
        self.formula = formula
        self.active_ingredient = principio_activo
        self.concentration = concentracion
        self.pharmaceutical_form_name = NOMBRE_FORMA_FARMACEUTICA
        self.pharmaceutical_company = laboratorio
        self.level_price = precio_nivel
        self.range_price = precio_rango
        self.minimum_price_presentation = precio_presentacion_min
        self.maximum_price_presentation = precio_presentacion_max
        self.rage_price = precios_rango