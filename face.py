from PIL import Image
from .modules import devices, logger as loggerUtil, imageUtils
import dlib
import os
import cv2
import numpy as np
import torch

logger = loggerUtil.logger

predictor_path = './models/shape_predictor_68_face_landmarks.dat'
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_path)

def get_landmark(im):
    rects = detector(im, 1)
    if len(rects) > 1:
        raise Exception('TooManyFaces')
    if len(rects) == 0:
        raise Exception('NoFaces')
    return np.matrix([[p.x, p.y] for p in predictor(im, rects[0]).parts()])

def transformation_from_points(points1, points2):
    points1 = points1.astype(np.float64)
    points2 = points2.astype(np.float64)

    c1 = np.mean(points1, axis=0)
    c2 = np.mean(points2, axis=0)
    points1 -= c1
    points2 -= c2

    s1 = np.std(points1)
    s2 = np.std(points2)
    points1 /= s1
    points2 /= s2

    U, S, Vt = np.linalg.svd(points1.T * points2)
    R = (U * Vt).T

    return np.vstack([np.hstack(((s2 / s1) * R,
                                 c2.T - (s2 / s1) * R * c1.T)),
                      np.matrix([0., 0., 1.])])


def warp_im(im, M_, dshape):
    output_im = np.zeros(dshape, dtype=im.dtype)
    cv2.warpAffine(im,
                   M_[:2],
                   (dshape[1], dshape[0]),
                   dst=output_im,
                   borderMode=cv2.BORDER_TRANSPARENT,
                   flags=cv2.WARP_INVERSE_MAP)
    return output_im


def warp_im1(im, M_, dshape):
    output_im = np.zeros(dshape, dtype=im.dtype)
    cv2.warpAffine(im,
                   M_[:2],
                   (dshape[1], dshape[0]),
                   dst=output_im,
                   borderValue=(1, 1, 1),
                   flags=cv2.WARP_INVERSE_MAP)
    return output_im

class FaceAlign:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image1": ("IMAGE",),
                "image2": ("IMAGE",),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "generate"

    CATEGORY = "utils"

    def generate(self, image1, image2):
        image = imageUtils.tensor2pil(image)
        mask = imageUtils.tensor2pil(mask)

        
        
        output_image = imageUtils.pil2comfy(output_image)
        return (torch.cat([output_image], dim=0),)
