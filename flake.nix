{
  description = "Parametric Geodesic Dome";

  inputs =
  {
    cqdev.url = "github:marcus7070/cq-flake";
  };

  outputs = { cqdev, self, nixpkgs }: {

    packages.x86_64-linux.hello = nixpkgs.legacyPackages.x86_64-linux.hello;

    defaultPackage.x86_64-linux = self.packages.x86_64-linux.hello;

  };
}
