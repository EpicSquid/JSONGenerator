from pathlib import Path

blockstates_folder = "input/assets/mod/blockstates/"
block_models_folder = "input/assets/mod/models/block/"
item_models_folder = "input/assets/mod/models/item/"
block_loot_tables_folder = "input/data/mod/loot_tables/blocks/"
item_tags_folder = "input/data/mod/tags/items/"
block_tags_folder = "input/data/mod/tags/blocks/"
recipes_folder = "input/data/mod/recipes/"

tool_types = ["sword", "pickaxe", "shovel", "axe", "hoe"]
armor_types = ["helmet", "chestplate", "leggings", "boots"]

mystical_world_tools = ["knife"]
metal_items = ["ingot", "nugget", "dust"]
metal_blocks = ["block"]
metal_ores = ["ore"]

forge_metal_item_tags = ["ingot", "nugget"]
forge_metal_block_tags = ["storage_block"]
forge_gem_item_tags = ["gem"]
forge_ore_block_tags = ["ore"]

recipes_ingot = ["block", "nugget", "ingot_from_block", "ingot_from_nuggets"]
recipe_ores = ["ingot", "ingot_from_blasting"]
recipes_tools = ["axe", "hoe", "pickaxe", "shovel", "sword"]
recipes_armor = ["helmet", "chestplate", "leggings", "boots", "nugget_from_blasting", "nugget_from_smelting"]
recipes_mystical_world = ["knife"]


def generate_block(modid, name, file_in):
    try:
        blockstate = Path(blockstates_folder + file_in + ".json").read_text()
        block_model = Path(block_models_folder + file_in + ".json").read_text()
        item_model = Path(item_models_folder + file_in + ".json").read_text()
        loot_table = Path(block_loot_tables_folder + file_in + ".json").read_text()
    except FileNotFoundError:
        blockstate = Path(blockstates_folder + "block.json").read_text()
        block_model = Path(block_models_folder + "block.json").read_text()
        item_model = Path(item_models_folder + "block.json").read_text()
        loot_table = Path(block_loot_tables_folder + "block.json").read_text()

    blockstate = blockstate.replace("$", modid)
    blockstate = blockstate.replace("@", name)
    block_model = block_model.replace("$", modid)
    block_model = block_model.replace("@", name)
    item_model = item_model.replace("$", modid)
    item_model = item_model.replace("@", name)
    loot_table = loot_table.replace("$", modid)
    loot_table = loot_table.replace("@", name)

    file_out = file_in
    if file_out == "block":
        file_out = name + ".json"
    else:
        file_out = name.replace("_" + file_in, "") + "_" + file_out + ".json"

    out_blockstate = Path("/", "output", "assets", modid, "blockstates")
    out_block_model = Path("/", "output", "assets", modid, "models", "block")
    out_item_model = Path("/", "output", "assets", modid, "models", "item")
    out_loot_table = Path("/", "output", "data", modid, "loot_tables", "blocks")

    out_blockstate.mkdir(exist_ok=True, parents=True)
    out_block_model.mkdir(exist_ok=True, parents=True)
    out_item_model.mkdir(exist_ok=True, parents=True)
    out_loot_table.mkdir(exist_ok=True, parents=True)

    out_blockstate.joinpath(file_out).write_text(blockstate)
    out_block_model.joinpath(file_out).write_text(block_model)
    out_item_model.joinpath(file_out).write_text(item_model)
    out_loot_table.joinpath(file_out).write_text(loot_table)


def generate_item(modid, name, file_in):
    try:
        item_model = Path(item_models_folder + file_in + ".json").read_text()
    except FileNotFoundError:
        item_model = Path(item_models_folder + "item.json").read_text()

    item_model = item_model.replace("$", modid)
    item_model = item_model.replace("@", name)

    file_out = file_in
    if file_out == "item":
        file_out = name + ".json"
    else:
        file_out = name.replace("_" + file_in, "") + "_" + file_out + ".json"

    out_item_model = Path("/", "output", "assets", modid, "models", "item")
    out_item_model.mkdir(exist_ok=True, parents=True)
    out_item_model.joinpath(file_out).write_text(item_model)


def generate_tags(tag_name, resource_name, is_item, modid, tag_modid="forge"):
    tag_file = Path(
        (item_tags_folder if is_item else block_tags_folder) + ("item.json" if is_item else "block.json")).read_text()
    tag_file = tag_file.replace("@", modid)
    tag_file = tag_file.replace("$", resource_name.replace("_storage", ""))

    tag_name_split = tag_name.split("/")

    file_out = Path("/", "output", "data", tag_modid, "tags", "items" if is_item else "blocks")
    for index, path in enumerate(tag_name_split):
        if index < len(tag_name_split) - 1:
            file_out = file_out.joinpath(path)

    file_out.mkdir(exist_ok=True, parents=True)
    file_out.joinpath(tag_name_split[len(tag_name_split) - 1] + ".json").write_text(tag_file)


def generate_recipes(modid, name, recipes_in):
    for recipe in recipes_in:
        file_in = Path(recipes_folder + recipe + ".json").read_text()
        file_in = file_in.replace("@", modid)
        file_in = file_in.replace("$", name)

        file_out = Path("/", "output", "data", modid, "recipes")
        file_out.mkdir(exist_ok=True, parents=True)
        file_out.joinpath(name + "_" + recipe + ".json").write_text(file_in)


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

    factories_tag_item = []
    factories_tag_block = []

    recipes = []

    if input("Set of Items/Blocks? (y/n): ").startswith("y"):
        print("Available Factories: tool, armor, mystical_world_tool, ore, metal\n")
        factories_in = input("Enter Factory names, separated by \" \": ")
        split_factories = factories_in.split(" ")
        for factory in split_factories:
            if factory == "tool":
                factories_item += tool_types
                recipes += recipes_tools
            elif factory == "armor":
                factories_item += armor_types
                recipes += recipes_armor
            elif factory == "mystical_world_tool":
                factories_item += mystical_world_tools
                recipes += recipes_mystical_world
            elif factory == "ore":
                factories_block += metal_ores
                factories_tag_block += forge_ore_block_tags
                factories_tag_item += forge_ore_block_tags
                recipes += recipe_ores
            elif factory == "metal":
                factories_block += metal_blocks
                factories_item += metal_items
                factories_tag_block += forge_metal_block_tags
                factories_tag_item += forge_metal_item_tags
                factories_tag_item += forge_metal_block_tags
                recipes += recipes_ingot

        cont = "y"
        while cont.startswith("y") or cont.startswith("Y"):
            name_in = input("Enter Item/Block Name: ")
            for factory_item in factories_item:
                generate_item(modid_in, name_in + "_" + factory_item, factory_item)
            for factory_block in factories_block:
                generate_block(modid_in, name_in + "_" + factory_block, factory_block)

            for factory_item_tag in factories_tag_item:
                generate_tags(factory_item_tag + "s/" + name_in,
                              name_in + "_" + factory_item_tag, True, modid_in)
            for factory_block_tag in factories_tag_block:
                generate_tags(factory_block_tag + "s/" + name_in,
                              name_in + "_" + factory_block_tag, False, modid_in)
            generate_recipes(modid_in, name_in, recipes)
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
