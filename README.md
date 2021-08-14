# ulauncher-jd

> 🚧 The project cannot be qualified as stable for the moment. WIP. 🚧

A [Ulauncher](https://ulauncher.io/) extension for the [Johnny Decimal](https://johnnydecimal.com/) filing system.

Inspired by [alfred-jd](https://github.com/bsag/alfred-jd), a twin project for [Alfred](https://www.alfredapp.com/).

## Glossary

- "component": either an area, a category or an ID
- "number": the prefix of a component; of the form "XX-XX" for areas, "XX" for categories and "XX.XX" for IDs

## Features

> 🚧 WIP section. 🚧

### Opening components

Open the component folder with the file browser.

`jd <query>`

**Examples**

- `jd 10-19` to open the area named `10-19 ...`
- `jd foo` to open the component named `... foo ...`

### Creating components

Create a new component. A parent component number can be supplied.

NB: The new component number will be automatically picked depending on availability.

`jdn [parent component number] <name>`

**Examples**

- `jdn foo` to create a new area named `XX-XX foo`
- `jdn 10-19 foo` to create a new category (inside area `10-19`) named `XX foo`
- `jdn 18 foo` to create a new ID (inside category `18`) named `XX.XX foo`
