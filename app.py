#!/usr/bin/env python3

from aws_cdk import core

from data_warehouse_experiment.data_warehouse_experiment_stack import DataWarehouseExperimentStack


app = core.App()
DataWarehouseExperimentStack(app, "data-warehouse-experiment")

app.synth()
