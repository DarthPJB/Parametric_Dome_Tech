{
  inputs =
  {
    cqdev.url = "github:marcus7070/cq-flake";
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };

  outputs = { cqdev, self, nixpkgs }:
  let 
    pkgs = nixpkgs.legacyPackages."x86_64-linux";
  in
  {
    # Fast preview for current configuration
    apps."x86_64-linux".PreviewDome = 
    let
      preview_script = pkgs.writeShellApplication
      {
        name = "PreviewDome.sh";
        runtimeInputs = 
        [ 
          # Marcus cq-dev flake used to bring in the CQ enviroment
          cqdev.outputs.packages."x86_64-linux".cadquery-env 
          # FastSTL for preview
          pkgs.fstl
        ];
        text = ''
          python full_model_generation.py
          fstl output/*.stl
        '';
      };
    in
    {
      type = "app";
      program = "${preview_script}/bin/PreviewDome.sh";
    };


    # devshell for quick development
    devShell."x86_64-linux" = pkgs.mkShell 
    {
      buildInputs = 
      [
        # Marcus cq-dev flake used to bring in the CQ enviroment
        cqdev.outputs.packages."x86_64-linux".cadquery-env 
        # FastSTL viewer to view resulting STL files
        pkgs.fstl
        # Inkscape for the inkview package (fast SVG viewer)
        pkgs.inkscape
        # atom and vim for effective code editing
        pkgs.atom pkgs.vim
        # figlet for attractive messages
        pkgs.figlet
      ];

    shellHook = ''
        figlet "Shell Active:"
        echo "starting editors"
        atom ./ --no-sandbox
        cq-editor ./Auto_Tip/casing.py &
        echo "to begin build sequence; run -"
        echo "nix run .#PreviewDome"
    '';
    };

    # generate final output stl files
    packages."x86_64-linux".cqgen = pkgs.stdenv.mkDerivation 
    {
      name = "cqgen";
      src = self;
      buildInputs = [ cqdev.outputs.packages."x86_64-linux".cadquery-env ];
      dontInstall = true;
      dontPatch = true;
      buildPhase = ''
        python full_model_generation.py
        mkdir -p $out
        mv output/*.stl $out/
      '';
    };

    defaultPackage."x86_64-linux" = self.packages."x86_64-linux".cqgen;
  };
}
