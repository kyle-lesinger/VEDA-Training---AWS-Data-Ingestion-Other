# Python Path Operations and Renaming Guide

## Overview

Python's `pathlib` module provides an object-oriented approach to handling filesystem paths. The `Path` class offers powerful methods and attributes for path manipulation, making file renaming and path operations intuitive and platform-independent.

**Reference Documentation**: [https://docs.python.org/3/library/pathlib.html](https://docs.python.org/3/library/pathlib.html)

## Getting Started

```python
from pathlib import Path
```

## Path Component Extraction

### `.name` - Full Filename
Returns the final path component, excluding drive and root.

```python
p = Path('/home/user/documents/report.pdf')
print(p.name)  # 'report.pdf'
```

### `.stem` - Filename Without Extension
Returns the final path component without its suffix.

```python
p = Path('archive.tar.gz')
print(p.stem)  # 'archive.tar'

p = Path('document.pdf')
print(p.stem)  # 'document'
```

### `.suffix` - File Extension
Returns the file extension (the last dot-separated portion).

```python
p = Path('script.py')
print(p.suffix)  # '.py'

p = Path('archive.tar.gz')
print(p.suffix)  # '.gz'
```

### `.suffixes` - All Extensions
Returns a list of all file suffixes.

```python
p = Path('archive.tar.gz')
print(p.suffixes)  # ['.tar', '.gz']

p = Path('data.backup.2024.zip')
print(p.suffixes)  # ['.backup', '.2024', '.zip']
```

### `.parent` - Parent Directory
Returns the logical parent path.

```python
p = Path('/usr/local/bin/python3')
print(p.parent)  # Path('/usr/local/bin')

# Multiple levels up
print(p.parent.parent)  # Path('/usr/local')
```

### `.parents` - All Parent Directories
Returns an immutable sequence of parent paths.

```python
p = Path('/usr/local/bin/python3')
for parent in p.parents:
    print(parent)
# /usr/local/bin
# /usr/local
# /usr
# /
```

### `.parts` - Path Components
Returns a tuple of path components.

```python
p = Path('/home/user/documents/file.txt')
print(p.parts)  # ('/', 'home', 'user', 'documents', 'file.txt')
```

## Path Manipulation Methods

### `.with_name()` - Replace Filename
Creates a new path with a different filename.

```python
p = Path('/documents/draft.txt')
new_p = p.with_name('final.txt')
print(new_p)  # Path('/documents/final.txt')
```

### `.with_suffix()` - Change Extension
Creates a new path with a modified suffix.

```python
p = Path('document.txt')
new_p = p.with_suffix('.pdf')
print(new_p)  # Path('document.pdf')

# Remove suffix
p = Path('archive.zip')
new_p = p.with_suffix('')
print(new_p)  # Path('archive')
```

### `.with_stem()` - Change Filename (Keep Extension)
Creates a new path with a modified stem (Python 3.9+).

```python
p = Path('old_name.py')
new_p = p.with_stem('new_name')
print(new_p)  # Path('new_name.py')
```

## Renaming Operations

### `.rename()` - Rename File or Directory
Renames the file or directory to the given target. Returns a new Path instance pointing to the target.

```python
p = Path('old_file.txt')
new_p = p.rename('new_file.txt')
# File is now renamed, new_p points to 'new_file.txt'
```

### `.replace()` - Replace Existing File
Similar to rename(), but will overwrite the target if it exists.

```python
p = Path('source.txt')
target = Path('destination.txt')
p.replace(target)
# source.txt is moved to destination.txt, overwriting if it exists
```

## Practical Examples

### Batch Rename with Timestamp
```python
from pathlib import Path
from datetime import datetime

def add_timestamp_to_files(directory, extension):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    for file in Path(directory).glob(f'*.{extension}'):
        new_name = f"{file.stem}_{timestamp}{file.suffix}"
        file.rename(file.parent / new_name)
        print(f"Renamed: {file.name} -> {new_name}")
```

### Convert Extensions
```python
def convert_extensions(directory, old_ext, new_ext):
    for file in Path(directory).glob(f'*.{old_ext}'):
        new_file = file.with_suffix(f'.{new_ext}')
        file.rename(new_file)
        print(f"Converted: {file.name} -> {new_file.name}")
```

### Organize Files by Extension
```python
def organize_by_extension(directory):
    base_path = Path(directory)
    
    for file in base_path.iterdir():
        if file.is_file():
            ext_folder = base_path / file.suffix[1:]  # Remove the dot
            ext_folder.mkdir(exist_ok=True)
            file.rename(ext_folder / file.name)
```

### Safe Rename with Backup
```python
def safe_rename(file_path, new_name):
    p = Path(file_path)
    new_p = p.parent / new_name
    
    # Check if target exists
    if new_p.exists():
        backup_name = f"{new_p.stem}_backup{new_p.suffix}"
        new_p.rename(p.parent / backup_name)
        print(f"Backed up existing file to {backup_name}")
    
    p.rename(new_p)
    return new_p
```

### Sequential Numbering
```python
def number_files_sequentially(directory, prefix="file"):
    files = sorted(Path(directory).glob('*'))
    
    for i, file in enumerate(files, start=1):
        if file.is_file():
            new_name = f"{prefix}_{i:03d}{file.suffix}"
            file.rename(file.parent / new_name)
```

## Advanced Path Operations

### Resolve Symbolic Links
```python
p = Path('symlink_to_file')
resolved = p.resolve()  # Returns the actual path
```

### Check Path Properties
```python
p = Path('/home/user/file.txt')

p.exists()      # Check if path exists
p.is_file()     # Check if it's a file
p.is_dir()      # Check if it's a directory
p.is_symlink()  # Check if it's a symbolic link
p.is_absolute() # Check if path is absolute
```

### Join Paths
```python
base = Path('/home/user')
full_path = base / 'documents' / 'file.txt'
# Path('/home/user/documents/file.txt')
```

### Glob Pattern Matching
```python
# Find all Python files
for py_file in Path('.').glob('**/*.py'):
    print(py_file)

# Find all files starting with 'test'
for test_file in Path('.').glob('test*'):
    print(test_file)
```

## Common Patterns

### Remove Spaces from Filenames
```python
for file in Path('.').glob('* *'):
    new_name = file.name.replace(' ', '_')
    file.rename(file.parent / new_name)
```

### Add Prefix/Suffix to Multiple Files
```python
def add_prefix(directory, prefix, pattern='*'):
    for file in Path(directory).glob(pattern):
        if file.is_file():
            new_name = f"{prefix}{file.name}"
            file.rename(file.parent / new_name)

def add_suffix_before_extension(directory, suffix, pattern='*'):
    for file in Path(directory).glob(pattern):
        if file.is_file():
            new_name = f"{file.stem}{suffix}{file.suffix}"
            file.rename(file.parent / new_name)
```

### Case Conversion
```python
# Convert to lowercase
for file in Path('.').iterdir():
    if file.is_file():
        file.rename(file.parent / file.name.lower())

# Convert to uppercase
for file in Path('.').iterdir():
    if file.is_file():
        file.rename(file.parent / file.name.upper())
```

## Best Practices

1. **Always check if target exists** before renaming to avoid accidental overwrites
2. **Use Path objects** instead of string manipulation for cross-platform compatibility
3. **Create backups** when performing batch operations
4. **Test with dry runs** (print what would be renamed without actually doing it)
5. **Use `.resolve()` to get absolute paths** when needed
6. **Handle exceptions** for permission errors and non-existent paths

## Error Handling

```python
from pathlib import Path

def safe_batch_rename(directory, operation):
    errors = []
    
    for file in Path(directory).iterdir():
        try:
            if file.is_file():
                operation(file)
        except PermissionError:
            errors.append(f"Permission denied: {file}")
        except FileExistsError:
            errors.append(f"Target exists: {file}")
        except Exception as e:
            errors.append(f"Error with {file}: {e}")
    
    if errors:
        print("Errors occurred:")
        for error in errors:
            print(f"  - {error}")
```

## Summary

The `pathlib` module provides a robust, object-oriented approach to path manipulation and file renaming. Key advantages include:

- Platform-independent path handling
- Intuitive method names and operations
- Built-in safety features
- Rich set of path manipulation methods
- Clean, readable code

For more detailed information and additional methods, refer to the official [Python pathlib documentation](https://docs.python.org/3/library/pathlib.html).