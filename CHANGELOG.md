# Changelog

## [0.6.0](https://github.com/iloveitaly/ipython-playground/compare/v0.5.0...v0.6.0) (2026-04-27)


### Features

* **extras:** include Enum classes in model discovery ([251e936](https://github.com/iloveitaly/ipython-playground/commit/251e936123912b731876c556cf5f4504b9085a80))
* **output:** use relative paths for local modules ([cc0aa59](https://github.com/iloveitaly/ipython-playground/commit/cc0aa59160d2991154af68d033540a492ea13899))
* refactor logging to dedicated module and add URL data reader ([d9d0b31](https://github.com/iloveitaly/ipython-playground/commit/d9d0b31574847e2a4205093b3e7cf17169f3f328))

## [0.5.0](https://github.com/iloveitaly/ipython-playground/compare/v0.4.1...v0.5.0) (2026-04-20)


### Features

* **playground:** improve signature formatting and module info reporting ([553eb37](https://github.com/iloveitaly/ipython-playground/commit/553eb370bba82def4c4056a792f721564ef79e0b))


### Bug Fixes

* **lint:** resolve import order and unused import errors ([a487e85](https://github.com/iloveitaly/ipython-playground/commit/a487e854de1e5d60ab1542a84a58a74a42f85d38))

## [0.4.1](https://github.com/iloveitaly/ipython-playground/compare/v0.4.0...v0.4.1) (2025-11-12)


### Bug Fixes

* replace SystemDateTime with ZonedDateTime for whenever library ([#19](https://github.com/iloveitaly/ipython-playground/issues/19)) ([2f9f99b](https://github.com/iloveitaly/ipython-playground/commit/2f9f99b2a44c7da0673246b70d172ec07cdb64b0))



## [0.4.0](https://github.com/iloveitaly/ipython-playground/compare/v0.3.0...v0.4.0) (2025-08-26)


### Features

* **ipython:** add redis client to playground interactive env ([7813e32](https://github.com/iloveitaly/ipython-playground/commit/7813e3210b03a89407499d79486ce6fcaee19a62))



## [0.3.0](https://github.com/iloveitaly/ipython-playground/compare/v0.2.0...v0.3.0) (2025-04-19)


### Bug Fixes

* handle NameError in get_type_hints for missing imports ([028a529](https://github.com/iloveitaly/ipython-playground/commit/028a529cdcb16825bbcbdbc7cd5b386d4b35a169))
* update playground to load all_extras globals before output ([6c5ee1f](https://github.com/iloveitaly/ipython-playground/commit/6c5ee1f8b5cfc27de1700bf6d8bafe488e9c256f))


### Features

* add app.jobs and sqlmodel to ipython playground imports ([608bc76](https://github.com/iloveitaly/ipython-playground/commit/608bc76220b844e28604a6b1c1755c00d883b8e0))
* add extras.all for loading modules and models in ipython ([793f620](https://github.com/iloveitaly/ipython-playground/commit/793f620396e234ddfa25ba4aa5268238d31b5f2f))



## [0.2.0](https://github.com/iloveitaly/ipython-playground/compare/9ee62b645e51b1d6aa25649db8b69fbeabaa6ab7...v0.2.0) (2025-03-19)


### Features

* add command-line help option to main function ([7d5e435](https://github.com/iloveitaly/ipython-playground/commit/7d5e435cc911a741451b89ce113346ef092f0609))
* add create_playground_file function ([1e01789](https://github.com/iloveitaly/ipython-playground/commit/1e017895582310d1cbb8d77a42721faa47286636))
* auto-import modules in ipython sessions ([9ee62b6](https://github.com/iloveitaly/ipython-playground/commit/9ee62b645e51b1d6aa25649db8b69fbeabaa6ab7))
