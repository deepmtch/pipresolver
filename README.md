# PipResolver

PipResolver is a tool to find compatible versions of Python packages based on their dependencies.

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/pipresolver.git
   cd pipresolver
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a symbolic link to the pipresolver script:
   ```
   sudo ln -s /path/to/pipresolver/pipresolver /usr/local/bin/pipresolver
   ```
   Replace `/path/to/pipresolver` with the actual path to the cloned repository.

## Usage

After creating the symbolic link, you can run PipResolver from anywhere using:
```
pipresolver <package> <dependency> <max_version>
```

For example:
```
pipresolver gradio typer 0.9.0
```
This will find the newest version of gradio that depends on typer 0.9.0 or lower.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. If you'd like to contribute to making PipResolver available on PyPI, your efforts would be greatly appreciated.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
