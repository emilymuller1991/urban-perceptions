import os
from pathlib import Path
from timeit import default_timer as timer

import torch
import torch.nn as nn
import wandb

from . import datautils, train
from .dataset_generator import dataloader_pp
from .logger import logger
from .model_builder import MyCNN
from .utils import detect_device, output_plots


def main(opt):

    # log output
    logger.info("Model running with parameters: %s" % opt)

    # detect devices
    device = detect_device()

    # WANDB for HO
    if opt.wandb:
        id = "%s" % opt.run_name
        wandb.login(key=os.getenv("WB_KEY"))
        wandb.init(
            id=id,
            project=os.getenv("WB_PROJECT"),
            entity=os.getenv("WB_USER"),
            settings=wandb.Settings(start_method="fork"),
        )

    # create dataloaders
    params = {
        "batch_size": opt.batch_size,
        "shuffle": True,
        "num_workers": 4,
        "pin_memory": False,
        "drop_last": False,
    }
    # train_dataloader, val_dataloader, N = dataloader(
    #     opt.data_dir, opt.root_dir, opt.pre, "train", params
    # )
    # test_dataloader, _, _ = dataloader(
    #     opt.data_dir, opt.root_dir, opt.pre, "val", params, val_split=0
    # )

    # load image metadata
    df_train, df_val, df_test = datautils.pp_process_input(
        opt.study_id,
        opt.root_dir,
        opt.data_dir,
        oversample=opt.oversample,
        verbose=True,
    )

    # create dataloaders
    train_dataloader = dataloader_pp(
        df_train, opt.root_dir, opt.data_dir, opt.pre, "train", params
    )
    val_dataloader = dataloader_pp(
        df_val, opt.root_dir, opt.data_dir, opt.pre, "val", params
    )
    test_dataloader = dataloader_pp(
        df_test, opt.root_dir, opt.data_dir, opt.pre, "test", params
    )

    # initialise model
    model = MyCNN(model_base=opt.model)
    model.to(device)
    logger.info("Model loaded with %s parameters" % str(model.count_params()))

    # Set up Loss and Optimizer
    optimizer = torch.optim.Adam(model.parameters(), opt.lr)

    def lambda_decay(epoch):
        # defines learning rate decay
        return opt.lr * 1 / (1.0 + (opt.lr / opt.epochs) * epoch)

    scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer, lambda_decay)
    # loss_fn = nn.CrossEntropyLoss()
    loss_fn = nn.MSELoss()

    # Start the timer
    start_time = timer()

    # Train model
    train_val_loss = train.train(
        model=model,
        train_dataloader=train_dataloader,
        val_dataloader=val_dataloader,
        optimizer=optimizer,
        scheduler=scheduler,
        loss_fn=loss_fn,
        epochs=opt.epochs,
        device=device,
        save_model=Path(opt.root_dir, "outputs/models/", opt.run_name + ".pt"),
        wb=opt.wandb,
    )
    output_plots(train_val_loss, opt.root_dir, opt.run_name)

    # End the timer and logger.info out how long it took
    end_time = timer()
    logger.info(f"Model trained in: {end_time-start_time:.3f} seconds")

    # Get Test Performance
    test_loss = train.test_step(
        model=model,
        test_dataloader=test_dataloader,
        loss_fn=loss_fn,
        device=device,
    )
    logger.info(f"Model tested in: {timer()-end_time:.3f} seconds")

    logger.info(
        "LOSS train {} valid {} test {}".format(
            train_val_loss["train_loss"][-1], train_val_loss["val_loss"][-1], test_loss
        )
    )
