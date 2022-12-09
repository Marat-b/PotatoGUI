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
    def save_providers(providers):
        provider = ';'.join(item['name'] for item in providers)
        OptionService.update_option('provider', provider)

    @staticmethod
    def get_providers():
        providers_ret = []
        provider = OptionService.get_option('provider')
        if provider is not None:
            providers = provider.Value.split(';')
            if type(providers) is list:
                providers_ret = providers if len(providers) > 0 else []
            else:
                providers_ret = [providers]
        return providers_ret

    @staticmethod
    def save_recipient(recipient):
        OptionService.update_option('recipient', recipient)

    @staticmethod
    def get_recipient():
        recipient = OptionService.get_option('recipient')
        return recipient.Value if recipient is not None else None

    @staticmethod
    def save_address(item):
        OptionService.update_option('address', item)

    @staticmethod
    def get_address():
        item = OptionService.get_option('address')
        return item.Value if item is not None else ''