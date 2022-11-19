import sys
sys.path.append('../')

from classes.bbox import Bbox
from classes.drawer_depth import Drawer
from classes.entity import Entity
from classes.identity import Identity
from classes.mask import Mask
from config.config import DEEPSORT, DETECTRON2, DISPLAY, NUM_CLASSES, USE_CUDA
from deep_sort import DeepSort
from classes.calculator2 import Calculator2
from classes.measurement_depth import Measurement
from classes.ts_detection import TorchscriptDetection


class Detector(object):
    def __init__(self):
        self.class_names = ['strong', 'rot']
        # self.class_names = ['strong', 'alternariosis', 'anthracnose', 'fomosis', 'fusarium', 'internalrot',
        #                     'necrosis', 'phytophthorosis', 'pinkrot', 'scab', 'wetrot']
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
            Measurement(1280, 72)
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
        bbox_xcycwh, cls_conf, cls_ids, masks = self.detectron2.detect(image[:, :, :-1])
        # print(f'len(cls_ids)={len(cls_ids)}, len(cls_conf)={len(cls_conf)}, len(masks)={len(masks)}')

        if len(bbox_xcycwh) > 0:
            outputs = self.deepsort.update(bbox_xcycwh, cls_conf, image[:, :, :-1], cls_ids, masks)
            # print(f'outputs={outputs}')
            if len(outputs) > 0:
                image, item_sorted, class_sorted = self.drawer.outputs(image, outputs)
                print(f'len(outputs)={len(outputs)}')

        return image, item_sorted, class_sorted
