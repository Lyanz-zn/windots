local palette_path = vim.fn.expand("~/.config/windots/matugen/generated/nvim.json")

return {
  "Senal-D-A-Gunaratna/matugen.nvim",
  lazy = false,
  priority = 1000,

  opts = {
    load_theme = true,
    palette_path = palette_path,
  },

  config = function(_, opts)
    local matugen = require("matugen")

    matugen.setup(opts)

    local apply_timer

    local function apply_matugen()
      if apply_timer then
        apply_timer:stop()
      end

      apply_timer = vim.defer_fn(function()
        matugen.reload_templates()
        matugen.load_theme(true)
        vim.cmd("doautocmd ColorScheme")
      end, 100)
    end

    vim.api.nvim_create_user_command("MatugenApply", apply_matugen, {
      desc = "Reload and apply Matugen theme",
    })

    local watcher = vim.uv.new_fs_event()

    watcher:start(
      palette_path,
      {},
      vim.schedule_wrap(function(err)
        if err then
          vim.notify("Matugen watcher error: " .. err, vim.log.levels.ERROR)
          return
        end

        apply_matugen()
      end)
    )
  end,
}
