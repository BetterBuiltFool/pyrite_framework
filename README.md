<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
<!--
[![LinkedIn][linkedin-shield]][linkedin-url]
-->



<!-- PROJECT LOGO -->
<br />
<!--
<div align="center">
  <a href="https://github.com/BetterBuiltFool/pyrite_framework">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>
-->

<h3 align="center">Pyrite</h3>

  <p align="center">
    The Simple Game Framework
    <br />
    <a href="https://github.com/BetterBuiltFool/pyrite_framework"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <!--
    <a href="https://github.com/BetterBuiltFool/pyrite_framework">View Demo</a>
    ·
    -->
    <a href="https://github.com/BetterBuiltFool/pyrite_framework/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/BetterBuiltFool/pyrite_framework/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
      <ul>
        <li><a href="#types">Types</a></li>
        <li><a href="#using-asset-handles">Using Asset Handles</a></li>
        <li><a href="#importing-resources">Importing Resources</a></li>
        <li><a href="#configuration">Configuration</a></li>
      </ul>
    <li><a href="#roadmap">Roadmap</a></li>
    <!--<li><a href="#contributing">Contributing</a></li>-->
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

<!--
[![Product Name Screen Shot][product-screenshot]](https://example.com)
-->

Pyrite is a framework for eliminating much of the boilerplate of setting up a pygame project and getting running, while encouraging good project architecture with proper seperation of responsibilities among game elements.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

Pyrite is written in pure python, with no system dependencies, and should be OS-agnostic.

### Installation

Pyrite can be installed from the [PyPI][pypi-url] using [pip][pip-url]:

```sh
pip install pyrite-framework
```

and can be imported for use with:
```python
import pyrite
```

Pyrite additionally is built for pygame-ce, which must also be installed.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Pyrite is built around a single main class: the Game class.
Game is useable as-is in its default state, or it can be subclassed to allow for more specific behaviors.

### Using Game

A game can be started in multiple ways.

1. Traditional way

```python
import pyrite

my_game = pyrite.Game()  # Creating with default settings
# ----------------------
#
# Game setup stuff here
#
# ----------------------
my_game.main()
```

This will create a window with a black background, at the default size (800x600), with a caption of "Game"

Keep in mind, anything after calling main() will be on hold until after the game stops running.

2. Context Manager

Alternatively, we can use python's ```with``` syntax to create a game.

```python
import pyrite

with pyrite.Game() as my_game:
    # ----------------------
    #
    # Game setup stuff here
    #
    # ----------------------
```

As with the above example, this will start a game with default settings. As a context manager, Game will start itself once the context ends.

Using context manager syntax offers a couple benefits.
1. Avoids needing to manually call main().

    This is minor, but it's an additional step that needs to be minded otherwise.

2. Indentation helps make it clear what code is being used to set up the game.

3. Errors are captured.

    Any error that occurs during the set up will be captured by the context manager, and Game has a setting to suppress these errors.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Game Settings

Game has several data classes that hold information for it. You can construct the yourself and pass them to the game instance, or you can pass their parameters as keywords into the Game constructor.

```python
# This:
display_settings = DisplaySettings((400, 300))
with Game(display_settings=display_settings) as my_game:
    ...

# Is the same as this
with Game(resolution=(400, 300)) as my_game:
    ...
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Loop Phases

A game is built around a loop, and that loop has certain phases. The pyrite game loop offers these phases:

1. Events: The pygame event queue is processed

2. Const_update: Runs at a fixed rate, regardless of frame rate. Useful for time-invariant things, like physics.

3. Pre_update: Runs earlier than the main update phase.

4. Update: Main update phase. Most logic is run here.

5. Post-update: Runs after the main update phase.

6. Render: For drawing to the screen.

7. UI Render: For rendering UI objects over top any game objects.

By default, each phase calls on active entities and renderables, and calls their own appropriate methods. If you subclass Game and overwrite any of those methods, ensure that they still call them on entities and renderables.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Entities, Renderables, and UI Elements
##### Oh, my!

These are the core feature of Pyrite. All game objects should inherit from at least one of these. They allow you to define behaviors, and render out images onto the screen.

#### Entity

An entity is any object that has behavior. They can be typical objects, like an enemy, or obstacle, or they can be systems and services, like a physics service. To use, simply subclass Entity, and overwrite one of the four update-phase methods. Then, when the entity is created, it will automatically have those methods called each frame.

```python

class MyEntity(Entity):

    def __init__(self, game_instance=None, enabled=True):
        super().__init__(game_instance, enabled)
        self.position: tuple[int, int] = (0, 0)


    def update(self, delta_time: float):
        keys = pygame.key.get_pressed()
        x = y = 0
        if keys[pygame.K_w]:
            y -= 1
        if keys[pygame.K_s]:
            y += 1
        if keys[pygame.K_a]:
            x -= 1
        if keys[pygame.K_d]:
            x += 1
        self.move((x, y))

    
    def move(self, direction: tuple[int, int]):
        self.position = (
            self.position[0] + direction[0], self.position[1] + direction[1]
        )
```

This will create a simple entity that will move with the WASD keys. Note, however, that it does not show anything on screen.


#### Renderables

Renderables are anything that needs to be drawn to the screen. They must implement the render method, and must return a surface and a point/rect.
Classes can inherit from both Entity and Renderable, to allow them to both be drawn and have behavior.

```python
class MyRenderable(Renderable):

    def render(self, delta_time: float):
        surface = Surface((10, 10))
        surface.fill(Color("fuchsia"))
        position = (100, 50)
        return (surface, position)
```

This will draw a small fuchsia square at a relative position of 100, 50.



<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [ ] 

<!--
- [ ] Feature 2
- [ ] Feature 3
    - [ ] Nested Feature
-->

See the [open issues](https://github.com/BetterBuiltFool/pyrite_framework/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
<!--
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Top contributors:

<a href="https://github.com/BetterBuiltFool/pyrite_framework/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=BetterBuiltFool/pyrite_framework" alt="contrib.rocks image" />
</a>
-->



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Better Built Fool - betterbuiltfool@gmail.com

Bluesky - [@betterbuiltfool.bsky.social](https://bsky.app/profile/betterbuiltfool.bsky.social)
<!--
 - [@twitter_handle](https://twitter.com/twitter_handle)
-->

Project Link: [https://github.com/BetterBuiltFool/pyrite_framework](https://github.com/BetterBuiltFool/pyrite_framework)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
<!--## Acknowledgments

* []()
* []()
* []()

<p align="right">(<a href="#readme-top">back to top</a>)</p>
-->


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/BetterBuiltFool/pyrite_framework.svg?style=for-the-badge
[contributors-url]: https://github.com/BetterBuiltFool/pyrite_framework/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/BetterBuiltFool/pyrite_framework.svg?style=for-the-badge
[forks-url]: https://github.com/BetterBuiltFool/pyrite_framework/network/members
[stars-shield]: https://img.shields.io/github/stars/BetterBuiltFool/pyrite_framework.svg?style=for-the-badge
[stars-url]: https://github.com/BetterBuiltFool/pyrite_framework/stargazers
[issues-shield]: https://img.shields.io/github/issues/BetterBuiltFool/pyrite_framework.svg?style=for-the-badge
[issues-url]: https://github.com/BetterBuiltFool/pyrite_framework/issues
[license-shield]: https://img.shields.io/github/license/BetterBuiltFool/pyrite_framework.svg?style=for-the-badge
[license-url]: https://github.com/BetterBuiltFool/pyrite_framework/blob/main/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[python.org]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[python-url]: https://www.python.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
[pypi-url]: https://pypi.org/project/pyrite-framework
[pip-url]: https://pip.pypa.io/en/stable/