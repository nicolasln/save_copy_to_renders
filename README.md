# Save Copy to Renders

Save Copy to Renders adds **Save Copy to Renders** to Blender's File menu and F3
search. It saves a copy of the current `.blend` file in a `Renders` directory
beside the working file and adds a timestamp generated within the add-on.

If the current filename already ends in a timestamp, the add-on replaces that
timestamp and saves the copy in the same directory instead. A timestamp is
recognized as a final space-separated suffix of at least four uppercase
Base36 characters (`0-9`, `A-Z`).

The stamp encodes the elapsed 20-second intervals since January 1 of the current
UTC year in uppercase Base36, padded to at least four characters. It is
generated fresh on every save. If a filename with that stamp already exists,
the add-on advances the stamp one interval at a time until it finds an unused
filename. This allows quick successive saves without overwriting earlier copies.

For example:

```text
~/Desktop/file.blend → ~/Desktop/Renders/file LM4M.blend
~/Desktop/Renders/file LM4M.blend → ~/Desktop/Renders/file LM4N.blend
```

Saving again during the same interval creates `file LM4N.blend`, then
`file LM4O.blend`, and so on, skipping any names that already exist.

The working file remains open and unchanged. The command is disabled until the
current file has been saved once. An existing versioned copy is never
overwritten.

## Installation

Requires Blender 5.1 or newer.

1. Download the add-on ZIP from the [latest release](https://github.com/nicolasln/save_copy_to_renders/releases/latest) and leave it zipped.
2. Drag the ZIP from Finder (or File Explorer on Windows) into the Blender window and confirm the installation.
3. Enable **Save Copy to Renders**.
