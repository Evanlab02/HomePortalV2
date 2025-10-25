# Changelog

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
