from classes.calculator import Calculator
from classes.bbox import Bbox
from classes.calculator2 import Calculator2
from classes.drawer import Drawer
from classes.entity import Entity
from classes.identity import Identity
from classes.mask import Mask
from classes.ts_detection import TorchscriptDetection
from config.config import DEEPSORT, DETECTRON2, DISPLAY, NUM_CLASSES, USE_CUDA
from deep_sort import DeepSort
from classes.measurement import Measurement


class Detector(object):
    def __init__(self):
        # self.class_names = ['strong', 'sick', 'stone']
        self.class_names = ['strong', 'alternariosis', 'anthracnose', 'fomosis', 'fusarium', 'internalrot',
                            'necrosis', 'phytophthorosis', 'pinkrot', 'scab', 'wetrot']
        use_cuda = USE_CUDA
        self.display = DISPLAY
        self.detectron2 = TorchscriptDetection(
            DETECTRON2,
            use_cuda=use_cuda
        )

        self.deepsort = DeepSort(DEEPSORT, max_dist=0.9, min_confidence=0.9, use_cuda=use_cuda, num_classes=NUM_CLASSES)
        self.drawer = Drawer().add_bbox(Bbox()).add_identity(Identity()).add_entity(Entity()).add_mask(
            Mask(
            )
        ).add_measurement(
            Measurement(3840, 120, 0.4)
        ) \
            .add_calculator(Calculator2([['small', 0.0, 0.035], ['middle', 0.035, 0.08], ['big', 0.08, 1.0]])) \
            .add_class_names(self.class_names)

    def detect(self, image):
        """
        Detection objects from image
        Parameters:
        ----------
            image: np.array - image

        Returns:
        -------
            image: np.array - image with detected objects

        """
        class_sorted = {}
        item_sorted = {}
        bbox_xcycwh, cls_conf, cls_ids, masks = self.detectron2.detect(image, confidence=0.8)
        # print(f'len(cls_ids)={len(cls_ids)}, len(cls_conf)={len(cls_conf)}, len(masks)={len(masks)}')
        print(f'cls_ids={cls_ids}')

        if len(bbox_xcycwh) > 0:
            # select class person
            # mask = cls_ids == 0
            #
            # bbox_xcycwh = bbox_xcycwh[mask]
            # bbox_xcycwh[:, 3:] *= 1.2
            #
            # cls_conf = cls_conf[mask]
            outputs = self.deepsort.update(bbox_xcycwh, cls_conf, image, cls_ids, masks)
            # print(f'outputs={outputs}')
            if len(outputs) > 0:
                image, item_sorted, class_sorted = self.drawer.outputs(image, outputs)
                # print(f'item_sorted={item_sorted}')


        return image, item_sorted, class_sorted
