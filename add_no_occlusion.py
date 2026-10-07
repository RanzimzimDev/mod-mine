with open("D:/Mine/src/main/java/com/wingsofthewild/init/ModBlocks.java", "r", encoding="utf-8") as f:
    code = f.read()

replacements = [
    ("""    public static final DeferredBlock<Block> DRAGON_NEST = registerBlock("dragon_nest",
            properties -> new Block(properties
                    .mapColor(MapColor.COLOR_BROWN)
                    .strength(0.8F)
                    .sound(SoundType.GRASS)
            )
    );""",
     """    public static final DeferredBlock<Block> DRAGON_NEST = registerBlock("dragon_nest",
            properties -> new Block(properties
                    .mapColor(MapColor.COLOR_BROWN)
                    .strength(0.8F)
                    .sound(SoundType.GRASS)
                    .noOcclusion()
            )
    );"""),

    ("""    public static final DeferredBlock<Block> DRACONIC_HEARTH = registerBlock("draconic_hearth",
            properties -> new DraconicHearthBlock(properties
                    .mapColor(MapColor.STONE)
                    .strength(3.5F)
                    .sound(SoundType.STONE)
                    .requiresCorrectToolForDrops()
            )
    );""",
     """    public static final DeferredBlock<Block> DRACONIC_HEARTH = registerBlock("draconic_hearth",
            properties -> new DraconicHearthBlock(properties
                    .mapColor(MapColor.STONE)
                    .strength(3.5F)
                    .sound(SoundType.STONE)
                    .requiresCorrectToolForDrops()
                    .noOcclusion()
            )
    );"""),

    ("""    public static final DeferredBlock<Block> TACK_WORKBENCH = registerBlock("tack_workbench",
            properties -> new TackWorkbenchBlock(properties
                    .mapColor(MapColor.WOOD)
                    .strength(2.5F)
                    .sound(SoundType.WOOD)
            )
    );""",
     """    public static final DeferredBlock<Block> TACK_WORKBENCH = registerBlock("tack_workbench",
            properties -> new TackWorkbenchBlock(properties
                    .mapColor(MapColor.WOOD)
                    .strength(2.5F)
                    .sound(SoundType.WOOD)
                    .noOcclusion()
            )
    );"""),

    ("""    public static final DeferredBlock<Block> INCUBATION_BRAZIER = registerBlock("incubation_brazier",
            properties -> new Block(properties
                    .mapColor(MapColor.METAL)
                    .strength(3.0F)
                    .sound(SoundType.LANTERN)
                    .lightLevel(state -> 15)
                    .requiresCorrectToolForDrops()
            )
    );""",
     """    public static final DeferredBlock<Block> INCUBATION_BRAZIER = registerBlock("incubation_brazier",
            properties -> new Block(properties
                    .mapColor(MapColor.METAL)
                    .strength(3.0F)
                    .sound(SoundType.LANTERN)
                    .lightLevel(state -> 15)
                    .requiresCorrectToolForDrops()
                    .noOcclusion()
            )
    );"""),

    ("""    public static final DeferredBlock<Block> DRACONIC_ANVIL = registerBlock("draconic_anvil",
            properties -> new Block(properties
                    .mapColor(MapColor.METAL)
                    .strength(5.0F, 1200.0F)
                    .sound(SoundType.ANVIL)
                    .requiresCorrectToolForDrops()
            )
    );""",
     """    public static final DeferredBlock<Block> DRACONIC_ANVIL = registerBlock("draconic_anvil",
            properties -> new Block(properties
                    .mapColor(MapColor.METAL)
                    .strength(5.0F, 1200.0F)
                    .sound(SoundType.ANVIL)
                    .requiresCorrectToolForDrops()
                    .noOcclusion()
            )
    );"""),

    ("""    public static final DeferredBlock<Block> FLAMEFANG_TROPHY_SKULL = registerBlock("flamefang_trophy_skull",
            properties -> new Block(properties
                    .mapColor(MapColor.QUARTZ)
                    .strength(2.0F)
                    .sound(SoundType.BONE_BLOCK)
            )
    );""",
     """    public static final DeferredBlock<Block> FLAMEFANG_TROPHY_SKULL = registerBlock("flamefang_trophy_skull",
            properties -> new Block(properties
                    .mapColor(MapColor.QUARTZ)
                    .strength(2.0F)
                    .sound(SoundType.BONE_BLOCK)
                    .noOcclusion()
            )
    );"""),

    ("""    public static final DeferredBlock<Block> DRAGON_PERCH = registerBlock("dragon_perch",
            properties -> new Block(properties
                    .mapColor(MapColor.STONE)
                    .strength(3.0F)
                    .sound(SoundType.STONE)
            )
    );""",
     """    public static final DeferredBlock<Block> DRAGON_PERCH = registerBlock("dragon_perch",
            properties -> new Block(properties
                    .mapColor(MapColor.STONE)
                    .strength(3.0F)
                    .sound(SoundType.STONE)
                    .noOcclusion()
            )
    );"""),

    ("""    public static final DeferredBlock<Block> DRACONIC_FOUNDRY = registerBlock("draconic_foundry",
            properties -> new DraconicFoundryBlock(properties
                    .mapColor(MapColor.METAL)
                    .strength(4.0F, 12.0F)
                    .sound(SoundType.NETHERITE_BLOCK)
                    .lightLevel(state -> 14)
                    .requiresCorrectToolForDrops()
            )
    );""",
     """    public static final DeferredBlock<Block> DRACONIC_FOUNDRY = registerBlock("draconic_foundry",
            properties -> new DraconicFoundryBlock(properties
                    .mapColor(MapColor.METAL)
                    .strength(4.0F, 12.0F)
                    .sound(SoundType.NETHERITE_BLOCK)
                    .lightLevel(state -> 14)
                    .requiresCorrectToolForDrops()
                    .noOcclusion()
            )
    );"""),

    ("""    public static final DeferredBlock<Block> DRACONIC_BRAZIER_STANDING = registerBlock("draconic_brazier_standing",
            properties -> new Block(properties
                    .mapColor(MapColor.STONE)
                    .strength(3.5F)
                    .sound(SoundType.STONE)
                    .lightLevel(state -> 15)
            )
    );""",
     """    public static final DeferredBlock<Block> DRACONIC_BRAZIER_STANDING = registerBlock("draconic_brazier_standing",
            properties -> new Block(properties
                    .mapColor(MapColor.STONE)
                    .strength(3.5F)
                    .sound(SoundType.STONE)
                    .lightLevel(state -> 15)
                    .noOcclusion()
            )
    );""")
]

for old, new in replacements:
    old_c = old.replace("\r\n", "\n")
    code_c = code.replace("\r\n", "\n")
    assert old_c in code_c, f"Nao achou: {old_c[:40]}"
    code = code_c.replace(old_c, new)

with open("D:/Mine/src/main/java/com/wingsofthewild/init/ModBlocks.java", "w", encoding="utf-8") as f:
    f.write(code)

print("Todos os blocos 3D atualizados com .noOcclusion() com sucesso!")
