### Changelog

All notable changes to this project will be documented in this file. Dates are displayed in UTC.

Generated by [`auto-changelog`](https://github.com/CookPete/auto-changelog).

#### [v0.7.0](https://github.com/valohai/valohai-utils/compare/v0.6.0...v0.7.0)

- Add upload_store as prepare parameter [`#135`](https://github.com/valohai/valohai-utils/pull/135)
- Drop support for Python 3.7 [`#144`](https://github.com/valohai/valohai-utils/pull/144)
- Add execution configuration helper [`#141`](https://github.com/valohai/valohai-utils/pull/141), [`#143`](https://github.com/valohai/valohai-utils/pull/143)

#### [v0.6.0](https://github.com/valohai/valohai-utils/compare/v0.5.0...v0.6.0)

- Output properties helper [`#139`](https://github.com/valohai/valohai-utils/pull/139)
- Support requesting on-demand inputs [`#137`](https://github.com/valohai/valohai-utils/pull/137)
- Update default Python image [`#136`](https://github.com/valohai/valohai-utils/pull/136)

#### [v0.5.0](https://github.com/valohai/valohai-utils/compare/v0.4.0...v0.5.0)

- Download datum://id and datum://alias files while running exec locally [`#134`](https://github.com/valohai/valohai-utils/pull/134)
- add trigger catalog support [`#127`](https://github.com/valohai/valohai-utils/pull/127)
- Parser: Handle annotation-assignment statements [`#130`](https://github.com/valohai/valohai-utils/pull/130)
- Make parsing parameter from CLI work properly when it is a list [`#128`](https://github.com/valohai/valohai-utils/pull/128)
- Ignore default value for inputs if it's local file path [`#124`](https://github.com/valohai/valohai-utils/pull/124)
- Support Step source-path option to create dynamic-file Steps [`#119`](https://github.com/valohai/valohai-utils/pull/119)
- Handle annotation-assignment statements [`#129`](https://github.com/valohai/valohai-utils/issues/129)

#### [v0.4.0](https://github.com/valohai/valohai-utils/compare/v0.3.1...v0.4.0)

> 5 September 2023

- Log to original __stdout__ when in notebook context [`#116`](https://github.com/valohai/valohai-utils/pull/116)
- Maintain valohai-yaml related tests [`#114`](https://github.com/valohai/valohai-utils/pull/114)
- Renovate build & CI [`#113`](https://github.com/valohai/valohai-utils/pull/113)
- Locate cached file using datum information [`#111`](https://github.com/valohai/valohai-utils/pull/111)
- Don't hard-require `tqdm` for downloads [`#102`](https://github.com/valohai/valohai-utils/pull/102)
- Document VH_FLAT_LOCAL_OUTPUTS [`#112`](https://github.com/valohai/valohai-utils/pull/112)
- Fix folder path for outputs [`#110`](https://github.com/valohai/valohai-utils/pull/110)
- Add vh_metadata to logger [`#109`](https://github.com/valohai/valohai-utils/pull/109)
- Switch linting to ruff [`#105`](https://github.com/valohai/valohai-utils/pull/105)
- Drop support for EOL Python 3.6 [`#106`](https://github.com/valohai/valohai-utils/pull/106)
- Log to original __stdout__ when in notebook context (#116) [`#115`](https://github.com/valohai/valohai-utils/issues/115)
- Add vh_metadata to logger (#109) [`#55`](https://github.com/valohai/valohai-utils/issues/55)
- Refactor download_url for less nesting [`6065049`](https://github.com/valohai/valohai-utils/commit/6065049b37ad7e2e92155a4ff982e935ccf93bb4)
- Switch build to hatch [`2e28c96`](https://github.com/valohai/valohai-utils/commit/2e28c965137b5e92f9f4df8f9469c8ff0c45953d)
- Fix lint complaints [`5ed1682`](https://github.com/valohai/valohai-utils/commit/5ed16824f419ed3d4946e6189bc9d1a202812bb7)

#### [v0.3.1](https://github.com/valohai/valohai-utils/compare/v0.3.0...v0.3.1)

> 31 October 2022

- Set up linting via pre-commit [`#101`](https://github.com/valohai/valohai-utils/pull/101)
- Replace third-party URLs in tests with ours [`#100`](https://github.com/valohai/valohai-utils/pull/100)
- Output path [`#99`](https://github.com/valohai/valohai-utils/pull/99)

#### [v0.3.0](https://github.com/valohai/valohai-utils/compare/v0.2.0...v0.3.0)

> 13 September 2022

- Add `valohai.set_status_detail` [`#96`](https://github.com/valohai/valohai-utils/pull/96)
- Todo cleanups [`#94`](https://github.com/valohai/valohai-utils/pull/94)
- Allow overriding environment in `prepare` [`#93`](https://github.com/valohai/valohai-utils/pull/93)
- Allow overriding environment= in `prepare` [`#92`](https://github.com/valohai/valohai-utils/issues/92)
- Rename dev requirements to requirements-lint (so tests can run w/o it on Python 3.6) [`8c1905a`](https://github.com/valohai/valohai-utils/commit/8c1905a0be78060cbb70accfd9efda5b971ba130)
- Bump to valohai-yaml 0.20.1+ to clean up some TODOs [`fd78e0c`](https://github.com/valohai/valohai-utils/commit/fd78e0ce0b8b583a57d5e29be18deb3cdb025e75)
- Fix some Mypy complaints [`b1f4364`](https://github.com/valohai/valohai-utils/commit/b1f4364f84749307e0026f668118f725d978f985)

#### [v0.2.0](https://github.com/valohai/valohai-utils/compare/v0.1.14...v0.2.0)

> 3 June 2022

- Declarative setup, PEP517 [`#89`](https://github.com/valohai/valohai-utils/pull/89)
- Add `valohai.distributed` with config parsing [`#88`](https://github.com/valohai/valohai-utils/pull/88)
- Make NotImplementedErrors more verbose [`#86`](https://github.com/valohai/valohai-utils/pull/86)
- Add `valohai.distributed` and config reading to that [`61bf6d5`](https://github.com/valohai/valohai-utils/commit/61bf6d5873280a638f6a1b3af87f88177da760cd)
- Add distributed config "dataclasses" [`83b0ae8`](https://github.com/valohai/valohai-utils/commit/83b0ae8d78a8370b65ab702e4bc92f26a66fddfa)
- Switch to declarative setup.cfg and PEP517 packaging [`0f43196`](https://github.com/valohai/valohai-utils/commit/0f4319610da28fed955e7ef0b664d7600fdfb5af)

#### [v0.1.14](https://github.com/valohai/valohai-utils/compare/v0.1.13...v0.1.14)

> 29 March 2022

- Concoct CHANGELOG [`300eac1`](https://github.com/valohai/valohai-utils/commit/300eac11a664a87961690f8014b6e51b6b6d74e2)
- Become 0.1.14 [`294cccb`](https://github.com/valohai/valohai-utils/commit/294cccb6c15eb8e8e1753712c91c9264af524afc)
- Parse inputs.json datum_id [`a07eb71`](https://github.com/valohai/valohai-utils/commit/a07eb71ec3e46559cacf6a0ce327aaa61d69877e)

#### [v0.1.13](https://github.com/valohai/valohai-utils/compare/v0.1.12...v0.1.13)

> 15 February 2022

- Handle metadata field when deserializing /valohai/config/inputs.json [`#83`](https://github.com/valohai/valohai-utils/pull/83)
- Don't treat booleans as flags [`#80`](https://github.com/valohai/valohai-utils/pull/80)
- Don't treat booleans as flags [`#78`](https://github.com/valohai/valohai-utils/issues/78)
- Make sure to add pass info to flags [`864d73a`](https://github.com/valohai/valohai-utils/commit/864d73ac3fcaed31b6725383c2855e588bf2c2eb)
- Become 0.1.13 [`50a1864`](https://github.com/valohai/valohai-utils/commit/50a1864c95ef7e2ddc1ac4171d3383b643f154c4)
- Add a test for passing in false flags via CLI [`7383ba0`](https://github.com/valohai/valohai-utils/commit/7383ba09eae152ab5f67665a851ace630ee1cdde)

#### [v0.1.12](https://github.com/valohai/valohai-utils/compare/v0.1.11...v0.1.12)

> 29 March 2022

- Fix local inputs with multiple files + add tests [`#77`](https://github.com/valohai/valohai-utils/pull/77)
- Make mypy --strict happy [`#75`](https://github.com/valohai/valohai-utils/pull/75)
- Refactor parameters & inputs parsing for .prepare() [`#72`](https://github.com/valohai/valohai-utils/pull/72)
- Ship py.typed [`#74`](https://github.com/valohai/valohai-utils/pull/74)
- Fix path separator for generated YAML on Windows (fixes #68) [`#69`](https://github.com/valohai/valohai-utils/pull/69)
- Add dir_path property to inputs (fixes #51) [`#67`](https://github.com/valohai/valohai-utils/pull/67)
- Merge pull request #69 from valohai/windows-yaml [`#68`](https://github.com/valohai/valohai-utils/issues/68)
- Fix path separator for generated YAML on Windows (fixes #68) [`#68`](https://github.com/valohai/valohai-utils/issues/68)
- Merge pull request #67 from valohai/dirpath [`#51`](https://github.com/valohai/valohai-utils/issues/51)
- Add dir_path property to inputs (fixes #51) [`#51`](https://github.com/valohai/valohai-utils/issues/51)
- Recursively compress output with ** wildcards and preserve the folder structure (fixes #58) [`#58`](https://github.com/valohai/valohai-utils/issues/58)
- Fix tests after parameters & inputs parsing refactor [`202b704`](https://github.com/valohai/valohai-utils/commit/202b704abb4e4da4d6911003bd8671bcbb718bc2)
- Update development dependencies [`854818b`](https://github.com/valohai/valohai-utils/commit/854818b13f88997db8727499354e948e7218ffc6)
- Work around valohai-yaml compat bug [`72c50b6`](https://github.com/valohai/valohai-utils/commit/72c50b6e85520dfe9b5ab707dc6afc5da1af682b)

#### [v0.1.11](https://github.com/valohai/valohai-utils/compare/v0.1.10...v0.1.11)

> 29 March 2022

- Allow full parameter and input definition via valohai-utils prepare() [`#63`](https://github.com/valohai/valohai-utils/pull/63)
- Add dict of dict(s) support for parameters & inputs in .prepare() [`8d1d7d0`](https://github.com/valohai/valohai-utils/commit/8d1d7d0a29fb53272bc1f459601e8c8ead4c432b)
- Change wikimedia.org urls to our own s3 urls for the tests [`9f22ce6`](https://github.com/valohai/valohai-utils/commit/9f22ce68a9fad9da58df274b364f4d06ddf3da96)
- Become v0.1.11 [`71c1e64`](https://github.com/valohai/valohai-utils/commit/71c1e64705c4e433eb9476ab94eb2b59d0eecad5)

#### [v0.1.10](https://github.com/valohai/valohai-utils/compare/v0.1.9...v0.1.10)

> 29 March 2022

- Add wildcard support for paths() and streams() (fixes #54) [`#60`](https://github.com/valohai/valohai-utils/pull/60)
- Support notebooks in YAML generator (fixes #61) [`#62`](https://github.com/valohai/valohai-utils/pull/62)
- Don't mangle filenames when extracted from containers [`#53`](https://github.com/valohai/valohai-utils/pull/53)
- Merge pull request #60 from valohai/input-wildcards [`#54`](https://github.com/valohai/valohai-utils/issues/54)
- Add wildcard support for paths() and streams() (fixes #54) [`#54`](https://github.com/valohai/valohai-utils/issues/54)
- Merge pull request #62 from valohai/notebook-step [`#61`](https://github.com/valohai/valohai-utils/issues/61)
- Tests for notebook YAML generation [`4c767d1`](https://github.com/valohai/valohai-utils/commit/4c767d1857c139b6af21acaacc455fb891776627)
- Add notebook (.ipynb) file support for yaml generator [`8c5bee3`](https://github.com/valohai/valohai-utils/commit/8c5bee3f51135debde27efb1fd4da1c346e94c18)
- Run black and isort [`8ec0c92`](https://github.com/valohai/valohai-utils/commit/8ec0c92e12f0683bf4b21e46b33f47b862042755)

#### [v0.1.9](https://github.com/valohai/valohai-utils/compare/v0.1.8...v0.1.9)

> 29 March 2022

- Make inputs optional if the defaults are set empty [`#59`](https://github.com/valohai/valohai-utils/pull/59)
- Become 0.1.9 [`12fa08e`](https://github.com/valohai/valohai-utils/commit/12fa08eca512f11e87d3dd2c1d5aa77b34fbc7ac)
- Fix typing for the inputs to match reality! [`ce311dc`](https://github.com/valohai/valohai-utils/commit/ce311dc2f76ea3366c9840bbd6a033697f6622e8)

#### [v0.1.8](https://github.com/valohai/valohai-utils/compare/v0.1.5...v0.1.8)

> 30 April 2021

- Expect AttributeError when trying to eval assignments (fixes #43) [`#44`](https://github.com/valohai/valohai-utils/pull/44)
- Style + lint + mypy [`#41`](https://github.com/valohai/valohai-utils/pull/41)
- Expect AttributeError when trying to eval assignments (fixes #43) (#44) [`#43`](https://github.com/valohai/valohai-utils/issues/43) [`#43`](https://github.com/valohai/valohai-utils/issues/43)
- Add support for defining pipelines via papi integration [`c2e4622`](https://github.com/valohai/valohai-utils/commit/c2e46225f5ec15603d119af87bd29c9104abd6b8)
- Add type hints using Monkeytype [`9bf5b92`](https://github.com/valohai/valohai-utils/commit/9bf5b92b4151df26a3f714000f42f40c608627de)
- Fix lint and style errors [`7b7a166`](https://github.com/valohai/valohai-utils/commit/7b7a166ef9f9539c5189a2302175b3544adc391a)

#### [v0.1.5](https://github.com/valohai/valohai-utils/compare/v0.1.4...v0.1.5)

> 7 April 2021

- Add requirements [`#38`](https://github.com/valohai/valohai-utils/pull/38)
- Updated default command [`6b53ed9`](https://github.com/valohai/valohai-utils/commit/6b53ed9f52eacceb798c096cd717a3e7558c1a7b)
- changed default test behavior, as we're adding requirements.txt to new steps [`aaea795`](https://github.com/valohai/valohai-utils/commit/aaea795eea6bcf8e2b4c9e107eecbde9cdecd1c9)
- changed default step to include requirements.txt installation [`ea2b244`](https://github.com/valohai/valohai-utils/commit/ea2b244f87577520c1ed4282a2479ce4fec0a090)

#### [v0.1.4](https://github.com/valohai/valohai-utils/compare/v0.1.3...v0.1.4)

> 22 March 2021

- Set docker image in valohai.prepare [`#34`](https://github.com/valohai/valohai-utils/pull/34)
- Flush with a newline, printing JSON on own line [`#36`](https://github.com/valohai/valohai-utils/pull/36)
- Added support to define docker file [`3e28d26`](https://github.com/valohai/valohai-utils/commit/3e28d265d44ebc4b48f5aeb43b0e4bbb26d11f79)
- Mark wheel non-universal, add python_requires stanza [`ca947f7`](https://github.com/valohai/valohai-utils/commit/ca947f7a7ee99d5d38161da2623c2ba6114bec3b)
- updated default values [`1b14278`](https://github.com/valohai/valohai-utils/commit/1b14278b59549f906b81c520f51519142c9eeb1c)

#### [v0.1.3](https://github.com/valohai/valohai-utils/compare/v0.1.2...v0.1.3)

> 10 March 2021

- Readme for API v2 [`#30`](https://github.com/valohai/valohai-utils/pull/30)
- Cleanup [`#33`](https://github.com/valohai/valohai-utils/pull/33)
- Run Black [`fd98d15`](https://github.com/valohai/valohai-utils/commit/fd98d15f96f71f498e0de0d05ff3919571ebcc51)
- API v2 readme [`5383a49`](https://github.com/valohai/valohai-utils/commit/5383a49cba66264dd3ed6cdaa4dcc24d62391d22)
- Update dev requirements [`17f5e90`](https://github.com/valohai/valohai-utils/commit/17f5e902be92d1bfdb735d6240c1ad86f747bec9)

#### v0.1.2

> 1 March 2021

- Add support for overriding inputs via CLI args [`#31`](https://github.com/valohai/valohai-utils/pull/31)
- Add step name for local input/output cache to avoid filename collisions [`#29`](https://github.com/valohai/valohai-utils/pull/29)
- API v2 [`#28`](https://github.com/valohai/valohai-utils/pull/28)
- Merging configs with custom merging strategy [`#23`](https://github.com/valohai/valohai-utils/pull/23)
- Python 3.6 compat [`#24`](https://github.com/valohai/valohai-utils/pull/24)
- Add compression utility [`#22`](https://github.com/valohai/valohai-utils/pull/22)
- Output utilities, part 1 [`#16`](https://github.com/valohai/valohai-utils/pull/16)
- AST parser to figure out inputs & parameters from python source [`#7`](https://github.com/valohai/valohai-utils/pull/7)
- Add VFS groundwork [`#5`](https://github.com/valohai/valohai-utils/pull/5)
- Use custom merging strategy for the configs [`1da28c7`](https://github.com/valohai/valohai-utils/commit/1da28c723c7e855e6393483a7e172ecaeead1d21)
- Add valohai.prepare() and input downloading [`b5fd3d8`](https://github.com/valohai/valohai-utils/commit/b5fd3d82687f4de5507be8ec6aad10bdd2dfd68c)
- Refactor inputs for API v2 + improve tests [`46dada8`](https://github.com/valohai/valohai-utils/commit/46dada85bd7a4ef793b0ad51abb918cfe020de13)
