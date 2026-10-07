package com.wingsofthewild.client.model;

import com.geckolib.constant.dataticket.DataTicket;
import com.geckolib.model.GeoModel;
import com.geckolib.renderer.base.GeoRenderState;
import com.wingsofthewild.WingsOfTheWild;
import com.wingsofthewild.entity.FlamefangEntity;
import net.minecraft.resources.Identifier;

public class FlamefangModel extends GeoModel<FlamefangEntity> {

    public static final DataTicket<Integer> DRAGON_STAGE = DataTicket.create("dragon_stage", Integer.class);

    private static final Identifier ADULT_MODEL =
            Identifier.fromNamespaceAndPath(WingsOfTheWild.MODID, "flamefang_adult");
    private static final Identifier JUVENILE_MODEL =
            Identifier.fromNamespaceAndPath(WingsOfTheWild.MODID, "flamefang_juvenile");
    private static final Identifier HATCHLING_MODEL =
            Identifier.fromNamespaceAndPath(WingsOfTheWild.MODID, "flamefang_hatchling");

    private static final Identifier ADULT_TEXTURE =
            Identifier.fromNamespaceAndPath(WingsOfTheWild.MODID, "textures/entity/flamefang_adult.png");
    private static final Identifier JUVENILE_TEXTURE =
            Identifier.fromNamespaceAndPath(WingsOfTheWild.MODID, "textures/entity/flamefang_juvenile.png");
    private static final Identifier HATCHLING_TEXTURE =
            Identifier.fromNamespaceAndPath(WingsOfTheWild.MODID, "textures/entity/flamefang_hatchling.png");

    private static final Identifier ADULT_ANIM =
            Identifier.fromNamespaceAndPath(WingsOfTheWild.MODID, "flamefang_adult");
    private static final Identifier JUVENILE_ANIM =
            Identifier.fromNamespaceAndPath(WingsOfTheWild.MODID, "flamefang_juvenile");
    private static final Identifier HATCHLING_ANIM =
            Identifier.fromNamespaceAndPath(WingsOfTheWild.MODID, "flamefang_hatchling");

    @Override
    public void addAdditionalStateData(FlamefangEntity animatable, Object extraData, GeoRenderState renderState) {
        super.addAdditionalStateData(animatable, extraData, renderState);
        renderState.addGeckolibData(DRAGON_STAGE, animatable.getStage());
    }

    @Override
    public Identifier getModelResource(GeoRenderState state) {
        Integer stage = state.getGeckolibData(DRAGON_STAGE);
        if (stage != null) {
            if (stage == FlamefangEntity.STAGE_HATCHLING) return HATCHLING_MODEL;
            if (stage == FlamefangEntity.STAGE_JUVENILE) return JUVENILE_MODEL;
        }
        return ADULT_MODEL;
    }

    @Override
    public Identifier getTextureResource(GeoRenderState state) {
        Integer stage = state.getGeckolibData(DRAGON_STAGE);
        if (stage != null) {
            if (stage == FlamefangEntity.STAGE_HATCHLING) return HATCHLING_TEXTURE;
            if (stage == FlamefangEntity.STAGE_JUVENILE) return JUVENILE_TEXTURE;
        }
        return ADULT_TEXTURE;
    }

    @Override
    public Identifier getAnimationResource(FlamefangEntity animatable) {
        int stage = animatable.getStage();
        if (stage == FlamefangEntity.STAGE_HATCHLING) return HATCHLING_ANIM;
        if (stage == FlamefangEntity.STAGE_JUVENILE) return JUVENILE_ANIM;
        return ADULT_ANIM;
    }
}
