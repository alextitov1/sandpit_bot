#!/usr/bin/env python
from constructs import Construct
from cdktf import App, TerraformStack, TerraformOutput, Token
from imports.azurerm.provider import AzurermProvider
from imports.azurerm.resource_group import ResourceGroup
from imports.azurerm.virtual_network import VirtualNetwork


class MyStack(TerraformStack):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)

        # define resources here
        loca = "Australia East"
        add_space = ["10.10.10.0/24"]
        rg_name = "rg-cdktf"
        tag = {
            "ENV": "Dev",
            "PROJECT": "poc-cdktf"
        }

        AzurermProvider(self, "Azurerm",
                        features={}
                        )

        example_rg = ResourceGroup(self, 'example-rg',
                                   name=rg_name,
                                   location=loca,
                                   tags=tag
                                   )

        example_vnet = VirtualNetwork(self, 'example_vnet',
                                      depends_on=[example_rg],
                                      name="example_vnet",
                                      location=loca,
                                      address_space=add_space,
                                      resource_group_name=Token().as_string(example_rg.name),
                                      tags=tag
                                      )

        TerraformOutput(self, 'vnet_id',
                        value=example_vnet.id
                        )


app = App()
MyStack(app, "cdktf-python")

app.synth()