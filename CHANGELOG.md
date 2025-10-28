# Changelog

## [0.6.2](https://github.com/Evanlab02/HomePortalV2/compare/v0.6.1...v0.6.2) (2025-10-28)


### Bug Fixes

* Add gluetun port to dev containers ([f9256d9](https://github.com/Evanlab02/HomePortalV2/commit/f9256d96b89047edb345e6d432d686ffd782a12a))
* **Admin:** Fix more UI issues ([b1ffca3](https://github.com/Evanlab02/HomePortalV2/commit/b1ffca31ece33ba4fd8bf67eb2069c2c2777d61a))
* **Admin:** Small admin page UI adjustments and fixes ([3e25333](https://github.com/Evanlab02/HomePortalV2/commit/3e253332b61ba4c19d72c6c176e57a640d51e7b3))


### Miscellaneous Chores

* Format ([e75ede2](https://github.com/Evanlab02/HomePortalV2/commit/e75ede29208a5acf1ffc6b9306550fc3a74b56ae))

## [0.6.1](https://github.com/Evanlab02/HomePortalV2/compare/v0.6.0...v0.6.1) (2025-10-27)


### Bug Fixes

* Add mount for gluetun forwarded port to prod compose ([500e593](https://github.com/Evanlab02/HomePortalV2/commit/500e5933139c53e69261e48d6927f30aa708033f))


### Reverts

* **Postgres:** Revert back to 17.6 ([a642baa](https://github.com/Evanlab02/HomePortalV2/commit/a642baa95819b30e53249aa13c57dd3e070c4ed6))


### Miscellaneous Chores

* Add queue to dev dockerfile ([27d3bf4](https://github.com/Evanlab02/HomePortalV2/commit/27d3bf48627027f134f96e7f57536a8b28b5e74c))

## [0.6.0](https://github.com/Evanlab02/HomePortalV2/compare/v0.5.0...v0.6.0) (2025-10-27)


### ⚠ BREAKING CHANGES

* **Queue:** Introduce queue/worker for scheduled tasks and queued tasks along with QBit syncing capabilities

### Features

* **Queue:** Introduce queue/worker for scheduled tasks and queued tasks along with QBit syncing capabilities ([f700395](https://github.com/Evanlab02/HomePortalV2/commit/f700395beb9afc0c3f4a815d7db23e2084ecc1b3))


### Miscellaneous Chores

* Fix linting issues ([efd6fae](https://github.com/Evanlab02/HomePortalV2/commit/efd6fae606c87333c25f815655fc03d599877690))
* Remove mypy from linting ([d4502ba](https://github.com/Evanlab02/HomePortalV2/commit/d4502ba08e26ec34034f65b6d1da724896767f90))

## [0.5.0](https://github.com/Evanlab02/HomePortalV2/compare/v0.4.0...v0.5.0) (2025-10-27)


### ⚠ BREAKING CHANGES

* **Compose:** Create a distinction between compose modules templates and actual files

### Features

* **Compose:** Create a distinction between compose modules templates and actual files ([985c900](https://github.com/Evanlab02/HomePortalV2/commit/985c9007f332a531cab23e2083371871b596f71f))
* **Dev:** Add dev module for testing changes before release on server ([317c75f](https://github.com/Evanlab02/HomePortalV2/commit/317c75f5baff3bc684a7ae6fd65b5a06a6176f81))


### Bug Fixes

* Fix an issue where we were not correctly copying compose modules from their templates during the make env command ([5cef1b4](https://github.com/Evanlab02/HomePortalV2/commit/5cef1b4e5979d0b6b6be525c3e273a433e8d783e))


### Documentation

* Update getting started guide with latest information ([75e1f48](https://github.com/Evanlab02/HomePortalV2/commit/75e1f48df714b749fa670ac96e5a0a642547bc2e))

## [0.4.0](https://github.com/Evanlab02/HomePortalV2/compare/v0.3.1...v0.4.0) (2025-10-27)


### ⚠ BREAKING CHANGES

* **Immich:** Upgrade to 2.1.0
* **Postgres:** Upgrade to postgres 18

### Features

* **Authentik:** Upgrade to 2025.8.4 ([5a93f9b](https://github.com/Evanlab02/HomePortalV2/commit/5a93f9b0434b1fc5609ca55894e8b8042e44d141))
* **Django:** Use server side bindings/cursors ([469f32c](https://github.com/Evanlab02/HomePortalV2/commit/469f32c6047c8a411d0c7741b728b7ef5d8a9692))
* **Immich:** Upgrade to 2.1.0 ([844c6fe](https://github.com/Evanlab02/HomePortalV2/commit/844c6fe352955a987aad69e26565a5b1a5c49e5b))
* **PgAdmin:** Upgrade to 9.9.0 ([5dd4aad](https://github.com/Evanlab02/HomePortalV2/commit/5dd4aadeac729ed00d70ac88ea289d4d68916bc8))
* **Postgres:** Upgrade to postgres 18 ([02e6585](https://github.com/Evanlab02/HomePortalV2/commit/02e6585f908ece8c1579c0842923552879badc44))
* **Valkey:** Upgrade to valkey 9 ([4ff75ff](https://github.com/Evanlab02/HomePortalV2/commit/4ff75ffaa1e246349ce4e94116dfd0dd28f2de9a))


### Bug Fixes

* **Caddy:** Update Caddyfiles for new updated immich ([480e21e](https://github.com/Evanlab02/HomePortalV2/commit/480e21ecb7410ec998372029d8459ee9157f781e))
* **Gluetun:** Pin to 3.40.0 ([056143b](https://github.com/Evanlab02/HomePortalV2/commit/056143b4674aee9b0ce3a20ae55ef854a463a7fc))
* **Pihole:** Pin pihole to 2025.10.10 ([032ae4a](https://github.com/Evanlab02/HomePortalV2/commit/032ae4ae5f5ba63ed9a68c5d0b183355d48afcfc))
* **Prowlarr:** Pin to 2.1.5 ([2e02c34](https://github.com/Evanlab02/HomePortalV2/commit/2e02c3492342e82ec9ac29e837d24a1f0246c803))
* **QBittorrent:** Pin to 5.1.2 ([7fb7b26](https://github.com/Evanlab02/HomePortalV2/commit/7fb7b26f0430cfca1989e850979793cd5fb2511c))
* **Radarr:** Pin to 5.28.0 ([28a5709](https://github.com/Evanlab02/HomePortalV2/commit/28a5709676e0bf1f7c9245558745a9e74c790c57))
* **Seerr:** Pin seerr to 2.7.3 ([ade72d7](https://github.com/Evanlab02/HomePortalV2/commit/ade72d71cc908aea7d9d5d05835a3af58a55453a))
* **Sonarr:** Pin to 4.0.15 ([d5d0a2b](https://github.com/Evanlab02/HomePortalV2/commit/d5d0a2b6113bd0ff307e21ae38c2dc221211c3fa))


### Dependencies

* **Django:** Upgrade django app deps ([237ec41](https://github.com/Evanlab02/HomePortalV2/commit/237ec41ac169d508506f21b8918360ee09378a06))
* **maintenance:** Updated maintenance front-end deps ([6e0444c](https://github.com/Evanlab02/HomePortalV2/commit/6e0444ca496427e1aa07711797866197202d4d53))


### Reverts

* Remove immich-ml domain from caddyfile ([692bdf6](https://github.com/Evanlab02/HomePortalV2/commit/692bdf644e286d5c1f384b15461d6fb371c678be))

## [0.3.1](https://github.com/Evanlab02/HomePortalV2/compare/v0.3.0...v0.3.1) (2025-10-25)


### Bug Fixes

* Small setup and compose fixes ([6e44554](https://github.com/Evanlab02/HomePortalV2/commit/6e44554cd8b345d76364256353b8c8dd5545424d))

## [0.3.0](https://github.com/Evanlab02/HomePortalV2/compare/v0.2.1...v0.3.0) (2025-10-25)


### ⚠ BREAKING CHANGES

* Add all modules to home portal

### Features

* Add all modules to home portal ([2f42bfc](https://github.com/Evanlab02/HomePortalV2/commit/2f42bfc0237690bcfd3fcd7855c540ce9874df06))


### Miscellaneous Chores

* Add modules from previous HomePortal ([9135be3](https://github.com/Evanlab02/HomePortalV2/commit/9135be3d9c5e726a6c762f7a98d34ba45d955c98))
* Fix some setup mk issues ([b979ec3](https://github.com/Evanlab02/HomePortalV2/commit/b979ec3f52b4c753910eb6660399896990a89486))

## [0.2.1](https://github.com/Evanlab02/HomePortalV2/compare/v0.2.0...v0.2.1) (2025-10-25)


### Bug Fixes

* Authentik versions in compose reference file ([6ddb730](https://github.com/Evanlab02/HomePortalV2/commit/6ddb730a4d015abd6f9e410b04e0fdbbcd61497b))


### Documentation

* Updated documentation guide for setup with authentik ([3e92880](https://github.com/Evanlab02/HomePortalV2/commit/3e9288033eee005c0bd91018afdc9d4bed1031bd))

## [0.2.0](https://github.com/Evanlab02/HomePortalV2/compare/v0.1.4...v0.2.0) (2025-10-25)


### ⚠ BREAKING CHANGES

* **Authentik:** Authentik integration into home portal

### Features

* **Authentik:** Authentik integration into home portal ([e117c27](https://github.com/Evanlab02/HomePortalV2/commit/e117c278014cf4284710e9454490f6d4875781c5))


### Miscellaneous Chores

* Small typo fixes ([a770a86](https://github.com/Evanlab02/HomePortalV2/commit/a770a86c73c6bfa9d8cb6bca686b568a3c90ccb8))

## [0.1.4](https://github.com/Evanlab02/HomePortalV2/compare/v0.1.3...v0.1.4) (2025-10-25)


### Features

* Simplified the setup process signifcantly ([f934ca1](https://github.com/Evanlab02/HomePortalV2/commit/f934ca132e37fc4c372cb2cfacb14f1a420b548b))


### Miscellaneous Chores

* Fix release please config issue ([50957a3](https://github.com/Evanlab02/HomePortalV2/commit/50957a3c07a2549ec16c36785f2dce1c79684fcb))
* Fix some linting issues ([068f984](https://github.com/Evanlab02/HomePortalV2/commit/068f9847b5fb4103fd7be18f724153300e41e816))


### Continuous Integration

* Removed some old build steps ([bab3ee7](https://github.com/Evanlab02/HomePortalV2/commit/bab3ee711ef514b55cf11fc61b13e8f7a2b05add))

## [0.1.3](https://github.com/Evanlab02/HomePortalV2/compare/v0.1.2...v0.1.3) (2025-10-24)


### Bug Fixes

* Fix CSRF issue in django app ([5e7b6ec](https://github.com/Evanlab02/HomePortalV2/commit/5e7b6ecb566615ed671292242c108b1afa1a285a))

## [0.1.2](https://github.com/Evanlab02/HomePortalV2/compare/v0.1.1...v0.1.2) (2025-10-24)


### Bug Fixes

* Various docker, script and compose issues ([b6e6b83](https://github.com/Evanlab02/HomePortalV2/commit/b6e6b839bbd0560217a83ddbb3084a87d0087c95))

## [0.1.1](https://github.com/Evanlab02/HomePortalV2/compare/v0.1.0...v0.1.1) (2025-10-24)


### Bug Fixes

* Add missing compose and caddyfile configuration ([79a4e36](https://github.com/Evanlab02/HomePortalV2/commit/79a4e362f906eb5854a9a2eb541ce9162a9b4557))


### Miscellaneous Chores

* Add some hosts to maintenance file ([fc29d6f](https://github.com/Evanlab02/HomePortalV2/commit/fc29d6fc14d667caa07ddd0e0f39168c7c0754c3))
* Makefile commands ([34dab63](https://github.com/Evanlab02/HomePortalV2/commit/34dab639dcbbfcb5c8aa4e2aff6c4becc4a88620))

## [0.1.0](https://github.com/Evanlab02/HomePortalV2/compare/v0.0.8...v0.1.0) (2025-10-24)


### ⚠ BREAKING CHANGES

* Integrate django app and start utilizing fixed hosts in caddy

### Features

* Integrate django app and start utilizing fixed hosts in caddy ([123215a](https://github.com/Evanlab02/HomePortalV2/commit/123215a411835b90cdee58e1221812aa12893f8a))


### Bug Fixes

* Add static files from django ([f36f3d5](https://github.com/Evanlab02/HomePortalV2/commit/f36f3d5d8b0882233e384da5da8ff0c9bf2888d7))


### Miscellaneous Chores

* Add static files to caddyfile ([17ee5f6](https://github.com/Evanlab02/HomePortalV2/commit/17ee5f6330fa3edc6ddbb735a49133c33d3f262b))


### Continuous Integration

* Remove build steps for dockerfiles that no longer exist ([3d304d4](https://github.com/Evanlab02/HomePortalV2/commit/3d304d412ab653f5fe578f4a7d16ff60a726840a))

## [0.0.8](https://github.com/Evanlab02/HomePortalV2/compare/v0.0.7...v0.0.8) (2025-10-24)


### Bug Fixes

* Add redis to packages to homeportal app packages ([13f5c77](https://github.com/Evanlab02/HomePortalV2/commit/13f5c7736bc5ddd6284c338f310c5fd06bfc0876))
* Remove expected timeline from maintenance page ([dd6fa91](https://github.com/Evanlab02/HomePortalV2/commit/dd6fa912f051b98dc1fc6743301014d023c789c0))


### Continuous Integration

* Add linting workflows ([8b02acb](https://github.com/Evanlab02/HomePortalV2/commit/8b02acbb68db8e6fb22396bc192c47bfbb3ad5ee))
* Fix a release please workflow typo ([a52acd4](https://github.com/Evanlab02/HomePortalV2/commit/a52acd49e727b5b1c5ac9cf992b40336abade072))

## [0.0.7](https://github.com/Evanlab02/HomePortalV2/compare/v0.0.6...v0.0.7) (2025-10-24)


### Features

* **Django:** Add django app to HomePortalV2 ([90e2c3e](https://github.com/Evanlab02/HomePortalV2/commit/90e2c3eb61de48dfd00890036c1480dfc73444a7))


### Miscellaneous Chores

* Additional files release please ([ec813a5](https://github.com/Evanlab02/HomePortalV2/commit/ec813a588577564cb9409f9ede6f79219e34bb9d))
* Fix admin dockerfile issue ([94f0880](https://github.com/Evanlab02/HomePortalV2/commit/94f08800f46c18ac91bf85a33bfb40a4fd75e990))


### Continuous Integration

* Fix docker build issues ([e5c9336](https://github.com/Evanlab02/HomePortalV2/commit/e5c9336d6a84f5fcdcafd4fdce1ab0b822063320))

## [0.0.6](https://github.com/Evanlab02/HomePortalV2/compare/v0.0.5...v0.0.6) (2025-10-23)


### Bug Fixes

* Actually copy maintenance frontend assets for production caddy containers ([a577422](https://github.com/Evanlab02/HomePortalV2/commit/a577422f4cb4413c6933fd2d606d27b2631c3b54))

## [0.0.5](https://github.com/Evanlab02/HomePortalV2/compare/v0.0.4...v0.0.5) (2025-10-23)


### Features

* Automated version bumping ([09f5e10](https://github.com/Evanlab02/HomePortalV2/commit/09f5e10c8c88f27120c933eea227c3059502f95d))

## [0.0.4](https://github.com/Evanlab02/HomePortalV2/compare/v0.0.3...v0.0.4) (2025-10-23)


### Features

* **Maintenance:** Add naintenance mode and commands ([2b4f8d5](https://github.com/Evanlab02/HomePortalV2/commit/2b4f8d5a74cfb30ea0660dc5fe585892b9bbb521))


### Miscellaneous Chores

* Fix small volume issue in maintenance compose file ([3afb37c](https://github.com/Evanlab02/HomePortalV2/commit/3afb37c4a3880623a1eab04a0c54abfc1a3d8229))


### Continuous Integration

* Add more image build commands to build workflows ([4ec21a0](https://github.com/Evanlab02/HomePortalV2/commit/4ec21a0bd759ce5d439bd21963e77d4e381244e6))

## [0.0.3](https://github.com/Evanlab02/HomePortalV2/compare/v0.0.2...v0.0.3) (2025-10-23)


### Bug Fixes

* **Docker:** Fix dockerfile labels to remove warnings ([8df0aab](https://github.com/Evanlab02/HomePortalV2/commit/8df0aabaf45bd76fedf628419821f68d2f59df41))


### Documentation

* Proper first implementation documentation ([c6e9755](https://github.com/Evanlab02/HomePortalV2/commit/c6e9755fb93fab2ed9a1dfd5ef21025701c4b161))


### Miscellaneous Chores

* Add prod compose file ([14aee04](https://github.com/Evanlab02/HomePortalV2/commit/14aee04e6da58586c09b9f03820707f254e386d9))
* Fix documentation build workflows ([c6337a8](https://github.com/Evanlab02/HomePortalV2/commit/c6337a8e99d02e31fbaef2a51a940a679f49f27f))


### Continuous Integration

* Add workflows to check docker builds are all correct ([ee07aed](https://github.com/Evanlab02/HomePortalV2/commit/ee07aed46b448f96718212ed5ca2afb51a38cb72))

## [0.0.2](https://github.com/Evanlab02/HomePortalV2/compare/v0.0.1...v0.0.2) (2025-10-23)


### Features

* **Documentation:** Initial documentation and caddy setup ([0935e1b](https://github.com/Evanlab02/HomePortalV2/commit/0935e1bee799d763902d871db4d0a9862113498b))


### Continuous Integration

* release please workflows ([3fee2da](https://github.com/Evanlab02/HomePortalV2/commit/3fee2da5c159811c285129bbc5c90a007414bcd9))
