import os

import numpy as np
import torch
import torchvision.datasets as datasets
import torchvision.transforms as transforms
from torch.utils.data import DataLoader, random_split

from .logger import logger


def preprocessing(transform):
    if transform == "resnet":
        preprocess = transforms.Compose(
            [
                transforms.Resize(256),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
                ),
            ]
        )
        return preprocess
    else:
        # create custom transform for model
        pass


def dataloader(data_dir, root_dir, transform, split, params, val_split=0.2):
    """Creates dataloader from
    train, val data folders"""

    dir = os.path.join(root_dir, data_dir, split)

    # get normalisation
    preprocess = preprocessing(transform)

    if os.path.isdir(dir):
        # Data loading
        if val_split > 0 and split == "train":
            data_iterator = datasets.ImageFolder(dir, preprocess)
            L = len(data_iterator)
            train_it, val_it = random_split(
                data_iterator,
                [int(np.floor((1 - val_split) * L)), int(np.ceil(val_split * L))],
                generator=torch.Generator().manual_seed(42),
            )
            loader = DataLoader(train_it, **params)
            val_loader = DataLoader(val_it, **params)
            logger.info(
                "There are %s images in the %s DataLoader"
                % (str(loader.__len__() * params["batch_size"]), split)
            )
            logger.info(
                "There are %s images in the %s DataLoader"
                % (str(val_loader.__len__() * params["batch_size"]), "val")
            )
            classes = len(os.listdir(dir))
        else:
            data_iterator = datasets.ImageFolder(dir, preprocess)
            loader = DataLoader(data_iterator, **params)
            logger.info(
                "There are %s images in the %s DataLoader"
                % (str(loader.__len__() * params["batch_size"]), split)
            )
            classes = len(os.listdir(dir))
            val_loader = None
    else:
        loader = None
        val_loader = None
        classes = None
    return loader, val_loader, classes
