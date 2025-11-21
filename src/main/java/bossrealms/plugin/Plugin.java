package bossrealms.plugin;

import java.io.File;

import org.bukkit.Bukkit;
import org.bukkit.plugin.java.JavaPlugin;
import org.bukkit.scheduler.BukkitRunnable;

import bossrealms.plugin.commands.AutoReload;
import io.papermc.paper.plugin.lifecycle.event.types.LifecycleEvents;

public class Plugin extends JavaPlugin {
    private static Plugin context;

    public static Plugin context() {
        return context;
    }

    @Override
    public void onEnable() {
        setupGlobalState();
        setupCommands();
        setupAutoReload();
    }

    public void setupGlobalState() {
        context = this;
    }

    public void setupCommands() {
        this.getLifecycleManager().registerEventHandler(LifecycleEvents.COMMANDS, commands -> {
            commands.registrar().register(AutoReload.createCommand().build());

        });
    }

    public void setupAutoReload() {
        // Get our compiled jar instead of the remapped paper jar
        String filePath = getFile().getAbsolutePath();
        filePath = filePath.substring(0, filePath.length() - 37) + filePath.substring(filePath.length() - 21);
        File file = new File(filePath);

        final long lastModified = file.lastModified();
        new BukkitRunnable() {
            @Override
            public void run() {
                if (file.lastModified() > lastModified && AutoReload.isAutoReloading()) {
                    cancel(); // used to prevent loops now just stops bukkit runnable since reload does squat
                    Bukkit.getServer().dispatchCommand(
                            Bukkit.getServer().getConsoleSender(), "paper reload"); // sub with utils later;
                                                                                    // https://www.spigotmc.org/resources/plugmanx.88135/
                                                                                    // for open source plugin manager?
                    // hard coded edit to addd this:
                    // https://www.spigotmc.org/resources/biletools-test-plugins-faster.54823/
                }
            }
        }.runTaskTimer(this, 0, 20); // every 20 ticks (1 second), do it

        try {

            org.bukkit.plugin.Plugin bossRealmsPlugin = getServer().getPluginManager()
                    .loadPlugin(
                            new File("/Users/keith/Development/the boss realms/paper/plugins/zomp-1.0-SNAPSHOT.jar"));
            getServer().getPluginManager().enablePlugin(bossRealmsPlugin);
        } catch (Exception e) {
            System.out.println("RATRATARTARRTARTARTARTRA");
            e.printStackTrace();
        }
    }
}
