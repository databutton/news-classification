# News classification demo

See the project live at [next.databutton.com](https://next.databutton.com/projects/17c80916-7087-4a80-8c75-92dc942a2fca)

Documentation can be found at [docs.databutton.com](https://docs.databutton.com)

## Getting started

### Install dependencies

```sh
poetry install
```

### Develop locally

Start the dev server using the following command:

```sh
poetry run databutton start
```

Your server should now be running with hot-reload enabled.

**Note**: In order to run the project locally you need your own databutton account

### Deploy changes to production

```sh
poetry run databutton deploy
```

## Fork the project

Delete `databutton.json` and deploy the project using `poetry run databutton start` to deploy the project to your own account

## License

The scripts and documentation in this project are released under the [MIT License](LICENSE)
