{
  inputs =
  {
    cqdev.url = "github:marcus7070/cq-flake";
  };

  outputs = { cqdev, self, nixpkgs }:
    let
      # Generate a user-friendly version numer.
      version = builtins.substring 0 8 self.lastModifiedDate;
      # System types to support.
      supportedSystems = [ "x86_64-linux" "x86_64-darwin" ];
      # Helper function to generate an attrset '{ x86_64-linux = f "x86_64-linux"; ... }'.
      forAllSystems = f: nixpkgs.lib.genAttrs supportedSystems (system: f system);
      # Nixpkgs instantiated for supported system types.
      nixpkgsFor = forAllSystems (system: import nixpkgs { inherit system; overlays = [ self.overlay ]; });
    in
    {
      overlay = final: prev: {
        cqgen = final.stdenv.mkDerivation rec {
          name = "cqgen";
          src = self;
          buildInputs = [ cqdev.outputs.packages.${final.system}.cadquery-env ];
          dontInstall = true;
          dontPatch = true;
          buildPhase = ''
            python full_model_generation.py
            mkdir -p $out/john_is_cool
            mv output/*.stl $out/john_is_cool
          '';
        };
      };

      packages = forAllSystems (system:
        {
          inherit (nixpkgsFor.${system}) cqgen;
        });

      defaultPackage = forAllSystems (system: self.packages.${system}.cqgen);

    };
}
