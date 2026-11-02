# Queue Version

Queue Version adds **Save Versioned Copy** to Blender's File menu. It saves a
copy of the current `.blend` file in a `Renders` directory beside the working
file and adds a timestamp generated within the add-on. No external script or
machine-specific path is required.

The stamp encodes the elapsed 20-second intervals since January 1 of the current
UTC year in uppercase Base36, padded to at least four characters. It is
generated fresh on every save. If a filename with that stamp already exists,
the add-on advances the stamp one interval at a time until it finds an unused
filename. This allows quick successive saves without overwriting earlier copies.

For example:

```text
~/Desktop/file.blend → ~/Desktop/Renders/file LM4M.blend
```

Saving again during the same interval creates `file LM4N.blend`, then
`file LM4O.blend`, and so on, skipping any names that already exist.

The working file remains open and unchanged. The command is disabled until the
current file has been saved once. An existing versioned copy is never
overwritten.
