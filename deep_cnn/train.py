from pathlib import Path
from typing import Dict

import numpy as np
import torch
import wandb
from tqdm import tqdm

from .logger import logger
from .utils import accuracy

"""
Contains functions for training and testing a PyTorch model.
"""


def train_step(
    epoch: int,
    model: torch.nn.Module,
    train_dataloader: torch.utils.data.DataLoader,
    loss_fn: torch.nn.Module,
    optimizer: torch.optim.Optimizer,
    scheduler: torch.optim.Optimizer,
    device: torch.device,
):
    """Trains the PyTorch model end-to-end for one epoch. Steps are:
    Forward pass, backward pass, loss calculation, optimizer step

    Args:
    model: a PyTorch model for training.
    dataloader: A DataLoader instance for the model to be trained on.
    loss_fn: A PyTorch loss function to minimise.
    optimizer: A PyTorch optimizer to help minimize the loss function.
    device: A target device to compute on (e.g. "cuda" or "cpu").
    """

    # Put model in train mode
    model.train()

    # Setup train loss over epoch
    running_loss = 0

    # loop over training batches using timer tqdm
    if train_dataloader is not None:
        with tqdm(train_dataloader, unit="batch") as tepoch:
            for data, target in tepoch:
                tepoch.set_description(f"Epoch {epoch}")

                # Format expected input dimensions and send data to device
                train_x = data.to(device)
                y = target.to(device)

                # 1. Forward Pass
                output = model.forward(train_x)

                # 2. Calculate/accumulate loss and calculate precision
                loss = loss_fn(output, y)
                running_loss += loss.detach().item()

                prec1, prec5 = accuracy(output.data, y, topk=(1, 5))

                # 3. Optimzer zero grad
                optimizer.zero_grad(set_to_none=False)

                # 4. Loss backprop
                loss.backward()

                # 5. Optimizer step
                optimizer.step()
                tepoch.set_postfix(loss=loss.detach().item())

        # 6. Optimizer Step
        if scheduler is not None:
            scheduler.step()

        # Adjust metrics to get average loss per batch
        avg_train_loss = running_loss / (len(train_dataloader))
        return avg_train_loss, (prec1.detach().item(), prec5.detach().item())
    else:
        return np.nan, np.nan, np.nan


def test_step(
    model: torch.nn.Module,
    test_dataloader: torch.utils.data.DataLoader,
    loss_fn: torch.nn.Module,
    device: torch.device,
):
    """Tests the PyTorch model end-to-end for one epoch. Steps are:
    Forward pass and loss calculation.

    Args:
    model: a PyTorch model for testing.
    dataloader: A DataLoader instance for the model to be trained on.
    loss_fn: A PyTorch loss function to calculate loss on test data.
    device: A target device to compute on (e.g. "cuda" or "cpu").
    """
    with torch.no_grad():
        # Put model in eval
        model.eval()

        # Setup train loss over epoch
        running_loss = 0

        # loop over val/test batches
        if test_dataloader is not None:
            for i, (data, y) in enumerate(test_dataloader):
                # Format expected input dimensions and send data to device
                test_x = data.to(device)

                y = y.to(device)

                # 1. Forward Pass
                output = model.forward(test_x)

                # 2. Calculate/accumulate loss and calculate accuracy
                loss = loss_fn(output, y)
                running_loss += loss.detach().item()

                prec1, prec5 = accuracy(output.data, y, topk=(1, 5))

            # Adjust metrics to get average loss and accuracy per batch
            avg_test_loss = running_loss / (len(test_dataloader))
            return avg_test_loss, (prec1.detach().item(), prec5.detach().item())
        else:
            return np.nan, np.nan, np.nan


def train(
    model: torch.nn.Module,
    train_dataloader: torch.utils.data.DataLoader,
    val_dataloader: torch.utils.data.DataLoader,
    optimizer: torch.optim.Optimizer,
    scheduler: torch.optim.Optimizer,
    loss_fn: torch.nn.Module,
    epochs: int,
    device: torch.device,
    save_model: str,
    wb: bool,
):
    """Trains PyTorch model and reports validation accuracy

    Passes a target PyTorch models through train and validation set
    functions for a number of epochs, training and validating the model
    in the same epoch loop.
    Calculates, prints and stores evaluation metrics throughout.

    Args:
    model: A PyTorch model to be trained and validated.
    train_dataloader: A DataLoader instance for the model to be trained on.
    val_dataloader: A DataLoader instance for the model to be validated on.
    optimizer: A PyTorch optimizer to help minimize the loss function.
    scheduler: A PyTorch scheduler to decrease learning rate over epochs.
    loss_fn: A PyTorch loss function to calculate loss on both datasets.
    epochs: An integer indicating how many epochs to train for.
    device: A target device to compute on (e.g. "cuda" or "cpu").
    Returns:
    A dictionary of training and testing loss as well as training and
    validation accuracy metrics. Each metric has a value in a list for
    each epoch.
    In the form: {train_loss: [...],
              val_loss: [...],
    For example if training for epochs=2:
             {train_loss: [2.0616, 1.0537],
              val_loss: [1.2641, 1.5706],
    """
    # Create empty results dictionary
    # results = {
    #     "train_loss": [float],
    #     "val_loss": [float],
    # }
    # Create empty results dictionary
    results: Dict[str, list] = {}
    results["train_loss"] = []
    results["val_loss"] = []
    results["train_precision@1"] = []
    results["val_precision@1"] = []
    results["train_precision@5"] = []
    results["val_precision@5"] = []

    # Loop through training and testing steps for a number of epochs
    for epoch in range(epochs):
        train_loss, train_precision = train_step(
            epoch=epoch,
            model=model,
            train_dataloader=train_dataloader,
            loss_fn=loss_fn,
            optimizer=optimizer,
            scheduler=scheduler,
            device=device,
        )

        logger.info("Calculating validation loss")
        val_loss, val_precision = test_step(
            model=model, test_dataloader=val_dataloader, loss_fn=loss_fn, device=device
        )

        # print out what's happening
        logger.info(
            f"Epoch: {epoch+1} | "
            f"train_loss: {train_loss:.4f} | "
            f"val_loss: {val_loss:.4f} | "
        )

        # Update results dictionary
        results["train_loss"].append(train_loss)
        results["val_loss"].append(val_loss)
        results["train_precision@1"].append(train_precision[0])
        results["val_precision@1"].append(val_precision[0])
        results["train_precision@5"].append(train_precision[1])
        results["val_precision@5"].append(val_precision[1])

        if wb is True:
            wandb.log(
                {
                    "loss_train": train_loss,
                    "precision_train@1": train_precision[0],
                    "precision_train@5": train_precision[1],
                    "loss_val": val_loss,
                    "precision_val@1": val_precision[0],
                    "precision_val@5": train_precision[1],
                }
            )

    if save_model is not None:
        state = {
            "epoch": epochs,
            "state_dict": model.state_dict(),
            "optimizer": optimizer.state_dict(),
        }
        if not Path(save_model).parent.is_dir():
            Path(save_model).parent.mkdir()
        torch.save(state, save_model)

    # Return the filled results at the end of the epochs
    return results
