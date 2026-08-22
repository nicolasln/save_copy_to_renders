# Queue Version

Queue Version adds **Save Versioned Copy** to Blender's File menu. It saves a
copy of the current `.blend` file in a `Renders` directory beside the working
file and adds the stamp produced by
`/Users/nicolas/Code/scripts/versionstamp.py`.

For example:

```text
~/Desktop/file.blend → ~/Desktop/Renders/file LM4M.blend
```

The working file remains open and unchanged. The command is disabled until the
current file has been saved once. An existing versioned copy is never
overwritten.
