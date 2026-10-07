package com.wingsofthewild.client.model;

import com.geckolib.model.GeoModel;
import com.geckolib.renderer.base.GeoRenderState;
import com.wingsofthewild.WingsOfTheWild;
import com.wingsofthewild.entity.FlamefangEntity;
import net.minecraft.resources.Identifier;

public class FlamefangModel extends GeoModel<FlamefangEntity> {

    private static final Identifier MODEL_RESOURCE =
            Identifier.fromNamespaceAndPath(WingsOfTheWild.MODID, "geo/flamefang_adult.geo.json");
    private static final Identifier TEXTURE_RESOURCE =
            Identifier.fromNamespaceAndPath(WingsOfTheWild.MODID, "textures/entity/flamefang_adult.png");
    private static final Identifier ANIMATION_RESOURCE =
            Identifier.fromNamespaceAndPath(WingsOfTheWild.MODID, "animations/flamefang_adult.animation.json");

    @Override
    public Identifier getModelResource(GeoRenderState state) {
        return MODEL_RESOURCE;
    }

    @Override
    public Identifier getTextureResource(GeoRenderState state) {
        return TEXTURE_RESOURCE;
    }

    @Override
    public Identifier getAnimationResource(FlamefangEntity animatable) {
        return ANIMATION_RESOURCE;
    }
}
