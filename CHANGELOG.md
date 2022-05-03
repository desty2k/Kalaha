# Changelog

- 0.3.0:
  - Create ClientController
  - Add CMaximax algorithm
  - Add option to create multiple boards secured by PIN
  - Use Python 3.10 feature - pattern matching
  - Change Dockerfile base image to `python:3.10-slim`
  - Optimize game engine code
  - Use `QBalancedServer` instead of `QThreadedServer`

- 0.2.0:
  - Rename CAutoPlayer to CMinimax
  - Fix checking if game over in AutoPlayer
  - Fix iterating over pit indexes available to the player in CMinimax
  - Minor optimizations

- 0.1.0:
  - Initial release
