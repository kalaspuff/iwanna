# `iwanna`

`iwanna` is a simple command line tool that leverages the power of OpenAI's GPT-4 model to help you find the right shell command to perform a specific action. With `iwanna`, you can get suggestions for shell commands to achieve your desired tasks, making your life easier and more efficient.

### Features

* 🪄 Get shell command suggestions based on your input
* 🤖 Utilizes OpenAI's GPT-4 model for accurate and relevant suggestions
* ✨ Easy to use and configure

### Demo of `iwanna` output

![output](https://user-images.githubusercontent.com/89139/226655066-898dbfdc-5ff7-4c86-a1af-9fdcbcd20c17.gif)

<sup>DISCLAIMER: Note that the suggestions from `iwanna` may not always be accurate or safe to run – use the suggested commands with great care.</sup>

---

## Installation

`iwanna` is preferably installed with `pipx`:

```bash
pipx install iwanna
```

However, you can also install it with `pip`:

```bash
pip install iwanna
```

## Configuration

Before using `iwanna`, you need to configure it with your OpenAI API key. This key allows the tool to access the OpenAI API and fetch suggestions from the GPT-4 model. To configure your API key, run:

```bash
iwanna --config
```

## Usage

To use `iwanna`, simply run the following command:

```bash
iwanna [options] <action>
```

Replace `<action>` with the task you want to perform.

### Example actions

```bash
iwanna search for a process
iwanna reduce the file size of a raw video file
iwanna find what wifi i am connected to
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Disclaimer

Note that the suggestions from `iwanna` may not be accurate or safe to run at all. Use the suggested output with great care.

This project is not affiliated with, nor endorsed by, OpenAI. It is an independent project created to showcase the potential use cases of the GPT-4 model.
