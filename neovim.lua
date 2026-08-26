return {
  {
    "echasnovski/mini.base16",
    lazy = false,
    priority = 1000,
    config = function()
      require("mini.base16").setup({
        palette = {
          base00 = "#0e1411",
          base01 = "#18211c",
          base02 = "#243029",
          base03 = "#4c5a50",
          base04 = "#8a9587",
          base05 = "#d6d1bd",
          base06 = "#e6e1cd",
          base07 = "#f2eddb",
          base08 = "#cc5a55",
          base09 = "#c98a4e",
          base0A = "#c9a554",
          base0B = "#85a760",
          base0C = "#6fa08d",
          base0D = "#5b7fa6",
          base0E = "#8e6f9e",
          base0F = "#b0413e",
        },
      })
    end,
  },
}
