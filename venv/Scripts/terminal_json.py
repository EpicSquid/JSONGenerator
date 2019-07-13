from pathlib import Path

blockstates_folder = "input/assets/mod/blockstates/"
block_models_folder = "input/assets/mod/models/block/"
item_models_folder = "input/assets/mod/models/item/"
block_loot_tables_folder = "input/data/mod/loot_tables/blocks/"
item_tags_folder = "input/data/mod/tags/items/"
block_tags_folder = "input/data/mod/tags/blocks/"

tool_types = ["sword", "pickaxe", "shovel", "axe", "hoe"]
armor_types = ["helmet", "chestplate", "leggings", "boots"]

mystical_world_tools = ["knife"]
metal_items = ["ingot", "nugget"]
metal_blocks = ["block"]
metal_ores = ["ore"]


def generate_block(modid, name, file_in, forge_tags=False):
    try:
        blockstate = Path(blockstates_folder + file_in + ".json").read_text()
        block_model = Path(block_models_folder + file_in + ".json").read_text()
        item_model = Path(item_models_folder + file_in + ".json").read_text()
        loot_table = Path(block_loot_tables_folder + file_in + ".json").read_text()
        if forge_tags:
            block_tags = Path(block_tags_folder + file_in + ".json").read_text()
    except FileNotFoundError:
        blockstate = Path(blockstates_folder + "block.json").read_text()
        block_model = Path(block_models_folder + "block.json").read_text()
        item_model = Path(item_models_folder + "block.json").read_text()
        loot_table = Path(block_loot_tables_folder + "block.json").read_text()
        if forge_tags:
            block_tags = Path(block_tags_folder + "block.json").read_text()

    blockstate = blockstate.replace("$", modid)
    blockstate = blockstate.replace("@", name)
    block_model = block_model.replace("$", modid)
    block_model = block_model.replace("@", name)
    item_model = item_model.replace("$", modid)
    item_model = item_model.replace("@", name)
    loot_table = loot_table.replace("$", modid)
    loot_table = loot_table.replace("@", name)
    if forge_tags:
        block_tags = block_tags.replace("$", modid)
        block_tags = block_tags.replace("@", name)

    file_out = file_in
    if file_out == "block":
        file_out = name + ".json"
    else:
        file_out = name.replace("_" + file_in, "") + "_" + file_out + ".json"

    out_blockstate = Path("/", "output", "assets", modid, "blockstates")
    out_block_model = Path("/", "output", "assets", modid, "models", "block")
    out_item_model = Path("/", "output", "assets", modid, "models", "item")
    out_loot_table = Path("/", "output", "data", modid, "loot_tables", "blocks")
    if forge_tags:
        out_block_tags = Path("/", "output", "data", modid, "tags", "blocks")

    out_blockstate.mkdir(exist_ok=True, parents=True)
    out_block_model.mkdir(exist_ok=True, parents=True)
    out_item_model.mkdir(exist_ok=True, parents=True)
    out_loot_table.mkdir(exist_ok=True, parents=True)
    if forge_tags:
        out_block_tags.mkdir(exist_ok=True, parents=True)

    out_blockstate.joinpath(file_out).write_text(blockstate)
    out_block_model.joinpath(file_out).write_text(block_model)
    out_item_model.joinpath(file_out).write_text(item_model)
    out_loot_table.joinpath(file_out).write_text(loot_table)
    if forge_tags:
        out_block_tags.joinpath(file_out).write_text(block_tags)


def generate_item(modid, name, file_in, forge_tags=False):
    try:
        item_model = Path(item_models_folder + file_in + ".json").read_text()
        if forge_tags:
            item_tags = Path(item_tags_folder + file_in + ".json").read_text()
    except FileNotFoundError:
        item_model = Path(item_models_folder + "item.json").read_text()
        if forge_tags:
            item_tags = Path(item_tags_folder + "item.json").read_text()

    item_model = item_model.replace("$", modid)
    item_model = item_model.replace("@", name)
    if forge_tags:
        item_tags = item_tags.replace("$", modid)
        item_tags = item_tags.replace("@", name)

    file_out = file_in
    if file_out == "item":
        file_out = name + ".json"
    else:
        file_out = name.replace("_" + file_in, "") + "_" + file_out + ".json"

    out_item_model = Path("/", "output", "assets", modid, "models", "item")
    out_item_model.mkdir(exist_ok=True, parents=True)
    out_item_model.joinpath(file_out).write_text(item_model)

    if forge_tags:
        out_item_tags = Path("/", "output", "data", modid, "tags", "items")
        out_item_tags.mkdir(exist_ok=True, parents=True)
        out_item_tags.joinpath(file_out).write_text(item_tags)


def generate_cube(modid, name):
    generate_block(modid, name, "block")


def generate_item_basic(modid, name):
    generate_item(modid, name, "item")


def generate_item_egg(modid, name):
    generate_item(modid, name, "spawn_egg")


if __name__ == '__main__':
    modid_in = input("Enter Mod Id: ")

    factories_item = []
    factories_block = []

    if input("Set of Items/Blocks? (y/n): ").startswith("y"):
        print("Available Factories: tool, armor, mystical_world_tool, ore, metal\n")
        factories_in = input("Enter Factory names, separated by \" \": ")
        split_factories = factories_in.split(" ")
        for factory in split_factories:
            if factory == "tool":
                factories_item += tool_types
            elif factory == "armor":
                factories_item += armor_types
            elif factory == "mystical_world_tool":
                factories_item += mystical_world_tools
            elif factory == "ore":
                factories_block += metal_ores
            elif factory == "metal":
                factories_block += metal_blocks
                factories_item += metal_items

        cont = "y"
        while cont.startswith("y") or cont.startswith("Y"):
            name_in = input("Enter Item/Block Name: ")
            for factory_item in factories_item:
                generate_item(modid_in, name_in + "_" + factory_item, factory_item,
                              forge_tags=(factory_item == "ingot" or factory_item == "nugget"))
            for factory_block in factories_block:
                generate_block(modid_in, name_in + "_" + factory_block, factory_block,
                               forge_tags=(factory_block == "block" or factory_block == "ore"))
            cont = input("Continue? (y/n): ")

    else:
        cont = "y"
        while cont.startswith("y") or cont.startswith("Y"):
            item_or_block = input("Item or Block? (item/block): ")
            if item_or_block.startswith("b") or item_or_block.startswith("B"):
                type_in = "Block"
            else:
                type_in = "Item"
            name_in = input("Enter " + type_in + " Name: ")

            if type_in == "Block":
                generate_cube(modid_in, name_in)
            elif type_in == "Item":
                generate_item_basic(modid_in, name_in)

            cont = input("Continue? (y/n): ")
