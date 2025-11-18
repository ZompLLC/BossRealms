package bossrealms.plugin.commands;

import com.mojang.brigadier.Command;
import com.mojang.brigadier.builder.LiteralArgumentBuilder;
import com.mojang.brigadier.context.CommandContext;

import io.papermc.paper.command.brigadier.CommandSourceStack;
import io.papermc.paper.command.brigadier.Commands;

public class AutoReload {
    private static boolean autoReloading = true;

    public static LiteralArgumentBuilder<CommandSourceStack> createCommand() {
        return Commands.literal("autoreload")
                .executes(AutoReload::flipAutoReloading);
    }

    private static int flipAutoReloading(CommandContext<CommandSourceStack> ctx) {
        System.out.println(ctx); // prevent warnings :3 will replace with debug.info once we get that up
        autoReloading = !autoReloading;
        return Command.SINGLE_SUCCESS;
    }

    public static boolean isAutoReloading() {
        return autoReloading;
    }
}