# Flappy Bird NEAT AI

## Project Overview

This project simulates the classic Flappy Bird game using Python and Pygame, integrated with the NEAT (NeuroEvolution of Augmenting Topologies) algorithm. It evolves AI agents that learn and improve their gameplay performance over generations.

### Key Features

- **Flappy Bird Game**: Playable version of the Flappy Bird game, complete with bird movement, pipes, and scoring.
- **NEAT Algorithm**: Utilizes evolved neural networks to train AI agents to play the game.
- **Loading Screen**: Custom loading screen with a progress bar and messages.
- **Sound Effects**: Background and event-specific sound effects for an immersive experience.
- **Configuration**: Flexible NEAT configuration for various evolutionary experiments.

## Project Structure

- `img/` - Contains images used in the game.
- `hit.mp3` - Sound effect for when the bird hits an obstacle.
- `point.mp3` - Sound effect for when the bird passes a pipe.
- `victory.mp3` - Sound effect for winning the game.
- `config-feedforward.txt` - Configuration file for the NEAT algorithm.
- `source.py` - Main script for running the game and NEAT algorithm.
- `winning.pkl` - Serialized best-performing neural network from NEAT.

## Installation

To set up and run this project, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/YuganshUwU/NEAT-Flappy-Bird.git
    cd NEAT-Flappy-Bird
    ```

2. **Install dependencies**:
    ```bash
    pip install pygame neat-python
    ```

3. **Download assets**: Ensure that the `NEAT-Flappy-Bird/` directory contains the following files:
    - Images: `bird1.png`, `bird2.png`, `bird3.png`, `pipe.png`, `base.png`, `bg.png`
    - Sounds: `hit.mp3`, `point.mp3`, `victory.mp3`

## Usage

To start the NEAT training and run the game, execute the following command:

```bash
python source.py
```

## Configuration

The NEAT algorithm is configured through the config-feedforward.txt file. You can modify this file to experiment with different parameters and settings for the evolutionary process. For detailed configuration options, refer to the [NEAT-Python documentation](https://neat-python.readthedocs.io/en/latest/config_file.html).



## Contributions

Contributions are welcome! If you want to contribute to this project:

- Fork the repository.
- Create a new branch:

```bash
git checkout -b feature-branch
```

- Make your changes and commit:
```bash
git commit -am 'Add new feature'
```

- Push to the Branch:
```bash
git push origin feature-branch
```

- Create a pull request with a description of your changes.


## License

This project is under the MIT License - see the [License](https://choosealicense.com/licenses/mit/) file for the details


## Acknowledgements

 - [Pygame](https://www.pygame.org/) - For the Game development library.
 - [NEAT](https://neat-python.readthedocs.io/en/latest/) - For the neuroevolution framework.


## Contact

If you have any questions or feedback, feel free to open an issue on the [Github Repository](https://github.com/YuganshUwU/NEAT-Flappy-Bird).

