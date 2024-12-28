#include <SDL.h>
#include <iostream>
#include <random>

void play() {
    int score = 0;

    std::string x = "Wave 1!";
    int y = 400;
    int z = 1;
    int a = 5;

    SDL_Init(SDL_INIT_VIDEO);
    SDL_Window* window = SDL_CreateWindow("ThePOCGame", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, 480, 640, 0);
    SDL_Renderer* renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);

    SDL_Rect Player_rect = { 30, 320, 45, 60 };
    SDL_Rect pipe_rect = { 30, 320, 45, 70 };

    SDL_Event event;
    float Player_velocity = 0.0f; // Bird's falling speed (velocity)
    float gravity = 0.75f; // Gravity force
    float jump_strength = -12.0f; // Jump strength
    Player_rect.y = 320;

    auto wave_check = [&]() {
        std::cout << "Wave: " << x << std::endl;
        };

    auto show_score = [&]() {
        std::cout << "Score: " << score << std::endl;
        };

    wave_check();

    while (true) {
        while (SDL_PollEvent(&event)) {
            if (event.type == SDL_QUIT) {
                SDL_DestroyRenderer(renderer);
                SDL_DestroyWindow(window);
                SDL_Quit();
                return;
            }

            if (event.type == SDL_KEYDOWN) {
                if (event.key.keysym.sym == SDLK_SPACE) { // Press space to jump
                    Player_velocity = jump_strength;
                }
            }
        }

        // Apply gravity
        Player_velocity += gravity;

        if (Player_velocity > 50.0f) {
            Player_velocity = 50.0f;
        }

        // Update the bird's position
        Player_rect.y += static_cast<int>(Player_velocity);

        // Prevent bird from falling out of bounds
        if (Player_rect.y > 640) {
            Player_rect.y = 0;
        }

        if (Player_rect.y < 0) {
            Player_rect.y = 640;
        }

        if (Player_rect.x > 480) {
            Player_rect.x = -50;
        }

        // Move the pipe
        pipe_rect.x -= a;

        if (pipe_rect.x < -70) { // Reset pipe position
            pipe_rect.x = 480;
            pipe_rect.y = rand() % 570;
            score += 1;
        }

        // Clear screen and redraw
        SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
        SDL_RenderClear(renderer);
        SDL_SetRenderDrawColor(renderer, 255, 0, 0, 255);
        SDL_RenderFillRect(renderer, &Player_rect);
        SDL_SetRenderDrawColor(renderer, 255, 255, 0, 255);
        SDL_RenderFillRect(renderer, &pipe_rect);

        if (SDL_HasIntersection(&Player_rect, &pipe_rect)) {
            score = 0;
        }

        show_score();

        if (score > 0 && score <= 10) {
            a = 5;
            x = "Wave 1";
            wave_check();
        }
        else if (score > 10 && score <= 20) {
            a = 10;
            x = "Wave 2";
            wave_check();
        }
        else if (score > 20 && score <= 30) {
            a = 15;
            x = "Wave 3";
            wave_check();
        }
        else if (score > 30 && score <= 40) {
            a = 20;
            x = "Wave 4";
            wave_check();
        }
        else if (score > 40 && score <= 50) {
            a = 25;
            x = "Wave 5";
            wave_check();
        }
        else if (score > 50) {
            a = 30;
        }

        SDL_RenderPresent(renderer);
        SDL_Delay(1000 / 60);
    }
}

int main(int argc, char* argv[]) {
    play();
    return 0;
}
