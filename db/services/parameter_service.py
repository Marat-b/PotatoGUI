from db.services.option_service import OptionService


class ParameterService:

    @staticmethod
    def save_cards(cars):
        print(f"cars['brand']={cars}")
        # car_brand = ';'.join(map(str, cars['brand']))
        car_brand = ';'.join(item['brand'] for item in cars )
        OptionService.update_option('car_brand', car_brand)

    @staticmethod
    def get_cards():
        brands = []
        models = []
        car_brand = OptionService.get_option('car_brand')
        if car_brand is not None:
            car_brands = car_brand.Value.split(';')
            if type(car_brands) is list:
                brands = car_brands if len(car_brands) > 0 else []
            else:
                brands = [car_brands]
        car_model = OptionService.get_option('car_model')
        if car_model is not None:
            car_models = car_brand.Value.split(';')
            if type(car_models) is list:
                models = car_models if len(car_models) > 0 else []
            else:
                models = [car_models]
        return brands, models