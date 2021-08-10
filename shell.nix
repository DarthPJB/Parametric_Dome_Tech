#Generate a nix-shell for compiling cadquery, editing source
# and viewing results

#default nixpkgs
{ pkgs ? import <nixpkgs> {} }:

let
baseconfig = { allowUnfree = true; };
unstableTarball =
  fetchTarball
    https://github.com/NixOS/nixpkgs/archive/nixos-unstable.tar.gz;
unstable = import unstableTarball
{
  config = baseconfig;
};
in

# Generate Shell
pkgs.mkShell
{
  buildInputs = [
  #Python37 and cadquery python37Packages; this provides basic ability
  # to use python CadQueryModel.py to generate output.
  pkgs.python37
  pkgs.python37Packages.cadquery
  #CQ-editor for native rendering of CadQuery Models
  unstable.cq-editor
  # FastSTL viewer to view resulting STL files
  pkgs.fstl
  # Inkscape for the inkview package (fast SVG viewer)
  pkgs.inkscape
  # atom and vim for effective code editing
  pkgs.atom pkgs.vim
  pkgs.figlet
  ];
  #Run build-task post generation (TODO: makefile)
  shellHook = ''
      figlet "Shell Active:"
      echo "starting editors"
      atom ./
      cq-editor ./Auto_Tip/casing.py&
      echo "to begin build sequence; run -"
      echo "./task.sh;"
  '';
}
