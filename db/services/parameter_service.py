from db.services.option_service import OptionService


class ParameterService:

    @staticmethod
    def save_cars(cars):
        # print(f"cars['brand']={cars}")
        # car_brand = ';'.join(map(str, cars['brand']))
        car_brand = ';'.join(item['brand'] for item in cars )
        OptionService.update_option('car_brand', car_brand)
        car_model = ';'.join(item['model'] for item in cars)
        OptionService.update_option('car_model', car_model)
        car_gosnumber = ';'.join(item['gosnumber'] for item in cars)
        OptionService.update_option('car_gosnumber', car_gosnumber)

    @staticmethod
    def get_cars():
        brands = []
        models = []
        gosnumbers = []
        car_brand = OptionService.get_option('car_brand')
        if car_brand is not None:
            car_brands = car_brand.Value.split(';')
            if type(car_brands) is list:
                brands = car_brands if len(car_brands) > 0 else []
            else:
                brands = [car_brands]
        car_model = OptionService.get_option('car_model')
        if car_model is not None:
            car_models = car_model.Value.split(';')
            if type(car_models) is list:
                models = car_models if len(car_models) > 0 else []
            else:
                models = [car_models]
        car_gosnumber = OptionService.get_option('car_gosnumber')
        if car_gosnumber is not None:
            car_gosnumbers = car_gosnumber.Value.split(';')
            if type(car_gosnumbers) is list:
                gosnumbers = car_gosnumbers if len(car_gosnumbers) > 0 else []
            else:
                gosnumbers = [car_gosnumbers]
        return brands, models, gosnumbers

    @staticmethod
    def save_nomenclatures(nomenclatures):
        print(f"nomenclatures['name']={nomenclatures}")
        # car_brand = ';'.join(map(str, cars['brand']))
        nomenclature = ';'.join(item['name'] for item in nomenclatures)
        OptionService.update_option('nomenclature', nomenclature)

    @staticmethod
    def get_nomenclatures():
        nomenclatures_ret = []
        nomenclature = OptionService.get_option('nomenclature')
        if nomenclature is not None:
            nomenclatures = nomenclature.Value.split(';')
            if type(nomenclatures) is list:
                nomenclatures_ret = nomenclatures if len(nomenclatures) > 0 else []
            else:
                nomenclatures_ret = [nomenclatures]
        return nomenclatures_ret

    @staticmethod
    def save_recipients(recipients):
        recipient  = ';'.join(item['name'] for item in recipients)
        OptionService.update_option('recipient', recipient)

    @staticmethod
    def get_recipients():
        recipients_ret = []
        recipient = OptionService.get_option('recipient')
        if recipient is not None:
            recipients = recipient.Value.split(';')
            if type(recipients) is list:
                recipients_ret = recipients if len(recipients) > 0 else []
            else:
                recipients_ret = [recipients]
        return recipients_ret