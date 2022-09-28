from pathlib import Path

import numpy as np
import torch
import torchvision.transforms as transforms
from torch.utils.data import DataLoader, Dataset
from torchvision.io import read_image

from .logger import logger


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
        image = read_image(
            str(Path(self.root, "images", img_path))
        )  # loads image to memory
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
        logger.info(
            "There are %s images in the %s DataLoader"
            % (str(dataloader.__len__() * params["batch_size"]), split)
        )
    return dataloader
