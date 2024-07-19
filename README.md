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

## Usage

Run the script with the following command:

```
python pipresolver.py <package> <dependency> <max_version>
```

For example:

```
python pipresolver.py gradio typer 0.9.0
```

This will find the newest version of gradio that depends on typer 0.9.0 or lower.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
