from db.services.option_service import OptionService


class ConfigService:
    @staticmethod
    def get_video_path() -> str:
        video_path = OptionService.get_option('video_path')
        return video_path.Value if video_path is not None else './'

    @staticmethod
    def save_video_path(video_path):
        OptionService.update_option('video_path', video_path)

    @staticmethod
    def get_video_height() -> int:
        video_height = OptionService.get_option('video_height')
        return int(video_height.Value) if video_height is not None else 600

    @staticmethod
    def save_video_height(video_height):
        OptionService.update_option('video_height', video_height)

    @staticmethod
    def get_video_width() -> int:
        video_width = OptionService.get_option('video_width')
        return int(video_width.Value) if video_width is not None else 600

    @staticmethod
    def save_video_width(video_width):
        OptionService.update_option('video_width', video_width)