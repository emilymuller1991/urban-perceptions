import os
from pathlib import Path

import numpy as np
import torch
import torchvision.datasets as datasets
import torchvision.transforms as transforms
from torch.utils.data import DataLoader, Dataset, random_split
from torchvision.io import read_image

from .logger import logger

# def preprocessing(transform):
#     if transform == "resnet":
#         preprocess = transforms.Compose(
#             [
#                 transforms.Resize(256),
#                 transforms.CenterCrop(224),
#                 transforms.ToTensor(),
#                 transforms.Normalize(
#                     mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
#                 ),
#             ]
#         )
#         return preprocess
#     else:
#         # create custom transform for model
#         pass


def preprocessing(transform):
    if transform == "resnet":
        preprocess = transforms.Compose(
            [
                transforms.Lambda(
                    lambda image: torch.from_numpy(
                        np.array(image).astype(np.float64) / 255
                    )
                ),
                transforms.Resize(256),
                transforms.CenterCrop(224),
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


class CustomImageDataset(Dataset):
    """Creates a custom Image Dataset which will be loaded at
     each iteration through the dataloader

    Args:
        img_dir: pandas dataframe of image metadata
        root_dir: path to recode-perceptions repo
        transform: string for pretrained model preprocessing
        target_transform: processing of output label
    """

    def __init__(self, img_dir, root_dir="", transform="resnet", target_transform=None):
        self.img_dir = img_dir
        self.transform = preprocessing(transform)
        self.target_transform = target_transform
        self.root = root_dir

    def __len__(self):
        return self.img_dir.shape[0]

    def __getitem__(self, idx):
        img_path = self.img_dir.iloc[idx]["file"]  # locates filename for next image
        image = read_image(str(Path(self.root, img_path)))  # loads image to memory
        label = self.img_dir.iloc[idx]["trueskill.score_norm"]  # gets outcome label
        if self.transform:
            image = self.transform(image)
        if self.target_transform:
            label = self.target_transform(label)
        return (image, label)


def dataloader_pp(df, root_dir, data_dir, transform, split, params):
    """Takes dataframe as input
    and creates Dataset Iterator
    wrapped in dataloader"""
    dataset_iterator = CustomImageDataset(df, Path(root_dir, data_dir), transform)
    if dataset_iterator.__len__() == 0:
        dataloader = None
    else:
        dataloader = DataLoader(dataset_iterator, **params)
        print(
            "There are %s images in the %s DataLoader"
            % (str(dataloader.__len__() * params["batch_size"]), split)
        )
    return dataloader
