package com.wingsofthewild.client.renderer;

import com.geckolib.renderer.GeoEntityRenderer;
import com.wingsofthewild.client.model.FlamefangModel;
import com.wingsofthewild.entity.FlamefangEntity;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.entity.state.LivingEntityRenderState;

public class FlamefangRenderer extends GeoEntityRenderer<FlamefangEntity, LivingEntityRenderState> {

    public FlamefangRenderer(EntityRendererProvider.Context renderManager) {
        super(renderManager, new FlamefangModel());
        this.shadowRadius = 1.3F;
    }

    @Override
    protected float getShadowRadius(LivingEntityRenderState state) {
        return 1.3F * state.scale;
    }
}
