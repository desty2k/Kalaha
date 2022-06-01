# Changelog

- 0.3.0:
  - Use MVC pattern
  - Move logic from views to controllers
  - Add lobby - create board, join board views
  - Add window for setting up autoplayer
  - Add autoplayer pit highlighting before making a move
  - Use Python 3.10 feature - pattern matching
  - Change Dockerfile base image to `python:3.10-slim`
  - Optimize game engine code
  - Bump `QtPyNetwork` to 0.7.0
  - Add GitHub Actions for release and deploy

- 0.2.0:
  - Rename CAutoPlayer to CMinimax
  - Fix checking if game over in AutoPlayer
  - Fix iterating over pit indexes available to the player in CMinimax
  - Minor optimizations

- 0.1.0:
  - Initial release
