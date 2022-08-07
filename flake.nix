{
  inputs =
  {
    cqdev.url = "github:marcus7070/cq-flake";
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };

  outputs = { cqdev, self, nixpkgs }:
  with import nixpkgs { system = "x86_64-linux"; };
  {
    # Fast preview for current configuration
    apps."x86_64-linux".PreviewDome = 
    {
      type = "app";
      buildInputs = 
      [ 
        # Marcus cq-dev flake used to bring in the CQ enviroment
        cqdev.outputs.packages."x86_64-linux".cadquery-env 
        # FastSTL for preview
        pkgs.fstl
      ];
      program = nixpkgs.writeShellScriptBin "PreviewDome.sh" ''
        python full_model_generation.py
        fstl output/*.stl
      '';
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
    packages."x86_64-linux".cqgen = stdenv.mkDerivation 
    {
      name = "cqgen";
      src = self;
      buildInputs = [ cqdev.outputs.packages."x86_64-linux".cadquery-env ];
      dontInstall = true;
      dontPatch = true;
      buildPhase = ''
        python full_model_generation.py
        mkdir -p $out/john_is_cool
        mv output/*.stl $out/john_is_cool
      '';
    };

    defaultPackage."x86_64-linux" = self.packages."x86_64-linux".cqgen;
  };
}
