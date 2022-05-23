# News classification demo

See full live at [next.databutton.com](https://next.databutton.com/projects/0bd86282-8420-4d18-ad2c-006c66fe7d3d)

Documentation can be found at [docs.databutton.com](https://docs.databutton.com)

## Getting started

### Install dependencies

```sh
poetry instrall
```

### Develop locally

Start the dev server using the following command:

```sh
poetry run databutton dev
```

Your server should now be running with hot-reload enabled.

**Note**: In order to run the project locally you need your own databutton account

### Deploy changes to production

```sh
poetry run databutton deploy
```

## Fork the project

Delete `databutton.json` and deploy the project using `poetry run databutton dev` to deploy the project to your own account

## License

The scripts and documentation in this project are released under the [MIT License](LICENSE)