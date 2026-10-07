package com.wingsofthewild.network;

import com.wingsofthewild.WingsOfTheWild;
import com.wingsofthewild.entity.FlamefangEntity;
import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.network.codec.ByteBufCodecs;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.Identifier;
import net.minecraft.world.entity.player.Player;
import net.neoforged.neoforge.network.handling.IPayloadContext;

public record DragonAttackPayload(int attackType) implements CustomPacketPayload {
    public static final Type<DragonAttackPayload> TYPE = new Type<>(Identifier.fromNamespaceAndPath(WingsOfTheWild.MODID, "dragon_attack"));

    public static final StreamCodec<RegistryFriendlyByteBuf, DragonAttackPayload> STREAM_CODEC = StreamCodec.composite(
            ByteBufCodecs.VAR_INT,
            DragonAttackPayload::attackType,
            DragonAttackPayload::new
    );

    @Override
    public Type<? extends CustomPacketPayload> type() {
        return TYPE;
    }

    public static void handle(DragonAttackPayload payload, IPayloadContext context) {
        context.enqueueWork(() -> {
            Player player = context.player();
            if (player.getVehicle() instanceof FlamefangEntity dragon) {
                if (dragon.getControllingPassenger() == player) {
                    if (payload.attackType() == 1 || dragon.isFlying()) {
                        dragon.shootFireball(player);
                    } else {
                        dragon.performBiteAttack();
                    }
                }
            }
        });
    }
}
