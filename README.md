# Queue Version

Queue Version adds **Save Versioned Copy** to Blender's File menu. It saves a
copy of the current `.blend` file in a `Renders` directory beside the working
file and adds a timestamp generated within the add-on. No external script or
machine-specific path is required.

The stamp encodes the elapsed 20-second intervals since January 1 of the current
UTC year in uppercase Base36, padded to at least four characters. It is
generated fresh on every save. Two saves in the same interval produce the same
stamp; an existing versioned copy is never overwritten.

For example:

```text
~/Desktop/file.blend → ~/Desktop/Renders/file LM4M.blend
```

The working file remains open and unchanged. The command is disabled until the
current file has been saved once. An existing versioned copy is never
overwritten.
