from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import torch.utils.data as data
from glob import glob

from torchvision import transforms as vision_transforms

import transforms
import common


VALIDATE_INDICES = [
    5, 17, 42, 45, 58, 62, 96, 111, 117, 120, 121, 131, 132,
    152, 160, 248, 263, 264, 291, 293, 295, 299, 316, 320, 336,
    337, 343, 358, 399, 401, 429, 438, 468, 476, 494, 509, 528,
    531, 572, 581, 583, 588, 593, 681, 688, 696, 714, 767, 786,
    810, 825, 836, 841, 883, 917, 937, 942, 970, 974, 980, 1016,
    1043, 1064, 1118, 1121, 1133, 1153, 1155, 1158, 1159, 1173,
    1187, 1219, 1237, 1238, 1259, 1266, 1278, 1296, 1354, 1378,
    1387, 1494, 1508, 1518, 1574, 1601, 1614, 1668, 1673, 1699,
    1712, 1714, 1737, 1841, 1872, 1879, 1901, 1921, 1934, 1961,
    1967, 1978, 2018, 2030, 2039, 2043, 2061, 2113, 2204, 2216,
    2236, 2250, 2274, 2292, 2310, 2342, 2359, 2374, 2382, 2399,
    2415, 2419, 2483, 2502, 2504, 2576, 2589, 2590, 2622, 2624,
    2636, 2651, 2655, 2658, 2659, 2664, 2672, 2706, 2707, 2709,
    2725, 2732, 2761, 2827, 2864, 2866, 2905, 2922, 2929, 2966,
    2972, 2993, 3010, 3025, 3031, 3040, 3041, 3070, 3113, 3124,
    3129, 3137, 3141, 3157, 3183, 3206, 3219, 3247, 3253, 3272,
    3276, 3321, 3328, 3333, 3338, 3341, 3346, 3351, 3396, 3419,
    3430, 3433, 3448, 3455, 3463, 3503, 3526, 3529, 3537, 3555,
    3577, 3584, 3591, 3594, 3597, 3603, 3613, 3615, 3670, 3676,
    3678, 3697, 3723, 3728, 3734, 3745, 3750, 3752, 3779, 3782,
    3813, 3817, 3819, 3854, 3885, 3944, 3947, 3970, 3985, 4011,
    4022, 4071, 4075, 4132, 4158, 4167, 4190, 4194, 4207, 4246,
    4249, 4298, 4307, 4317, 4318, 4319, 4320, 4382, 4399, 4401,
    4407, 4416, 4423, 4484, 4491, 4493, 4517, 4525, 4538, 4578,
    4606, 4609, 4620, 4623, 4637, 4646, 4662, 4668, 4716, 4739,
    4747, 4770, 4774, 4776, 4785, 4800, 4845, 4863, 4891, 4904,
    4922, 4925, 4956, 4963, 4964, 4994, 5011, 5019, 5036, 5038,
    5041, 5055, 5118, 5122, 5130, 5162, 5164, 5178, 5196, 5227,
    5266, 5270, 5273, 5279, 5299, 5310, 5314, 5363, 5375, 5384,
    5393, 5414, 5417, 5433, 5448, 5494, 5505, 5509, 5525, 5566,
    5581, 5602, 5609, 5620, 5653, 5670, 5678, 5690, 5700, 5703,
    5724, 5752, 5765, 5803, 5811, 5860, 5881, 5895, 5912, 5915,
    5940, 5952, 5966, 5977, 5988, 6007, 6037, 6061, 6069, 6080,
    6111, 6127, 6146, 6161, 6166, 6168, 6178, 6182, 6190, 6220,
    6235, 6253, 6270, 6343, 6372, 6379, 6410, 6411, 6442, 6453,
    6481, 6498, 6500, 6509, 6532, 6541, 6543, 6560, 6576, 6580,
    6594, 6595, 6609, 6625, 6629, 6644, 6658, 6673, 6680, 6698,
    6699, 6702, 6705, 6741, 6759, 6785, 6792, 6794, 6809, 6810,
    6830, 6838, 6869, 6871, 6889, 6925, 6995, 7003, 7026, 7029,
    7080, 7082, 7097, 7102, 7116, 7165, 7200, 7232, 7271, 7282,
    7324, 7333, 7335, 7372, 7387, 7407, 7472, 7474, 7482, 7489,
    7499, 7516, 7533, 7536, 7566, 7620, 7654, 7691, 7704, 7722,
    7746, 7750, 7773, 7806, 7821, 7827, 7851, 7873, 7880, 7884,
    7904, 7912, 7948, 7964, 7965, 7984, 7989, 7992, 8035, 8050,
    8074, 8091, 8094, 8113, 8116, 8151, 8159, 8171, 8179, 8194,
    8195, 8239, 8263, 8290, 8295, 8312, 8367, 8374, 8387, 8407,
    8437, 8439, 8518, 8556, 8588, 8597, 8601, 8651, 8657, 8723,
    8759, 8763, 8785, 8802, 8813, 8826, 8854, 8856, 8866, 8918,
    8922, 8923, 8932, 8958, 8967, 9003, 9018, 9078, 9095, 9104,
    9112, 9129, 9147, 9170, 9171, 9197, 9200, 9249, 9253, 9270,
    9282, 9288, 9295, 9321, 9323, 9324, 9347, 9399, 9403, 9417,
    9426, 9427, 9439, 9468, 9486, 9496, 9511, 9516, 9518, 9529,
    9557, 9563, 9564, 9584, 9586, 9591, 9599, 9600, 9601, 9632,
    9654, 9667, 9678, 9696, 9716, 9723, 9740, 9820, 9824, 9825,
    9828, 9863, 9866, 9868, 9889, 9929, 9938, 9953, 9967, 10019,
    10020, 10025, 10059, 10111, 10118, 10125, 10174, 10194,
    10201, 10202, 10220, 10221, 10226, 10242, 10250, 10276,
    10295, 10302, 10305, 10327, 10351, 10360, 10369, 10393,
    10407, 10438, 10455, 10463, 10465, 10470, 10478, 10503,
    10508, 10509, 10809, 11080, 11331, 11607, 11610, 11864,
    12390, 12393, 12396, 12399, 12671, 12921, 12930, 13178,
    13453, 13717, 14499, 14517, 14775, 15297, 15556, 15834,
    15839, 16126, 16127, 16386, 16633, 16644, 16651, 17166,
    17169, 17958, 17959, 17962, 18224, 21176, 21180, 21190,
    21802, 21803, 21806, 22584, 22857, 22858, 22866]


class FlyingChairs(data.Dataset):
    def __init__(self,
                 args,
                 root,
                 photometric_augmentations=False,
                 resize_targets=[-1, -1],
                 num_examples=-1,
                 dstype="train"):

        self._args = args
        self._resize_targets = resize_targets

        # -------------------------------------------------------------
        # filenames for all input images and target flows
        # -------------------------------------------------------------
        image_filenames = sorted(glob(os.path.join(root, "*.ppm")))
        flow_filenames = sorted(glob(os.path.join(root, "*.flo")))
        assert (len(image_filenames)/2 == len(flow_filenames))
        num_flows = len(flow_filenames)

        # -------------------------------------------------------------
        # Remove invalid validation indices
        # -------------------------------------------------------------
        validate_indices = [
            x for x in VALIDATE_INDICES if x in range(num_flows)]

        # ----------------------------------------------------------
        # Construct list of indices for training/validation
        # ----------------------------------------------------------
        list_of_indices = None
        if dstype == "train":
            list_of_indices = [x for x in range(
                num_flows) if x not in validate_indices]
        elif dstype == "valid":
            list_of_indices = validate_indices
        elif dstype == "full":
            list_of_indices = range(num_flows)
        else:
            raise ValueError("FlyingChairs: dstype '%s' unknown!", dstype)

        # ----------------------------------------------------------
        # Restrict dataset indices if num_examples is given
        # ----------------------------------------------------------
        if num_examples > 0:
            restricted_indices = common.deterministic_indices(
                seed=0, k=num_examples, n=len(list_of_indices))
            list_of_indices = [list_of_indices[i] for i in restricted_indices]

        # ----------------------------------------------------------
        # Save list of actual filenames for inputs and flows
        # ----------------------------------------------------------
        self._image_list = []
        self._flow_list = []
        for i in list_of_indices:
            flo = flow_filenames[i]
            im1 = image_filenames[2*i]
            im2 = image_filenames[2*i + 1]
            self._image_list += [[im1, im2]]
            self._flow_list += [flo]
        self._size = len(self._image_list)
        assert len(self._image_list) == len(self._flow_list)

        # ----------------------------------------------------------
        # photometric_augmentations
        # ----------------------------------------------------------
        if photometric_augmentations:
            self._photometric_transform = transforms.ConcatTransformSplitChainer([
                # uint8 -> PIL
                vision_transforms.ToPILImage(),
                # PIL -> PIL : random hsv and contrast
                vision_transforms.ColorJitter(
                    brightness=0.5, contrast=0.5, saturation=0.5, hue=0.5),
                # PIL -> FloatTensor
                vision_transforms.transforms.ToTensor(),
                transforms.RandomGamma(
                    min_gamma=0.7, max_gamma=1.5, clip_image=True),
            ], from_numpy=True, to_numpy=False)

        else:
            self._photometric_transform = transforms.ConcatTransformSplitChainer([
                # uint8 -> FloatTensor
                vision_transforms.transforms.ToTensor(),
            ], from_numpy=True, to_numpy=False)

    def __getitem__(self, index):
        index = index % self._size

        im1_filename = self._image_list[index][0]
        im2_filename = self._image_list[index][1]
        flo_filename = self._flow_list[index]

        # read float32 images and flow
        im1_np0 = common.read_image_as_byte(im1_filename)
        im2_np0 = common.read_image_as_byte(im2_filename)
        flo_np0 = common.read_flo_as_float32(flo_filename)

        # possibly apply photometric transformations
        im1, im2 = self._photometric_transform(im1_np0, im2_np0)

        # import numpy as np
        # from matplotlib import pyplot as plt
        # import numpy as np
        # plt.figure()
        # im1_np = im1.numpy().transpose([1,2,0])
        # im2_np = im2.numpy().transpose([1,2,0])
        # plt.imshow(np.concatenate((im1_np0.astype(np.float32)/255.0, im2_np0.astype(np.float32)/255.0, im1_np, im2_np), 1))
        # plt.show(block=True)

        # convert flow to FloatTensor
        flo = common.numpy2torch(flo_np0)

        # example filename
        basename = os.path.basename(im1_filename)[:5]

        example_dict = {
            "input1": im1,
            "input2": im2,
            "target1": flo,
            "index": index,
            "basename": basename
        }

        return example_dict

    def __len__(self):
        return self._size


class FlyingChairsTrain(FlyingChairs):
    def __init__(self,
                 args,
                 root,
                 photometric_augmentations=True,
                 num_examples=-1):
        super(FlyingChairsTrain, self).__init__(
            args,
            root=root,
            photometric_augmentations=photometric_augmentations,
            dstype="train",
            num_examples=num_examples)


class FlyingChairsValid(FlyingChairs):
    def __init__(self,
                 args,
                 root,
                 photometric_augmentations=False,
                 num_examples=-1):
        super(FlyingChairsValid, self).__init__(
            args,
            root=root,
            photometric_augmentations=photometric_augmentations,
            dstype="valid",
            num_examples=num_examples)


class FlyingChairsFull(FlyingChairs):
    def __init__(self,
                 args,
                 root,
                 photometric_augmentations=False,
                 num_examples=-1):
        super(FlyingChairsValid, self).__init__(
            args,
            root=root,
            photometric_augmentations=photometric_augmentations,
            dstype="full",
            num_examples=num_examples)
