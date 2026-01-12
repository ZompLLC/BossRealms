package bossrealms.plugin.Commands;

import org.bukkit.command.Command;
import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;

public class AutoReload implements CommandExecutor {

    private static boolean autoReloading = true;

    @Override
    public boolean onCommand(CommandSender sender, Command cmd, String label, String[] args) {
        autoReloading = !autoReloading;
        // new ChatBuilder(autoReloading ? "Enabled autoReload" : "Disabled
        // autoReload").sendAll();
        return true;
    }

    public static boolean isAutoReloading() {
        return autoReloading;
    }
}